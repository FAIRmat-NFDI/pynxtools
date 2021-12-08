#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import sys
import yaml


def nx_name_type_resolving(tmp):
    """
    extracts the eventually custom name {optional_string} an type {nexus_type} from a YML section string.
    YML section string syntax: optional_string(nexus_type)
    """
    if tmp.count('(') == 1 and tmp.count(')') == 1:
        # we can safely assume that every valid YML key resolves
        # either an nx_ (type, base, candidate) class contains only 1 '(' and ')'
        idxStart = tmp.index('(')
        idxEnd = tmp.index(')', idxStart + 1)
        typ = tmp[idxStart + 1:idxEnd]
        nam = tmp.replace('(' + typ + ')', '')
        return nam, typ
    # or a name for a member
    typ = ''
    nam = tmp
    return nam, typ


nx_clss = ['NXaperture', 'NXattenuator', 'NXbeam', 'NXbeam_stop', 'NXbending_magnet', 'NXcapillary', 'NXcite',
           'NXcollection', 'NXcollimator', 'NXcrystal', 'NXcylindrical_geometry', 'NXdata', 'NXdetector',
           'NXdetector_group', 'NXdetector_module', 'NXdisk_chopper', 'NXentry', 'NXenvironment', 'NXevent_data',
           'NXfermi_chopper', 'NXfilter', 'NXflipper', 'NXfresnel_zone_plate, ''NXgeometry', 'NXgrating', 'NXguide',
           'NXinsertion_device', 'NXinstrument', 'NXlog', 'NXmirror', 'NXmoderator', 'NXmonitor', 'NXmonochromator',
           'NXnote', 'NXobject', 'NXoff_geometry', 'NXorientation', 'NXparameters', 'NXpdb', 'NXpinhole', 'NXpolarizer',
           'NXpositioner', 'NXprocess', 'NXreflections', 'NXroot', 'NXsample', 'NXsample_component', 'NXsensor', 'NXshape',
           'NXslit', 'NXsource', 'NXsubentry', 'NXtransformations', 'NXtranslation', 'NXuser', 'NXvelocity_selector',
           'NXxraylens']

nx_type_keys = ['NX_BINARY', 'NX_BOOLEAN', 'NX_CHAR', 'NX_DATE_TIME',
                'NX_FLOAT', 'NX_INT', 'NX_NUMBER', 'NX_POSINT', 'NX_UINT']

nx_attr_idnt = '\\@'
nx_unit_idnt = 'unit'
nx_unit_typs = ['NX_ANGLE', 'NX_ANY', 'NX_AREA', 'NX_CHARGE', 'NX_CROSS_SECTION', 'NX_CURRENT', 'NX_DIMENSIONLESS',
                'NX_EMITTANCE', 'NX_ENERGY', 'NX_FLUX', 'NX_FREQUENCY', 'NX_LENGTH', 'NX_MASS', 'NX_MASS_DENSITY',
                'NX_MOLECULAR_WEIGHT', 'NX_PERIOD', 'NX_PER_AREA', 'NX_PER_LENGTH', 'NX_POWER', 'NX_PRESSURE',
                'NX_PULSES', 'NX_SCATTERING_LENGTH_DENSITY', 'NX_SOLID_ANGLE', 'NX_TEMPERATURE', 'NX_TIME',
                'NX_TIME_OF_FLIGHT', 'NX_TRANSFORMATION', 'NX_UNITLESS', 'NX_VOLTAGE', 'NX_VOLUME', 'NX_WAVELENGTH',
                'NX_WAVENUMBER']
