#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 17:41:08 2021
@author: kuehbach
"""


import os, sys
import yaml
##import punx
##import json
from lxml import etree
#import lxml.etree.ElementTree as ET


def nx_base_clss_string_mangling(tmp):
    if tmp[0:3] == 'nx_':
        return 'NX'+tmp[3::]
    else:
        return tmp
        #raise ValueError(tmp+' is not a properly formatted nexus keyword which this parser knows!')

def nx_name_type_resolving(tmp):
    """
    extracts the type and eventually custom name from a YML section string
    """
    #tmp = '' #will throw
    #tmp = '(NXentry)' #will return '', 'NXentry' tuple
    #tmp = 'condensor(NXem_lens)' #will return 'condensor', 'NXem_lens' tuple
    #tmp = 'type'
    if tmp.count('(') == 1 and tmp.count(')') == 1: 
        #we can safely assume that every valid YML key resolves
        #either an nx_ (type, base, candidate) class contains only 1 '(' and ')'
        idxStart = tmp.index('(')
        idxEnd = tmp.index(')',idxStart+1)
        typ = tmp[idxStart+1:idxEnd] #.replace('NX','nx_')
        nam = tmp.replace('('+typ+')','') #.replace('nx_','NX')+')','')
        return nam, typ
    #or a name for a member
    typ = ''
    nam = tmp
    return nam, typ


nx_base_clss = ['nx_aperture', 'nx_attenuator', 'nx_beam', 'nx_beam_stop', 'nx_bending_magnet', 'nx_capillary', 'nx_cite', 
    'nx_collection', 'nx_collimator', 'nx_crystal', 'nx_cylindrical_geometry', 'nx_data', 'nx_detector', 
    'nx_detector_group', 'nx_detector_module', 'nx_disk_chopper', 'nx_entry', 'nx_environment', 'nx_event_data', 
    'nx_fermi_chopper', 'nx_filter', 'nx_flipper', 'nx_fresnel_zone_plate, ''nx_geometry', 'nx_grating', 'nx_guide', 
    'nx_insertion_device', 'nx_instrument', 'nx_log', 'nx_mirror', 'nx_moderator', 'nx_monitor', 'nx_monochromator', 
    'nx_note', 'nx_object', 'nx_off_geometry', 'nx_orientation', 'nx_parameters', 'nx_pdb', 'nx_pinhole', 'nx_polarizer', 
    'nx_positioner', 'nx_process', 'nx_reflections', 'nx_root', 'nx_sample', 'nx_sample_component', 'nx_sensor', 'nx_shape', 
    'nx_slit', 'nx_source', 'nx_subentry', 'nx_transformations', 'nx_translation', 'nx_user', 'nx_velocity_selector',
    'nx_xraylens']

nx_type_keys = ['nx_binary', 'nx_boolean', 'nx_char', 'nx_date_time', 
                'nx_float', 'nx_int', 'nx_number', 'nx_posint', 'nx_uint']
#nx_grpnm_tag = '___'
nx_attr_idnt = '\@'
nx_unit_idnt = 'unit'
nx_unit_typs = ['nx_angle',  'nx_any', 'nx_area', 'nx_charge', 'nx_cross_section', 'nx_current', 'nx_dimensionless',
                'nx_emittance', 'nx_energy', 'nx_flux', 'nx_frequency', 'nx_length', 'nx_mass', 'nx_mass_density',
                'nx_molecular_weight', 'nx_period', 'nx_per_area', 'nx_per_length', 'nx_power', 'nx_pressure',
                'nx_pulses', 'nx_scattering_length_density', 'nx_solid_angle', 'nx_temperature', 'nx_time',
                'nx_time_of_flight', 'nx_transformation', 'nx_unitless', 'nx_voltage', 'nx_volume', 'nx_wavelength',
                'nx_wavenumber']

nx_cand_clss = ['nx_em_lens', 'nx_em_cs_corr','nx_em_deflector','nx_em_stage']