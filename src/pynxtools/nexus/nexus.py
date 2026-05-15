# pylint: disable=too-many-lines
"""Utility functions for inspecting NeXus NXDL files.

TODO: All functions in this module are currently used only by the NOMAD parser
(NomadParser/HandleNexus) via the legacy `get_nxdl_doc` / `get_nxdl_entry`
interface.  Once a dedicated NomadVisitor (implementing NexusVisitor) is
implemented, these functions can be removed entirely.  The Annotator no longer
depends on anything here except `get_default_plottable`.
"""

import logging
import os
import sys
from functools import cache, lru_cache
from typing import Any, Optional, Union

import h5py
import lxml.etree as ET
import numpy as np

# TODO: remove these imports when NomadVisitor is implemented
from pynxtools.annotator.nxdata import (
    axis_helper,
    chk_nxdata_axis,
    chk_nxdata_axis_v2,
    entry_helper,
    find_attrib_axis_actual_dim_num,
    get_single_or_multiple_axes,
    logger_auxiliary_signal,
    nxdata_helper,
    print_default_plottable_header,
    signal_helper,
)
from pynxtools.definitions.dev_tools.utils.nxdl_utils import (
    add_base_classes,
    check_attr_name_nxdl,
    get_best_child,
    get_hdf_info_parent,
    get_local_name_from_xml,
    get_node_concept_path,
    get_node_name,
    get_nx_class,
    get_nxdl_child,
    get_required_string,
    other_attrs,
    try_find_default,
    try_find_units,
    walk_elist,
    write_doc_string,
)
from pynxtools.nexus.utils import decode_if_string

_logger = logging.getLogger(__file__)


def get_nxdl_entry(hdf_info):
    """Get the nxdl application definition for an HDF5 node"""
    entry = hdf_info
    if (
        "NX_class" in entry["hdf_node"].attrs.keys()
        and decode_if_string(entry["hdf_node"].attrs["NX_class"]) == "NXroot"
    ):
        return "NXroot"
    while (
        isinstance(entry["hdf_node"], h5py.Dataset)
        or "NX_class" not in entry["hdf_node"].attrs.keys()
        or decode_if_string(entry["hdf_node"].attrs["NX_class"]) != "NXentry"
    ):
        entry = get_hdf_info_parent(entry)
        if entry["hdf_node"].name == "/":
            return "NO NXentry found"
    try:
        nxdef = entry["hdf_node"]["definition"][()]
        return nxdef.decode()
    except KeyError:  # 'NO Definition referenced'
        return "NXroot"


def get_nx_class_path(hdf_info):
    """Get the full path of an HDF5 node using nexus classes
    in case of a field, end with the field name"""
    hdf_node = hdf_info["hdf_node"]
    if hdf_node.name == "/":
        return ""
    if isinstance(hdf_node, h5py.Group):
        return (
            get_nx_class_path(get_hdf_info_parent(hdf_info))
            + "/"
            + (
                decode_if_string(hdf_node.attrs["NX_class"])
                if "NX_class" in hdf_node.attrs.keys()
                else hdf_node.name.split("/")[-1]
            )
        )
    if isinstance(hdf_node, h5py.Dataset):
        return (
            get_nx_class_path(get_hdf_info_parent(hdf_info))
            + "/"
            + hdf_node.name.split("/")[-1]
        )
    return ""


def _check_deprecation_enum_axis(
    variables, doc, elem_list, attr, hdf_node, logger: logging.Logger | None = None
):
    """Check for several attributes. - deprecation - enums - nxdata_axis"""
    logger = logger or _logger

    elem, path = variables
    dep_str = elem.attrib.get("deprecated")  # check for deprecation
    if dep_str:
        if doc:
            logger.debug("DEPRECATED - " + dep_str)
    for base_elem in elem_list if not attr else [elem]:  # check for enums
        s_doc = get_nxdl_child(base_elem, "enumeration", go_base=False)
        if s_doc is not None:
            if doc:
                logger.debug("enumeration (" + get_node_concept_path(base_elem) + "):")
            for item in s_doc:
                if isinstance(item, ET._Comment):
                    continue
                if get_local_name_from_xml(item) == "item":
                    if doc:
                        logger.debug("-> " + item.attrib["value"])
    chk_nxdata_axis(
        hdf_node, path.split("/")[-1]
    )  # look for NXdata reference (axes/signal)
    for base_elem in elem_list if not attr else [elem]:  # check for doc
        s_doc = get_nxdl_child(base_elem, "doc", go_base=False)
        if doc:
            logger.debug("documentation (" + get_node_concept_path(base_elem) + "):")
            logger.debug(s_doc.text if s_doc is not None else "")
    return elem, path, doc, elem_list, attr, hdf_node


def _get_nxdl_attr_doc(  # pylint: disable=too-many-arguments,too-many-locals
    elem,
    elem_list,
    attr,
    hdf_node,
    doc,
    nxdl_path,
    req_str,
    path,
    hdf_info,
    logger: logging.Logger | None = None,
):
    """Get nxdl documentation for an attribute"""
    logger = logger or _logger

    new_elem = []
    old_elem = elem
    attr_inheritance_chain: list = []
    for elem_index, act_elem1 in enumerate(elem_list):
        act_elem = act_elem1
        # NX_class is a compulsory attribute for groups in a nexus file
        # which should match the type of the corresponding NXDL element
        if (
            attr == "NX_class"
            and not isinstance(hdf_node, h5py.Dataset)
            and elem_index == 0
        ):
            elem = None
            _, doc, attr = write_doc_string(_logger, doc, attr)
            new_elem = elem
            break
        # units category is a compulsory attribute for any fields
        if attr == "units" and isinstance(hdf_node, h5py.Dataset):
            req_str = "<<REQUIRED>>"
            _, act_elem, attr_inheritance_chain, doc, attr = try_find_units(
                logger, act_elem, attr_inheritance_chain, doc, attr
            )
        # units for attributes can be given as ATTRIBUTENAME_units
        elif attr.endswith("_units"):
            _, act_elem, attr_inheritance_chain, doc, attr, req_str = (
                check_attr_name_nxdl(
                    (_logger, act_elem, attr_inheritance_chain, doc, attr, req_str)
                )
            )
        # default is allowed for groups
        elif attr == "default" and not isinstance(hdf_node, h5py.Dataset):
            req_str = "<<RECOMMENDED>>"
            # try to find if default is defined as a child of the NXDL element
            act_elem = get_nxdl_child(
                act_elem, attr, nexus_type="attribute", go_base=False
            )
            _, act_elem, attr_inheritance_chain, doc, attr = try_find_default(
                logger, act_elem1, act_elem, attr_inheritance_chain, doc, attr
            )
        else:  # other attributes
            act_elem = get_nxdl_child(
                act_elem, attr, nexus_type="attribute", go_base=False
            )
            if act_elem is not None:
                _, act_elem, attr_inheritance_chain, doc, attr = other_attrs(
                    logger, act_elem1, act_elem, attr_inheritance_chain, doc, attr
                )
        if act_elem is not None:
            new_elem.append(act_elem)
            if req_str is None:
                req_str = get_required_string(act_elem)  # check for being required
                if doc:
                    logger.debug(req_str)
            variables = [act_elem, path]
            (
                elem,
                path,
                doc,
                elem_list,
                attr,
                hdf_node,
            ) = _check_deprecation_enum_axis(variables, doc, elem_list, attr, hdf_node)
    elem = old_elem
    if req_str is None and doc:
        if attr != "NX_class":
            logger.debug("@" + attr + " - IS NOT IN SCHEMA")
        logger.debug("")

    # Add the lowest child element to the nxdl_path
    if attr_inheritance_chain:
        nxdl_path.append(attr_inheritance_chain[0])
    return (req_str, get_nxdl_entry(hdf_info), nxdl_path)


def get_nxdl_doc(hdf_info, doc, attr=False, logger: logging.Logger | None = None):
    """Get nxdl documentation for an HDF5 node (or its attribute).

    .. deprecated::
        Uses the legacy XML-element traversal approach.  This function exists
        solely to support the NOMAD parser callback in
        :class:`~.annotation.Annotator`; that call-site is tagged TODO for
        migration to :class:`~.nexus_tree.NexusNode`.
    """
    logger = logger or _logger

    hdf_node = hdf_info["hdf_node"]
    # new way: retrieve multiple inherited base classes
    (class_path, nxdl_path, elem_list) = _get_inherited_hdf_nodes(
        nx_name=get_nxdl_entry(hdf_info),
        hdf_node=hdf_node,
        hdf_path=hdf_info["hdf_path"] if "hdf_path" in hdf_info else None,
        hdf_root=hdf_info["hdf_root"] if "hdf_root" in hdf_info else None,
    )
    # Copy the nxdl_path, otherwise the cached object is altered
    nxdl_path = nxdl_path.copy()
    elem = elem_list[0] if class_path and elem_list else None
    if doc:
        logger.debug("classpath: " + str(class_path))
        logger.debug(
            "NOT IN SCHEMA"
            if elem is None
            else "classes:\n" + "\n".join(get_node_concept_path(e) for e in elem_list)
        )
    # old solution with a single elem instead of using elem_list
    path = get_nx_class_path(hdf_info)
    req_str = None
    if elem is None:
        if doc:
            logger.debug("")
        return ("None", None, None)
    if attr:
        return _get_nxdl_attr_doc(
            elem,
            elem_list,
            attr,
            hdf_node,
            doc,
            nxdl_path,
            req_str,
            path,
            hdf_info,
        )
    req_str = get_required_string(elem)  # check for being required
    if doc:
        logger.debug(req_str)
    variables = [elem, path]
    elem, path, doc, elem_list, attr, hdf_node = _check_deprecation_enum_axis(
        variables, doc, elem_list, attr, hdf_node, logger
    )
    return (req_str, get_nxdl_entry(hdf_info), nxdl_path)


def _helper_get_inherited_nodes(hdf_info2, elem_list, path_index, attr):
    """find the best fitting name in all children"""
    hdf_path, hdf_node, hdf_class_path = hdf_info2
    hdf_name = hdf_path[path_index]
    hdf_class_name = hdf_class_path[path_index]
    if path_index < len(hdf_path) - (2 if attr else 1):
        act_nexus_type = "group"
    elif path_index == len(hdf_path) - 1 and attr:
        act_nexus_type = "attribute"
    else:
        act_nexus_type = "field" if isinstance(hdf_node, h5py.Dataset) else "group"
    # find the best fitting name in all children
    best_fit = -1
    html_name = None
    for ind in range(len(elem_list) - 1, -1, -1):
        new_elem, fit = get_best_child(
            elem_list[ind], hdf_node, hdf_name, hdf_class_name, act_nexus_type
        )
        if fit >= best_fit and new_elem is not None:
            best_fit = fit
            html_name = get_node_name(new_elem)
    return hdf_path, hdf_node, hdf_class_path, elem_list, path_index, attr, html_name


def _get_hdf_path(hdf_info):
    """Get the hdf_path from an hdf_info"""
    if "hdf_path" in hdf_info:
        return hdf_info["hdf_path"].split("/")[1:]
    return hdf_info["hdf_node"].name.split("/")[1:]


@cache
def _get_inherited_hdf_nodes(
    nx_name: str = None,
    elem: ET._Element = None,
    hdf_node=None,
    hdf_path=None,
    hdf_root=None,
    attr=False,
):
    """Returns a list of ET._Element for the given path."""
    # let us start with the given definition file
    if hdf_node is None:
        raise ValueError("hdf_node must not be None")
    if nx_name == "NO NXentry found":
        return (None, [], [])
    elem_list = []  # type: ignore[var-annotated]
    add_base_classes(elem_list, nx_name, elem)
    nxdl_elem_path = [elem_list[0]]

    class_path = []  # type: ignore[var-annotated]
    hdf_info = {"hdf_node": hdf_node}
    if hdf_path:
        hdf_info["hdf_path"] = hdf_path
    if hdf_root:
        hdf_root["hdf_root"] = hdf_root
    hdf_node = hdf_info["hdf_node"]
    hdf_path = _get_hdf_path(hdf_info)
    hdf_class_path = get_nx_class_path(hdf_info).split("/")[1:]
    if attr:
        hdf_path.append(attr)
        hdf_class_path.append(attr)
    path = hdf_path

    for path_index in range(len(path)):
        if len(path) == 1 and path[0] == "":
            return ([""], ["/"], elem_list)
        hdf_info2 = [hdf_path, hdf_node, hdf_class_path]
        [
            hdf_path,
            hdf_node,
            hdf_class_path,
            elem_list,
            path_index,
            attr,
            html_name,
        ] = _helper_get_inherited_nodes(hdf_info2, elem_list, path_index, attr)
        if html_name is None:  # return if NOT IN SCHEMA
            return (class_path, nxdl_elem_path, None)
        elem_list, html_name = walk_elist(elem_list, html_name)
        if elem_list:
            class_path.append(get_nx_class(elem_list[0]))
            nxdl_elem_path.append(elem_list[0])
    return (class_path, nxdl_elem_path, elem_list)


def _process_node(
    hdf_node, hdf_path, parser, doc=True, logger: logging.Logger | None = None
):
    """Processes an hdf5 node.
    - it logs the node found and also checks for its attributes
    - retrieves the corresponding nxdl documentation
    TODO:
    - follow variants
    - NOMAD parser: store in NOMAD"""
    logger = logger or _logger

    hdf_info = {"hdf_path": hdf_path, "hdf_node": hdf_node}
    if isinstance(hdf_node, h5py.Dataset):
        logger.debug(f"===== FIELD (/{hdf_path}): {hdf_node}")
        val = (
            str(decode_if_string(hdf_node[()])).split("\n")
            if len(hdf_node.shape) <= 1
            else str(decode_if_string(hdf_node[0])).split("\n")
        )
        logger.debug(f"value: {val[0]} {'...' if len(val) > 1 else ''}")
    else:
        logger.debug(
            f"===== GROUP (/{hdf_path} "
            f"[{get_nxdl_entry(hdf_info)}"
            f"::{get_nx_class_path(hdf_info)}]): {hdf_node}"
        )
    (req_str, nxdef, nxdl_path) = get_nxdl_doc(hdf_info, doc)
    if parser is not None and isinstance(hdf_node, h5py.Dataset):
        parser(
            {
                "hdf_info": hdf_info,
                "nxdef": nxdef,
                "nxdl_path": nxdl_path,
                "val": val,
                "logger": logger,
            }
        )
    for key, value in hdf_node.attrs.items():
        logger.debug(f"===== ATTRS (/{hdf_path}@{key})")
        val = str(decode_if_string(value)).split("\n")
        logger.debug(f"value: {val[0]} {'...' if len(val) > 1 else ''}")
        (req_str, nxdef, nxdl_path) = get_nxdl_doc(hdf_info, doc, attr=key)
        if (
            parser is not None
            and req_str is not None
            and "NOT IN SCHEMA" not in req_str
            and "None" not in req_str
        ):
            parser(
                {
                    "hdf_info": hdf_info,
                    "nxdef": nxdef,
                    "nxdl_path": nxdl_path,
                    "val": val,
                    "logger": logger,
                },
                attr=key,
            )


def get_default_plottable(
    root,
    logger: logging.Logger | None = None,
):
    """Walk *root* to identify and log the default plottable signal and axes.

    Implements the three NeXus Data Plotting Standard conventions (v3→v2→v1)
    via :func:`~pynxtools.nexus.nxdata.find_default_nxdata` and
    :func:`~pynxtools.nexus.nxdata.inspect_nxdata`.
    """
    from pynxtools.nexus.nxdata import (
        find_default_nxdata,
        find_default_nxentry,
        inspect_nxdata,
    )

    logger = logger or _logger
    print_default_plottable_header(logger)

    nxentry = find_default_nxentry(root)
    if not nxentry:
        logger.debug("No NXentry has been found")
        return
    logger.debug("")
    logger.debug("NXentry has been identified: " + nxentry.name)

    nxdata = find_default_nxdata(root)
    if not nxdata:
        logger.debug("No NXdata group has been found")
        return
    logger.debug("")
    logger.debug("NXdata group has been identified: " + nxdata.name)

    info = inspect_nxdata(nxdata)
    if info.signal is None:
        logger.debug("No Signal has been found")
        return
    logger.debug("")
    logger.debug("Signal has been identified: " + info.signal.name)
    logger_auxiliary_signal(nxdata, logger)

    for a_item, ax_list in enumerate(info.axes):
        logger.debug("")
        logger.debug(
            f"For Axis #{a_item}, {len(ax_list)} axes have been identified: {ax_list!s}"
        )


#: Backward-compatibility alias — new code should use ``_get_inherited_hdf_nodes``.
# TODO: remove when NomadVisitor exists
get_inherited_hdf_nodes = _get_inherited_hdf_nodes


def get_all_is_a_rel_from_hdf_node(hdf_node, hdf_path):
    """Return list of nxdl concept paths for a nxdl element which corresponds to
    hdf node.

    .. deprecated::
        This function uses the legacy XML-element traversal approach.
        The ``-c`` / concept-query code path in :class:`~.annotation.Annotator`
        is the only first-party caller and should be migrated to use
        :class:`~.nexus_tree.NexusNode` directly.
    """
    hdf_info = {"hdf_path": hdf_path, "hdf_node": hdf_node}
    (_, _, elem_list) = _get_inherited_hdf_nodes(
        nx_name=get_nxdl_entry(hdf_info),
        hdf_node=hdf_node,
        hdf_path=hdf_info["hdf_path"] if "hdf_path" in hdf_info else None,
        hdf_root=hdf_info["hdf_root"] if "hdf_root" in hdf_info else None,
    )
    return elem_list


class HandleNexus:
    """
    Thin wrapper around `NexusFileHandler` + `Annotator`.

    .. deprecated::
        Construct `NexusFileHandler` and `Annotator` directly.
        This class is retained for backward compatibility and will be removed
        in a future release.
    """

    # TODO: remove this in future releases

    def __init__(
        self,
        logger,
        nexus_file,
        documentation=None,
        concept=None,
        is_open=False,
    ):
        import warnings

        from pynxtools.nexus.handler import NexusFileHandler

        warnings.warn(
            "HandleNexus is deprecated. Use NexusFileHandler + Annotator directly.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.logger = logger
        self.documentation = documentation
        self.concept = concept
        self._handler = NexusFileHandler(nexus_file, is_open=is_open)

    def process_nexus_master_file(self, parser=None):
        """Process a NeXus/HDF5 master file by processing all its nodes and their attributes.

        The *parser* argument is ignored — the NOMAD parser now uses
        ``NomadVisitor`` directly instead of the legacy callback interface.
        """
        from pynxtools.annotator.annotator import Annotator

        visitor = Annotator(
            self.logger,
            documentation=self.documentation,
            concept=self.concept,
        )
        self._handler.process(visitor)


if __name__ == "__main__":
    from pynxtools.annotator.cli import read

    # TODO: this is deprecated, should be removed in the future

    read()  # type: ignore[has-type]
