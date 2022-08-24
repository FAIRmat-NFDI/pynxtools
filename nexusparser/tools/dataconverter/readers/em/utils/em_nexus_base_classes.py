#!/usr/bin/env python3
"""General metadata object connecting units and values for a quantity."""

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

# pylint: disable=E1101

# from typing import Tuple

from nexusparser.tools.dataconverter.readers.em.utils.em_versioning \
    import NX_EM_ADEF_NAME, NX_EM_ADEF_VERSION, \
    NX_EM_EXEC_NAME, NX_EM_EXEC_VERSION


class NxObject:
    """An object in a graph e.g. a field or group in NeXus."""

    def __init__(self,
                 name: str = None,
                 unit: str = None,
                 dtype=str,
                 value=None,
                 *args, **kwargs):
        if name is not None:
            assert name != '', 'Argument name needs to be a non-empty string !'
        if unit is not None:
            assert unit != '', 'Argument unit needs to be a non-empty string !'
        assert dtype is not None, 'Argument dtype must not be None !'
        if dtype is not None:
            assert isinstance(dtype, type), \
                'Argument dtype needs a valid, ideally numpy, datatype !'
        # ##MK::if value is not None:
        self.is_a = 'NXobject'
        self.is_attr = False  # if True indicates object is attribute
        self.doc = ''  # docstring
        self.name = name  # name of the field
        self.unit = unit  # not unit category but actual unit
        # use special values 'unitless' for NX_UNITLESS (e.g. 1) and
        # 'dimensionless' for NX_DIMENSIONLESS (e.g. 1m / 1m)
        self.dtype = dtype  # use np.dtype if possible
        if value is None or dtype is str:
            self.unit = 'unitless'
        if value is not None:
            self.value = value
        else:
            self.value = None
        # value should be a numpy scalar, tensor, or string if possible
        if 'is_attr' in kwargs.keys():
            assert isinstance(kwargs['is_attr'], bool), \
                'Kwarg is_attr needs to be a boolean !'
            self.is_attr = kwargs['is_attr']

    def print(self):
        """Report values."""
        print('name: ')
        print(str(self.name))
        print('unit:')
        print(str(self.unit))
        print('dtype: ')
        print(self.dtype)

# test = NxObject(name='test', unit='baud', dtype=np.uint32, value=32000)
# test.print()


class NxEmOperator:
    """An object representing an operator, typically a human."""

    def __init__(self, *args, **kwargs):
        self.name = NxObject()
        self.affiliation = NxObject()
        self.address = NxObject()
        self.email = NxObject()
        self.orcid = NxObject()
        self.telephone_number = NxObject()
        self.role = NxObject()
        self.social_media_name = NxObject()
        self.social_media_platform = NxObject()

    def report(self, prefix: str, template: dict) -> dict:
        """Copy data from self into template the appdef instance.

        Paths in template are prefixed by prefix and have to be compliant
        with the application definition.
        """
        template[prefix + "/address"] = self.address.value
        template[prefix + "/affiliation"] = self.affiliation.value
        template[prefix + "/email"] = self.email.value
        template[prefix + "/name"] = self.name.value
        template[prefix + "/orcid"] = self.orcid.value
        template[prefix + "/role"] = self.role.value
        template[prefix + "/social_media_name"] = self.social_media_name.value
        template[prefix + "/social_media_platform"] = self.social_media_platform.value
        template[prefix + "/telephone_number"] = self.telephone_number.value
        return template

# test = NxEmOperator()
# test.name.value = 'NOMAD OASIS'
# a = test.report("/ENTRY", {})


class NxEmSample:
    """An object representing a sample."""

    def __init__(self, *args, **kwargs):
        self.method = NxObject(value='experimental')
        self.name = NxObject()
        self.sample_history = NxObject()
        self.preparation_date = NxObject()
        self.short_title = NxObject()
        self.atom_types = NxObject(value=[])
        self.thickness = NxObject()
        self.description = NxObject()

    def report(self, prefix: str, template: dict) -> dict:
        """Copy data from self into template the appdef instance.

        Paths in template are prefixed by prefix and have to be compliant
        with the application definition.
        """
        template[prefix + "/method"] = self.method.value
        template[prefix + "/name"] = self.name.value
        template[prefix + "/sample_history"] = self.sample_history.value
        template[prefix + "/preparation_date"] = self.preparation_date.value
        template[prefix + "/short_title"] = self.short_title.value
        template[prefix + "/atom_types"] = self.atom_types.value
        template[prefix + "/thickness"] = self.thickness.value
        template[prefix + "/thickness/@units"] = self.thickness.unit
        template[prefix + "/description"] = self.description.value
        return template

# test = NxEmSample()


class NxAppDefHeader:
    """An object representing the typical header of nexus-fairmat appdefs."""

    def __init__(self, *args, **kwargs):
        self.version = NxObject(value=NX_EM_ADEF_VERSION,
                                is_attr=True)
        self.definition = NxObject(value=NX_EM_ADEF_NAME)
        self.experiment_identifier = NxObject()
        self.experiment_description = NxObject()
        self.start_time = NxObject()
        self.end_time = NxObject()
        self.program = NxObject(value=NX_EM_EXEC_NAME)
        self.program_version = NxObject(value=NX_EM_EXEC_VERSION,
                                        is_attr=True)
        self.experiment_documentation = NxObject()
        self.thumbnail = NxObject()
        self.thumbnail_type = NxObject()

    def report(self, prefix: str, template: dict) -> dict:
        """Copy data from self into template the appdef instance.

        Paths in template are prefixed by prefix and have to be compliant
        with the application definition.
        """
        template[prefix + "/@version"] = self.version.value
        template[prefix + "/definition"] = self.definition.value
        template[prefix + "/experiment_identifier"] \
            = self.experiment_identifier.value
        template[prefix + "/experiment_description"] \
            = self.experiment_description.value
        template[prefix + "/start_time"] = self.start_time.value
        template[prefix + "/end_time"] = self.end_time.value
        template[prefix + "/program"] = self.program.value
        template[prefix + "/program/@version"] = self.program_version.value
        template[prefix + "/experiment_documentation"] \
            = self.experiment_documentation.value
        template[prefix + "/thumbnail"] = self.thumbnail.value
        template[prefix + "/thumbnail/@type"] = self.thumbnail_type.value
        return template

# test = NxAppDefHeader()
