"""Read files from different format and print it in a standard Nexus format
"""
# Nexus definitions in github: https://github.com/nexusformat/definitions
# to be cloned under os.environ['NEXUS_DEF_PATH']

import os
import xml.etree.ElementTree as ET
# import re
import sys
import logging
import textwrap
import h5py


class NxdlAttributeError(Exception):
    """An exception for throwing an error when an Nxdl attribute is not found."""


# check for NEXUS definitions
def get_nexus_definitions_path():
    """Check NEXUS_DEF_PATH variable.
If it is empty, this function is filling it"""
    try:
        # either given by sys env
        return os.environ['NEXUS_DEF_PATH']
    except KeyError:
        # or it should be available locally under the dir 'definitions'
        local_dir = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(local_dir, f"..{os.sep}definitions")


def get_nx_class_path(hdf_node):
    """Get the full path of an HDF5 node using nexus classes
in case of a field, end with the field name"""
    if hdf_node.name == '/':
        return ''
    if isinstance(hdf_node, h5py.Group):
        return get_nx_class_path(hdf_node.parent) + '/' + \
            (hdf_node.attrs['NX_class'] if 'NX_class' in hdf_node.attrs.keys() else
             hdf_node.name.split('/')[-1])
    if isinstance(hdf_node, h5py.Dataset):
        return get_nx_class_path(
            hdf_node.parent) + '/' + hdf_node.name.split('/')[-1]
    return ''


def get_nxdl_entry(hdf_node):
    """Get the nxdl application definition for an HDF5 node"""
    entry = hdf_node
    while isinstance(entry, h5py.Dataset) or \
            'NX_class' not in entry.attrs.keys() or \
            entry.attrs['NX_class'] != 'NXentry':
        entry = entry.parent
        if entry.name == '/':
            return 'NO NXentry found'
    try:
        nxdef = entry['definition'][()]
        return nxdef.decode()
    except KeyError:
        # 'NO Definition referenced'
        return "NXentry"


def get_nx_class(nxdl_elem):
    """Get the nexus class for a NXDL node"""
    if 'category' in nxdl_elem.attrib.keys():
        return None
    try:
        return nxdl_elem.attrib['type']
    except KeyError:
        return 'NX_CHAR'


def get_nx_namefit(hdf_name, name):
    """Checks if an HDF5 node name corresponds to a child of the NXDL element
uppercase letters in front can be replaced by arbitraty name, but
uppercase to lowercase match is preferred,
so such match is counted as a measure of the fit"""
    # count leading capitals
    counting = 0
    while counting < len(name) and name[counting].upper() == name[counting]:
        counting += 1
    # if potential fit
    if counting == len(name) or hdf_name.endswith(name[counting:]):
        # count the matching chars
        fit = 0
        for i in range(min(counting, len(hdf_name))):
            if hdf_name[i].upper() == name[i]:
                fit += 1
            else:
                break
        # accept only full fits as better fits
        if fit == min(counting, len(hdf_name)):
            return fit
        return 0
    # no fit
    return -1


def get_nx_classes():
    """Read base classes from the Nexus definition/base_classes folder"""
    base_classes_list_files = os.listdir(os.path.join(get_nexus_definitions_path(), 'base_classes'))
    nx_clss = sorted([str(s)[:-9] for s in base_classes_list_files])
    return nx_clss


def get_nx_units():
    """Read unit kinds from the Nexus definition/nxdlTypes.xsd file"""
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
    """Read attribute types from the Nexus definition/nxdlTypes.xsd file"""
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
    the string is coverted to UPPER case.'''
    if 'name' in node.attrib.keys():
        name = node.attrib['name']
    else:
        name = node.attrib['type']
        if name.startswith('NX'):
            name = name[2:].upper()
    return name


def belongs_to(nxdl_elem, child, name, class_type=None, hdf_name=None):
    """Checks if an HDF5 node name corresponds to a child of the NXDL element
uppercase letters in front can be replaced by arbitraty name, but
uppercase to lowercase match is preferred"""
    if class_type and get_nx_class(child) != class_type:
        return False
    act_htmlname = get_node_name(child)
    # nx_class_regex = re.compile(r"NX[a-z_]+")
    # chk_name = name[2:].upper() if nx_class_regex.search(name) and \
    #    'name' not in child.attrib else name
    chk_name = hdf_name or name
    if act_htmlname == chk_name:
        return True
    # search for name fits is only allowed for hdf_nodes
    if not hdf_name:
        return False
    # check if nameType allows different name
    try:
        name_any = bool(child.attrib['nameType'] == "any")
        # if child.attrib['nameType'] == "any":
        #    name_any = True
        # else:
        #    name_any = False
    except KeyError:
        name_any = False
    # or starts with capital and no reserved words used
    # if (name_any or act_htmlname[0].lower() != act_htmlname[0]) and \
    if (name_any or 'A' <= act_htmlname[0] <= 'Z') and \
            name != 'doc' and name != 'enumeration':
        # check if name fits
        fit = get_nx_namefit(chk_name, act_htmlname)
        if fit < 0:
            return False
        for child2 in nxdl_elem:
            if get_local_name_from_xml(child) != \
                    get_local_name_from_xml(child2) or get_node_name(child2) == act_htmlname:
                continue
            # check if the name of another sibling fits better
            fit2 = get_nx_namefit(chk_name, get_node_name(child2))
            if fit2 > fit:
                return False
        # accept this fit
        return True
    return False


def get_local_name_from_xml(element):
    """Helper function to extract the element tag without the namespace."""
    return element.tag[element.tag.rindex("}") + 1:]


def get_own_nxdl_child(nxdl_elem, name, class_type=None, hdf_name=None, nexus_type=None):
    """Checks if an NXDL child node fits to the specific name (either nxdl or hdf)
        name - nxdl name
        class_type - nxdl type or hdf classname (for groups, it is obligatory)
        hdf_name - hdf name"""
    for child in nxdl_elem:
        if 'name' in child.attrib and child.attrib['name'] == name:
            if nxdl_elem.get('nxdlbase'):
                child.set('nxdlbase', nxdl_elem.get('nxdlbase'))
                child.set('nxdlpath', nxdl_elem.get('nxdlpath') + '/' + get_node_name(child))
            return child

    for child in nxdl_elem:
        if "name" in child.attrib and child.attrib["name"] == name:
            child.set('nxdlbase', nxdl_elem.get('nxdlbase'))
            return child

    for child in nxdl_elem:
        if get_local_name_from_xml(child) == 'doc' and name == 'doc':
            if nxdl_elem.get('nxdlbase'):
                child.set('nxdlbase', nxdl_elem.get('nxdlbase'))
                child.set('nxdlpath', nxdl_elem.get('nxdlpath') + '/doc')
            return child
        if get_local_name_from_xml(child) == 'enumeration' and name == 'enumeration':
            if nxdl_elem.get('nxdlbase'):
                child.set('nxdlbase', nxdl_elem.get('nxdlbase'))
                child.set('nxdlpath', nxdl_elem.get('nxdlpath') + '/enumeration')
            return child
        if nexus_type and get_local_name_from_xml(child) != nexus_type:
            continue
        if get_local_name_from_xml(child) == 'group':
            if (class_type is None or (class_type and get_nx_class(child) == class_type)) and \
                    belongs_to(nxdl_elem, child, name, class_type, hdf_name):
                if nxdl_elem.get('nxdlbase'):
                    child.set('nxdlbase', nxdl_elem.get('nxdlbase'))
                    child.set('nxdlpath', nxdl_elem.get('nxdlpath') + '/' + get_node_name(child))
                return child
        if get_local_name_from_xml(child) == 'field' and \
                belongs_to(nxdl_elem, child, name, None, hdf_name):
            if nxdl_elem.get('nxdlbase'):
                child.set('nxdlbase', nxdl_elem.get('nxdlbase'))
                child.set('nxdlpath', nxdl_elem.get('nxdlpath') + '/' + get_node_name(child))
            return child
        if get_local_name_from_xml(child) == 'attribute' and \
                belongs_to(nxdl_elem, child, name, None, hdf_name):
            if nxdl_elem.get('nxdlbase'):
                child.set('nxdlbase', nxdl_elem.get('nxdlbase'))
                child.set('nxdlpath', nxdl_elem.get('nxdlpath') + '/' + get_node_name(child))
            return child
    return None


def get_nxdl_child(nxdl_elem, name, class_type=None, hdf_name=None, nexus_type=None, go_base=True):
    """Get the NXDL child node corresponding to a specific name
(e.g. of an HDF5 node,or of a documentation)
note that if child is not found in application definition,
it also checks for the base classes"""
    # search for posiible fits for hdf_nodes : skipped
    # only exact hits are returned when searching an nxdl child
    own_child = get_own_nxdl_child(nxdl_elem, name, class_type, hdf_name, nexus_type)
    # own_child = get_own_nxdl_child(nxdl_elem, name, class_type)
    if own_child is not None:
        return own_child
    if not go_base:
        return None
    # check in the base class
    bc_name = get_nx_class(nxdl_elem)
    # filter primitive types
    if bc_name[2] == '_':
        return None

    # Checking if it is actually the root element. Then we send it to NXroot.nxdl.xml
    if bc_name == "group":
        bc_name = "NXroot"
    bc_filename = f"{get_nexus_definitions_path()}{os.sep}" \
        f"base_classes{os.sep}{bc_name}.nxdl.xml"
    bc_obj = ET.parse(bc_filename).getroot()
    bc_obj.set('nxdlbase', bc_filename)
    bc_obj.set('nxdlpath', '')
    return get_own_nxdl_child(bc_obj, name, class_type, hdf_name, nexus_type)


def get_required_string(nxdl_elem):
    """Check for being required
REQUIRED, RECOMMENDED, OPTIONAL, NOT IN SCHEMA"""
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
    # default optionality
    # in BASE CLASSES: true
    # in APPLICATIONS: false
    try:
        if "base_classes" in nxdl_elem.get('nxdlbase'):
            return "<<OPTIONAL>>"
    except TypeError:
        return "<<REQUIRED>>"
    return "<<REQUIRED>>"


def chk_nxdataaxis_v2(hdf_node, name):
    """Check if dataset is an axis"""
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
    if own_axis is int:
        # also convention v1
        if ownpaxis is int and ownpaxis == 1:
            LOGGER.info("Dataset referenced (v2) as NXdata AXIS #%d", own_axis - 1)
        else:
            LOGGER.info(
                "Dataset referenced (v2) as NXdata (primary/alternative) AXIS #%d", own_axis - 1)
    return None


def chk_nxdataaxis(hdf_node, name, loger):
    """NEXUS Data Plotting Standard v3: new version from 2014"""
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
    """Get nxdl documentation for an HDF5 node (or its attribute)"""
    # new way: retrieve multiple inherited base classes
    (class_path, nxdl_path, elist) = \
        get_inherited_nodes(None, nx_name=get_nxdl_entry(hdf_node), hdf_node=hdf_node)
    elem = elist[0] if class_path and elist else None
    if doc:
        loger.info("classpath: " + str(class_path))
        loger.info("NOT IN SCHEMA" if elem is None else
                   "classes:\n" + "\n".join
                   (str(e.get('nxdlbase').split('/')[-1] + ":" + e.get('nxdlpath')) for e in elist))
    # old solution with a single elem instead of using elist
    path = get_nx_class_path(hdf_node)
    req_str = None
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
                elem = get_nxdl_child(elem, attr, nexus_type='attribute')
                if elem is not None:
                    if doc:
                        loger.info("@" + attr + ' - [' + get_nx_class(elem) + ']')
                    nxdl_path.append(elem)
                else:
                    # if no units category were defined in NXDL:
                    if doc:
                        loger.info("@" + attr + " - REQUIRED, but undefined unit category")
                    nxdl_path.append(attr)
        # units for attributes can be given as ATTRIBUTENAME_units
        elif attr.endswith('_units'):
            # check for ATTRIBUTENAME_units in NXDL (normal)
            elem2 = get_nxdl_child(elem, attr, nexus_type='attribute')
            if elem2 is not None:
                elem = elem2
                if doc:
                    loger.info("@" + attr + ' - [' + get_nx_class(elem) + ']')
                nxdl_path.append(elem)
            else:
                # if not defined, check for ATTRIBUTENAME to see if the ATTRIBUTE
                # is in the SCHEMA, but no units category were defined
                elem2 = get_nxdl_child(elem, attr[:-6], nexus_type='attribute')
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
        # default is allowed for groups
        elif attr == 'default' and not isinstance(hdf_node, h5py.Dataset):
            req_str = "<<RECOMMENDED>>"
            # try to find if default is defined as a child of the NXDL element
            elem = get_nxdl_child(elem, attr, nexus_type='attribute')
            if elem is not None:
                if doc:
                    loger.info("@" + attr + ' - [' + get_nx_class(elem) + ']')
                nxdl_path.append(elem)
            else:
                # if no default category were defined in NXDL:
                if doc:
                    loger.info("@" + attr + " - [NX_CHAR]")
                nxdl_path.append(attr)
        # other attributes
        else:
            elem = get_nxdl_child(elem, attr, nexus_type='attribute')
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
        for base_elem in elist if not attr else [elem]:
            sdoc = get_nxdl_child(base_elem, 'enumeration', go_base=False)
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
        for base_elem in elist if not attr else [elem]:
            sdoc = get_nxdl_child(base_elem, 'doc', go_base=False)
            if doc:
                loger.info(sdoc.text if sdoc is not None else "")
    return (req_str, get_nxdl_entry(hdf_node), nxdl_path)


def get_doc(node, ntype, nxhtml, nxpath):
    """Get documentation"""
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
    """Print documentation"""
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
    otherwise empty string."""
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


def add_base_classes(elist, nx_name=None, elem: ET.Element = None):
    """ add the base classes corresponsing to the last eleme in elist to the list
        Note that if elist is empty, a nxdl file with the name of nx_name or
                                     a rather room elem is used if privded"""
    if elist and nx_name is None:
        nx_name = get_nx_class(elist[-1])
    if elist and nx_name and f"{nx_name}.nxdl.xml" in (e.get('nxdlbase') for e in elist):
        return
    if elem is None:
        if not nx_name:
            return
        nxdl_file_path = f"{nx_name}.nxdl.xml"
        for root, dirs, files in os.walk(get_nexus_definitions_path()):  # pylint: disable=unused-variable
            if nxdl_file_path in files:
                nxdl_file_path = os.path.join(root, nxdl_file_path)
                break
        elem = ET.parse(nxdl_file_path).getroot()
        elem.set('nxdlbase', nxdl_file_path)
    else:
        elem.set('nxdlbase', '')
    elem.set('nxdlpath', '')
    elist.append(elem)
    # add inherited base classes
    if 'extends' in elem.attrib and elem.attrib['extends'] != 'NXobject':
        add_base_classes(elist, elem.attrib['extends'])
    else:
        add_base_classes(elist)


def get_direct_child(nxdl_elem, html_name):
    """ returns the child of nxdl_elem which has a name
        corresponding to the the html documentation name html_name"""
    for child in nxdl_elem:
        if get_local_name_from_xml(child) in ('group', 'field', 'attribute') and \
                html_name == get_node_name(child):
            if nxdl_elem.get('nxdlbase'):
                child.set('nxdlbase', nxdl_elem.get('nxdlbase'))
                child.set('nxdlpath', nxdl_elem.get('nxdlpath') + '/' + get_node_name(child))
            return child


def get_best_child(nxdl_elem, hdf_name, hdf_class_name, nexus_type):
    """ returns the child of nxdl_elem which has a name
        corresponding to the the html documentation name html_name"""
    bestfit = -1
    bestchild = None
    for child in nxdl_elem:
        fit = -2
        if get_local_name_from_xml(child) == nexus_type and \
                (nexus_type != 'group' or get_nx_class(child) == hdf_class_name):
            fit = get_nx_namefit(hdf_name, get_node_name(child))
        if fit > bestfit:
            bestfit = fit
            bestchild = child
    return (bestchild, bestfit)


def get_inherited_nodes(nxdl_path: str = None,
                        nx_name: str = None, elem: ET.Element = None,
                        hdf_node=None, attr=False):
    """Returns a list of ET.Element for the given path."""
    # let us start with the given definition file
    elist = []  # type: ignore[var-annotated]
    add_base_classes(elist, nx_name, elem)
    nxdl_elem_path = [elist[0]]

    class_path = []  # type: ignore[var-annotated]
    if hdf_node is not None:
        hdf_path = hdf_node.name.split('/')[1:]
        hdf_class_path = get_nx_class_path(hdf_node).split('/')[1:]
        if attr:
            hdf_path.append(attr)
            hdf_class_path.append(attr)
        path = hdf_path
    else:
        html_path = nxdl_path.split('/')[1:]
        path = html_path
    for pind in range(len(path)):
        if hdf_node is not None:
            hdf_name = hdf_path[pind]
            hdf_class_name = hdf_class_path[pind]
            if pind < len(hdf_path) - (2 if attr else 1):
                act_nexus_type = 'group'
            elif pind == len(hdf_path) - 1 and attr:
                act_nexus_type = 'attribute'
            else:
                act_nexus_type = 'field' if isinstance(hdf_node, h5py.Dataset) else 'group'
            # find the best fitting name in all children
            bestfit = -1
            html_name = None
            for ind in range(len(elist) - 1, -1, -1):
                newelem, fit = get_best_child(elist[ind],
                                              hdf_name,
                                              hdf_class_name,
                                              act_nexus_type)
                if fit >= bestfit and newelem is not None:
                    html_name = get_node_name(newelem)
            # return if NOT IN SCHEMA
            if html_name is None:
                return (class_path, nxdl_elem_path, None)
        else:
            html_name = html_path[pind]

        # from low priority inheritance classes to higher
        for ind in range(len(elist) - 1, -1, -1):
            elist[ind] = get_direct_child(elist[ind], html_name)
            if elist[ind] is None:
                del elist[ind]
                continue
            # override: remove low priority inheritance classes if class_type is overriden
            if len(elist) > ind + 1 and get_nx_class(elist[ind]) != get_nx_class(elist[ind + 1]):
                del elist[ind + 1:]
            # add new base class(es) if new element brings such (and not a primitive type)
            if len(elist) == ind + 1 and get_nx_class(elist[ind])[0:3] != 'NX_':
                add_base_classes(elist)
        if elist:
            class_path.append(get_nx_class(elist[0]))
            nxdl_elem_path.append(elist[0])
    return (class_path, nxdl_elem_path, elist)


def get_node_at_nxdl_path(nxdl_path: str = None,
                          nx_name: str = None, elem: ET.Element = None,
                          exc: bool = True):
    """Returns an ET.Element for the given path.
    This function either takes the name for the Nexus Application Definition
    we are looking for or the root elem from a previously loaded NXDL file
    and finds the corresponding XML element with the needed attributes."""
    (class_path, nxdl_path, elist) = get_inherited_nodes(nxdl_path, nx_name, elem)
    if class_path and nxdl_path and elist:
        elem = elist[0]
    else:
        elem = None
        if exc:
            raise NxdlAttributeError(f"Attributes were not found for {nxdl_path}. "
                                     "Please check this entry in the template dictionary.")
    return elem


def process_node(hdf_node, hdf_path, parser, logger, doc=True):
    """
            #processes an hdf5 node
            #- it logs the node found and also checks for its attributes
            #- retrieves the corresponding nxdl documentation
            #TODO:
            # - follow variants
            # - NOMAD parser: store in NOMAD"""
    hdf_info = {'hdf_path': hdf_path, 'hdf_node': hdf_node}
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
        parser(hdf_info, nxdef, nxdl_path, val)
    for key, value in hdf_node.attrs.items():
        logger.info('===== ATTRS (/%s@%s)' % (hdf_path, key))
        val = str(value).split('\n')
        logger.info('value: %s %s' % (val[0], "..." if len(val) > 1 else ''))
        (req_str, nxdef, nxdl_path) = \
            get_nxdl_doc(hdf_node, logger, doc, attr=key)
        if parser is not None and 'NOT IN SCHEMA' not in req_str and 'None' not in req_str:
            parser(hdf_info, nxdef, nxdl_path, val)


def get_default_plotable(root, logger):
    """Get default plotable"""
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
        logger.info('No NXentry has been found')
        return
    logger.info('')
    logger.info('NXentry has been identified: ' + nxentry.name)
    # process_node(nxentry, None, False)
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
    except (TypeError, KeyError):
        signal = None
    if not signal:
        signal = signal_helper(nxdata)
    if not signal:
        logger.info('No Signal has been found')
        return
    logger.info('')
    logger.info('Signal has been identified: ' + signal.name)
    process_node(signal, signal.name, None, logger, False)
    # check auxiliary_signals
    aux = nxdata.attrs.get('auxiliary_signals')
    if aux is not None:
        if isinstance(aux, str):
            aux = [aux]
        for asig in aux:
            logger.info('Further auxiliary signal has been identified: %s' % (asig))
    dim = len(signal.shape)
    # axes
    axes = []
    axis_helper(dim, nxdata, signal, axes, logger)


def entry_helper(root):
    """Check entry related data"""
    nxentries = []
    for key in root.keys():
        if isinstance(root[key], h5py.Group) and root[key].attrs.get('NX_class') and \
                root[key].attrs['NX_class'] == "NXentry":
            nxentries.append(root[key])
    # v3: as there was no selection given, only 1 nxentry shall exists
    # v2: take any
    if len(nxentries) >= 1:
        return nxentries[0]
    return None


def nxdata_helper(nxentry):
    """Check if nxentry hdf5 object has a NX_class and, if it contains NXdata,
return its value"""
    lnxdata = []
    for key in nxentry.keys():
        if isinstance(nxentry[key], h5py.Group) and nxentry[key].attrs.get('NX_class') and \
                nxentry[key].attrs['NX_class'] == "NXdata":
            lnxdata.append(nxentry[key])
    # v3: as there was no selection given, only 1 nxdata shall exists
    # v2: take any
    if len(lnxdata) >= 1:
        return lnxdata[0]
    return None


def signal_helper(nxdata):
    """Check signal related data"""
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
            if sig.attrs.get("signal") and sig.attrs.get("signal") is str and \
                    sig.attrs.get("signal") == "1":
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
        if isinstance(ax_datasets, str):
            # explicite definition of dimension number
            ind = nxdata.attrs.get(ax_datasets + '_indices')
            if ind and ind is int:
                if ind == a_item:
                    ax_list.append(nxdata[ax_datasets])
            # positional determination of the dimension number
            elif a_item == 0:
                ax_list.append(nxdata[ax_datasets])
        # multiple axes are listed
        else:
            # explicite definition of dimension number
            for aax in ax_datasets:
                ind = nxdata.attrs.get(aax + '_indices')
                if ind and isinstance(ind, int):
                    if ind == a_item:
                        ax_list.append(nxdata[aax])
            # positional determination of the dimension number
            if not ax_list:
                ax_list.append(nxdata[ax_datasets[a_item]])
    except KeyError:
        pass
    return ax_list


def axis_helper(dim, nxdata, signal, axes, logger):
    """Check axis related data"""
    for a_item in range(dim):
        ax_list = []
        # primary axes listed in attribute axes
        ax_datasets = nxdata.attrs.get("axes")
        ax_list = get_single_or_multiple_axes(nxdata, ax_datasets, a_item, ax_list)
        # check for corresponding AXISNAME_indices
        for attr in nxdata.attrs.keys():
            if attr.endswith('_indices') and nxdata.attrs[attr] == a_item and \
                    nxdata[attr.split('_indices')[0]] not in ax_list:
                ax_list.append(nxdata[attr.split('_indices')[0]])
        # v2
        # check for ':' separated axes defined in Signal
        if not ax_list:
            try:
                ax_datasets = signal.attrs.get("axes").split(':')
                ax_list.append(nxdata[ax_datasets[a_item]])
            except (KeyError, AttributeError):
                pass
        # check for axis/primary specifications
        if not ax_list:
            find_attrib_axis_actual_dim_num(nxdata, a_item, ax_list)
        axes.append(ax_list)
        logger.info('')
        logger.info('For Axis #%d, %d axes have been identified: %s' %
                    (a_item, len(ax_list), str(ax_list)))


class HandleNexus:
    """documentation"""
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
