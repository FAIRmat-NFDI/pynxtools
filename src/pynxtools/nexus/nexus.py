# pylint: disable=too-many-lines
"""Read files from different format and print it in a standard NeXus format"""

import logging
import os
import sys
from functools import cache, lru_cache
from typing import Any, Optional, Union

import click
import h5py
import lxml.etree as ET
import numpy as np

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
from pynxtools.nexus.nxdata import (
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
from pynxtools.nexus.utils import decode_if_string


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


def check_deprecation_enum_axis(variables, doc, elem_list, attr, hdf_node):
    """Check for several attributes. - deprecation - enums - nxdata_axis"""
    logger, elem, path = variables
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
        hdf_node, path.split("/")[-1], logger
    )  # look for NXdata reference (axes/signal)
    for base_elem in elem_list if not attr else [elem]:  # check for doc
        s_doc = get_nxdl_child(base_elem, "doc", go_base=False)
        if doc:
            logger.debug("documentation (" + get_node_concept_path(base_elem) + "):")
            logger.debug(s_doc.text if s_doc is not None else "")
    return logger, elem, path, doc, elem_list, attr, hdf_node


def get_nxdl_attr_doc(  # pylint: disable=too-many-arguments,too-many-locals
    elem, elem_list, attr, hdf_node, logger, doc, nxdl_path, req_str, path, hdf_info
):
    """Get nxdl documentation for an attribute"""
    new_elem = []
    old_elem = elem
    attr_inheritance_chain = []
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
            logger, doc, attr = write_doc_string(logger, doc, attr)
            new_elem = elem
            break
        # units category is a compulsory attribute for any fields
        if attr == "units" and isinstance(hdf_node, h5py.Dataset):
            req_str = "<<REQUIRED>>"
            logger, act_elem, attr_inheritance_chain, doc, attr = try_find_units(
                logger, act_elem, attr_inheritance_chain, doc, attr
            )
        # units for attributes can be given as ATTRIBUTENAME_units
        elif attr.endswith("_units"):
            logger, act_elem, attr_inheritance_chain, doc, attr, req_str = (
                check_attr_name_nxdl(
                    (logger, act_elem, attr_inheritance_chain, doc, attr, req_str)
                )
            )
        # default is allowed for groups
        elif attr == "default" and not isinstance(hdf_node, h5py.Dataset):
            req_str = "<<RECOMMENDED>>"
            # try to find if default is defined as a child of the NXDL element
            act_elem = get_nxdl_child(
                act_elem, attr, nexus_type="attribute", go_base=False
            )
            logger, act_elem, attr_inheritance_chain, doc, attr = try_find_default(
                logger, act_elem1, act_elem, attr_inheritance_chain, doc, attr
            )
        else:  # other attributes
            act_elem = get_nxdl_child(
                act_elem, attr, nexus_type="attribute", go_base=False
            )
            if act_elem is not None:
                logger, act_elem, attr_inheritance_chain, doc, attr = other_attrs(
                    logger, act_elem1, act_elem, attr_inheritance_chain, doc, attr
                )
        if act_elem is not None:
            new_elem.append(act_elem)
            if req_str is None:
                req_str = get_required_string(act_elem)  # check for being required
                if doc:
                    logger.debug(req_str)
            variables = [logger, act_elem, path]
            (
                logger,
                elem,
                path,
                doc,
                elem_list,
                attr,
                hdf_node,
            ) = check_deprecation_enum_axis(variables, doc, elem_list, attr, hdf_node)
    elem = old_elem
    if req_str is None and doc:
        if attr != "NX_class":
            logger.debug("@" + attr + " - IS NOT IN SCHEMA")
        logger.debug("")

    # Add the lowest child element to the nxdl_path
    if attr_inheritance_chain:
        nxdl_path.append(attr_inheritance_chain[0])
    return (req_str, get_nxdl_entry(hdf_info), nxdl_path)


def get_nxdl_doc(hdf_info, logger, doc, attr=False):
    """Get nxdl documentation for an HDF5 node (or its attribute)"""
    hdf_node = hdf_info["hdf_node"]
    # new way: retrieve multiple inherited base classes
    (class_path, nxdl_path, elem_list) = get_inherited_hdf_nodes(
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
        return get_nxdl_attr_doc(
            elem,
            elem_list,
            attr,
            hdf_node,
            logger,
            doc,
            nxdl_path,
            req_str,
            path,
            hdf_info,
        )
    req_str = get_required_string(elem)  # check for being required
    if doc:
        logger.debug(req_str)
    variables = [logger, elem, path]
    logger, elem, path, doc, elem_list, attr, hdf_node = check_deprecation_enum_axis(
        variables, doc, elem_list, attr, hdf_node
    )
    return (req_str, get_nxdl_entry(hdf_info), nxdl_path)


def helper_get_inherited_nodes(hdf_info2, elem_list, path_index, attr):
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


def get_hdf_path(hdf_info):
    """Get the hdf_path from an hdf_info"""
    if "hdf_path" in hdf_info:
        return hdf_info["hdf_path"].split("/")[1:]
    return hdf_info["hdf_node"].name.split("/")[1:]


# pylint: disable=too-many-arguments,too-many-locals
@cache
def get_inherited_hdf_nodes(
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
    hdf_path = get_hdf_path(hdf_info)
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
        ] = helper_get_inherited_nodes(hdf_info2, elem_list, path_index, attr)
        if html_name is None:  # return if NOT IN SCHEMA
            return (class_path, nxdl_elem_path, None)
        elem_list, html_name = walk_elist(elem_list, html_name)
        if elem_list:
            class_path.append(get_nx_class(elem_list[0]))
            nxdl_elem_path.append(elem_list[0])
    return (class_path, nxdl_elem_path, elem_list)


def process_node(hdf_node, hdf_path, parser, logger, doc=True):
    """Processes an hdf5 node.
    - it logs the node found and also checks for its attributes
    - retrieves the corresponding nxdl documentation
    TODO:
    - follow variants
    - NOMAD parser: store in NOMAD"""
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
    (req_str, nxdef, nxdl_path) = get_nxdl_doc(hdf_info, logger, doc)
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
        (req_str, nxdef, nxdl_path) = get_nxdl_doc(hdf_info, logger, doc, attr=key)
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


def get_default_plottable(root, logger):
    """Get default plottable"""
    print_default_plottable_header(logger)
    # v3 from 2014
    # nxentry
    nxentry = None
    default_nxentry_group_name = decode_if_string(root.attrs.get("default"))
    if default_nxentry_group_name:
        try:
            nxentry = root[default_nxentry_group_name]
        except KeyError:
            nxentry = None
    if not nxentry:
        nxentry = entry_helper(root)
    if not nxentry:
        logger.debug("No NXentry has been found")
        return
    logger.debug("")
    logger.debug("NXentry has been identified: " + nxentry.name)
    # nxdata
    nxdata = None
    nxgroup = nxentry
    default_group_name = decode_if_string(nxgroup.attrs.get("default"))
    while default_group_name:
        try:
            nxgroup = nxgroup[default_group_name]
            default_group_name = decode_if_string(nxgroup.attrs.get("default"))
        except KeyError:
            logger.debug(f"""No default group with a name
                         {default_group_name} for {nxgroup} has been found.""")
            break

    if nxgroup == nxentry:
        nxdata = nxdata_helper(nxentry)
    else:
        nxdata = nxgroup
    if not nxdata:
        logger.debug("No NXdata group has been found")
        return
    logger.debug("")
    logger.debug("NXdata group has been identified: " + nxdata.name)
    process_node(nxdata, nxdata.name, None, logger, False)
    # signal
    signal = None
    signal_dataset_name = decode_if_string(nxdata.attrs.get("signal"))
    try:
        signal = nxdata[signal_dataset_name]
    except (TypeError, KeyError):
        signal = None
    if not signal:
        signal = signal_helper(nxdata)
    if not signal:
        logger.debug("No Signal has been found")
        return
    logger.debug("")
    logger.debug("Signal has been identified: " + signal.name)
    process_node(signal, signal.name, None, logger, False)
    logger = logger_auxiliary_signal(logger, nxdata)  # check auxiliary_signals
    dim = len(signal.shape)
    axes = []  # axes
    axis_helper(dim, nxdata, signal, axes, logger)


def get_all_is_a_rel_from_hdf_node(hdf_node, hdf_path):
    """Return list of nxdl concept paths for a nxdl element which corresponds to
    hdf node.
    """
    hdf_info = {"hdf_path": hdf_path, "hdf_node": hdf_node}
    (_, _, elem_list) = get_inherited_hdf_nodes(
        nx_name=get_nxdl_entry(hdf_info),
        hdf_node=hdf_node,
        hdf_path=hdf_info["hdf_path"] if "hdf_path" in hdf_info else None,
        hdf_root=hdf_info["hdf_root"] if "hdf_root" in hdf_info else None,
    )
    return elem_list


def hdf_node_to_self_concept_path(hdf_info, logger):
    """Get concept or nxdl path from given hdf_node."""
    # The below logger is for deactivating unnecessary debug message above
    if logger is None:
        logger = logging.getLogger("pynxtools")
        logger.setLevel(logging.INFO)
    (_, _, nxdl_path) = get_nxdl_doc(hdf_info, logger, None)
    con_path = ""
    if nxdl_path:
        for nd_ in nxdl_path:
            con_path = con_path + "/" + get_node_name(nd_)
    return con_path


class HandleNexus:
    """
    Thin wrapper around `NexusFileHandler` + `Annotator`.

    .. deprecated::
        Construct `NexusFileHandler` and `Annotator` directly.
        This class is retained for backward compatibility and will be removed
        in a future release.
    """

    def __init__(
        self,
        logger,
        nexus_file,
        d_inq_nd=None,
        c_inq_nd=None,
        is_in_memory_file=False,
    ):
        import warnings

        from pynxtools.nexus.handler import NexusFileHandler

        warnings.warn(
            "HandleNexus is deprecated. Use NexusFileHandler + Annotator directly.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.logger = logger
        self.d_inq_nd = d_inq_nd
        self.c_inq_nd = c_inq_nd
        self._handler = NexusFileHandler(
            nexus_file, is_in_memory_file=is_in_memory_file
        )

    def process_nexus_master_file(self, parser):
        """Process a nexus master file by processing all its nodes and their attributes."""
        from pynxtools.nexus.annotation import Annotator

        visitor = Annotator(
            self.logger,
            d_inq_nd=self.d_inq_nd,
            c_inq_nd=self.c_inq_nd,
            parser=parser,
        )
        self._handler.process(visitor)


@click.command()
@click.argument("nexus_file", type=click.Path(exists=True))
@click.option(
    "-d",
    "--documentation",
    required=False,
    default=None,
    help=(
        "HDF5 path of a single node to document. "
        "Returns all schema information for that path. "
        "Example: /entry/instrument/analyser/data"
    ),
)
@click.option(
    "-c",
    "--concept",
    required=False,
    default=None,
    help=(
        "NXDL concept path. Lists all HDF5 nodes in the file that satisfy "
        "an IS-A relation with that concept. "
        "Example: /NXarpes/ENTRY/INSTRUMENT/analyser"
    ),
)
def main(nexus_file, documentation, concept):
    """Annotate a NeXus/HDF5 file with NXDL schema documentation.

    Walks NEXUS_FILE and prints schema information (concept paths, optionality,
    inheritance chain, documentation, enumerations) for every node.

    Use -d to focus on a single HDF5 path, or -c to find all nodes that
    implement a given NXDL concept.
    """
    # The pynxtools logger already has a StreamHandler installed by pynxtools/__init__.py.
    # We only need to lower the level to DEBUG so that detail lines are visible, and
    # keep propagate=False so root-logger handlers don't double-emit messages.
    logger = logging.getLogger("pynxtools")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    if documentation and concept:
        raise click.UsageError(
            "Options -d/--documentation and -c/--concept are mutually exclusive."
        )

    from pynxtools.nexus.annotation import Annotator
    from pynxtools.nexus.handler import NexusFileHandler

    NexusFileHandler(nexus_file).process(
        Annotator(logger, d_inq_nd=documentation, c_inq_nd=concept)
    )


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
