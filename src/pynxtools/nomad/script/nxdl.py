from os import walk
import xml.dom.minidom
import xml.etree.ElementTree as ET
import os
from pynxtools.definitions.dev_tools.utils import nxdl_utils as nexus



local_dir = os.path.abspath(os.path.dirname(__file__))
nexus_def_path = os.path.join(local_dir, f"..{os.sep}..{os.sep}definitions")
os.environ['NEXUS_DEF_PATH']=nexus_def_path
nxdl_folders = ["base_classes", "applications"]
nxdl_folders_full = ["contributed_definitions", "base_classes", "applications"]

namespace = {"nxdl": "http://definition.nexusformat.org/nxdl/3.1"}

def get_all_tags(iterator, xml_tag):
    path = []
    skip = False
    for event, element in iterator:
        if element.tag == "{http://definition.nexusformat.org/nxdl/3.1}choice":
            skip = True if event == "start" else False
            continue
        if skip:
            continue
        if element.get("name") or (element.tag == "{http://definition.nexusformat.org/nxdl/3.1}group" and element.get("type")):
            if event == "start":
                name = element.get("name") or element.get("type").upper()[2:]
                path.append(name)
                if element.tag == "{http://definition.nexusformat.org/nxdl/3.1}"+xml_tag:
                    yield '/'.join(path), element
            else:
                if len(path)>0:
                    path.pop()

def safe_get_xml_doc(element):
    docEl = element.find("nxdl:doc", namespace)
    if docEl is None or docEl.text is None:
        return ""
    return docEl.text

def load_data_types():
    types_dom = xml.dom.minidom.parse(nexus_def_path + "/nxdlTypes.xsd")

    typesDict = {}
    for nxtype in types_dom.getElementsByTagName('xs:simpleType'):
        name = nxtype.getAttribute('name')
        if name == "primitiveType":
            union_el = nxtype.getElementsByTagName('xs:union')
            types = union_el[0].getAttribute('memberTypes')
            types = types.replace(" ", "").split("nxdl:")[1:]
    
    for type in types:
        typesDict[type] = {}

    for nxtype in types_dom.getElementsByTagName('xs:simpleType'):
        name = nxtype.getAttribute('name')
        if name in types:
            doc = nxtype.getElementsByTagName("xs:documentation")[0]
            typesDict[name]["doc"] = doc.firstChild.nodeValue

    return typesDict

def load_unit_categories():
    types_dom = xml.dom.minidom.parse(nexus_def_path + "/nxdlTypes.xsd")

    typesDict = {}
    for nxtype in types_dom.getElementsByTagName('xs:simpleType'):
        name = nxtype.getAttribute('name')
        if name == "anyUnitsAttr":
            union_el = nxtype.getElementsByTagName('xs:union')
            types = union_el[0].getAttribute('memberTypes')
            types = types.replace(" ", "").split("xs:")[0].split("nxdl:")[1:]
    
    for type in types:
        typesDict[type] = {}

    for nxtype in types_dom.getElementsByTagName('xs:simpleType'):
        name = nxtype.getAttribute('name')
        if name in types:
            doc = nxtype.getElementsByTagName("xs:documentation")[0]
            typesDict[name]["doc"] = doc.firstChild.nodeValue
            examples = doc.getElementsByTagName("xs:element")
            typesDict[name]["examples"] = []
            for example in examples:
                typesDict[name]["examples"].append(example.firstChild.nodeValue)      
    return typesDict

def get_min_occurs_from_xml_node(element, isBase):
    if element.get("minOccurs"):
        return int(element.get("minOccurs"))
    elif element.get("optional") == "true" or element.get("recommended") == "true" or element.get("required") == "false":
        return 0
    elif element.get("optional") == "false" or element.get("recommended") == "false" or element.get("required") == "true":
        return 1
    elif isBase:
        return 0
    return 1

def get_max_occurs_from_xml_node(element):
    maxOccurs = element.get("maxOccurs")
    if maxOccurs and maxOccurs != "unbounded":
        return int(element.get("maxOccurs"))
    return None

def load_all_nxdls(full = True) -> dict:
    nxdl_info = {"base_classes":{}, "applications":{}, "field":{}, "attribute":{}, "group":{}}
    just_fnames = []
    files = []

    act_folders = nxdl_folders_full if full else nxdl_folders

    for folder in act_folders:
        files_in_folder = next(walk(nexus_def_path + "/" + folder), (None, None, []))[2]
        files_in_folder = list(filter(lambda filename: filename.endswith(".nxdl.xml"), files_in_folder))
        intersection = [value for value in just_fnames if value in files_in_folder]
        just_fnames.extend(files_in_folder)
        files.extend([nexus_def_path+"/"+folder+"/"+path for path in files_in_folder])
        if len(intersection)>0:
            for f in intersection:
                files.remove(nexus_def_path+"/"+folder+"/"+f)
    
    for file in files:
        root = ET.parse(file).getroot()
        
        class_dict_to_append = nxdl_info["base_classes"]
        if root.get("category") == "application":
            class_dict_to_append = nxdl_info["applications"]
        
        className = root.get("name")
        class_dict_to_append[className] = {"doc": root.find("nxdl:doc", namespace).text, "extends": root.get("extends"), "category": file.split("/")[-2]}

        # Take care of all fields here
        for xml_tag in list(nxdl_info.keys())[2:]:
            iterator = ET.iterparse(file, events=("start", "end"))
            for path, element in get_all_tags(iterator, xml_tag):
                nxdl_info[xml_tag][path] = {"comment": safe_get_xml_doc(element), "category": file.split("/")[-2], "type": element.get("type") or "NX_CHAR", "unit_category": element.get("units") or "NX_ANY",
                                            "minOccurs": get_min_occurs_from_xml_node(element, root.get("category") == "base"), "maxOccurs": get_max_occurs_from_xml_node(element)}
                enums = nexus.get_enums(element)
                if enums is not None:
                    enums = enums[0].strip("[").strip("]")
                    nxdl_info[xml_tag][path]["enums"] = enums.split(",")
                elist = nexus.get_inherited_nodes(nxdl_path=path[path.find("/"):], nx_name=path[:path.find("/")])[2]
                if len(elist)>1:
                    nxdl_info[xml_tag][path]["superclass_path"] = nexus.get_node_concept_path(elist[1]).replace(".nxdl.xml:","")
                nxdl_info[xml_tag][path]["deprecated"] = element.get("deprecated")

    return nxdl_info
