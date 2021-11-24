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
import textwrap
import os


def get_node_name(node):
    '''
        node - xml node
        returns:
            html documentation name
            Either as specified by the 'name' or taken from the type (nx_class).
            Note that if only class name is available, the NX prefix is removed and
            the string is coverted to UPPER case.
    '''
    if 'name' in node.attrib.keys():
        name=node.attrib['name']
    else:
        name=node.attrib['type']
        if name.startswith('NX'):
            name=name[2:].upper()
    return name

def get_nx_class(node):
    '''
        node - xml node
        returns:
            nx_class name
            Note that if 'type' is not defined, NX_CHAR is assumes
    '''
    return node.attrib['type'] if 'type' in node.attrib.keys() else 'NX_CHAR'

def get_required_string(node, nxhtml):
    """
        check for being required.
        returns:
         REQUIRED, RECOMMENDED, OPTIONAL, NOT IN SCHEMA
    """
    if node is None:
        return "<<NOT IN SCHEMA>>"
    elif ('optional' in node.attrib.keys() and node.attrib['optional']=="true") or \
        ('minOccurs' in node.attrib.keys() and node.attrib['minOccurs']=="0"):
        return "<<OPTIONAL>>"
    elif 'recommended' in node.attrib.keys() and node.attrib['recommended'] == "true":
        return "<<RECOMMENDED>>"
    elif 'optional' in node.attrib.keys() and node.attrib['optional'] == "false":
        return "<<REQUIRED>>"
    elif nxhtml.split("/")[0] == "base_classes":
        return "<<OPTIONAL>>"
    else:
        return "<<REQUIRED>>"

def get_doc(node, ntype, level, nxhtml, nxpath):
    #URL for html documentation
    anchor=''
    for n in nxpath:
        anchor+=n.lower()+"-"
    anchor='https://manual.nexusformat.org/classes/'+nxhtml+"#"+anchor.replace('_', '-')+ntype
    if len(ntype)==0:
        anchor=anchor[:-1]

    #RST documentation from the field 'doc'
    try:
        doc=node.doc.pyval
    except:
        doc=None
    return anchor,doc

def print_doc(node, ntype, level, nxhtml, nxpath):
    anchor,doc = get_doc(node, ntype, level, nxhtml, nxpath)
    print("  "*(level+1)+anchor)

    preferredWidth = 80 + level*2
    wrapper = textwrap.TextWrapper(initial_indent='  '*(level+1), width=preferredWidth,
                               subsequent_indent='  '*(level+1),expand_tabs=False,tabsize=0)
    #doc=node.find('doc')
    if doc is not None:
        #for par in doc.text.split('\n'):
        for par in doc.split('\n'):
            print(wrapper.fill(par))
    #print(doc.text if doc is not None else "")

def get_enums(node):
    """
    makes list of enumerations, if node contains any.
    Returns comma separated STRING of enumeration values, if there are enum tag,
    otherwise empty string.
    """
    #collect item values from enumeration tag, if any
    try:
        for items in node.enumeration:
            enums = []
            for values in items.findall('item'):
                enums.append(values.attrib['value'])
            enums = ','.join(enums)
            return (True, enums)
    #if there is no enumeration tag, returns empty string
    except:
        return (False, '')


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
    nxpath_new.append(get_node_name(node))
    indent='  ' *level
    print("%s%s: %s (%s) %s %s" % (indent,ntype,nxpath_new[-1],get_nx_class(node),'DEPRICATED!!!' if 'deprecated' in node.attrib.keys() else '',get_required_string(node, nxhtml)))
    print_doc(node, ntype, level, nxhtml, nxpath_new)

    #Create a sub-section
    metaNode=Section(name=get_nx_class(node))
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
        if prop not in nx_props:
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
    anchor, doc = get_doc(node, ntype, level, nxhtml, nxpath)
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
    reqStr=get_required_string(node, nxhtml)
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
    (o, enums) = get_enums(node)
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
