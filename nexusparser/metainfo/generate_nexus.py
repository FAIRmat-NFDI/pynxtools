#
#from nomad.metainfo.generate import generate_metainfo_code
from nomad.metainfo.metainfo import MEnum, MSection
from generate import generate_metainfo_code
from nomad.metainfo import Package
from nomad.metainfo import Section, Quantity, SubSection
#from nomad.datamodel.metainfo.nxobject import NXobject

# you define a quantity like this
q = Quantity(
    name='machine_name',
    type=str,
    shape=[],
    description='''
    ''')

# you define a section like this
m = Section(name='Equipment')

# you can add a quantity to a section like this
m.quantities.append(q)

# you can add a sub section to a section like this
r = Section(name='Experiment')
r.sub_sections.append(SubSection(sub_section=m, name='experiment', repeats=True))

# we then package all section definitions
p = Package(name='Package')
p.section_definitions.append(m)
p.section_definitions.append(r)

# we write the schema as file
#generate_metainfo_code(p, 'meta.py')




# TODO:
#  - dimension
#  - enumeration
#  - units
#  - minOccurs / maxOccurs

from lxml import etree, objectify
import os
from tools import read_nexus

def parse_node(m,node, ntype, level, nxhtml, nxpath):
    '''
        node   - xml node
        ntype  - node type (e.g. group, field, attribute)
        level  - hierachy depth (level 1 - definition)
        nxhtml - url extension to html documentation (e.g. 'applications/NXxas.html')
        nxpath - list of NX nodes in hierarchy
                 elements are in html documentation format. E.g. ['NXxas', 'ENTRY']
    '''
    nxpath_new=nxpath.copy()
    nxpath_new.append(read_nexus.get_node_name(node))
    indent='  ' *level
    print("%s%s: %s (%s) %s %s" % (indent,ntype,nxpath_new[-1],read_nexus.get_nx_class(node),'DEPRICATED!!!' if 'deprecated' in node.attrib.keys() else '',read_nexus.get_required_string(node)))
    read_nexus.print_doc(node, ntype, level, nxhtml, nxpath_new)

    #Create a sub-section
    metaNode=Section(name=read_nexus.get_nx_class(node))
    sub_section_name = 'nxp_' + nxpath_new[-1]
    mss = SubSection(sub_section=metaNode,name=sub_section_name, repeats=True)
    metaNode.nexus_parent = mss
    #decorate with properties
    decorate(metaNode,node,ntype,level,nxhtml,nxpath_new)
    #add the section
    m.sub_sections.append(mss)

    #fields and groups can have sub-elements
    if ntype!='attribute':
        #sub-attributes
        for attr in node.findall('attribute'):
            parse_node(metaNode,attr, 'attribute', level+1,nxhtml,nxpath_new)

        #groups can have sub-groups and sub-fields, too
        if ntype!='field':
            #sub-fields
            for field in node.findall('field'):
                parse_node(metaNode,field, 'field', level+1,nxhtml,nxpath_new)
            #sub-groups
            for sub_group in node.findall('group'):
                parse_node(metaNode,sub_group, 'group', level+1,nxhtml,nxpath_new)

nx_props = []

def decorate(metaNode,node, ntype, level, nxhtml, nxpath):
    '''
        decoreates a metainfo node (Section, Quantity) by nx metainfo
    '''
    #add inherited nx properties (e.g. type, minOccurs, depricated)
    for prop in node.attrib.keys():
      if "}schemaLocation" not in prop:
        if node.tag=='attribute' and prop not in nx_props:
            nx_props.append(prop)
        q = Quantity(
            name='nxp_'+prop,
            type=str,
            shape=[],
            description='''
            ''',
            default=node.attrib[prop])
        metaNode.quantities.append(q)
    #add documentation
    anchor, doc = read_nexus.get_doc(node, ntype, level, nxhtml, nxpath)
    q = Quantity(
        name='nxp_documentation',
        type=str,
        shape=[],
        description=('\n'+doc+'\n ' if doc is not None else '''
        ''')+anchor+" .",
        default=anchor)
    metaNode.quantities.append(q)

    #add derived nx properties (e.g. required)
    #REQUIRED
    reqStr=read_nexus.get_required_string(node)
    if 'REQUIRED' in reqStr:
        q = Quantity(
            name='nxp_required',
            type=bool,
            shape=[],
            description='''
            ''',
            default=True )
        metaNode.quantities.append(q)
    if 'RECOMENDED' in reqStr:
        q = Quantity(
            name='nxp_recommended',
            type=bool,
            shape=[],
            description='''
            ''',
            default=True)
        metaNode.quantities.append(q)
    if 'OPTIONAL' in reqStr:
        q = Quantity(
            name='nxp_optional',
            type=bool,
            shape=[],
            description='''
            ''',
            default=True)
        metaNode.quantities.append(q)
    #DEPRECATED
    if 'deprecated' in node.attrib.keys():
        q = Quantity(
            name='nxp_deprecated',
            type=bool,
            shape=[],
            description='''
            ''',
            default=True )
        metaNode.quantities.append(q)
    #ENUMS
    (o, enums) = read_nexus.get_enums(node)
    if o:
        q = Quantity(
            name='nxp_enumeration',
            type=str,
            shape=[],
            description='''
            '''+"\n Possible values:\n"+enums,
            default=enums)
        metaNode.quantities.append(q)

def parse_definition(definition,nxhtml):
    '''
        definition - definition node
        nxhtml     - url extension to html documentation (e.g. 'applications/NXxas.html')
    '''
    print('definition: %s' % (definition.attrib['name']))
    #Create a section
    m = Section(name=definition.attrib['name'])
    #check for base classes
    if 'extends' in definition.keys():
        #try to find the proposed based class
        for base in p.section_definitions:
            if base.name == definition.attrib['extends']:
                m.extends_base_section = True
                m.base_sections = [base.section_cls.m_def] #.m_def]
                break
        if not m.extends_base_section:
            if not definition.attrib['extends'] == 'NXobject':
                print('!!! PROBLEM WITH BASE CLASS !!! %s(%s)' % (definition.attrib['name'],definition.attrib['extends']))
            m.extends_base_section = True
            m.base_sections = [NXobject.m_def]
    #decorate with properties
    decorate(m,definition,'',1,nxhtml,[nxhtml.replace('.html', '').split('/')[-1]])
    #parse the definition
    for nodeType in ['group','field','attribute']:
        for node in definition.findall(nodeType):
            parse_node(m,node,nodeType,1,nxhtml,[nxhtml.replace('.html', '').split('/')[-1]])
    #add the section
    p.section_definitions.append(m)


def parse_file(nxdef):
    '''
        Parse an NXDL definition file

        nxdef - filename (with path) under the subfolder 'definitions'
    '''
    xmlparser = objectify.parse(os.environ["NEXUS_DEF_PATH"] + nxdef)
    #tag-ging elements with their names
    for elem in xmlparser.getiterator():
        try:
            elem.tag = etree.QName(elem).localname
            #print(elem.tag)
        except ValueError:
            print(f"Error with {elem.tag}")
    #parse elements under 'definition'
    root=xmlparser.getroot()
    for definition in root.iter('definition'):
        parse_definition(definition,nxdef.replace('nxdl.xml', 'html'))

def getfiles(path):
    '''
        get the NXDL files in the different definition subfolders
        (e.g. 'applications','base_classes','contributed_definitions')
    '''
    dirs=['base_classes', 'applications','contributed_definitions']
    for dir in dirs:
        for file in os.listdir(path+'/'+dir):
            if file.endswith('nxdl.xml'):
                yield dir+'/'+file


p = Package(name='NEXUS')

# add NXobject as a base class
class NXobject(MSection):
    pass
#p.section_definitions.append(NXobject)

#parse_file('applications/NXmx.nxdl.xml')
for file in getfiles(os.environ["NEXUS_DEF_PATH"]):
    print(file)
    if 'NXtranslation.' not in file and \
        'NXorientation.' not in file and \
        'NXobject.' not in file:
        parse_file(file)
        #break


# sorting all sections
def compare_dependencies(i1, i2):
    for i in i1.sub_sections:
        if i.sub_section.name == i2.name:
            return True
    return False


l = p.section_definitions
i=0
while i<len(l):
 j=i+1
 while j<len(l):
  if compare_dependencies(l[i],l[j]):
   #l[i],l[j]=l[j],l[i]
   l.append(l[i])
   l.__delitem__(i)
   break
  j=j+1
 if j==len(l):
  i=i+1
print(l)


# we write the schema as file
generate_metainfo_code(p, 'meta_nexus.py')
print('!!! meta_nexus.py is ready to be used:')
print('cp meta_nexus.py nexus.py\n')

print('==============================================')
for prop in nx_props:
    print(prop)
