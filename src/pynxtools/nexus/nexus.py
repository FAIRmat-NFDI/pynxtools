# pylint: disable=too-many-lines
"""Read files from different format and print it in a standard NeXus format"""

import logging
import os
import sys
from functools import lru_cache

import click
import h5py
import lxml.etree as ET

from pynxtools.definitions.dev_tools.utils.nxdl_utils import (
    NxdlAttributeNotFoundError,
    add_base_classes,
    check_attr_name_nxdl,
    get_best_child,
    get_enums,
    get_hdf_info_parent,
    get_inherited_nodes,
    get_local_name_from_xml,
    get_nexus_definitions_path,
    get_node_at_nxdl_path,
    get_node_concept_path,
    get_node_name,
    get_nx_attribute_type,
    get_nx_class,
    get_nx_classes,
    get_nx_units,
    get_nxdl_child,
    get_required_string,
    other_attrs,
    try_find_default,
    try_find_units,
    walk_elist,
    write_doc_string,
)


def get_nxdl_entry(hdf_info):
    """Get the nxdl application definition for an HDF5 node"""
    entry = hdf_info
    while (
        isinstance(entry["hdf_node"], h5py.Dataset)
        or "NX_class" not in entry["hdf_node"].attrs.keys()
        or entry["hdf_node"].attrs["NX_class"] != "NXentry"
    ):
        entry = get_hdf_info_parent(entry)
        if entry["hdf_node"].name == "/":
            return "NO NXentry found"
    try:
        nxdef = entry["hdf_node"]["definition"][()]
        return nxdef.decode()
    except KeyError:  # 'NO Definition referenced'
        return "NXentry"


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
                hdf_node.attrs["NX_class"]
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


def chk_nxdataaxis_v2(hdf_node, name, logger):
    """Check if dataset is an axis"""
    own_signal = hdf_node.attrs.get("signal")  # check for being a Signal
    if own_signal is str and own_signal == "1":
        logger.debug("Dataset referenced (v2) as NXdata SIGNAL")
    own_axes = hdf_node.attrs.get("axes")  # check for being an axis
    if own_axes is str:
        axes = own_axes.split(":")
        for i in len(axes):
            if axes[i] and name == axes[i]:
                logger.debug("Dataset referenced (v2) as NXdata AXIS #%d", i)
                return None
    ownpaxis = hdf_node.attrs.get("primary")
    own_axis = hdf_node.attrs.get("axis")
    if own_axis is int:
        # also convention v1
        if ownpaxis is int and ownpaxis == 1:
            logger.debug("Dataset referenced (v2) as NXdata AXIS #%d", own_axis - 1)
        else:
            logger.debug(
                "Dataset referenced (v2) as NXdata (primary/alternative) AXIS #%d",
                own_axis - 1,
            )
    return None


def chk_nxdataaxis(hdf_node, name, logger):
    """NEXUS Data Plotting Standard v3: new version from 2014"""
    if not isinstance(
        hdf_node, h5py.Dataset
    ):  # check if it is a field in an NXdata node
        return None
    parent = hdf_node.parent
    if not parent or (parent and not parent.attrs.get("NX_class") == "NXdata"):
        return None
    signal = parent.attrs.get("signal")  # chk for Signal
    if signal and name == signal:
        logger.debug("Dataset referenced as NXdata SIGNAL")
        return None
    axes = parent.attrs.get("axes")  # check for default Axes
    if axes is str:
        if name == axes:
            logger.debug("Dataset referenced as NXdata AXIS")
            return None
    elif axes is not None:
        for i, j in enumerate(axes):
            if name == j:
                indices = parent.attrs.get(j + "_indices")
                if indices is int:
                    logger.debug(f"Dataset referenced as NXdata AXIS #{indices}")
                else:
                    logger.debug(f"Dataset referenced as NXdata AXIS #{i}")
                return None
    indices = parent.attrs.get(name + "_indices")  # check for alternative Axes
    if indices is int:
        logger.debug(f"Dataset referenced as NXdata alternative AXIS #{indices}")
    return chk_nxdataaxis_v2(hdf_node, name, logger)  # check for older conventions


def check_deprecation_enum_axis(variables, doc, elist, attr, hdf_node):
    """Check for several attributes. - deprecation - enums - nxdataaxis"""
    logger, elem, path = variables
    dep_str = elem.attrib.get("deprecated")  # check for deprecation
    if dep_str:
        if doc:
            logger.debug("DEPRECATED - " + dep_str)
    for base_elem in elist if not attr else [elem]:  # check for enums
        sdoc = get_nxdl_child(base_elem, "enumeration", go_base=False)
        if sdoc is not None:
            if doc:
                logger.debug("enumeration (" + get_node_concept_path(base_elem) + "):")
            for item in sdoc:
                if isinstance(item, ET._Comment):
                    continue
                if get_local_name_from_xml(item) == "item":
                    if doc:
                        logger.debug("-> " + item.attrib["value"])
    chk_nxdataaxis(
        hdf_node, path.split("/")[-1], logger
    )  # look for NXdata reference (axes/signal)
    for base_elem in elist if not attr else [elem]:  # check for doc
        sdoc = get_nxdl_child(base_elem, "doc", go_base=False)
        if doc:
            logger.debug("documentation (" + get_node_concept_path(base_elem) + "):")
            logger.debug(sdoc.text if sdoc is not None else "")
    return logger, elem, path, doc, elist, attr, hdf_node


def get_nxdl_attr_doc(  # pylint: disable=too-many-arguments,too-many-locals
    elem, elist, attr, hdf_node, logger, doc, nxdl_path, req_str, path, hdf_info
):
    """Get nxdl documentation for an attribute"""
    new_elem = []
    old_elem = elem
    attr_inheritance_chain = []
    for elem_index, act_elem1 in enumerate(elist):
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
                elist,
                attr,
                hdf_node,
            ) = check_deprecation_enum_axis(variables, doc, elist, attr, hdf_node)
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
    (class_path, nxdl_path, elist) = get_inherited_hdf_nodes(
        nx_name=get_nxdl_entry(hdf_info),
        hdf_node=hdf_node,
        hdf_path=hdf_info["hdf_path"] if "hdf_path" in hdf_info else None,
        hdf_root=hdf_info["hdf_root"] if "hdf_root" in hdf_info else None,
    )
    # Copy the nxdl_path, otherwise the cached object is altered
    nxdl_path = nxdl_path.copy()
    elem = elist[0] if class_path and elist else None
    if doc:
        logger.debug("classpath: " + str(class_path))
        logger.debug(
            "NOT IN SCHEMA"
            if elem is None
            else "classes:\n" + "\n".join(get_node_concept_path(e) for e in elist)
        )
    # old solution with a single elem instead of using elist
    path = get_nx_class_path(hdf_info)
    req_str = None
    if elem is None:
        if doc:
            logger.debug("")
        return ("None", None, None)
    if attr:
        return get_nxdl_attr_doc(
            elem, elist, attr, hdf_node, logger, doc, nxdl_path, req_str, path, hdf_info
        )
    req_str = get_required_string(elem)  # check for being required
    if doc:
        logger.debug(req_str)
    variables = [logger, elem, path]
    logger, elem, path, doc, elist, attr, hdf_node = check_deprecation_enum_axis(
        variables, doc, elist, attr, hdf_node
    )
    return (req_str, get_nxdl_entry(hdf_info), nxdl_path)


def helper_get_inherited_nodes(hdf_info2, elist, pind, attr):
    """find the best fitting name in all children"""
    hdf_path, hdf_node, hdf_class_path = hdf_info2
    hdf_name = hdf_path[pind]
    hdf_class_name = hdf_class_path[pind]
    if pind < len(hdf_path) - (2 if attr else 1):
        act_nexus_type = "group"
    elif pind == len(hdf_path) - 1 and attr:
        act_nexus_type = "attribute"
    else:
        act_nexus_type = "field" if isinstance(hdf_node, h5py.Dataset) else "group"
    # find the best fitting name in all children
    bestfit = -1
    html_name = None
    for ind in range(len(elist) - 1, -1, -1):
        newelem, fit = get_best_child(
            elist[ind], hdf_node, hdf_name, hdf_class_name, act_nexus_type
        )
        if fit >= bestfit and newelem is not None:
            html_name = get_node_name(newelem)
    return hdf_path, hdf_node, hdf_class_path, elist, pind, attr, html_name


def get_hdf_path(hdf_info):
    """Get the hdf_path from an hdf_info"""
    if "hdf_path" in hdf_info:
        return hdf_info["hdf_path"].split("/")[1:]
    return hdf_info["hdf_node"].name.split("/")[1:]


# pylint: disable=too-many-arguments,too-many-locals
@lru_cache(maxsize=None)
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
    elist = []  # type: ignore[var-annotated]
    add_base_classes(elist, nx_name, elem)
    nxdl_elem_path = [elist[0]]

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

    for pind in range(len(path)):
        hdf_info2 = [hdf_path, hdf_node, hdf_class_path]
        [
            hdf_path,
            hdf_node,
            hdf_class_path,
            elist,
            pind,
            attr,
            html_name,
        ] = helper_get_inherited_nodes(hdf_info2, elist, pind, attr)
        if html_name is None:  # return if NOT IN SCHEMA
            return (class_path, nxdl_elem_path, None)
        elist, html_name = walk_elist(elist, html_name)
        if elist:
            class_path.append(get_nx_class(elist[0]))
            nxdl_elem_path.append(elist[0])
    return (class_path, nxdl_elem_path, elist)


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
            str(hdf_node[()]).split("\n")
            if len(hdf_node.shape) <= 1
            else str(hdf_node[0]).split("\n")
        )
        logger.debug(f'value: {val[0]} {"..." if len(val) > 1 else ""}')
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
        val = str(value).split("\n")
        logger.debug(f'value: {val[0]} {"..." if len(val) > 1 else ""}')
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


def logger_auxiliary_signal(logger, nxdata):
    """Handle the presence of auxiliary signal"""
    aux = nxdata.attrs.get("auxiliary_signals")
    if aux is not None:
        if isinstance(aux, str):
            aux = [aux]
        for asig in aux:
            logger.debug(f"Further auxiliary signal has been identified: {asig}")
    return logger


def print_default_plotable_header(logger):
    """Print a three-lines header"""
    logger.debug("========================")
    logger.debug("=== Default Plotable ===")
    logger.debug("========================")


def get_default_plotable(root, logger):
    """Get default plotable"""
    print_default_plotable_header(logger)
    # v3 from 2014
    # nxentry
    nxentry = None
    default_nxentry_group_name = root.attrs.get("default")
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
    default_group_name = nxgroup.attrs.get("default")
    while default_group_name:
        try:
            nxgroup = nxgroup[default_group_name]
            default_group_name = nxgroup.attrs.get("default")
        except KeyError:
            pass
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
    signal_dataset_name = nxdata.attrs.get("signal")
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


def entry_helper(root):
    """Check entry related data"""
    nxentries = []
    for key in root.keys():
        if (
            isinstance(root[key], h5py.Group)
            and root[key].attrs.get("NX_class")
            and root[key].attrs["NX_class"] == "NXentry"
        ):
            nxentries.append(root[key])
    if len(nxentries) >= 1:
        return nxentries[0]
    return None


def nxdata_helper(nxentry):
    """Check if nxentry hdf5 object has a NX_class and, if it contains NXdata,
    return its value"""
    lnxdata = []
    for key in nxentry.keys():
        if (
            isinstance(nxentry[key], h5py.Group)
            and nxentry[key].attrs.get("NX_class")
            and nxentry[key].attrs["NX_class"] == "NXdata"
        ):
            lnxdata.append(nxentry[key])
    if len(lnxdata) >= 1:
        return lnxdata[0]
    return None


def signal_helper(nxdata):
    """Check signal related data"""
    signals = []
    for key in nxdata.keys():
        if isinstance(nxdata[key], h5py.Dataset):
            signals.append(nxdata[key])
    if (
        len(signals) == 1
    ):  # v3: as there was no selection given, only 1 data field shall exists
        return signals[0]
    if len(signals) > 1:  # v2: select the one with an attribute signal="1" attribute
        for sig in signals:
            if (
                sig.attrs.get("signal")
                and sig.attrs.get("signal") is str
                and sig.attrs.get("signal") == "1"
            ):
                return sig
    return None


def find_attrib_axis_actual_dim_num(nxdata, a_item, ax_list):
    """Finds axis that have defined dimensions"""
    # find those with attribute axis= actual dimension number
    lax = []
    for key in nxdata.keys():
        if isinstance(nxdata[key], h5py.Dataset):
            try:
                if nxdata[key].attrs["axis"] == a_item + 1:
                    lax.append(nxdata[key])
            except KeyError:
                pass
    if len(lax) == 1:
        ax_list.append(lax[0])
    # if there are more alternatives, prioritise the one with an attribute primary="1"
    elif len(lax) > 1:
        for sax in lax:
            if sax.attrs.get("primary") and sax.attrs.get("primary") == 1:
                ax_list.insert(0, sax)
            else:
                ax_list.append(sax)


def get_single_or_multiple_axes(nxdata, ax_datasets, a_item, ax_list):
    """Gets either single or multiple axes from the NXDL"""
    try:
        if isinstance(ax_datasets, str):  # single axis is defined
            # explicite definition of dimension number
            ind = nxdata.attrs.get(ax_datasets + "_indices")
            if ind and ind is int:
                if ind == a_item:
                    ax_list.append(nxdata[ax_datasets])
            elif a_item == 0:  # positional determination of the dimension number
                ax_list.append(nxdata[ax_datasets])
        else:  # multiple axes are listed
            # explicite definition of dimension number
            for aax in ax_datasets:
                ind = nxdata.attrs.get(aax + "_indices")
                if ind and isinstance(ind, int):
                    if ind == a_item:
                        ax_list.append(nxdata[aax])
            if not ax_list and a_item < len(
                ax_datasets
            ):  # positional determination of the dimension number
                ax_list.append(nxdata[ax_datasets[a_item]])
    except KeyError:
        pass
    return ax_list


def axis_helper(dim, nxdata, signal, axes, logger):
    """Check axis related data"""
    for a_item in range(dim):
        ax_list = []
        ax_datasets = nxdata.attrs.get("axes")  # primary axes listed in attribute axes
        ax_list = get_single_or_multiple_axes(nxdata, ax_datasets, a_item, ax_list)
        for attr in nxdata.attrs.keys():  # check for corresponding AXISNAME_indices
            if (
                attr.endswith("_indices")
                and nxdata.attrs[attr] == a_item
                and nxdata[attr.split("_indices")[0]] not in ax_list
            ):
                ax_list.append(nxdata[attr.split("_indices")[0]])
        # v2  # check for ':' separated axes defined in Signal
        if not ax_list:
            try:
                ax_datasets = signal.attrs.get("axes").split(":")
                ax_list.append(nxdata[ax_datasets[a_item]])
            except (KeyError, AttributeError):
                pass
        if not ax_list:  # check for axis/primary specifications
            find_attrib_axis_actual_dim_num(nxdata, a_item, ax_list)
        axes.append(ax_list)
        logger.debug("")
        logger.debug(
            f"For Axis #{a_item}, {len(ax_list)} axes have been identified: {str(ax_list)}"
        )


def get_all_is_a_rel_from_hdf_node(hdf_node, hdf_path):
    """Return list of nxdl concept paths for a nxdl element which corresponds to
    hdf node.
    """
    hdf_info = {"hdf_path": hdf_path, "hdf_node": hdf_node}
    (_, _, elist) = get_inherited_hdf_nodes(
        nx_name=get_nxdl_entry(hdf_info),
        hdf_node=hdf_node,
        hdf_path=hdf_info["hdf_path"] if "hdf_path" in hdf_info else None,
        hdf_root=hdf_info["hdf_root"] if "hdf_root" in hdf_info else None,
    )
    return elist


def hdf_node_to_self_concept_path(hdf_info, logger):
    """Get concept or nxdl path from given hdf_node."""
    # The bellow logger is for deactivatine unnecessary debug message above
    if logger is None:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
    (_, _, nxdl_path) = get_nxdl_doc(hdf_info, logger, None)
    con_path = ""
    if nxdl_path:
        for nd_ in nxdl_path:
            con_path = con_path + "/" + get_node_name(nd_)
    return con_path


class HandleNexus:
    """documentation"""

    # pylint: disable=too-many-instance-attributes
    def __init__(
        self,
        logger,
        nexus_file,
        d_inq_nd=None,
        c_inq_nd=None,
        is_in_memory_file=False,
    ):
        self.logger = logger
        local_dir = os.path.abspath(os.path.dirname(__file__))

        self.input_file_name = (
            nexus_file
            if nexus_file is not None
            else os.path.join(local_dir, "../data/201805_WSe2_arpes.nxs")
        )
        self.parser = None
        self.in_file = None
        self.is_hdf5_file_obj = is_in_memory_file
        self.d_inq_nd = d_inq_nd
        self.c_inq_nd = c_inq_nd
        # Aggregating hdf path corresponds to concept query node
        self.hdf_path_list_for_c_inq_nd = []

    def visit_node(self, hdf_name, hdf_node):
        """Function called by h5py that iterates on each node of hdf5file.
        It allows h5py visititems function to visit nodes."""
        if self.d_inq_nd is None and self.c_inq_nd is None:
            process_node(hdf_node, "/" + hdf_name, self.parser, self.logger)
        elif self.d_inq_nd is not None and hdf_name in (
            self.d_inq_nd,
            self.d_inq_nd[1:],
        ):
            process_node(hdf_node, "/" + hdf_name, self.parser, self.logger)
        elif self.c_inq_nd is not None:
            attributed_concept = self.c_inq_nd.split("@")
            attr = attributed_concept[1] if len(attributed_concept) > 1 else None
            elist = get_all_is_a_rel_from_hdf_node(hdf_node, "/" + hdf_name)
            if elist is None:
                return
            fnd_superclass = False
            fnd_superclass_attr = False
            for elem in reversed(elist):
                tmp_path = elem.get("nxdlbase").split(".nxdl")[0]
                con_path = "/NX" + tmp_path.split("NX")[-1] + elem.get("nxdlpath")
                if fnd_superclass or con_path == attributed_concept[0]:
                    fnd_superclass = True
                    if attr is None:
                        self.hdf_path_list_for_c_inq_nd.append(hdf_name)
                        break
                    for attribute in hdf_node.attrs.keys():
                        attr_concept = get_nxdl_child(
                            elem, attribute, nexus_type="attribute", go_base=False
                        )
                        if attr_concept is not None and attr_concept.get(
                            "nxdlpath"
                        ).endswith(attr):
                            fnd_superclass_attr = True
                            con_path = (
                                "/NX"
                                + tmp_path.split("NX")[-1]
                                + attr_concept.get("nxdlpath")
                            )
                            self.hdf_path_list_for_c_inq_nd.append(
                                hdf_name + "@" + attribute
                            )
                            break
                if fnd_superclass_attr:
                    break

    def not_yet_visited(self, root, name):
        """checking if a new node has already been visited in its path"""
        path = name.split("/")
        for i in range(1, len(path)):
            act_path = "/".join(path[:i])
            # print(act_path+' - '+name)
            if root["/" + act_path] == root["/" + name]:
                return False
        return True

    def full_visit(self, root, hdf_node, name, func):
        """visiting recursivly all children, but avoiding endless cycles"""
        # print(name)
        if len(name) > 0:
            func(name, hdf_node)
        if isinstance(hdf_node, h5py.Group):
            for ch_name, child in hdf_node.items():
                full_name = ch_name if len(name) == 0 else name + "/" + ch_name
                if self.not_yet_visited(root, full_name):
                    self.full_visit(root, child, full_name, func)

    def process_nexus_master_file(self, parser):
        """Process a nexus master file by processing all its nodes and their attributes"""
        self.parser = parser
        try:
            if not self.is_hdf5_file_obj:
                self.in_file = h5py.File(
                    self.input_file_name[0]
                    if isinstance(self.input_file_name, list)
                    else self.input_file_name,
                    "r",
                )
            else:
                self.in_file = self.input_file_name

            self.full_visit(self.in_file, self.in_file, "", self.visit_node)

            if self.d_inq_nd is None and self.c_inq_nd is None:
                get_default_plotable(self.in_file, self.logger)
            # To log the provided concept and concepts founded
            if self.c_inq_nd is not None:
                for hdf_path in self.hdf_path_list_for_c_inq_nd:
                    self.logger.info(hdf_path)
        finally:
            # To test if hdf_file is open print(self.in_file.id.valid)
            self.in_file.close()
            # To test if hdf_file is open print(self.in_file.id.valid)


@click.command()
@click.option(
    "-f",
    "--nexus-file",
    required=False,
    default=None,
    help=(
        "NeXus file with extension .nxs to learn NeXus different concept"
        " documentation and concept."
    ),
)
@click.option(
    "-d",
    "--documentation",
    required=False,
    default=None,
    help=(
        "Definition path in nexus output (.nxs) file. Returns debug"
        "log relavent with that definition path. Example: /entry/data/delays"
    ),
)
@click.option(
    "-c",
    "--concept",
    required=False,
    default=None,
    help=(
        "Concept path from application definition file (.nxdl,xml). Finds out"
        "all the available concept definition (IS-A realation) for rendered"
        "concept path. Example: /NXarpes/ENTRY/INSTRUMENT/analyser"
    ),
)
def main(nexus_file, documentation, concept):
    """The main function to call when used as a script."""
    logging_format = "%(levelname)s: %(message)s"
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    logging.basicConfig(
        level=logging.INFO, format=logging_format, handlers=[stdout_handler]
    )
    logger = logging.getLogger(__name__)
    logger.addHandler(stdout_handler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    if documentation and concept:
        raise ValueError(
            "Only one option either documentation (-d) or is_a relation "
            "with a concept (-c) can be requested."
        )
    nexus_helper = HandleNexus(
        logger, nexus_file, d_inq_nd=documentation, c_inq_nd=concept
    )
    nexus_helper.process_nexus_master_file(None)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
