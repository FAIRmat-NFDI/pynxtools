from nomad.metainfo.generate import generate_metainfo_code
from nomad.metainfo import Package
from nomad.metainfo import Section, Quantity, SubSection

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

def get_required_string(node):
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
    print("%s%s: %s (%s) %s %s" % (indent,ntype,nxpath_new[-1],get_nx_class(node),'DEPRICATED!!!' if 'deprecated' in node.attrib.keys() else '',get_required_string(node)))
    print_doc(node, ntype, level, nxhtml, nxpath_new)

    #Create a sub-section
    metaNode=Section(name=get_nx_class(node))
    mss = SubSection(sub_section=metaNode,name=nxpath_new[-1], repeats=True)
    #decorate with properties
    decorate(metaNode,node,ntype,level,nxhtml,nxpath)
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
        description='\n'+doc+'\n' if doc is not None else '''
        ''',
        default=anchor)
    metaNode.quantities.append(q)

    #add derived nx properties (e.g. required)
    #REQUIRED
    reqStr=get_required_string(node)
    q = Quantity(
        name='nxd_required',
        type=bool,
        shape=[],
        description='''
        ''',
        default=True if 'REQUIRED' in  reqStr else False)
    metaNode.quantities.append(q)
    q = Quantity(
        name='nxd_recommended',
        type=bool,
        shape=[],
        description='''
        ''',
        default=True if 'RECOMENDED' in  reqStr else False)
    metaNode.quantities.append(q)
    #DEPRECATED
    q = Quantity(
        name='nxd_deprecated',
        type=bool,
        shape=[],
        description='''
        ''',
        default=True if 'deprecated' in node.attrib.keys() else False)
    metaNode.quantities.append(q)

def parse_definition(definition,nxhtml):
    '''
        definition - definition node
        nxhtml     - url extension to html documentation (e.g. 'applications/NXxas.html')
    '''
    print('definition: %s' % (definition.attrib['name']))
    #Create a section
    m = Section(name=definition.attrib['name'])
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
    dirs=['applications','base_classes','contributed_definitions']
    for dir in dirs:
        for file in os.listdir(path+'/'+dir):
            if file.endswith('nxdl.xml'):
                yield dir+'/'+file


p = Package(name='NEXUS')


#parse_file('applications/NXmx.nxdl.xml')

for file in getfiles(os.environ["NEXUS_DEF_PATH"]):
    print(file)
    parse_file(file)

# we write the schema as file
generate_metainfo_code(p, 'meta_nexus.py')

print('==============================================')
for prop in nx_props:
    print(prop)
