#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 17:48:21 2021

@author: kuehbach
"""
import os, sys
import yaml
from lxml import etree
from yaml2nxdl_utils import nx_name_type_resolving
from yaml2nxdl_utils import nx_base_clss, nx_cand_clss, nx_unit_idnt, nx_unit_typs
from yaml2nxdl_utils import nx_type_keys, nx_attr_idnt

def xml_handle_docstring(obj, k, v):
    obj.set('doc', str(v))

def xml_handle_units(obj, k, v):
    obj.set('units', v)

def xml_handle_exists(obj, k, v):
    if v != None:
        if isinstance(v,list): #handle []
            if len(v) == 2:
                if v[0] == 'min':
                    obj.set('minOccurs', str(v[1]))
                if v[0] == 'max':
                    obj.set('maxOccurs', str(v[1]))
            elif len(v) == 4:
                if v[0] == 'min' and v[2] == 'max':
                    obj.set('minOccurs', str(v[1]))
                    if str(v[3]) != 'infty':
                        obj.set('maxOccurs', str(v[3]))
                    else:
                        obj.set('maxOccurs', 'unbounded')
                else:
                    raise ValueError('exists keyword needs to go either with optional, recommended, a list with two entries either [min, <uint>] or [max, <uint>], or a list of four entries [min, <uint>, max, <uint>] !')
            else:
                raise ValueError('exists keyword needs to go either with optional, recommended, a list with two entries either [min, <uint>] or [max, <uint>], or a list of four entries [min, <uint>, max, <uint>] !')
        else:
            if v == 'optional':
                obj.set('optional', 'true')
            elif v == 'recommended':
                obj.set('recommended', 'true')
            elif v == 'required':
                obj.set('minOccurs', '1')
            else:
                obj.set('minOccurs', '0')
    else:
        raise ValueError('exists keyword found but value is None !')

def xml_handle_dimensions(obj, k, v):
    if v != None:
        if isinstance(v,dict):
            if 'rank' in v and 'dim' in v:
                dims = etree.SubElement(obj, 'dimensions')
                dims.set('rank', str(v['rank']))
                for m in v['dim']:
                    if isinstance(m, list):
                        if len(m) >= 2:
                            dim = etree.SubElement(dims, 'dim')
                            dim.set('index', str(m[0]))
                            dim.set('value', str(m[1]))
                        if len(m) == 3:
                            if m[2] == 'optional':
                                dim.set('required', 'false')
                            else:
                                print('WARNING: '+k+' dimensions with len(3) list with non-optional argument, unexpected case !')
                    else:
                        raise ValueError('WARNING: '+k+' dimensions list item needs to have at least two members !' )
            else:
                raise ValueError('exists keyword found, value is dict but has no keys rank and dim !')
        else:
            raise ValueError('exists keyword found but value is not a dictionary !')
    else:
        raise ValueError('exists keyword found but value is None !')

def xml_handle_enumeration(obj, k, v):
    enum = etree.SubElement(obj, 'enumeration')
    #assume we get a list as the value argument
    if v != None:
        if isinstance(v, list):
            for m in v:
                itm = etree.SubElement(enum, 'item')
                itm.set('value', str(m))
        else:
            raise ValueError('ERROR: '+k+' we found an enumeration key-value pair but the value is not an ordinary Python list !')
    else:
        raise ValueError('ERROR: '+k+' we found an enumeration key-value pair but the value is None !')

def xml_handle_links(obj, k, v):
    #if we have a link we decode the name attribute from <optional string>(link)[:-6]
    if len(k[:-6]) >= 1 and isinstance(v,dict) and 'target' in v.keys():
        if isinstance(v['target'],str) and len(v['target']) >= 1:
            lnk = etree.SubElement(obj, 'link')
            lnk.set('name', k[:-6])
            lnk.set('target', v['target'])
        else:
            raise ValueError(k+' value for target member of a link is invalid !')
    else:
        raise ValueError(k+' the formatting of what seems to be a link is invalid in the yml file !')


def recursive_build(obj, dct):
    """
    obj is the current node where we want to append to, dct is a dictionary object which represents the content of the child in the nested set of dictionaries
    """
    for k, v in iter(dct.items()):
        print('Processing key '+k+' value v is a dictionary '+str(isinstance(v,dict)))
        #base class prefix tag removal
        #k = '(NXentry)'
        #k = 'sensor_size(NX_INT)'
        kName, kType = nx_name_type_resolving(k)
        print('kName: '+kName+' kType: '+kType)
        if kName == '' and kType == '':
            raise ValueError('ERROR: Found an improper YML key !')
        elif kType in nx_base_clss or kType in nx_cand_clss or kType not in nx_type_keys:
            #we can be sure we need to instantiate a new group
            grp = etree.SubElement(obj, 'group')
            if kName != '': #use the custom name for the group
                grp.set('name', kName) #because we are a base or cand clss kName is a NX<str>
            else: #use the NeXus default to infer the name from the base/cand class name stripping the 'NX' decorator prefix
                if kType != '':
                    grp.set('name', kType)                                  
            grp.set('type', kType)
            if v != None:
                if isinstance(v,dict):
                    if v != {}:
                        recursive_build(grp, v)
        elif kName[0:2] == nx_attr_idnt: #check if obj qualifies as an attribute, do not impose a constraint on kType
            attr = etree.SubElement(obj, 'attribute')
            attr.set('name', kName[2:])
            if v != None:
                if isinstance(v,dict):
                    for kk, vv in iter(v.items()):
                        if kk == 'name':
                            attr.set('name', vv)
                        elif kk == 'doc':
                            attr.set('doc', vv)
                        elif kk == 'type':
                            attr.set('type', vv.upper())
                        elif kk == 'enumeration':
                            xml_handle_enumeration(attr,kk, vv)
                        else:
                            raise ValueError(kk+' facing an unknown situation while processing attributes of an attribute !')
            #else: #e.g. for case like \@depends_on:
            #    attr.set('name', k[2:])
        #handle special keywords, ###MK::add handling of symbols!
        elif k == 'doc':
            xml_handle_docstring(obj, k, v)
        elif k == 'enumeration':
            xml_handle_enumeration(obj, k, v)
        elif k == 'dimensions':
            xml_handle_dimensions(obj, k, v)
        elif k == 'exists':
            xml_handle_exists(obj, k, v)
        #elif k == 'link': ##MK:check handling of links for
        #base/cand classes, attributes, and special keywords handled, so only members remain
        elif k[-6:] == '(link)':
            xml_handle_links(obj, k, v)
        elif kName != '': #dealing with a field because classes and attributes already ruled out
            typ = 'NX_CHAR'
            if kType in nx_type_keys:
                typ = kType
            #else:
            #    raise valueError(kk+' facing an unknown kType !')
            #assume type is NX_CHAR, a NeXus default assumption if in doubt
            fld = etree.SubElement(obj, 'field')
            fld.set('name', kName)
            fld.set('type', typ)
            if v != None: #a field may have subordinated attributes
                if isinstance(v,dict):
                    for kk, vv in iter(v.items()):
                        #print(kk+' field-attribute handling')
                        #if vv != None:
                        #    print('field-attribute handling'+kk+' is taken!')
                        if kk[0:2] == nx_attr_idnt:
                            attr = etree.SubElement(fld, 'attribute')
                            #attributes may also come with an nx_type specifier which we need to decipher first
                            kkName, kkType = nx_name_type_resolving(kk[2:]) #strip the nx_attr_idnt prefix
                            attr.set('name', kkName)
                            typ = 'NX_CHAR'
                            if kkType in nx_type_keys:
                                typ = kkType
                            attr.set('type', typ)
                            if vv != None:
                                if isinstance(vv,dict):
                                    for kkk, vvv in iter(vv.items()):
                                        if kkk == 'doc':
                                            attr.set('doc', vvv)
                                        elif kkk == 'exists':
                                            xml_handle_exists(attr, kkk, vvv)
                                        elif kkk == 'enumeration':
                                            xml_handle_enumeration(attr, kkk, vvv)
                                        else:
                                            raise ValueError(k+' '+kk+' '+kkk+' attribute handling !')
                        elif kk == 'doc':
                            fld.set('doc', str(vv))
                        elif kk == nx_unit_idnt:
                            xml_handle_units(fld, kk, vv)
                        elif kk == 'exists':
                            xml_handle_exists(fld, kk, vv)
                        elif kk == 'dimensions':
                            xml_handle_dimensions(fld, kk, vv)
                        elif kk == 'enumeration':
                            xml_handle_enumeration(fld, kk, vv)
                        elif kk == 'link':
                            fld.set('link', '')
                        else:
                            raise ValueError(k+' '+kk+' faced unknown situation !')
            else:
                if k == 'type':
                    print(k+' facing a type where we would not expect it!')
                elif k == 'doc': #key is a documentation string specifier
                    xml_handle_docstring(fld, k, v)
                elif k == nx_unit_idnt:
                    xml_handle_units(fld, k, v)
                elif k[0:2] == nx_attr_idnt: #attribute of a field
                    raise ValueError(k+' unknown attribute of a field case coming from no dict !')
                elif k == 'exists':
                    xml_handle_exists(fld, k, v)
                elif k == 'dimensions':
                    raise ValueError(k+' unknown dimensions of a field case coming from no dict !')
                else:
                    pass
                #else:
                #    raise ValueError(k+' faces a completely unexpected situation !')