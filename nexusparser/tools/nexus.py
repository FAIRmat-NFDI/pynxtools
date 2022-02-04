"""Read files from different format and print it in a standard Nexus format

"""
# Nexus definitions in github: https://github.com/nexusformat/definitions
# to be cloned under os.environ['NEXUS_DEF_PATH']

import os
import xml.etree.ElementTree as ET
import re
import sys
import logging
import textwrap
import h5py

# LOGGING_FORMAT = "%(levelname)s: %(message)s"
# stdout_handler = logging.StreamHandler(sys.stdout)
# stdout_handler.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT, handlers=[stdout_handler])
# logger = logging.getLogger()


# check for NEXUS definitions
def get_nexus_definitions_path():
    """Check NEXUS_DEF_PATH variable.
If it is empty, this function is filling it

"""
    try:
        # either given by sys env
        return os.environ['NEXUS_DEF_PATH']
    except KeyError:
        # or it should be available locally under the dir 'definitions'
        local_dir = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(local_dir, f"..{os.sep}definitions")


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
    except KeyError:
        return 'NO Definition referenced'


def get_nx_class(nxdl_elem):
    """Get the nexus class for a NXDL node

"""
    try:
        return nxdl_elem.attrib['type']
    except KeyError:
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
    base_classes_list_files = os.listdir(os.path.join(get_nexus_definitions_path(), 'base_classes'))
    nx_clss = sorted([str(s)[:-9] for s in base_classes_list_files])
    return nx_clss


def get_nx_units():
    """Read unit kinds from the Nexus definition/nxdlTypes.xsd file

"""
    filepath = f"{get_nexus_definitions_path()}{os.sep}nxdlTypes.xsd"
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
    filepath = get_nexus_definitions_path() + '/nxdlTypes.xsd'
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
        name_any = bool(child.attrib['nameType'] == "any")
        # if child.attrib['nameType'] == "any":
        #    name_any = True
        # else:
        #    name_any = False
    except KeyError:
        name_any = False
    childname = get_node_name(child)
    nx_class_regex = re.compile(r"NX[a-z_]+")
    name = hdf_name[2:].upper() if nx_class_regex.search(hdf_name) and 'name\
    ' not in child.attrib else hdf_name
    # and no reserved words used
    if name_any and name != 'doc' and name != 'enumeration':
        # check if name fits
        fit = get_nx_namefit(name, childname)
        if fit < 0:
            return False
        for child2 in nxdl_elem:
            if get_local_name_from_xml(child) != \
                    get_local_name_from_xml(child2) or get_node_name(child2) == childname:
                continue
            # check if the name of another sibling fits better
            fit2 = get_nx_namefit(name, get_node_name(child2))
            if fit2 > fit:
                return False
        # accept this fit
        return True
    if childname == name:
        return True
    return False


def get_local_name_from_xml(element):
    """Helper function to extract the element tag without the namespace."""
    return element.tag[element.tag.rindex("}") + 1:]


def get_own_nxdl_child(nxdl_elem, name):
    """Checks if an NXDL child node fits to the specific name"""
    for child in nxdl_elem:
        if get_local_name_from_xml(child) == 'group' and belongs_to(nxdl_elem, child, name):
            # get_nx_class(child) == name:
            return child
        if get_local_name_from_xml(child) == 'field' and belongs_to(nxdl_elem, child, name):
            return child
        if get_local_name_from_xml(child) == 'attribute' and belongs_to(nxdl_elem, child, name):
            return child
        if get_local_name_from_xml(child) == 'doc' and name == 'doc':
            return child
        if get_local_name_from_xml(child) == 'enumeration' and name == 'enumeration':
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
    bc_obj = ET.parse(f"{get_nexus_definitions_path()}{os.sep}"
                      f"base_classes{os.sep}{bc_name}.nxdl.xml").getroot()
    return get_own_nxdl_child(bc_obj, name)


def get_required_string(nxdl_elem):
    """Check for being required
REQUIRED, RECOMMENDED, OPTIONAL, NOT IN SCHEMA

"""
    if nxdl_elem is None:
        return "<<NOT IN SCHEMA>>"
    is_optional = 'optional' in nxdl_elem.attrib.keys() \
        and nxdl_elem.attrib['optional'] == "true"
    is_minoccurs = 'minOccurs' in nxdl_elem.attrib.keys() \
        and nxdl_elem.attrib['minOccurs'] == "0"
    # is_required = 'required' in nxdl_elem.attrib.keys() and nxdl_elem.attrib['required'] == "true"
    is_recommended = 'recommended' in nxdl_elem.attrib.keys() \
        and nxdl_elem.attrib['recommended'] == "true"

    if is_recommended:
        return "<<RECOMMENDED>>"
    if is_optional or is_minoccurs:
        return "<<OPTIONAL>>"
    return "<<REQUIRED>>"

    # default optionality
    # in BASE CLASSES: true
    # in APPLICATIONS: false

    # TODO: confirm with Sandor if we can get rid of these lines
    # if "base" in nxdl_elem.attrib and "base_classes" in nxdl_elem.base:
    #    return "<<OPTIONAL>>"


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
                return None
    ownpaxis = hdf_node.attrs.get('primary')
    own_axis = hdf_node.attrs.get('axis')
    assert own_axis is int, 'axis is not int type!'
    # also convention v1
    if ownpaxis is int and ownpaxis == 1:
        LOGGER.info("Dataset referenced (v2) as NXdata AXIS #%d", own_axis - 1)
        return None
    if not (ownpaxis is int and ownpaxis == 1):
        LOGGER.info(
            "Dataset referenced (v2) as NXdata (primary/alternative) AXIS #%d", own_axis - 1)
        return None
    return None


def chk_nxdataaxis(hdf_node, name, loger):
    """NEXUS Data Plotting Standard v3: new version from 2014

"""
    # check if it is a field in an NXdata node
    if not isinstance(hdf_node, h5py.Dataset):
        return None
    parent = hdf_node.parent
    if not parent or (parent and not parent.attrs.get('NX_class') == "NXdata"):
        return None
    # chk for Signal
    signal = parent.attrs.get('signal')
    if signal and name == signal:
        loger.info("Dataset referenced as NXdata SIGNAL")
        return None
    # check for default Axes
    axes = parent.attrs.get('axes')
    if axes is str:
        if name == axes:
            loger.info("Dataset referenced as NXdata AXIS")
            return None
    elif axes is not None:
        for i, j in enumerate(axes):
            if name == j:
                indices = parent.attrs.get(j + '_indices')
                if indices is int:
                    loger.info("Dataset referenced as NXdata AXIS #%d" % indices)
                else:
                    loger.info("Dataset referenced as NXdata AXIS #%d" % i)
                return None
    # check for alternative Axes
    indices = parent.attrs.get(name + '_indices')
    if indices is int:
        loger.info("Dataset referenced as NXdata alternative AXIS #%d" % indices)
    # check for older conventions
    return chk_nxdataaxis_v2(hdf_node, name)

def get_nxdl_doc(hdf_node, loger, doc, attr=False):
    """Get nxdl documentation for an HDF5 node (or its attribute)
"""
    nxdl_file_path = (f"{get_nexus_definitions_path()}{os.sep}applications"
                      f"{os.sep}{get_nxdl_entry(hdf_node)}.nxdl.xml")
    elem = ET.parse(nxdl_file_path).getroot()
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
                # try to find if units is defined inside the field in the NXDL element
                unit = elem.attrib[attr]
                if doc:
                    loger.info("@" + attr + ' [' + unit + ']')
                elem = None
                nxdl_path.append(attr)
            except KeyError:
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

    if (elem is None and req_str is None):
        if doc:
            loger.info("")
        return ('None', None, None)
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
            for item in sdoc:
                if get_local_name_from_xml(item) == 'item':
                    if doc:
                        loger.info("-> " + item.attrib['value'])
        # check for NXdata references (axes/signal)
        chk_nxdataaxis(hdf_node, path.split('/')[-1], loger)
        # check for doc
        sdoc = get_nxdl_child(elem, 'doc')
        if doc:
            loger.info(get_local_name_from_xml(sdoc) if sdoc is not None else "")
    return (req_str, get_nxdl_entry(hdf_node), nxdl_path)


def get_doc(node, ntype, nxhtml, nxpath):
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
    doc = ""
    doc_field = node.find("doc")
    if doc_field is not None:
        doc = doc_field.text

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
    """Print documentation
"""
    anchor, doc = get_doc(node, ntype, nxhtml, nxpath)
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


def get_namespace(element) -> str:
    """Extracts the namespace for elements in the NXDL"""
    return element.tag[element.tag.index("{"):element.tag.rindex("}") + 1]


def get_enums(node):
    """
    makes list of enumerations, if node contains any.
    Returns comma separated STRING of enumeration values, if there are enum tag,
    otherwise empty string.
    """
    # collect item values from enumeration tag, if any
    namespace = get_namespace(node)
    enums = []
    for enumeration in node.findall(f"{namespace}enumeration"):
        for item in enumeration.findall(f"{namespace}item"):
            enums.append(item.attrib["value"])
        enums = ','.join(enums)
        if enums != "":
            return (True, '[' + enums + ']')
    # if there is no enumeration tag, returns empty string
    return (False, "")


def get_node_at_nxdl_path(nxdl_path: str = None,
                          nx_name: str = None,
                          elem: ET.Element = None):
    """Returns an ET.Element for the given path.

This function either takes the name for the Nexus Application Definition
we are looking for or the root elem from a previously loaded NXDL file
and finds the corresponding XML element with the needed attributes.

"""
    if elem is None:
        nxdl_file_path = (f"{get_nexus_definitions_path()}{os.sep}"
                          f"applications{os.sep}{nx_name}.nxdl.xml")
        elem = ET.parse(nxdl_file_path).getroot()
    for group in nxdl_path.split('/')[1:]:
        elem = get_nxdl_child(elem, group)
    if elem is None:
        raise Exception(f"Attributes were not found for {nxdl_path}. "
                        "Please check this entry in the template dictionary.")
    return elem


def process_node(hdf_node, hdf_path, parser, logger, doc=True):
    """
            #processes an hdf5 node
            #- it logs the node found and also checks for its attributes
            #- retrieves the corresponding nxdl documentation
            #TODO:
            # - follow variants
            # - NOMAD parser: store in NOMAD
            """
    if isinstance(hdf_node, h5py.Dataset):
        logger.info('===== FIELD (/%s): %s' % (hdf_path, hdf_node))
        val = str(hdf_node[()]).split('\n') if len(hdf_node.shape) <= 1 else str(
            hdf_node[0]).split('\n')
        logger.info('value: %s %s' % (val[0], "..." if len(val) > 1 else ''))
    else:
        logger.info('===== GROUP (/%s [%s::%s]): %s' %
                    (hdf_path, get_nxdl_entry(hdf_node),
                     get_nx_class_path(hdf_node), hdf_node))
    (req_str, nxdef, nxdl_path) = get_nxdl_doc(hdf_node, logger, doc)
    if parser is not None and isinstance(hdf_node, h5py.Dataset):
        parser(hdf_path, hdf_node, nxdef, nxdl_path)
    for key, value in hdf_node.attrs.items():
        logger.info('===== ATTRS (/%s@%s)' % (hdf_path, key))
        val = str(value).split('\n')
        logger.info('value: %s %s' % (val[0], "..." if len(val) > 1 else ''))
        (req_str, nxdef, nxdl_path) = get_nxdl_doc(hdf_node, logger, doc, attr=key)
        if parser is not None and 'NOT IN SCHEMA' not in req_str and 'None' not in req_str:
            parser(hdf_path, hdf_node, nxdef, nxdl_path)


def get_default_plotable(root, logger):
    """Get default plotable

"""
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
        except KeyError:
            nxentry = None
    if not nxentry:
        nxentry = entry_helper(root)
    if not nxentry:
        logger.info('No NXentry has been found')  # TODO the code always falls here, solve it
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
        except KeyError:
            nxdata = None
    if not nxdata:
        nxdata = nxdata_helper(nxentry)
    if not nxdata:
        logger.info('No NXdata group has been found')
        return
    logger.info('')
    logger.info('NXdata group has been identified: ' + nxdata.name)
    process_node(nxdata, nxdata.name, None, logger, False)
    # signal
    signal = None
    signal_dataset_name = nxdata.attrs.get("signal")
    try:
        signal = nxdata[signal_dataset_name]
    except KeyError:
        signal = None
    if not signal:
        signal = signal_helper(nxdata)
    if not signal:
        logger.info('No Signal has been found')
        return
    logger.info('')
    logger.info('Signal has been identified: ' + signal.name)
    process_node(signal, signal.name, None, logger, False)
    dim = len(signal.shape)
    # axes
    axes = []
    axis_helper(dim, nxdata, signal, axes, logger)


def entry_helper(root):
    """Check entry related data

"""
    nxentries = []
    for key in root.keys():
        if (isinstance(root[key], h5py.Group) and root[key].attrs.get('NX_class\
        ') and root[key].attrs['NX_class'] == "NXentry"):
            nxentries.append(root[key])
    # v3: as there was no selection given, only 1 nxentry shall exists
    # v2: take any
    if len(nxentries) >= 1:
        return nxentries[0]
    return None


def nxdata_helper(nxentry):
    """Check if nxentry hdf5 object has a NX_class and, if it contains NXdata,
return its value

"""
    lnxdata = []
    for key in nxentry.keys():
        if isinstance(nxentry[key], h5py.Group) and nxentry[key].attrs.get('NX_class\
        ') and nxentry[key].attrs['NX_class'] == "NXdata":
            lnxdata.append(nxentry[key])
    # v3: as there was no selection given, only 1 nxdata shall exists
    # v2: take any
    if len(lnxdata) >= 1:
        return lnxdata[0]
    return None


def signal_helper(nxdata):
    """Check signal related data

"""
    signals = []
    for key in nxdata.keys():
        if isinstance(nxdata[key], h5py.Dataset):
            signals.append(nxdata[key])
    # v3: as there was no selection given, only 1 data field shall exists
    if len(signals) == 1:
        return signals[0]
    # v2: select the one with an attribute signal="1" attribute
    if len(signals) > 1:
        for sig in signals:
            if sig.attrs.get("signal") and sig.attrs.get("signal\
            ") is str and sig.attrs.get("signal") == "1":
                return sig
    return None

def find_attrib_axis_actual_dim_num(nxdata, a_item, ax_list):
    """Finds axis that have defined dimensions"""
    # find those with attribute axis= actual dimension number
    lax = []
    for key in nxdata.keys():
        if isinstance(nxdata[key], h5py.Dataset):
            try:
                if nxdata[key].attrs['axis'] == a_item + 1:
                    lax.append(nxdata[key])
            except KeyError:
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

def get_single_or_multiple_axes(nxdata, ax_datasets, a_item, ax_list):
    """Gets either single or multiple axes from the NXDL"""
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
    except KeyError:
        pass

def axis_helper(dim, nxdata, signal, axes, logger):
    """Check axis related data

"""
    for a_item in range(dim):
        ax_list = []
        # primary axes listed in attribute axes
        ax_datasets = nxdata.attrs.get("axes")
        get_single_or_multiple_axes(nxdata, ax_datasets, a_item, ax_list)
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
            except KeyError:
                pass
        # check for axis/primary specifications
        if not ax_list:
            find_attrib_axis_actual_dim_num(nxdata, a_item, ax_list)
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

    def visit_node(self, hdf_name, hdf_node):
        """Function called by h5py that iterates on each node of hdf5file.

        It allows h5py visititems function to visit nodes.

        """
        hdf_path = '/' + hdf_name
        process_node(hdf_node, hdf_path, self.parser, self.logger)

    def process_nexus_master_file(self, parser):
        """
        Process a nexus master file by processing all its nodes and their attributes

        """
        self.parser = parser
        self.in_file = h5py.File(self.input_file_name, 'r')
        self.in_file.visititems(self.visit_node)
        get_default_plotable(self.in_file, self.logger)
        self.in_file.close()


if __name__ == '__main__':
    LOGGING_FORMAT = "%(levelname)s: %(message)s"
    STDOUT_HANDLER = logging.StreamHandler(sys.stdout)
    STDOUT_HANDLER.setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT, handlers=[STDOUT_HANDLER])
    LOGGER = logging.getLogger()
    NEXUS_HELPER = HandleNexus(LOGGER, sys.argv[1:])
    NEXUS_HELPER.process_nexus_master_file(None)
