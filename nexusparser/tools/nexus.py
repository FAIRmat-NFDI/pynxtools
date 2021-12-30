#!/usr/bin/env python3
"""Read files from different format and print it in a standard Nexus format

"""
# Nexus definitions in github: https://github.com/nexusformat/definitions
# to be cloned under os.environ['NEXUS_DEF_PATH']

import os
import xml.etree.ElementTree as ET
import sys
import logging
import textwrap
from lxml import etree, objectify
import h5py

# LOGGING_FORMAT = "%(levelname)s: %(message)s"
# stdout_handler = logging.StreamHandler(sys.stdout)
# stdout_handler.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT, handlers=[stdout_handler])
# logger = logging.getLogger()

# check for NEXUS definitions
try:
    # either given by sys env
    NEXUS_DEF_PATH = os.environ['NEXUS_DEF_PATH']
except BaseException:
    # or it should be available locally under the dir 'definitions'
    LOCAL_DIR = os.path.abspath(os.path.dirname(__file__))
    NEXUS_DEF_PATH = os.path.join(LOCAL_DIR, '../definitions')


def get_nx_class_path(hdf_node):
    """Get the full path of an HDF5 node using nexus classes
in case of a field, end with the field name

"""

    if hdf_node.name == '/':
        return ''
    if isinstance(hdf_node, h5py.Group):
        return get_nx_class_path(
            hdf_node.parent) + '/' + hdf_node.attrs['NX_class']
    if isinstance(hdf_node, h5py.Dataset):
        return get_nx_class_path(
            hdf_node.parent) + '/' + hdf_node.name.split('/')[-1]
    return ''


def get_nxdl_entry(hdf_node):
    """Get the nxdl application definition for an HDF5 node

"""

    entry = hdf_node
    while isinstance(entry,
                     h5py.Dataset) or entry.attrs['NX_class'] != 'NXentry':
        entry = entry.parent
        if entry.name == '/':
            return 'NO NXentry found'
    try:
        nxdef = entry['definition'][()]
        return nxdef.decode()
    except BaseException:
        return 'NO Definition referenced'


def get_nx_class(nxdl_elem):
    """Get the nexus class for a NXDL node

"""
    try:
        return nxdl_elem.attrib['type']
    except BaseException:
        return 'NX_CHAR'


def get_nx_namefit(hdf_name, name):
    """Checks if an HDF5 node name corresponds to a child of the NXDL element
uppercase letters in front can be replaced by arbitraty name, but
uppercase to lowercase match is preferred,
so such match is counted as a measure of the fit

"""
    # count leading capitals
    counting = 0
    while counting < len(name) and name[counting] >= 'A' and name[counting] <= 'Z':
        counting += 1
    # if potential fit
    if counting == len(name) or hdf_name.endswith(name[counting:]):
        # count the matching chars
        fit = 0
        for i in range(max(counting, len(hdf_name))):
            if hdf_name[i].upper() == name[i]:
                fit += 1
            else:
                break
        # accept only full fits as better fits
        if fit == max(counting, len(hdf_name)):
            return fit
        return 0
    # no fit
    return -1


def get_nx_classes():
    """Read base classes from the Nexus definition/base_classes folder

"""
    base_classes_list_files = os.listdir(os.path.join(NEXUS_DEF_PATH, 'base_classes'))
    nx_clss = sorted([s.strip('.nxdl.xml') for s in base_classes_list_files])
    return nx_clss


def get_nx_units():
    """Read unit kinds from the Nexus definition/nxdlTypes.xsd file

"""
    filepath = NEXUS_DEF_PATH + '/nxdlTypes.xsd'
    tree = ET.parse(filepath)
    root = tree.getroot()
    units_and_type_list = []
    for child in root:
        for i in child.attrib.values():
            units_and_type_list.append(i)
    flag = False
    for line in units_and_type_list:
        if line == 'anyUnitsAttr':
            flag = True
            nx_units = []
        elif 'NX' in line and flag is True:
            nx_units.append(line)
        elif line == 'primitiveType':
            flag = False
        else:
            pass
    return nx_units


def get_nx_attribute_type():
    """Read attribute types from the Nexus definition/nxdlTypes.xsd file

"""
    filepath = NEXUS_DEF_PATH + '/nxdlTypes.xsd'
    tree = ET.parse(filepath)
    root = tree.getroot()
    units_and_type_list = []
    for child in root:
        for i in child.attrib.values():
            units_and_type_list.append(i)
    flag = False
    for line in units_and_type_list:
        if line == 'primitiveType':
            flag = True
            nx_types = []
        elif 'NX' in line and flag is True:
            nx_types.append(line)
        elif line == 'anyUnitsAttr':
            flag = False
        else:
            pass
    return nx_types


def get_node_name(node):
    '''Node - xml node
returns:
    html documentation name
    Either as specified by the 'name' or taken from the type (nx_class).
    Note that if only class name is available, the NX prefix is removed and
    the string is coverted to UPPER case.

'''
    if 'name' in node.attrib.keys():
        name = node.attrib['name']
    else:
        name = node.attrib['type']
        if name.startswith('NX'):
            name = name[2:].upper()
    return name


def belongs_to(nxdl_elem, child, hdf_name):
    """Checks if an HDF5 node name corresponds to a child of the NXDL element
uppercase letters in front can be replaced by arbitraty name, but
uppercase to lowercase match is preferred

"""
    # check if nameType allows different name
    try:
        if child.attrib['nameType'] == "any":
            name_any = True
        else:
            name_any = False
    except BaseException:
        name_any = False
    childname = get_node_name(child)
    name = hdf_name[2:].upper() if hdf_name.startswith('NX') and 'name\
    ' not in child.attrib else hdf_name
    # and no reserved words used
    if name_any and name != 'doc' and name != 'enumeration':
        # check if name fits
        fit = get_nx_namefit(name, childname)
        if fit < 0:
            return False
        for child2 in nxdl_elem.getchildren():
            if etree.QName(child).localname != \
                    etree.QName(child2).localname or get_node_name(child2) == childname:
                continue
            # check if the name of another sibling fits better
            fit2 = get_nx_namefit(name, get_node_name(child2))
            if fit2 > fit:
                return False
        # accept this fit
        return True
    else:
        if childname == name:
            return True
    return False


def get_own_nxdl_child(nxdl_elem, name):
    """Checks if an NXDL child node fits to the specific name

"""
    for child in nxdl_elem.getchildren():
        if etree.QName(child).localname == 'group' and belongs_to(nxdl_elem, child, name):
            # get_nx_class(child) == name:
            return child
        if etree.QName(child).localname == 'field' and belongs_to(nxdl_elem, child, name):
            return child
        if etree.QName(child).localname == 'attribute' and belongs_to(nxdl_elem,
                                                                      child, name):
            return child
        if etree.QName(child).localname == 'doc' and name == 'doc':
            return child
        if etree.QName(
                child).localname == 'enumeration' and name == 'enumeration':
            return child
    return None


def get_nxdl_child(nxdl_elem, name):
    """Get the NXDL child node corresponding to a specific name
(e.g. of an HDF5 node,or of a documentation)
note that if child is not found in application definition,
it also checks for the base classes

"""
    own_child = get_own_nxdl_child(nxdl_elem, name)
    if own_child is not None:
        return own_child
    # check in the base class
    bc_name = get_nx_class(nxdl_elem)
    # filter primitive types
    if bc_name[2] == '_':
        return None
    bc_obj = objectify.parse(NEXUS_DEF_PATH + '/base_classes/' + bc_name + '.nxdl.xml').getroot()
    return get_own_nxdl_child(bc_obj, name)


def get_required_string(nxdl_elem):
    """Check for being required
REQUIRED, RECOMMENDED, OPTIONAL, NOT IN SCHEMA

"""
    if nxdl_elem is None:
        return "<<NOT IN SCHEMA>>"
    # if optionality is defined
    elif ('optional' in nxdl_elem.attrib.keys() and nxdl_elem.attrib['optional'] == "true") or \
        ('minOccurs' in nxdl_elem.attrib.keys() and nxdl_elem.attrib['minOccurs'] == "0") or \
            ('required' in nxdl_elem.attrib.keys() and nxdl_elem.attrib['required'] == "false"):
        return "<<OPTIONAL>>"
    elif ('optional' in nxdl_elem.attrib.keys() and nxdl_elem.attrib['optional'] == "false") or \
        ('minOccurs' in nxdl_elem.attrib.keys() and int(nxdl_elem.attrib['minOccurs']) > 0) or \
            ('required' in nxdl_elem.attrib.keys() and nxdl_elem.attrib['required'] == "true"):
        return "<<REQUIRED>>"
    # new expression for being recommended
    elif 'recommended' in nxdl_elem.attrib.keys() and nxdl_elem.attrib['recommended'] == "true":
        return "<<RECOMMENDED>>"
    # default optionality
    # in BASE CLASSES: true
    # in APPLICATIONS: false
    elif "base_classes" in nxdl_elem.base:
        return "<<OPTIONAL>>"
    return "<<REQUIRED>>"


def chk_nxdataaxis_v2(hdf_node, name):
    """Check if dataset is an axis

"""
    # check for being a Signal
    own_signal = hdf_node.attrs.get('signal')
    if own_signal is str and own_signal == "1":
        LOGGER.info("Dataset referenced (v2) as NXdata SIGNAL")
    # check for being an axis
    own_axes = hdf_node.attrs.get('axes')
    if own_axes is str:
        axes = own_axes.split(':')
        for i in len(axes):
            if axes[i] and name == axes[i]:
                LOGGER.info("Dataset referenced (v2) as NXdata AXIS #%d", i)
                return
    ownpaxis = hdf_node.attrs.get('primary')
    own_axis = hdf_node.attrs.get('axis')
    assert own_axis is int, 'axis is not int type!'
    # also convention v1
    if ownpaxis is int and ownpaxis == 1:
        LOGGER.info("Dataset referenced (v2) as NXdata AXIS #%d", own_axis - 1)
        return
    if not (ownpaxis is int and ownpaxis == 1):
        LOGGER.info(
            "Dataset referenced (v2) as NXdata (primary/alternative) AXIS #%d", own_axis - 1)
        return


def chk_nxdataaxis(hdf_node, name, loger):
    """NEXUS Data Plotting Standard v3: new version from 2014

"""
    # check if it is a field in an NXdata node
    if not isinstance(hdf_node, h5py.Dataset):
        return
    parent = hdf_node.parent
    if not parent or (parent and not parent.attrs.get('NX_class') == "NXdata"):
        return
    # chk for Signal
    signal = parent.attrs.get('signal')
    if signal and name == signal:
        loger.info("Dataset referenced as NXdata SIGNAL")
        return
    # check for default Axes
    axes = parent.attrs.get('axes')
    if axes is str:
        if name == axes:
            loger.info("Dataset referenced as NXdata AXIS")
            return
    elif axes is not None:
        for i, j in enumerate(axes):
            if name == axes[i.index(j)]:
                indices = parent.attrs.get(axes[i.index(j)] + '_indices')
                if indices is int:
                    loger.info("Dataset referenced as NXdata AXIS #%d" % indices)
                else:
                    loger.info("Dataset referenced as NXdata AXIS #%d" % i.index(j))
                return
    # check for alternative Axes
    indices = parent.attrs.get(name + '_indices')
    if indices is int:
        loger.info("Dataset referenced as NXdata alternative AXIS #%d" % indices)
    # check for older conventions
    return chk_nxdataaxis_v2(hdf_node, name)


def get_nxdl_doc(hdf_node, loger, doc, attr=False):
    """Get nxdl documentation for an HDF5 node (or its attribute)

"""

    nxdef = get_nxdl_entry(hdf_node)
    root = objectify.parse(NEXUS_DEF_PATH + "/applications/" + nxdef + ".nxdl.xml")
    elem = root.getroot()
    nxdl_path = [elem]
    path = get_nx_class_path(hdf_node)
    req_str = None
    for group in path.split('/')[1:]:
        if group.startswith('NX'):
            elem = get_nxdl_child(elem, group)
            if elem is not None:
                if doc:
                    loger.info("/" + group)
                nxdl_path.append(elem)
            else:
                if doc:
                    loger.info("/" + group + " - IS NOT IN SCHEMA")
        else:
            if elem is not None:
                elem = get_nxdl_child(elem, group)
                nxdl_path.append(elem)
            if elem is not None:
                if attr:
                    if doc:
                        loger.info("/" + group)
                else:
                    if doc:
                        loger.info("/" + group + ' [' + get_nx_class(elem) + ']')
            else:
                if doc:
                    loger.info("/" + group + " - IS NOT IN SCHEMA")
    if elem is not None and attr:
        # NX_class is a compulsory attribute for groups in a nexus file
        # which should match the type of the corresponding NXDL element
        if attr == 'NX_class' and not isinstance(hdf_node, h5py.Dataset):
            elem = None
            if doc:
                loger.info("@" + attr + ' [NX_CHAR]')
        # units category is a compulsory attribute for any fields
        elif attr == 'units' and isinstance(hdf_node, h5py.Dataset):
            req_str = "<<REQUIRED>>"
            try:
                # try to find if units is deinfed inside the field in the NXDL element
                unit = elem.attrib[attr]
                if doc:
                    loger.info("@" + attr + ' [' + unit + ']')
                elem = None
                nxdl_path.append(attr)
            except BaseException:
                # otherwise try to find if units is defined as a child of the NXDL element
                elem = get_nxdl_child(elem, attr)
                if elem is not None:
                    if doc:
                        loger.info("@" + attr + ' - [' + get_nx_class(elem) + ']')
                    nxdl_path.append(elem)
                else:
                    # if no units category were defined in NXDL:
                    if doc:
                        loger.info("@" + attr + " - REQUIRED, but undefined unit category")
                    nxdl_path.append(attr)
                    # pass
        # units for attributes can be given as ATTRIBUTENAME_units
        elif attr.endswith('_units'):
            # check for ATTRIBUTENAME_units in NXDL (normal)
            elem2 = get_nxdl_child(elem, attr)
            if elem2 is not None:
                elem = elem2
                if doc:
                    loger.info("@" + attr + ' - [' + get_nx_class(elem) + ']')
                nxdl_path.append(elem)
            else:
                # if not defined, check for ATTRIBUTENAME to see if the ATTRIBUTE
                # is in the SCHEMA, but no units category were defined
                elem2 = get_nxdl_child(elem, attr[:-6])
                if elem2 is not None:
                    req_str = '<<RECOMMENDED>>'
                    if doc:
                        loger.info("@" + attr + " - RECOMMENDED, but undefined unit category")
                    nxdl_path.append(attr)
                else:
                    # otherwise: NOT IN SCHEMA
                    elem = elem2
                    if doc:
                        loger.info("@" + attr + " - IS NOT IN SCHEMA")
        # other attributes
        else:
            elem = get_nxdl_child(elem, attr)
            if elem is not None:
                if doc:
                    loger.info("@" + attr + ' - [' + get_nx_class(elem) + ']')
                nxdl_path.append(elem)
            else:
                if doc:
                    loger.info("@" + attr + " - IS NOT IN SCHEMA")
    if elem is None and req_str is None:
        if doc:
            loger.info("")
        return ('None', None, None, None)
    else:
        if req_str is None:
            # check for being required
            req_str = get_required_string(elem)
            if doc:
                loger.info(req_str)
        if elem is not None:
            # check for deprecation
            dep_str = elem.attrib.get('deprecated')
            if dep_str:
                if doc:
                    loger.info("DEPRECATED - " + dep_str)
            # check for enums
            sdoc = get_nxdl_child(elem, 'enumeration')
            if sdoc is not None:
                if doc:
                    loger.info("enumeration:")
                for item in sdoc.getchildren():
                    if etree.QName(item).localname == 'item':
                        if doc:
                            loger.info("-> " + item.attrib['value'])
            # check for NXdata references (axes/signal)
            chk_nxdataaxis(hdf_node, path.split('/')[-1], loger)
            # check for doc
            sdoc = get_nxdl_child(elem, 'doc')
            if doc:
                loger.info(sdoc if sdoc is not None else "")
        return (req_str, elem, nxdef, nxdl_path)


def get_doc(node, ntype, level, nxhtml, nxpath):
    """Get documentation

    """
    # URL for html documentation
    anchor = ''
    for n_item in nxpath:
        anchor += n_item.lower() + "-"
    anchor = ('https://manual.nexusformat.org/classes/',
              nxhtml + "#" + anchor.replace('_', '-') + ntype)
    if not ntype:
        anchor = anchor[:-1]

    # RST documentation from the field 'doc'
    try:
        doc = node.doc.pyval
    except BaseException:
        doc = ""

    # enums
    (index, enums) = get_enums(node)
    if index:
        enum_str = "\n " + ("Possible values:"
                            if len(enums.split(',')) > 1
                            else "Obligatory value:") + "\n   " + enums + "\n"
    else:
        enum_str = ""

    return anchor, doc + enum_str


def print_doc(node, ntype, level, nxhtml, nxpath):
    anchor, doc = get_doc(node, ntype, level, nxhtml, nxpath)
    print("  " * (level + 1) + anchor)

    preferred_width = 80 + level * 2
    wrapper = textwrap.TextWrapper(initial_indent='  ' * (level + 1), width=preferred_width,
                                   subsequent_indent='  ' * (level + 1), expand_tabs=False,
                                   tabsize=0)
    # doc=node.find('doc')
    if doc is not None:
        # for par in doc.text.split('\n'):
        for par in doc.split('\n'):
            print(wrapper.fill(par))
    # print(doc.text if doc is not None else "")


def get_enums(node):
    """
    makes list of enumerations, if node contains any.
    Returns comma separated STRING of enumeration values, if there are enum tag,
    otherwise empty string.
    """
    # collect item values from enumeration tag, if any
    try:
        for items in node.enumeration:
            enums = []
            for values in items.findall('item'):
                enums.append("'" + values.attrib['value'] + "'")
            enums = ','.join(enums)
            return (True, '[' + enums + ']')
    # if there is no enumeration tag, returns empty string
    except BaseException:
        return (False, '')


def nxdl_to_attr_obj(nxdl_path):  # Leave this one
    """
    Finds the path entry in NXDL file
    Grabs all the attrs in NXDL entry
    Checks Nexus base application defs for missing attrs and adds them as well
    returns attr as a Python obj that can be directly placed into the h5py library
    """
    nxdef = nxdl_path.split(':')[0]
    root = objectify.parse(NEXUS_DEF_PATH + "/applications/" + nxdef + ".nxdl.xml")
    elem = root.getroot()
    path = nxdl_path.split(':')[1]
    for group in path.split('/')[1:]:
        elem = get_nxdl_child(elem, group)
    return elem


def process_node(hdf_node, parser, logger, doc=True):
    """
            #processes an hdf5 node
            #- it logs the node found and also checks for its attributes
            #- retrieves the corresponding nxdl documentation
            #TODO:
            # - follow variants
            # - NOMAD parser: store in NOMAD
            """
    hdf_path = hdf_node.name
    if isinstance(hdf_node, h5py.Dataset):
        logger.info('===== FIELD (/%s): %s' % (hdf_path, hdf_node))
        val = str(hdf_node[()]).split('\n') if len(hdf_node.shape) <= 1 else str(
            hdf_node[0]).split('\n')
        logger.info('value: %s %s' % (val[0], "..." if len(val) > 1 else ''))
    else:
        logger.info('===== GROUP (/%s [%s::%s]): %s' %
                    (hdf_path, get_nxdl_entry(hdf_node),
                     get_nx_class_path(hdf_node), hdf_node))
    (req_str, elem, nxdef, nxdl_path) = get_nxdl_doc(hdf_node, logger, doc)
    if parser is not None and isinstance(hdf_node, h5py.Dataset):
        parser(hdf_path, hdf_node, nxdef, nxdl_path, val)
    for key, value in hdf_node.attrs.items():
        logger.info('===== ATTRS (/%s@%s)' % (hdf_path, key))
        val = str(value).split('\n')
        logger.info('value: %s %s' % (val[0], "..." if len(val) > 1 else ''))
        (req_str, elem, nxdef, nxdl_path) = get_nxdl_doc(hdf_node, logger, doc, attr=key)
        if parser is not None and 'NOT IN SCHEMA' not in req_str and 'None' not in req_str:
            parser(hdf_path, hdf_node, nxdef, nxdl_path, val)


def get_default_plotable(root, parser, logger):
    logger.info('========================')
    logger.info('=== Default Plotable ===')
    logger.info('========================')
    # v3 from 2014

    # nxentry
    nxentry = None
    default_nxentry_group_name = root.attrs.get("default")
    if default_nxentry_group_name:
        try:
            nxentry = root[default_nxentry_group_name]
        except BaseException:
            nxentry = None
    if not nxentry:
        nxentries = []
        for key in root.keys():
            if (isinstance(root[key], h5py.Group) and root[key].attrs.get('NX_class\
            ') and root[key].attrs['NX_class'] == "NXentry"):
                nxentries.append(root[key])
        # v3: as there was no selection given, only 1 nxentry shall exists
        # v2: take any
        if len(nxentries) >= 1:
            nxentry = nxentries[0]
    if not nxentry:
        logger.info('No NXentry has been found')
        return
    logger.info('')
    logger.info('NXentry has been identified: ' + nxentry.name)
    # process_node(nxentry, None, False)
    # nxdata
    nxdata = None
    default_nxdata_group_name = nxentry.attrs.get("default")
    if default_nxdata_group_name:
        try:
            nxdata = nxentry[default_nxdata_group_name]
        except BaseException:
            nxdata = None
    if not nxdata:
        lnxdata = []
        for key in nxentry.keys():
            if isinstance(nxentry[key], h5py.Group) and nxentry[key].attrs.get('NX_class\
            ') and nxentry[key].attrs['NX_class'] == "NXdata":
                lnxdata.append(nxentry[key])
        # v3: as there was no selection given, only 1 nxdata shall exists
        # v2: take any
        if len(lnxdata) >= 1:
            nxdata = lnxdata[0]
    if not nxdata:
        logger.info('No NXdata group has been found')
        return
    logger.info('')
    logger.info('NXdata group has been identified: ' + nxdata.name)
    process_node(nxdata, None, logger, False)
    # signal
    signal = None
    signal_dataset_name = nxdata.attrs.get("signal")
    try:
        signal = nxdata[signal_dataset_name]
    except BaseException:
        signal = None
    if not signal:
        signals = []
        for key in nxdata.keys():
            if isinstance(nxdata[key], h5py.Dataset):
                signals.append(nxdata[key])
        # v3: as there was no selection given, only 1 data field shall exists
        if len(signals) == 1:
            signal = signals[0]
        # v2: select the one with an attribute signal="1" attribute
        elif len(signals) > 1:
            for sig in signals:
                if sig.attrs.get("signal") and sig.attrs.get("signal\
                ") is str and sig.attrs.get("signal") == "1":
                    signal = sig
                    break
    if not signal:
        logger.info('No Signal has been found')
        return
    logger.info('')
    logger.info('Signal has been identified: ' + signal.name)
    process_node(signal, None, logger, False)
    dim = len(signal.shape)
    # axes
    axes = []
    for a_item in range(dim):
        ax_list = []
        # primary axes listed in attribute axes
        ax_datasets = nxdata.attrs.get("axes")
        try:
            # single axis is defined
            if ax_datasets is str:
                # explicite definition of dimension number
                ind = nxdata.attrs.get(ax_datasets + '_indices')
                if ind and ind is int:
                    if ind == a_item:
                        ax_list.append(nxdata[nxdata[ax_datasets]])
                # positional determination of the dimension number
                elif a_item == 0:
                    ax_list.append(nxdata[nxdata[ax_datasets]])
            # multiple axes are listed
            else:
                # explicite definition of dimension number
                for aax in ax_datasets:
                    ind = nxdata.attrs.get(aax + '_indices')
                    if ind and ind is int:
                        if ind == a_item:
                            ax_list.append(nxdata[nxdata[aax]])
                # positional determination of the dimension number
                if not ax_list:
                    ax_list.append(nxdata[ax_datasets[a_item]])
        except BaseException:
            pass
        # check for corresponding AXISNAME_indices
        for attr in nxdata.attrs.keys():
            if attr.endswith('_indices') and nxdata.sttrs[attr] == a_item:
                ax_list.append(nxdata[attr.split('_indices')[0]])
        # v2
        # check for ':' separated axes defined in Signal
        if not ax_list:
            try:
                ax_datasets = signal.attrs.get("axes").split(':')
                ax_list.append(nxdata[ax_datasets[a_item]])
            except BaseException:
                pass
        # check for axis/primary specifications
        if not ax_list:
            # find those with attribute axis= actual dimension number
            lax = []
            for key in nxdata.keys():
                if isinstance(nxdata[key], h5py.Dataset):
                    try:
                        if nxdata[key].attrs['axis'] == a_item + 1:
                            lax.append(nxdata[key])
                    except BaseException:
                        pass
            if len(lax) == 1:
                ax_list.append(lax[0])
            # if there are more alternatives, prioritise the one with an attribute primary="1"
            elif len(lax) > 1:
                for sax in lax:
                    if sax.attrs.get('primary') and sax.attrs.get('primary') == 1:
                        ax_list.insert(0, sax)
                    else:
                        ax_list.append(sax)
        axes.append(ax_list)
        logger.info('')
        logger.info('For Axis #%d, %d axes have been identified: %s\
        ' % (a_item, len(ax_list), str(ax_list)))


class HandleNexus:
    """documentation

    """
    def __init__(self, logger, args):
        self.logger = logger
        self.input_file_name = args[0] if len(
            # args) >= 1 else 'wcopy/from_dallanto_master_from_defs.h5'
            # args) >= 1 else 'ARPES/201805_WSe2_arpes.nxs'
            args) >= 1 else 'tests/data/nexus_test_data/201805_WSe2_arpes.nxs'
        self.parser = None
        self.in_file = None

    def visit_node(self, hdf_path, hdf_node):
        """Visit node

        """
        process_node(hdf_node, self.parser, self.logger)

    def process_nexus_master_file(self, parser):
        """
        Process a nexus master file by processing all its nodes and their attributes

        """
        self.parser = parser
        self.in_file = h5py.File(self.input_file_name, 'r')
        self.in_file.visititems(self.visit_node)
        get_default_plotable(self.in_file, self.parser, self.logger)
        self.in_file.close()


if __name__ == '__main__':
    LOGGING_FORMAT = "%(levelname)s: %(message)s"
    STDOUT_HANDLER = logging.StreamHandler(sys.stdout)
    STDOUT_HANDLER.setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT, handlers=[STDOUT_HANDLER])
    LOGGER = logging.getLogger()
    NEXUS_HELPER = HandleNexus(LOGGER, sys.argv[1:])
    NEXUS_HELPER.process_nexus_master_file(None)
