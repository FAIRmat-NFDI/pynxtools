#!/usr/bin/env python3
"""Generic parser for loading atom probe microscopy data into NXapm."""

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

import json

from typing import Tuple

import numpy as np

from nexusparser.tools.dataconverter.readers.base.reader import BaseReader
from nexusparser.tools.dataconverter.readers.apm.utils.aptfim_io_apt6_reader \
    import ReadAptFileFormat
from nexusparser.tools.dataconverter.readers.apm.utils.aptfim_io_pos_reader \
    import ReadPosFileFormat
from nexusparser.tools.dataconverter.readers.apm.utils.aptfim_io_epos_reader \
    import ReadEposFileFormat
from nexusparser.tools.dataconverter.readers.apm.utils.aptfim_io_rng_reader \
    import ReadRngFileFormat
from nexusparser.tools.dataconverter.readers.apm.utils.aptfim_io_rrng_reader \
    import ReadRrngFileFormat

# NEW ISSUE: move these globals and the assess function to utilities like

RECON_TYPES = ['pos', 'epos', 'apt']
RANGE_TYPES = ['rng', 'rrng']
ELAB_TYPES = ['json']

INVALID_INPUT = -1
SINGLE_RECON_SINGLE_RANGE = 0
# each reconstruction should be stored as an own file because for commercial
# atom probe microscopes it is currently impossible to get less processed data
# from the microscopes

# to be done: add support for SINGLE_RECON_MULTIPLE_RANGE


def assess_situation_with_input_files(file_paths: Tuple[str] = None) -> dict:
    """Different file formats contain different types of data.

    Identify how many files of specific type Tuple contains to judge if the
    input has at all a chance to populate all required fields of
    the application definition.

    """
    filetype_dict = {}
    for file_name in file_paths:
        index = file_name.lower().rfind('.')
        if index >= 0:
            suffix = file_name.lower()[index + 1::]
            if suffix in \
               RECON_TYPES + RANGE_TYPES + ELAB_TYPES:
                if suffix in filetype_dict.keys():
                    filetype_dict[suffix].append(file_name)
                else:
                    filetype_dict[suffix] = [file_name]
        # files without endings are ignored

    # identify which use case we face
    filetype_counts = {}
    for suffix, filenames in filetype_dict.items():
        filetype_counts[suffix] = len(filenames)

    number_of_reconstructions = 0
    number_of_rangingdefs = 0
    number_of_elab_metadata = 0
    for suffix, count in filetype_counts.items():
        if suffix in RECON_TYPES:
            number_of_reconstructions += count
        elif suffix in RANGE_TYPES:
            number_of_rangingdefs += count
        elif suffix in ELAB_TYPES:
            number_of_elab_metadata += count
        else:
            return (filetype_dict, INVALID_INPUT)

    if number_of_reconstructions == 1 \
        and number_of_rangingdefs == 1 \
            and number_of_elab_metadata == 1:
        return (filetype_dict, SINGLE_RECON_SINGLE_RANGE)

    return (filetype_dict, INVALID_INPUT)


def report_appdef_version(template: dict) -> dict:
    """Specify which application definition version is used."""
    template["/ENTRY[entry]/definition"] = "NXapm"
    template["/ENTRY[entry]/definition/@version"] = "1"

    return template


def extract_data_from_apt_file(file_name: str, template: dict) -> dict:
    """Add those required information which a APT file has."""
    print('Extracting data from APT file: ' + file_name)
    aptfile = ReadAptFileFormat(file_name)

    path_prefix = '/ENTRY[entry]/atom_probe/'
    xyz = aptfile.get_named_quantity('Position')
    template[path_prefix + 'reconstruction/reconstructed_positions'] \
        = xyz.value
    template[path_prefix + 'reconstruction/reconstructed_positions/@units'] \
        = xyz.unit

    m_z = aptfile.get_named_quantity('Mass')
    template[path_prefix + 'mass_to_charge_conversion/mass_to_charge'] \
        = m_z.value
    template[path_prefix + 'mass_to_charge_conversion/mass_to_charge/@units'] \
        = m_z.unit

    # all less explored optional branches in an APT6 file can also be already be accessed via the
    # aptfile.get_named_quantity function but it needs to be checked if this returns values

    return template


def extract_data_from_pos_file(file_name: str, template: dict) -> dict:
    """Add those required information which a POS file has."""
    print('Extracting data from POS file: ' + file_name)
    posfile = ReadPosFileFormat(file_name)

    path_prefix = '/ENTRY[entry]/atom_probe/'
    xyz = posfile.get_reconstructed_positions()
    template[path_prefix + 'reconstruction/reconstructed_positions'] \
        = xyz.value
    template[path_prefix + 'reconstruction/reconstructed_positions/@units'] \
        = xyz.unit

    m_z = posfile.get_mass_to_charge()
    template[path_prefix + 'mass_to_charge_conversion/mass_to_charge'] \
        = m_z.value
    template[path_prefix + 'mass_to_charge_conversion/mass_to_charge/@units'] \
        = m_z.unit

    return template


def extract_data_from_epos_file(file_name: str, template: dict) -> dict:
    """Add those required information which a POS file has."""
    print('Extracting data from EPOS file: ' + file_name)
    eposfile = ReadEposFileFormat(file_name)

    path_prefix = '/ENTRY[entry]/atom_probe/'
    xyz = eposfile.get_reconstructed_positions()
    template[path_prefix + 'reconstruction/reconstructed_positions'] \
        = xyz.value
    template[path_prefix + 'reconstruction/reconstructed_positions/@units'] \
        = xyz.unit

    m_z = eposfile.get_mass_to_charge()
    template[path_prefix + 'mass_to_charge_conversion/mass_to_charge'] \
        = m_z.value
    template[path_prefix + 'mass_to_charge_conversion/mass_to_charge/@units'] \
        = m_z.unit

    raw_tof = eposfile.get_raw_time_of_flight()
    template[path_prefix + 'voltage_and_bowl_correction/raw_tof'] \
        = raw_tof.value
    template[path_prefix + 'voltage_and_bowl_correction/raw_tof/@units'] \
        = raw_tof.unit

    # NEW ISSUE:ADD RECURSIVE LOADING OF BASE CLASSES
    # NEW ISSUE:ADD HANDLING OF OPTIONALITY OF GROUPS, FIELDS, ATTRIBUTES

    # dc_voltage = eposfile.get_standing_voltage()
    # template[path_prefix + 'laser_and_high_voltage_pulser/standing_voltage'] = dc_voltage.value
    # template[path_prefix + 'laser_and_voltage_pulser/standing_voltage/@units'] = dc_voltage.unit

    # pu_voltage = eposfile.get_pulse_voltage()
    # template[path_prefix \
    #    + 'laser_and_high_voltage_pulser/pulsed_voltage'] = pu_voltage.value
    # template[path_prefix \
    #    + 'laser_and_high_voltage_pulser/pulsed_voltage/@units'] = pu_voltage.unit

    hit_positions = eposfile.get_hit_positions()
    template[path_prefix + 'ion_impact_positions/hit_positions'] \
        = hit_positions.value
    template[path_prefix + 'ion_impact_positions/hit_positions/@units'] \
        = hit_positions.unit

    # little bit more discussion with e.g. F. M. M. at MPIE required
    # how to add these
    # npulses = eposfile.get_number_of_pulses()
    # ions_per_pulse = eposfile.get_ions_per_pulse()

    # pulser NXpulser_apm the problem is if members of these base
    # classes are not specified in the application definition
    # the converter currently ignores them

    return template


def configure_ranging_data(template: dict) -> dict:
    """Remove to be renamed entries with multiple occurrences."""
    # for keyword in template.keys():
    #     if keyword.find('ION[ion]') >= 0:
    #         del template[keyword]

    template['/ENTRY[entry]/atom_probe/ranging/maximum_number_of_atoms_per_molecular_ion'] \
        = np.uint32(32)

    return template


def extract_data_from_rng_file(file_name: str, template: dict) -> dict:
    """Add those required information which an RNG file has."""
    # modify the template to take into account ranging
    # ranging is currently not resolved recursively because
    # ranging(NXprocess) is a group which has a minOccurs=1, \
    #     maxOccurs="unbounded" set of possible named
    # NXion members, same case for more than one operator
    print('Extracting data from RNG file: ' + file_name)
    rangefile = ReadRngFileFormat(file_name)

    rangefile.read()

    # ion indices are on the interval [1, 256]
    assert len(rangefile.rng['ions'].keys()) <= np.iinfo(np.uint8).max + 1, \
        'Current implementation does not support more than 256 ion types'

    template['/ENTRY[entry]/atom_probe/ranging/number_of_iontypes'] \
        = np.uint8(len(rangefile.rng['ions'].keys()))

    ion_id = 1
    path_prefix = '/ENTRY[entry]/atom_probe/ranging/peak_identification/'
    for ion_obj in rangefile.rng['ions'].values():
        path_specifier = path_prefix + 'ION[ion' + str(ion_id) + ']/'

        template[path_specifier + 'ion_type'] \
            = np.uint8(ion_id)
        template[path_specifier + 'isotope_vector'] \
            = ion_obj.isotope_vector.value
        template[path_specifier + 'charge_state'] \
            = ion_obj.charge_state.value
        template[path_specifier + 'charge_state/@units'] \
            = ""  # NX_DIMENSIONLESS
        template[path_specifier + 'name'] \
            = ion_obj.name.value
        template[path_specifier + 'mass_to_charge_range'] \
            = ion_obj.ranges.value
        template[path_specifier + 'mass_to_charge_range/@units'] \
            = ion_obj.ranges.unit
        # charge_state and name is not included in rng rangefiles

        ion_id += 1

    return template


def extract_data_from_rrng_file(file_name: str, template: dict) -> dict:
    """Add those required information which an RRNG file has."""
    # modify the template to take into account ranging
    # ranging is currently not resolved recursively because
    # ranging(NXprocess) is a group which has a minOccurs=1, \
    #     maxOccurs="unbounded" set of possible named
    # NXion members, same case for more than one operator
    print('Extracting data from RRNG file: ' + file_name)
    rangefile = ReadRrngFileFormat(file_name)

    rangefile.read()

    # ion indices are on the interval [1, 256]
    assert len(rangefile.rrng['ions'].keys()) <= np.iinfo(np.uint8).max + 1, \
        'Current implementation does not support more than 256 ion types'

    template['/ENTRY[entry]/atom_probe/ranging/number_of_iontypes'] \
        = np.uint8(len(rangefile.rrng['ions'].keys()))

    ion_id = 1
    path_prefix = '/ENTRY[entry]/atom_probe/ranging/peak_identification/'
    for ion_obj in rangefile.rrng['ions'].values():
        path_specifier = path_prefix + 'ION[ion' + str(ion_id) + ']/'

        template[path_specifier + 'ion_type'] \
            = np.uint8(ion_id)
        template[path_specifier + 'isotope_vector'] \
            = ion_obj.isotope_vector.value
        template[path_specifier + 'charge_state'] \
            = ion_obj.charge_state.value
        template[path_specifier + 'charge_state/@units'] \
            = ""  # NX_DIMENSIONLESS
        template[path_specifier + 'name'] \
            = ion_obj.name.value
        template[path_specifier + 'mass_to_charge_range'] \
            = ion_obj.ranges.value
        template[path_specifier + 'mass_to_charge_range/@units'] \
            = ion_obj.ranges.unit
        # charge_state and name is not included in rrng rangefiles

        ion_id += 1

    return template


def extract_data_from_json_file(file_name: str, template: dict) -> dict:
    """Add those required information which a JSON file has."""
    # file_name = 'R31_06365-v02.ELabFTW.12.json'
    with open(file_name, 'r') as file_handle:
        jsn = json.load(file_handle)

    # use a translation dictionary to enable that the JSON dictionary
    # from the electronic lab notebook can have a different set of keywords

    for keyword, value in jsn.items():
        assert keyword in template.keys(), \
            print(keyword + ' is not a keyword in template!')
        template[keyword] = value

    return template


class ApmReader(BaseReader):
    """Parse content from community file formats.

    Specifically, local electrode atom probe microscopy
    towards a NXapm.nxdl-compliant NeXus file.

    """

    # pylint: disable=too-few-public-methods

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls = ["NXapm"]

    def read(self, template: dict = None,
             file_paths: Tuple[str] = None) -> dict:
        """Read data from given file, return filled template dictionary."""
        typed_files, case = assess_situation_with_input_files(file_paths)
        assert case > INVALID_INPUT, \
            'Each reconstruction should have only one \
                range file and an associated metadata file!'

        report_appdef_version(template)

        print('Add metadata which come from other sources...')
        if 'json' in typed_files.keys():
            assert len(typed_files['json']) == 1, \
                'List of json files is ambiguous!'
            extract_data_from_json_file(typed_files['json'][0], template)
        else:
            print('Unable to extract information from a lab notebook!')
            return {}

        print("Add (optional) vendor file data...")
        if 'apt' in typed_files.keys():
            assert len(typed_files['apt']) == 1, \
                'List of apt files is ambiguous!'
            extract_data_from_apt_file(typed_files['apt'][0], template)
        elif 'epos' in typed_files.keys():
            assert len(typed_files['epos']) == 1, \
                'List of epos files is ambiguous!'
            extract_data_from_epos_file(typed_files['epos'][0], template)
        elif 'pos' in typed_files.keys():
            assert len(typed_files['pos']) == 1, \
                'List of pos files is ambiguous!'
            extract_data_from_pos_file(typed_files['pos'][0], template)
        else:
            print('Unable to extract information from a reconstruction!')
            return {}

        print("Add (optional) ranging data...")
        configure_ranging_data(template)

        if 'rng' in typed_files.keys():
            assert len(typed_files['rng']) == 1, \
                'List of rng files is ambiguous!'
            extract_data_from_rng_file(typed_files['rng'][0], template)
        elif 'rrng' in typed_files.keys():
            assert len(typed_files['rrng']) == 1, \
                'List of rrng files is ambiguous!'
            extract_data_from_rrng_file(typed_files['rrng'][0], template)
        else:
            print('Unable to extract information from a range file!')
            return {}

        for keyword in template.keys():
            if template[keyword] is None:
                print("Entry: '" + keyword + " is not properly defined yet!")

        # delete_not_properly_handled_fields(template)
        # NEW ISSUE: these deleted fields should be handled during the
        # instantiation of the template, i.e. if ION[ion] is minOccur=0
        # the converter should not ask for this field to be present !

        # hot fixed for now suggesting to implement as a new issue
        # NEW ISSUE: implement a functionality to return NX data type information
        # at this reader level so that values of a certain type family, like NX_UINT
        # get transformed into the specific datatype, like uint32 or uint64 e.g.
        implicit_int_to_uint32 = [
        "/ENTRY[entry]/atom_probe/hit_multiplicity/hit_multiplicity",
        "/ENTRY[entry]/atom_probe/hit_multiplicity/pulses_since_last_ion",
        "/ENTRY[entry]/atom_probe/hit_multiplicity/pulse_id",
        "/ENTRY[entry]/atom_probe/ranging/peak_identification/ION[ion]/ion_type",
        "/ENTRY[entry]/atom_probe/ranging/peak_identification/ION[ion]/isotope_vector"]
        for entry in implicit_int_to_uint32:
            template[entry] = np.uint32(template[entry])

        return template


# This has to be set to allow the convert script to use this reader.
READER = ApmReader


# deprecated
# =============================================================================
# def delete_not_properly_handled_fields(template: dict) -> dict:
#     """Remove fields which are currently not properly handled by the converter."""
#     prefix = "/ENTRY[entry]/atom_probe/"
#     nxdl_paths = [
#         prefix + "ranging/peak_identification/ION[ion]/name",
#         prefix + "ranging/peak_identification/ION[ion]/charge_state",
#         prefix + "ranging/peak_identification/ION[ion]/charge_state/@units",
#         prefix + "ranging/peak_identification/ION[ion]/ion_type",
#         prefix + "ranging/peak_identification/ION[ion]/isotope_vector",
#         prefix + "ranging/peak_identification/ION[ion]/mass_to_charge_range",
#         prefix + "ranging/peak_identification/ION[ion]/mass_to_charge_range/@units",
#         prefix + "control_software/analysis_chamber/pressure",
#         prefix + "control_software/analysis_chamber/pressure/@units",
#         prefix + "hit_multiplicity/hit_multiplicity",
#         prefix + "hit_multiplicity/pulses_since_last_ion",
#         prefix + "ion_impact_positions/hit_positions",
#         prefix + "ion_impact_positions/hit_positions/@units",
#         prefix + "laser_or_high_voltage_pulser/pulsed_voltage",
#         prefix + "laser_or_high_voltage_pulser/pulsed_voltage/@units",
#         prefix + "laser_or_high_voltage_pulser/standing_voltage",
#         prefix + "laser_or_high_voltage_pulser/standing_voltage/@units",
#         prefix + "voltage_and_bowl_correction/calibrated_tof/@units",
#         prefix + "voltage_and_bowl_correction/raw_tof",
#         prefix + "voltage_and_bowl_correction/raw_tof/@units"]
#
#     for path in nxdl_paths:
#         assert path in template.keys(), \
#             "nxdl_path: " + path + " is not a key in template!"
#         template.pop(path, None)
#
#     # NEW ISSUE: remove also these fields in the future they are redundant for peak_identification
#     prefix = "/ENTRY[entry]/atom_probe/"
#     nxdl_paths = [
#         prefix + "ranging/peak_search_and_deconvolution/PEAK[peak]/intensity",
#         prefix + "ranging/peak_search_and_deconvolution/PEAK[peak]/intensity/@units",
#         prefix + "ranging/peak_search_and_deconvolution/PEAK[peak]/label",
#         prefix + "ranging/peak_search_and_deconvolution/PEAK[peak]/peak_model",
#         prefix + "ranging/peak_search_and_deconvolution/PEAK[peak]/position",
#         prefix + "ranging/peak_search_and_deconvolution/PEAK[peak]/position/@units"]
#
#     for path in nxdl_paths:
#         assert path in template.keys(), \
#             "nxdl_path: " + path + " is not a key in template!"
#         template.pop(path, None)
#
#     return template
# =============================================================================
