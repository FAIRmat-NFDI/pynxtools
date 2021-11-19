#Nexus definitions in github: https://github.com/nexusformat/definitions
#to be cloned under os.environ['NEXUS_DEF_PATH'] 

import os
import h5py
import sys
from lxml import etree, objectify
import logging
import subprocess

LOGGING_FORMAT = "%(levelname)s: %(message)s"
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT, handlers=[stdout_handler])
logger = logging.getLogger()

#check for NEXUS definitions
try:
    #either given by sys env
    nexusDefPath = os.environ['NEXUS_DEF_PATH']
except:
    #or it should be available locally under the dir 'definitions'
    localDir=os.path.abspath(os.path.dirname(__file__))
    nexusDefPath=os.path.join(localDir,'definitions')
    if not os.path.exists(nexusDefPath):
        #check the definitions out if it has not been done yet
        cwd=os.getcwd()
        os.chdir(localDir)
        subprocess.call(['git','clone','https://github.com/nexusformat/definitions'])
        os.chdir(cwd)
        

def get_nx_class_path(hdfNode):
    """
            #get the full path of an HDF5 node using nexus classes
            #in case of a field, end with the field name
            """

    if hdfNode.name == '/':
        return ''
    elif isinstance(hdfNode, h5py.Group):
        return get_nx_class_path(
            hdfNode.parent) + '/' + hdfNode.attrs['NX_class']
    elif isinstance(hdfNode, h5py.Dataset):
        return get_nx_class_path(
            hdfNode.parent) + '/' + hdfNode.name.split('/')[-1]
    return ''


def get_nxdl_entry(hdfNode):
    """ #get the nxdl application definition for an HDF5 node """

    entry = hdfNode
    while isinstance(entry,
                     h5py.Dataset) or entry.attrs['NX_class'] != 'NXentry':
        entry = entry.parent
        if entry.name == '/':
            return 'NO NXentry found'
    try:
        nxdef = entry['definition'][()]
        return nxdef.decode()
    except:
        return 'NO Definition referenced'


def get_nx_class(nxdlElem):
    """ #get the nexus class for a NXDL node """

    try:
        return nxdlElem.attrib['type']
    except:
        return 'NX_CHAR'


def belongs_to(nxdlElem, hdfName):
    """
            #checks if an HDF5 node name corresponds to an NXDL element
            #uppercase letters in front can be replaced by arbitraty name
            """

    #check if nameType allows different name
    try:
        if nxdlElem.attrib['nameType'] == "any":
            nameAny = True
        else:
            nameAny = False
    except:
        nameAny = False
    #and no reserved words used
    if nameAny and hdfName != 'doc' and hdfName != 'enumeration':
        ct = 0
        while ct < len(nxdlElem.attrib['name']) and nxdlElem.attrib['name'][
                ct] >= 'A' and nxdlElem.attrib['name'][ct] <= 'Z':
            ct += 1
        if ct == len(nxdlElem.attrib['name']) or hdfName.endswith(
                nxdlElem.attrib['name'][ct:]):
            return True
        return False
    else:
        if nxdlElem.attrib['name'] == hdfName:
            return True
    return False


def get_own_nxdl_child(nxdlElem, name):
    """
    checks if an NXDL child node fits to the specific name
    """
    for child in nxdlElem.getchildren():
        if etree.QName(child).localname == 'group' and get_nx_class(
                child) == name:
            return child
        if etree.QName(child).localname == 'field' and belongs_to(child, name):
            return child
        if etree.QName(child).localname == 'attribute' and belongs_to(
                child, name):
            return child
        if etree.QName(child).localname == 'doc' and name == 'doc':
            return child
        if etree.QName(
                child).localname == 'enumeration' and name == 'enumeration':
            return child
    return None


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


def get_nxdl_child(nxdlElem, name):
    """
            #get the NXDL child node corresponding to a specific name
            #(e.g. of an HDF5 node,or of a documentation)
            #note that if child is not found in application definition, it also checks for the base classes
            """

    ownChild = get_own_nxdl_child(nxdlElem, name)
    if ownChild is not None:
        return ownChild
    #check in the base class
    bc_name = get_nx_class(nxdlElem)
    #filter primitive types
    if bc_name[2] == '_':
        return None
    bc = objectify.parse(nexusDefPath + '/base_classes/' + bc_name +
                         '.nxdl.xml').getroot()
    return get_own_nxdl_child(bc, name)


def get_required_string(nxdlElem):
    """
            #check for being required
            # REQUIRED, RECOMMENDED, OPTIONAL, NOT IN SCHEMA
            """

    if nxdlElem is None:
        return "<<NOT IN SCHEMA>>"
    #if optionality is defined
    elif ('optional' in nxdlElem.attrib.keys() and nxdlElem.attrib['optional']=="true") or \
        ('minOccurs' in nxdlElem.attrib.keys() and nxdlElem.attrib['minOccurs']=="0") :
        return "<<OPTIONAL>>"
    #new expression for being recommended
    elif 'recommended' in nxdlElem.attrib.keys(
    ) and nxdlElem.attrib['recommended'] == "true":
        return "<<RECOMMENDED>>"
    #default optionality
    # in BASE CLASSES: true
    # in APPLICATIONS: false
    elif "base_classes" in nxdlElem.base or \
        ('required' in nxdlElem.attrib.keys() and nxdlElem.attrib['required']=="false") :
        return "<<OPTIONAL>>"
    return "<<REQUIRED>>"


def chk_NXdataAxis_v2(hdfNode, name):
    #check for being a Signal
    ownSignal = hdfNode.attrs.get('signal')
    if ownSignal is str and ownSignal == "1":
        logger.info("Dataset referenced (v2) as NXdata SIGNAL")
    #check for being an axis
    ownAxes = hdfNode.attrs.get('axes')
    if ownAxes is str:
        axes = ownAxes.split(':')
        for i in len(axes):
            if axes[i] and name == axes[i]:
                logger.info("Dataset referenced (v2) as NXdata AXIS #%d" % i)
                return
    ownPAxis = hdfNode.attrs.get('primary')
    ownAxis = hdfNode.attrs.get('axis')
    if ownAxis is int:
        #also convention v1
        if ownPAxis is int and ownPAxis == 1:
            logger.info("Dataset referenced (v2) as NXdata AXIS #%d" %
                         ownAxis - 1)
            return
        else:
            logger.info(
                "Dataset referenced (v2) as NXdata (primary/alternative) AXIS #%d"
                % ownAxis - 1)
            return


def chk_NXdataAxis(hdfNode, name):
    """
        NEXUS Data Plotting Standard v3: new version from 2014
    """
    #check if it is a field in an NXdata node
    if not isinstance(hdfNode, h5py.Dataset):
        return
    parent = hdfNode.parent
    if not parent or (parent and not "NXdata" == parent.attrs.get('NX_class')):
        return
    #chk for Signal
    signal = parent.attrs.get('signal')
    if signal and name == signal:
        logger.info("Dataset referenced as NXdata SIGNAL")
        return
    #check for default Axes
    axes = parent.attrs.get('axes')
    axisFnd = False
    if axes is str:
        if name == axes:
            logger.info("Dataset referenced as NXdata AXIS")
            return
    elif axes is not None:
        for i in range(len(axes)):
            if name == axes[i]:
                indices = parent.attrs.get(axes[i] + '_indices')
                if indices is int:
                    logger.info("Dataset referenced as NXdata AXIS #%d" %
                                 indices)
                else:
                    logger.info("Dataset referenced as NXdata AXIS #%d" % i)
                return
    #check for alternative Axes
    indices = parent.attrs.get(name + '_indices')
    if indices is int:
        logger.info("Dataset referenced as NXdata alternative AXIS #%d" %
                     indices)
    #check for older conventions
    return chk_NXdataAxis_v2(hdfNode, name)


def get_nxdl_doc(hdfNode, doc, attr=False):
    """get nxdl documentation for an HDF5 node (or its attribute)"""

    nxdef = get_nxdl_entry(hdfNode)
    root = objectify.parse(nexusDefPath + "/applications/" + nxdef + ".nxdl.xml")
    elem = root.getroot()
    nxdlPath = [elem]
    path = get_nx_class_path(hdfNode)
    for group in path.split('/')[1:]:
        if group.startswith('NX'):
            elem = get_nxdl_child(elem, group)
            if elem is not None:
                if doc: logger.info("/" + group)
                nxdlPath.append(elem)
            else:
                if doc: logger.info("/" + group + " - IS NOT IN SCHEMA")
        else:
            if elem is not None:
                elem = get_nxdl_child(elem, group)
                nxdlPath.append(elem)
            if elem is not None:
                if attr != False:
                    if doc: logger.info("/" + group)
                else:
                    if doc: logger.info("/" + group + ' [' + get_nx_class(elem) + ']')
            else:
                if doc: logger.info("/" + group + " - IS NOT IN SCHEMA")
    if elem is not None and attr != False:
        if attr == 'NX_class':
            elem = None
            if doc: logger.info("@" + attr + ' [NX_CHAR]')
        elif attr == 'units':
            try:
                #try to handle if units is deinfed in the field
                if doc: logger.info("@" + attr + ' [' + elem.attrib[attr] + ']')
                elem = None
                nxdlPath.append(attr)
            except:
                #handle if units is defined as an attribute
                elem = get_nxdl_child(elem, attr)
                if elem is not None:
                    if doc: logger.info("@" + attr + ' - [' + get_nx_class(elem) +
                                 ']')
                    nxdlPath.append(attr)
                else:
                    if doc: logger.info("@" + attr + " - IS NOT IN SCHEMA")
        else:
            elem = get_nxdl_child(elem, attr)
            if elem is not None:
                if doc: logger.info("@" + attr + ' - [' + get_nx_class(elem) + ']')
                nxdlPath.append(attr)
            else:
                if doc: logger.info("@" + attr + " - IS NOT IN SCHEMA")
    if elem is None:
        if doc: logger.info("")
        return ('None',None,None,None)
    else:
        #check for being required
        REQstr = get_required_string(elem)
        if doc: logger.info(REQstr)
        #check for deprecation
        depStr = elem.attrib.get('deprecated')
        if depStr:
            if doc: logger.info("DEPRECATED - " + depStr)
        #check for enums
        sdoc = get_nxdl_child(elem, 'enumeration')
        if sdoc is not None:
            if doc: logger.info("enumeration:")
            for item in sdoc.getchildren():
                if etree.QName(item).localname == 'item':
                    if doc: logger.info("-> " + item.attrib['value'])
        #check for NXdata references (axes/signal)
        chk_NXdataAxis(hdfNode, path.split('/')[-1])
        #check for doc
        sdoc = get_nxdl_child(elem, 'doc')
        if doc: logger.info(sdoc if sdoc is not None else "")
        return (REQstr,elem,nxdef,nxdlPath)


def process_node(hdfNode,parser,doc=True):
    """
            #processes an hdf5 node
            #- it logs the node found and also checks for its attributes
            #- retrieves the corresponding nxdl documentation
            #TODO:
            # - follow variants
            # - NOMAD parser: store in NOMAD
            """
    hdfPath=hdfNode.name
    if isinstance(hdfNode, h5py.Dataset):
        logger.info('===== FIELD (/%s): %s' % (hdfPath, hdfNode))
        val = str(hdfNode[()]).split('\n') if len(hdfNode.shape) <= 1 else str(
            hdfNode[0]).split('\n')
        logger.info('value: %s %s' % (val[0], "..." if len(val) > 1 else ''))
    else:
        logger.info('===== GROUP (/%s [%s::%s]): %s' %
                     (hdfPath, get_nxdl_entry(hdfNode),
                      get_nx_class_path(hdfNode), hdfNode))
    (REQstr,elem,nxdef,nxdlPath) = get_nxdl_doc(hdfNode,doc)
    if parser is not None and isinstance(hdfNode, h5py.Dataset):
        parser(hdfPath,hdfNode,nxdef,nxdlPath,val)
    for k, v in hdfNode.attrs.items():
        logger.info('===== ATTRS (/%s@%s)' % (hdfPath, k))
        val = str(v).split('\n')
        logger.info('value: %s %s' % (val[0], "..." if len(val) > 1 else ''))
        (REQstr,elem,nxdef,nxdlPath) = get_nxdl_doc(hdfNode, doc, attr=k)
        if parser is not None and not 'NOT IN SCHEMA' in REQstr and not 'None' in REQstr:
            parser(hdfPath,hdfNode,nxdef,nxdlPath,val)

def get_default_plotable(root,parser):
    logger.info('========================')
    logger.info('=== Default Plotable ===')
    logger.info('========================')
    #v3 from 2014

    #nxentry
    nxentry=None
    default_nxentry_group_name = root.attrs.get("default")
    if default_nxentry_group_name:
        try:
            nxentry = root[default_nxentry_group_name]
        except:
            nxentry=None
    if not nxentry:
        nxentries=[]
        for key in root.keys():
            if isinstance(root[key], h5py.Group) and root[key].attrs.get('NX_class') and root[key].attrs['NX_class']=="NXentry":
                nxentries.append(root[key])
        #v3: as there was no selection given, only 1 nxentry shall exists
        #v2: take any
        if len(nxentries)>=1:
            nxentry=nxentries[0]
    if not nxentry:
        logger.info('No NXentry has been found')
        return
    logger.info('')    
    logger.info('NXentry has been identified: '+nxentry.name)
    #process_node(nxentry, None, False)
    #nxdata
    nxdata=None
    default_nxdata_group_name = nxentry.attrs.get("default")
    if default_nxdata_group_name:
        try:
            nxdata = nxentry[default_nxdata_group_name]
        except:
            nxdata=None
    if not nxdata:
        lnxdata=[]
        for key in nxentry.keys():
            if isinstance(nxentry[key], h5py.Group) and nxentry[key].attrs.get('NX_class') and nxentry[key].attrs['NX_class']=="NXdata":
                lnxdata.append(nxentry[key])
        #v3: as there was no selection given, only 1 nxdata shall exists
        #v2: take any
        if len(lnxdata)>=1:
            nxdata=lnxdata[0]
    if not nxdata:
        logger.info('No NXdata group has been found')
        return
    logger.info('')    
    logger.info('NXdata group has been identified: '+nxdata.name)
    process_node(nxdata, None, False)
    #signal
    signal=None
    signal_dataset_name = nxdata.attrs.get("signal")
    try:
        signal=nxdata[signal_dataset_name]
    except:
        signal=None
    if not signal:
        signals=[]
        for key in nxdata.keys():
            if isinstance(nxdata[key], h5py.Dataset):
                signals.append(nxdata[key])
        #v3: as there was no selection given, only 1 data field shall exists
        if len(signals)==1:
            signal=signals[0]
        #v2: select the one with an attribute signal="1" attribute
        elif len(signals)>1:
            for s in signals:
                if s.attrs.get("signal") and s.attrs.get("signal") is str and s.attrs.get("signal")=="1":
                    signal=s
                    break
    if not signal:
        logger.info('No Signal has been found')
        return
    logger.info('')    
    logger.info('Signal has been identified: '+signal.name)
    process_node(signal, None, False)
    dim=len(signal.shape)
    #axes
    axes=[]
    for a in range(dim):
        ax=[]
        #primary axes listed in attribute axes
        ax_datasets = nxdata.attrs.get("axes")
        try:
            #single axis is defined
            if ax_datasets is str:
                #explicite definition of dimension number
                ind=nxdata.attrs.get(ax_datasets+'_indices')                
                if ind and ind is int:
                    if ind==a:
                        ax.append(nxdata[nxdata[ax_datasets]])
                #positional determination of the dimension number
                elif a==0:
                    ax.append(nxdata[nxdata[ax_datasets]])
            #multiple axes are listed
            else:
                #explicite definition of dimension number
                for aax in ax_datasets:
                    ind=nxdata.attrs.get(aax+'_indices')
                    if ind and ind is int:
                        if ind==a:
                            ax.append(nxdata[nxdata[aax]])
                #positional determination of the dimension number
                if len(ax)==0:
                        ax.append(nxdata[ax_datasets[a]])
        except:
            pass
        #check for corresponding AXISNAME_indices
        for attr in nxdata.attrs.keys():
            if attr.endswith('_indices') and nxdata.sttrs[attr]==a:
                ax.append(nxdata[attr.split('_indices')[0]])
        #v2
        #check for ':' separated axes defined in Signal
        if len(ax)==0:
            try:
                ax_datasets = signal.attrs.get("axes").split(':')
                ax.append(nxdata[ax_datasets[a]])
            except:
                pass
        #check for axis/primary specifications
        if len(ax)==0:
            #find those with attribute axis= actual dimension number
            lax=[]
            for key in nxdata.keys():
                if isinstance(nxdata[key], h5py.Dataset):
                    try:
                        if nxdata[key].attrs['axis']==a+1:
                            lax.append(nxdata[key])
                    except:
                        pass
            if len(lax)==1:
                ax.append(lax[0])
            #if there are more alternatives, prioritise the one with an attribute primary="1"
            elif len(lax)>1:
                for sax in lax:
                    if sax.attrs.get('primary') and sax.attrs.get('primary')==1:
                        ax.insert(0,sax)
                    else:
                        ax.append(sax)
        axes.append(ax)
        logger.info('')    
        logger.info('For Axis #%d, %d axes have been identified: %s' % (a,len(ax),str(ax)))


class HandleNexus:
    def __init__(self, args):
        self.input_file_name = args[0] if len(
            #args) >= 1 else 'wcopy/from_dallanto_master_from_defs.h5'
            args) >= 1 else 'ARPES/201805_WSe2_arpes.nxs'

    def visit_node(self,hdfPath,hdfNode):
        process_node(hdfNode, self.parser)

    def process_nexus_master_file(self,parser):
        """ Process a nexus master file by processing all its nodes and their attributes"""

        self.parser=parser
        self.in_file = h5py.File(self.input_file_name, 'r')
        self.in_file.visititems(self.visit_node)
        get_default_plotable(self.in_file,self.parser)
        self.in_file.close()


if __name__ == '__main__':
    nexus_helper = HandleNexus(sys.argv[1:])
    nexus_helper.process_nexus_master_file(None)
