#!/usr/bin/env python3
"""Generic parser for loading electron microscopy data into NXem."""

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

# \\wsl.localhost\Ubuntu\home\mkuehbach\markus_archive\TESTING\nomad-parser-nexus\nexusparser\tools\dataconverter


from typing import Tuple, Any

import flatdict as fd

import yaml

import numpy as np

# from ase.data import atomic_numbers
# from ase.data import chemical_symbols

from nexusparser.tools.dataconverter.readers.base.reader import BaseReader
# from nexusparser.tools.dataconverter.readers.apm.utils.aptfim_io_apt6_reader \
#    import ReadAptFileFormat

# NEW ISSUE: move these globals and the assess function to utilities like


NX_EM_ADEF_NAME = 'NXem'
NX_EM_ADEF_VERSION = '50433d9039b3f33299bab338998acb5335cd8951'
# based on https://fairmat-experimental.github.io/nexus-fairmat-proposal
NX_EM_EXEC_NAME = 'dataconverter/reader/em.py'
NX_EM_EXEC_VERSION = 'add gitsha of parent repo automatically'


class EmUseCaseSelector:
    """Decision maker about what needs to be parsed given arbitrary input.

    Users might invoke this dataconverter with arbitrary input, no input, or
    too much input. The UseCaseSelector decide what to do in each case.
    """

    def __init__(self, file_paths: Tuple[str] = None, *args, **kwargs):
        """Initialize the class.

        dataset injects numerical data and metadata from an analysis.
        eln injects additional metadata and eventually numerical data.
        """
        self.case = {}
        self.is_valid = False
        self.supported_mime_types = ['bcf', 'yaml', 'yml']
        for mime_type in self.supported_mime_types:
            self.case[mime_type] = []
        for file_name in file_paths:
            index = file_name.lower().rfind('.')
            if index >= 0:
                suffix = file_name.lower()[index+1::]
                if suffix in self.supported_mime_types:
                    if file_name not in self.case[suffix]:
                        self.case[suffix].append(file_name)
        if len(self.case['bcf']) == 1:
            condition = len(self.case['yaml']) + len(self.case['yml'])
            if 0 <= condition and condition <= 1:
                self.is_valid = True
                self.micr = []
                for mime_type in ['bcf']:
                    self.micr += self.case[mime_type]
                self.eln = []
                for mime_type in ['yaml', 'yml']:
                    self.eln += self.case[mime_type]

# test = EmUseCaseSelector(('a.bcf', 'b.yaml', 'c.apt'))


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
        self.value = None
        if dtype is str:
            if value is None:
                self.value = 'unitless'
            else:
                self.value = value
        else:
            self.value = value  # make np scalar, tensor, string if possible
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


# test = NxObject(name='test', unit='baud', dtype=np.uint32, value=32000)


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


# test = NxAppDefHeader()


def hyperspy_parser(file_name: str, template: dict) -> dict:
    """Use hyperspy to parse content from electron microscopy files."""
    # ##MK::
    pass


def nomad_oasis_eln_parser(file_name: str, template: dict) -> dict:
    """Parse out output from a YAML file from a NOMAD OASIS YAML."""
    # ##MK::
    pass


def create_default_plottable_data(template: dict) -> dict:
    """For a valid NXS file at least one default plot is required."""
    # ##MK::
    pass


class EmReader(BaseReader):
    """Parse content from community file formats.

    Specifically, electron microscopy
    towards a NXem.nxdl-compliant NeXus file.
    """

    # pylint: disable=too-few-public-methods

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls = ["NXem"]

    def read(self,
             template: dict = None,
             file_paths: Tuple[str] = None,
             objects: Tuple[Any] = None) -> dict:
        """Read data from given file, return filled template dictionary."""
        case = EmUseCaseSelector(file_paths)
        assert case.is_valid is True, \
            'Such a combination of input-file if any is not supported !'

        # nx_em_header = NxAppDefHeader()

        # ##MK:: #####
        # report_appdef_version(template)

        print("Parsing numerical data and metadata with hyperspy...")
        if case.micr != []:
            hyperspy_parser(case.micr[0], template)
        else:
            print("No input-file defined for micr data !")
            return {}

        print("Parsing metadata as well as numerical data from NOMAD OASIS ELN...")
        if case.eln != []:
            nomad_oasis_eln_parser(case.eln[0], template)
        else:
            print("No input file defined for eln data !")

        print("Creating default plottable data...")
        create_default_plottable_data(template)

        # reporting of what has not been properly defined at the reader level
        print('\n\nDebugging...')
        for keyword in template.keys():
            # if template[keyword] is None:
            print(keyword + '...')
            print(template[keyword])
            # if template[keyword] is None:
            #     print("Entry: '" + keyword + " is not properly defined yet!")

        print("Forwarding the instantiated template to the NXS writer...")

        return template


# This has to be set to allow the convert script to use this reader.
READER = EmReader
