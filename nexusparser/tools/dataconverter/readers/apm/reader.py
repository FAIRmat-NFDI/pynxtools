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

from typing import Tuple, Any

import flatdict as fd

import yaml

import numpy as np

# from ase.data import atomic_numbers
from ase.data import chemical_symbols

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
ELAB_TYPES = ['yaml']

INVALID_INPUT = -1
SINGLE_RECON_SINGLE_RANGE = 0
# each reconstruction should be stored as an own file because for commercial
# atom probe microscopes it is currently impossible to get less processed data
# from the microscopes

# to be done: add support for SINGLE_RECON_MULTIPLE_RANGE


def get_dct_value(flat_dict: fd.FlatDict, keyword_path: str):
    """Extract value from a dict nest under keyword_path."""
    # keyword_path = 'NXapm/entry/specimen/name'  #'/name'
    # keyword_path = 'NXapm/entry/atom_probe/pulser/pulse_frequency/value'
    # dct = yml
    # print(keyword_path)
    is_leaf = (keyword_path in flat_dict.keys()) \
        & (isinstance(flat_dict[keyword_path], fd.FlatDict) is False)
    if is_leaf is True:
        return flat_dict[keyword_path]
    return None


def assess_situation_with_input_files(file_paths: Tuple[str] = None) -> Tuple[dict, int]:
    """Different file formats contain different types of data.

    Identify how many files of specific type Tuple contains to judge if the
    input has at all a chance to populate all required fields of
    the application definition.

    """
    filetype_dict: dict = {}
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
    template["/ENTRY[entry]/@version"] \
        = "NeXus Code Camp 2022 NXapm.yaml and NXapm.nxdl.xml"
    template["/ENTRY[entry]/definition"] = "NXapm"
    return template


def extract_data_from_apt_file(file_name: str, template: dict) -> dict:
    """Add those required information which a APT file has."""
    print('Extracting data from APT file: ' + file_name)
    aptfile = ReadAptFileFormat(file_name)

    trg = '/ENTRY[entry]/atom_probe/reconstruction/'
    xyz = aptfile.get_named_quantity('Position')
    template[trg + 'reconstructed_positions'] = np.array(xyz.value, np.float32)
    template[trg + 'reconstructed_positions/@units'] = xyz.unit
    del xyz

    trg = '/ENTRY[entry]/atom_probe/mass_to_charge_conversion/'
    m_z = aptfile.get_named_quantity('Mass')
    template[trg + 'mass_to_charge'] = np.array(m_z.value, np.float32)
    template[trg + 'mass_to_charge/@units'] = m_z.unit
    del m_z

    # all less explored optional branches in an APT6 file can also already
    # be accessed via the aptfile.get_named_quantity function
    # but it needs to be checked if this returns values as these are
    # optional quantities with apt files
    return template


def extract_data_from_pos_file(file_name: str, template: dict) -> dict:
    """Add those required information which a POS file has."""
    print('Extracting data from POS file: ' + file_name)
    posfile = ReadPosFileFormat(file_name)

    trg = '/ENTRY[entry]/atom_probe/reconstruction/'
    xyz = posfile.get_reconstructed_positions()
    template[trg + 'reconstructed_positions'] = np.array(xyz.value, np.float32)
    template[trg + 'reconstructed_positions/@units'] = xyz.unit
    del xyz

    trg = '/ENTRY[entry]/atom_probe/mass_to_charge_conversion/'
    m_z = posfile.get_mass_to_charge()
    template[trg + 'mass_to_charge'] = np.array(m_z.value, np.float32)
    template[trg + 'mass_to_charge/@units'] = m_z.unit
    del m_z
    return template


def extract_data_from_epos_file(file_name: str, template: dict) -> dict:
    """Add those required information which a POS file has."""
    print('Extracting data from EPOS file: ' + file_name)
    eposfile = ReadEposFileFormat(file_name)

    trg = '/ENTRY[entry]/atom_probe/reconstruction/'
    xyz = eposfile.get_reconstructed_positions()
    template[trg + 'reconstructed_positions'] = np.array(xyz.value, np.float32)
    template[trg + 'reconstructed_positions/@units'] = xyz.unit
    del xyz

    trg = '/ENTRY[entry]/atom_probe/mass_to_charge_conversion/'
    m_z = eposfile.get_mass_to_charge()
    template[trg + 'mass_to_charge'] = np.array(m_z.value, np.float32)
    template[trg + 'mass_to_charge/@units'] = m_z.unit
    del m_z

    # there are inconsistencies in the literature as to which units these
    # quantities have, so we skip exporting the following quantities for now
    # -->
    # trg = '/ENTRY[entry]/atom_probe/voltage_and_bowl_correction/'
    # raw_tof = eposfile.get_raw_time_of_flight()
    # template[trg + 'raw_tof'] = raw_tof.value
    # template[trg + 'raw_tof/@units'] = raw_tof.unit
    # # this somehow calibrated ToF is not available from an EPOS file
    # template[trg + 'calibrated_tof'] = raw_tof.value
    # template[trg + 'calibrated_tof/@units'] = raw_tof.unit
    # # is this really a raw ToF, if so, raw wrt to what?
    # # needs clarification from Cameca/AMETEK how this is internally computed
    # # especially when scientists write APT files and transcode them
    # # to EPOS using APSuite
    # del raw_tof

    # trg = '/ENTRY[entry]/atom_probe/pulser/'
    # dc_voltage = eposfile.get_standing_voltage()
    # template[trg + 'standing_voltage'] = dc_voltage.value
    # template[trg + 'standing_voltage/@units'] = dc_voltage.unit
    # del dc_voltage

    # pu_voltage = eposfile.get_pulse_voltage()
    # template[trg + 'pulsed_voltage'] = pu_voltage.value
    # template[trg + 'pulsed_voltage/@units'] = pu_voltage.unit
    # del pu_voltage

    # trg = '/ENTRY[entry]/atom_probe/ion_impact_positions/'
    # hit_positions = eposfile.get_hit_positions()
    # template[trg + 'hit_positions'] = hit_positions.value
    # template[trg + 'hit_positions/@units'] = hit_positions.unit
    # del hit_positions

    # trg = '/ENTRY[entry]/atom_probe/hit_multiplicity/'
    # # little bit more discussion with e.g. F. M. M. at MPIE required

    # # currently npulses is 'number of pulses since last event detected'
    # npulses = eposfile.get_number_of_pulses()
    # template[trg + 'hit_multiplicity'] = npulses.value
    # template[trg + 'hit_multiplicity/@units'] = npulses.unit
    # del npulses

    # ions_per_pulse = eposfile.get_ions_per_pulse()
    # # currently ions_per_pulse is 'ions per pulse, 0 after the first ion'
    # template[trg + 'pulses_since_last_ion'] = ions_per_pulse.value
    # template[trg + 'pulses_since_last_ion/@units'] \
    # = ions_per_pulse.unit
    # del ions_per_pulse
    # -->

    return template


def configure_ranging_data(template: dict) -> dict:
    """Remove to be renamed entries with multiple occurrences."""
    # for keyword in template.keys():
    #     if keyword.find('ION[ion]') >= 0:
    #         del template[keyword]

    # resolve the next two program references more informatively
    trg = "/ENTRY[entry]/atom_probe/ranging/"
    template[trg + "program"] \
        = "unclear, not documented in range files"
    template[trg + "program/@version"] \
        = "unclear, not documented in range files"

    template[trg + "peak_identification/program"] \
        = "unclear, not documented in range files"
    template[trg + "peak_identification/program/@version"] \
        = "unclear, not documented in range files"

    path_specifier = trg + "peak_identification/ION[ion0]/"
    template[path_specifier + 'isotope_vector'] \
        = np.reshape(np.asarray(([0] * 32), np.uint16), (1, 32))
    template[path_specifier + 'isotope_vector/@units'] \
        = "NX_UNITLESS"
    template[path_specifier + 'charge_state'] \
        = np.uint8(0)  # unsigned deprecated should become np.int8
    template[path_specifier + 'charge_state/@units'] \
        = 'NX_DIMENSIONLESS'
    template[path_specifier + 'mass_to_charge_range'] \
        = np.reshape(np.asarray([0.0, 0.001], np.float32), (1, 2))
    template[path_specifier + 'mass_to_charge_range/@units'] \
        = "Da"

    template[trg + "maximum_number_of_atoms_per_molecular_ion"] \
        = np.uint32(32)
    template[trg + 'maximum_number_of_atoms_per_molecular_ion/@units'] \
        = 'NX_UNITLESS'
    # for RNG and RRNG range file it is anyway unclear where they come
    # because neither the range file has no reference to its origin
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

    rangefile.read_rng()

    # ion indices are on the interval [1, 256]
    assert len(rangefile.rng['ions'].keys()) <= np.iinfo(np.uint8).max + 1, \
        'Current implementation does not support more than 256 ion types'

    trg = '/ENTRY[entry]/atom_probe/ranging/'
    template[trg + 'number_of_ion_types'] \
        = np.int32(len(rangefile.rng['ions'].keys()))
    template[trg + 'number_of_ion_types/@units'] = 'NX_UNITLESS'

    ion_id = 1
    trg = '/ENTRY[entry]/atom_probe/ranging/peak_identification/'
    for ion_obj in rangefile.rng['ions'].values():
        path_specifier = trg + 'ION[ion' + str(ion_id) + ']/'

        template[path_specifier + 'isotope_vector'] \
            = np.array(ion_obj.isotope_vector.value, np.uint16)
        template[path_specifier + 'isotope_vector/@units'] \
            = 'NX_UNITLESS'
        template[path_specifier + 'charge_state'] \
            = np.uint8(ion_obj.charge_state.value)
        # unsigned deprecated will become int32
        template[path_specifier + 'charge_state/@units'] \
            = 'NX_DIMENSIONLESS'
        template[path_specifier + 'mass_to_charge_range'] \
            = np.array(ion_obj.ranges.value, np.float32)
        template[path_specifier + 'mass_to_charge_range/@units'] \
            = ion_obj.ranges.unit
        # template[path_specifier + 'ion_type'] = np.uint8(ion_id)
        # template[path_specifier + 'name'] = ion_obj.name.value
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

    rangefile.read_rrng()

    # ion indices are on the interval [1, 256]
    assert len(rangefile.rrng['ions'].keys()) <= np.iinfo(np.uint8).max + 1, \
        'Current implementation does not support more than 256 ion types'

    trg = '/ENTRY[entry]/atom_probe/ranging/'
    template[trg + "number_of_ion_types"] \
        = np.int32(len(rangefile.rrng['ions'].keys()))
    template[trg + "number_of_ion_types/@units"] = 'NX_UNITLESS'

    ion_id = 1
    trg = '/ENTRY[entry]/atom_probe/ranging/peak_identification/'
    for ion_obj in rangefile.rrng['ions'].values():
        path_specifier = trg + 'ION[ion' + str(ion_id) + ']/'

        template[path_specifier + 'isotope_vector'] \
            = np.array(ion_obj.isotope_vector.value, np.uint16)
        template[path_specifier + 'isotope_vector/@units'] \
            = 'NX_UNITLESS'
        template[path_specifier + 'charge_state'] \
            = np.uint8(ion_obj.charge_state.value)
        # unsigned deprecated will become int32
        template[path_specifier + 'charge_state/@units'] \
            = 'NX_DIMENSIONLESS'
        template[path_specifier + 'mass_to_charge_range'] \
            = np.array(ion_obj.ranges.value, np.float32)
        template[path_specifier + 'mass_to_charge_range/@units'] \
            = ion_obj.ranges.unit
        # template[path_specifier + 'ion_type'] = np.uint8(ion_id)
        # template[path_specifier + 'name'] = ion_obj.name.value
        # charge_state and name is not included in rrng rangefiles
        ion_id += 1

    return template


# =============================================================================
# def extract_data_from_json_file(file_name: str, template: dict) -> dict:
#     """Add those required information which a JSON file has."""
#     # file_name = 'R31_06365-v02.ELabFTW.12.json'
#     with open(file_name, 'r') as file_handle:
#         jsn = json.load(file_handle)
#
#     # use a translation dictionary to enable that the JSON dictionary
#     # from the electronic lab notebook can have a different set of keywords
#
#     for keyword, value in jsn.items():
#         assert keyword in template.keys(), \
#             print(keyword + ' is not a keyword in template!')
#         template[keyword] = value
#
#     return template
# =============================================================================

def parse_entry_section(yml: fd.FlatDict, template: dict) -> dict:
    """Add (metadata) in the entry section."""
    trg = "/ENTRY[entry]/"
    msg = "NeXus 2022.06 commitID d9574a8f90626a929c677f1505729d1751170989 NXapm"
    assert yml["entry:attr_version"] == msg, \
        "Facing an ELN schema instance which is inconsistent with NXapm!"
    assert yml["entry:definition"] == "NXapm", \
        "Facing an ELN schema instance which is inconsistent with NXapm!"

    src = "entry"
    template[trg + "operation_mode"] \
        = get_dct_value(yml, src + ":operation_mode")
    template[trg + "program"] \
        = get_dct_value(yml, src + ":program")
    template[trg + "program/@version"] \
        = get_dct_value(yml, src + ":program__attr_version")
    template[trg + "run_number"] \
        = get_dct_value(yml, src + ":run_number")
    template[trg + "start_time"] \
        = get_dct_value(yml, src + ":start_time")
    template[trg + "experiment_identifier"] \
        = get_dct_value(yml, src + ":experiment_identifier")
    return template


def parse_operator_section(yml: fd.FlatDict, template: dict) -> dict:
    """Add (meta)data in the operator section."""
    src = "operator"
    assert isinstance(yml[src], list), \
        "Facing an ELN schema instance with an incorrect operator section!"
    assert len(yml[src]) >= 1, \
        "Facing an ELN schema instance with an empty operator section!"
    # there is a bug in NXapm, it should not be operator but NXuser
    # USER(NXuser) therefore we need to overwrite for now
    # and take only the first entry
    trg = "/ENTRY[entry]/operator/"
    template[trg + "name"] = yml[src][0]["name"]
    template[trg + "email"] = yml[src][0]["email"]
    # operator_id = 1
    # for operator in yml[src]:
    #     trg = "/ENTRY[entry]/operator_" + str(operator_id)
    #     template[trg + "/name"] = operator["name"]
    #     template[trg + "/email"] = operator["email"]
    #     operator_id += 1
    return template


def parse_specimen_section(yml: fd.FlatDict, template: dict) -> dict:
    """Add (meta)data in the specimen section."""
    src = "specimen"
    assert isinstance(yml[src + ":atom_types"], list), \
        "Facing an ELN schema instance with an incorrect atom_types info!"
    assert len(yml[src + ":atom_types"]) >= 1, \
        "Facing an ELN schema instance with an empty atom_types info!"
    for symbol in yml[src + ":atom_types"]:
        assert isinstance(symbol, str), \
            "Facing an atom_types list entry which is not a string!"
        assert (symbol in chemical_symbols) & (symbol != 'X'), \
            "Facing an atom_types list entry which is an element symbol!"
    trg = "/ENTRY[entry]/specimen/"
    template[trg + "atom_types"] = yml[src + ":atom_types"]
    template[trg + "name"] \
        = get_dct_value(yml, src + ":name")
    template[trg + "preparation_date"] \
        = get_dct_value(yml, src + ":preparation_date")
    template[trg + "sample_history"] \
        = get_dct_value(yml, src + ":sample_history")
    return template


def parse_reconstruction_section(yml: fd.FlatDict, template: dict) -> dict:
    """Add (meta)data in the reconstruction section."""
    src = "reconstruction"
    trg = "/ENTRY[entry]/atom_probe/reconstruction/"
    template[trg + "program"] \
        = get_dct_value(yml, src + ":program")
    template[trg + "program/@version"] \
        = get_dct_value(yml, src + ":program__attr_version")

    trg = "/ENTRY[entry]/atom_probe/voltage_and_bowl_correction/"
    # if template[trg + "calibrated_tof"] is not None:

    template[trg + "program"] \
        = get_dct_value(yml, src + ":program")
    template[trg + "program/@version"] \
        = get_dct_value(yml, src + ":program__attr_version")
    template[trg + "calibrated_tof"] \
        = np.asarray([0.0], np.float32)
    template[trg + "calibrated_tof/@units"] \
        = "s"
    return template


def parse_ranging_section(yml: fd.FlatDict, template: dict) -> dict:
    """Add (meta)data in the ranging section."""
    src = "ranging"
    trg = "/ENTRY[entry]/atom_probe/ranging/"
    # if template[trg + "maximum_number_of_atoms_per_molecular_ion"] is not None:

    template[trg + "program"] \
        = get_dct_value(yml, src + ":program")
    template[trg + "program/@version"] \
        = get_dct_value(yml, src + ":program__attr_version")

    # will the tool throw if there are no ranges?
    src = "ranging"
    trg = "/ENTRY[entry]/atom_probe/ranging/peak_identification/"
    template[trg + "program"] \
        = get_dct_value(yml, src + ":program")
    template[trg + "program/@version"] \
        = get_dct_value(yml, src + ":program__attr_version")
    src = "ranging"
    trg = "/ENTRY[entry]/atom_probe/ranging/background_quantification/"
    template[trg + "program"] \
        = get_dct_value(yml, src + ":program")
    template[trg + "program/@version"] \
        = get_dct_value(yml, src + ":program__attr_version")
    src = "ranging"
    trg = "/ENTRY[entry]/atom_probe/ranging/peak_search_and_deconvolution/"
    template[trg + "program"] \
        = get_dct_value(yml, src + ":program")
    template[trg + "program/@version"] \
        = get_dct_value(yml, src + ":program__attr_version")

    return template


def parse_instrument_section(yml: fd.FlatDict, template: dict) -> dict:
    """Parse (meta)data of the atom_probe instrument section."""
    src = "atom_probe"
    trg = "/ENTRY[entry]/atom_probe/"
    if "atom_probe:reflectron_applied" not in yml.keys():
        template[trg + "REFLECTRON[reflectron]/applied"] = False
    else:
        template[trg + "REFLECTRON[reflectron]/applied"] = True
    template[trg + "STAGE_LAB[stage_lab]/base_temperature"] \
        = np.float32(get_dct_value(yml, src + ":stage_lab_base_temperature:value"))
    template[trg + "STAGE_LAB[stage_lab]/base_temperature/@units"] \
        = get_dct_value(yml, src + ":stage_lab_base_temperature:unit")
    template[trg + "flight_path_length"] \
        = np.float32(get_dct_value(yml, src + ":flight_path_length:value"))
    template[trg + "flight_path_length/@units"] \
        = get_dct_value(yml, src + ":flight_path_length:unit")
    template[trg + "instrument_name"] \
        = get_dct_value(yml, src + ":instrument_name")
    template[trg + "ion_detector/type"] \
        = get_dct_value(yml, src + ":ion_detector_type")
    template[trg + "ion_detector/name"] \
        = get_dct_value(yml, src + ":ion_detector_name")
    template[trg + "local_electrode/name"] \
        = get_dct_value(yml, src + ":local_electrode_name")

    src = "atom_probe"
    trg = "/ENTRY[entry]/atom_probe/ion_impact_positions/"
    template[trg + "detection_rate"] = np.float32(
        get_dct_value(yml, src + ":ion_impact_positions_detection_rate"))
    template[trg + "detection_rate/@units"] = "NX_DIMENSIONLESS"

    src = "atom_probe"
    trg = "/ENTRY[entry]/atom_probe/specimen_monitoring/"
    template[trg + "initial_radius"] = np.float32(
        get_dct_value(yml, src + ":specimen_monitoring_initial_radius:value"))
    template[trg + "initial_radius/@units"] \
        = get_dct_value(yml, src + ":specimen_monitoring_initial_radius:unit")
    template[trg + "shank_angle"] = np.float32(
        get_dct_value(yml, src + ":specimen_monitoring_shank_angle:value"))
    template[trg + "shank_angle/@units"] \
        = get_dct_value(yml, src + ":specimen_monitoring_shank_angle:unit")

    src = "atom_probe"
    trg = "/ENTRY[entry]/atom_probe/control_software/analysis_chamber/"
    template[trg + "pressure"] = np.float32(
        get_dct_value(yml, src + ":analysis_chamber_pressure:value"))
    template[trg + "pressure/@units"] \
        = get_dct_value(yml, src + ":analysis_chamber_pressure:unit")

    src = "control_software"
    trg = "/ENTRY[entry]/atom_probe/"
    template[trg + "program"] \
        = get_dct_value(yml, src + ":program")
    template[trg + "program/@version"] \
        = get_dct_value(yml, src + ":program__attr_version")

    src = "atom_probe:pulser"
    trg = "/ENTRY[entry]/atom_probe/pulser/"
    template[trg + "pulse_fraction"] \
        = np.float32(get_dct_value(yml, src + ":pulse_fraction"))
    template[trg + "pulse_fraction/@units"] \
        = "NX_DIMENSIONLESS"
    template[trg + "pulse_frequency"] \
        = np.float32(get_dct_value(yml, src + ":pulse_frequency:value"))
    template[trg + "pulse_frequency/@units"] \
        = get_dct_value(yml, src + ":pulse_frequency:unit")
    template[trg + "pulse_mode"] \
        = get_dct_value(yml, src + ":pulse_mode")
    # pulsed voltage should not be required
    if template[trg + "pulsed_voltage"] is None:
        print('Setting pulsed_voltage not specified by vendor!')
        template[trg + "pulsed_voltage"] \
            = np.asarray([0.0], np.float32)
        template[trg + "pulsed_voltage/@units"] = "V"

    return template


def parse_analysis_workflow_section(template: dict) -> dict:
    """Add additional fields related to NXprocess analysis steps."""
    # hit_positions are not part of POS, EPOS, or APT files but a required
    trg = "/ENTRY[entry]/atom_probe/hit_multiplicity/"
    # data_available = (template[trg + "pulses_since_last_ion"] is not None) \
    #     | (template[trg + "hit_multiplicity"] is not None) \
    #     | (template[trg + "pulse_id"] is not None)
    template[trg + "program"] \
        = "possibly the control_software"
    template[trg + "program/@version"] \
        = "possibly the one of the control software"

    trg = "/ENTRY[entry]/atom_probe/ion_impact_positions/"
    if template[trg + "hit_positions"] is None:
        print('Setting hit_positions not specified by vendor!')
        template[trg + "hit_positions"] \
            = np.asarray([0.0, 0.0], np.float32)
        template[trg + "hit_positions/@units"] = "cm"
        # resolve this conflict, when one just gives
        # POS, ePOS or apt files it is not clear how the
        # impact positions where computed
        # assume for now it was the control software
    template[trg + "program"] \
        = "possibly the control_software"
    template[trg + "program/@version"] \
        = "possibly the one of the control software"

    # src = "NXapm/entry/atom_probe/mass_to_charge_conversion/"
    trg = "/ENTRY[entry]/atom_probe/mass_to_charge_conversion/"
    # resolve where this these two fields are best populated
    template[trg + "program"] \
        = "possibly the control software"
    template[trg + "program/@version"] \
        = "possibly the one of the control software"
    return template


def extract_data_from_yaml_file(file_name: str, template: dict) -> dict:
    """Add (meta)data from YAML file e.g. nomadOASIS APM ELN."""
    # it is planned that the ELN and NeXus application definition schemata
    # will eventually merge into one. In this case and also in general
    # making a data artifact to comply with an application definition
    # demands that required groups/field/attribute need to optional one
    # may be filled and end in the NeXus file
    # therefore, in order to match these constraints of a specific appdef
    # like NXapm (here implemented) demands that the required entries are
    # in the yaml, if they cannot be filled by vendor files
    # (pos, epos, apt, rng, rrng)
    # when the ELN and NeXus appdef schema syntax have been harmonized
    # the same keywords will be used. So it is possible that the function
    # here just parses specific (eventually nested) keyword, values from
    # the ELN yaml file, as in this case anyway all content in a yaml file
    # that is not also available in the appdef will be ignored

    # given that the syntax for nomadOASIS ELN and NeXus schemata is
    # as of 2022/06/28 not yet fully harmonized plus we dont want
    # to create an extra blocker in sprint 8, we carry the values hardcoded
    file_name = 'eln_data.yaml'
    with open(file_name, 'r') as stream:
        yml = fd.FlatDict(yaml.safe_load(stream), delimiter=':')

    parse_entry_section(yml, template)
    parse_operator_section(yml, template)
    parse_specimen_section(yml, template)
    parse_instrument_section(yml, template)
    parse_analysis_workflow_section(template)
    parse_reconstruction_section(yml, template)
    parse_ranging_section(yml, template)
    return template


def create_default_plottable_data_reconstruction(template: dict) -> dict:
    """Compute on-the-fly, add, and give path to discretized reconstruction."""
    trg = "/ENTRY[entry]/atom_probe/reconstruction"
    xyz = template[trg + "/reconstructed_positions"]

    print('--> Enter histogram computation ')
    print(np.shape(xyz))

    resolution = 1.0  # in nm
    bounds = np.zeros([3, 2], np.float32)  # in nm
    for i in np.arange(0, 3):
        bounds[i, 0] = np.min(xyz[:, i])
        bounds[i, 1] = np.max(xyz[:, i])
    # make the bounding box a quadric prism
    xymax = np.ceil(np.max(np.array(
        np.fabs(bounds[0:1, 0])[0],
        np.fabs(bounds[0:1, 1])[0])))
    zmin = np.floor(bounds[2, 0])
    zmax = np.ceil(bounds[2, 1])

    xedges = np.linspace(-1.0 * xymax, +1.0 * xymax,
                         num=int(np.ceil(2.0 * xymax / resolution)) + 1,
                         endpoint=True)
    # for debugging correct cuboidal storage order make prism a cuboid
    # yedges = np.linspace(-9 + -1.0 * xymax, +9 + +1.0 * xymax,
    #                      num=int(np.ceil((+9 +xymax - (-xymax -9))
    #                                      / resolution))+1,
    #                      endpoint=True)
    yedges = xedges
    zedges = np.linspace(zmin, zmax,
                         num=int(np.ceil((zmax - zmin) / resolution)) + 1,
                         endpoint=True)

    hist3d = np.histogramdd((xyz[:, 0], xyz[:, 1], xyz[:, 2]),
                            bins=(xedges, yedges, zedges))
    del xyz
    assert isinstance(hist3d[0], np.ndarray), \
        'Hist3d computation from the reconstruction failed!'
    assert len(np.shape(hist3d[0])) == 3, \
        'Hist3d computation from the reconstruction failed!'
    for i in np.arange(0, 3):
        assert np.shape(hist3d[0])[i] > 0, \
            'Dimensions ' + str(i) + ' has no length!'

    trg = "/ENTRY[entry]/atom_probe/reconstruction/"
    trg += "naive_point_cloud_density_map/"
    template[trg + "program"] \
        = "nomad-parser-nexus/apm/reader.py"
    template[trg + "program/@version"] \
        = "Add current GitCommit message"  # NEW ISSUE

    trg += "DATA[data]/"
    template[trg + "@signal"] = "counts"
    template[trg + "@axes"] = ["xpos", "ypos", "zpos"]
    # mind that histogram does not follow Cartesian conventions so a transpose
    # might be necessary, for now we implement the transpose in the appdef

    template[trg + "counts"] = np.array(hist3d[0], np.uint32)
    template[trg + "counts/@units"] = "NX_UNITLESS"
    template[trg + "xpos"] = np.array(hist3d[1][0][1::], np.float32)
    template[trg + "xpos/@units"] = "nm"
    template[trg + "@xpos_indices"] = 0  # "my x axis"
    template[trg + "ypos"] = np.array(hist3d[1][1][1::], np.float32)
    template[trg + "ypos/@units"] = "nm"
    template[trg + "@ypos_indices"] = 1  # "my y axis"
    template[trg + "zpos"] = np.array(hist3d[1][2][1::], np.float32)
    template[trg + "zpos/@units"] = "nm"
    template[trg + "@zpos_indices"] = 2  # "my z axis"
    template[trg + "@long_name"] = "hist3d tomographic reconstruction"
    print('Default plot 3D discretized reconstruction at 1nm binning.')
    del hist3d

    return template


def create_default_plottable_data_mass_spectrum(template: dict) -> dict:
    """Compute on-the-fly, add, and give path to discretized reconstruction."""
    trg = "/ENTRY[entry]/atom_probe/mass_to_charge_conversion/"
    m_z = template[trg + "mass_to_charge"]

    print('--> Enter mass spectrum computation ')
    print(np.shape(m_z))

    mqmin = 0.0  # in Da, do not plot unphysical values < 0.0
    mqmax = np.ceil(np.max(m_z[:]))
    mqincr = 0.01  # in Da by default

    hist1d = np.histogram(
        m_z[:],
        np.linspace(mqmin, mqmax,
                    num=int(np.ceil((mqmax - mqmin) / mqincr)) + 1,
                    endpoint=True))
    del m_z
    assert isinstance(hist1d[0], np.ndarray), \
        'Hist1d computation from the mass spectrum failed!'
    assert len(np.shape(hist1d[0])) == 1, \
        'Hist1d computation from the mass spectrum failed!'
    for i in np.arange(0, 1):
        assert np.shape(hist1d[0])[i] > 0, \
            'Dimensions ' + str(i) + ' has no length!'

    trg = "/ENTRY[entry]/atom_probe/ranging/"
    trg += "mass_to_charge_distribution/"
    template[trg + "program"] \
        = "nomad-parser-nexus/apm/reader.py"
    template[trg + "program/@version"] \
        = "Add current GitCommit message"  # NEW ISSUE

    template[trg + "range_increment"] = mqincr
    template[trg + "range_increment/@units"] = "Da"
    template[trg + "range_minmax"] \
        = np.array([mqmin, mqmax], np.float32)
    template[trg + "range_minmax/@units"] = "Da"

    trg += "mass_spectrum/"
    template[trg + "@signal"] = "counts"
    template[trg + "@axes"] = "bin_ends"
    template[trg + "counts"] = np.array(hist1d[0], np.uint32)
    template[trg + "counts/@units"] = "NX_UNITLESS"
    template[trg + "@long_name"] = "hist1d mass-to-charge-state ratios"
    template[trg + "bin_ends"] = np.array(hist1d[1][1::], np.float32)
    template[trg + "bin_ends/@units"] = "Da"
    template[trg + "@bin_ends_indices"] = 0
    print('Plot mass spectrum at 0.01Da binning was created.')
    del hist1d

    return template


def create_default_plottable_data(template: dict) -> dict:
    """Compute on-the-fly, add, and give path to default plottable data."""
    print('Create default plots on-the-fly...')
    # now the reader implements what is effectively the task of a normalizer step
    # adding plot (discretized representation of the dataset), for now the default plot
    # adding plot mass-to-charge-state ratio histogram, termed mass spectrum in APM community

    # NEW ISSUE: add path to default plottable data

    # check if reconstructed ion positions have been stored
    trg = "/ENTRY[entry]/atom_probe/reconstruction/"
    has_valid_xyz = False
    if isinstance(template[trg + "reconstructed_positions"],
                  np.ndarray):
        has_valid_xyz = True

    trg = "/ENTRY[entry]/atom_probe/mass_to_charge_conversion/"
    has_valid_m_z = False
    if isinstance(template[trg + "mass_to_charge"], np.ndarray):
        has_valid_m_z = True

    has_default_data = has_valid_xyz | has_valid_m_z
    assert has_default_data is True, \
        'Having no recon or mass-to-charge data is inacceptable at the moment!'

    # NEW ISSUE: fall-back solution to plot something else, however
    # currently POS, EPOS and APT provide always xyz, and m_z data

    # generate default plottable and add path
    template["/@default"] = "entry"
    template["/ENTRY[entry]/@default"] = "atom_probe"

    if has_valid_xyz is True:
        create_default_plottable_data_reconstruction(template)

        # generate path to the default plottable
        trg = "/ENTRY[entry]/atom_probe/"
        template[trg + "@default"] = "reconstruction"
        trg += "reconstruction/"
        template[trg + "@default"] = "naive_point_cloud_density_map"
        trg += "naive_point_cloud_density_map/"
        template[trg + "@default"] = "data"
        # to instruct h5web of which class this is

    if has_valid_m_z is True:
        create_default_plottable_data_mass_spectrum(template)

        # tomographic reconstruction is the default plot unless...
        if has_valid_xyz is False:
            # ... the mass_spectrum has to take this role
            trg = "/ENTRY[entry]/atom_probe/"
            template[trg + "@default"] = "ranging"
            trg += "ranging/"
            template[trg + "@default"] = "mass_to_charge_distribution"
            trg += "mass_to_charge_distribution/"
            template[trg + "@default"] = "mass_spectrum"

    # NEW ISSUE: visualize detector stack data

    return template


class ApmReader(BaseReader):
    """Parse content from community file formats.

    Specifically, local electrode atom probe microscopy
    towards a NXapm.nxdl-compliant NeXus file.

    """

    # pylint: disable=too-few-public-methods

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls = ["NXapm"]

    def read(self,
             template: dict = None,
             file_paths: Tuple[str] = None,
             objects: Tuple[Any] = None) -> dict:
        """Read data from given file, return filled template dictionary."""
        typed_files, case = assess_situation_with_input_files(file_paths)
        print(typed_files)
        print(case)
        assert case > INVALID_INPUT, \
            'Each reconstruction should have only one \
                range file and an associated metadata file!'

        report_appdef_version(template)

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

        # delete_not_properly_handled_fields(template)
        # NEW ISSUE: these deleted fields should be handled during the
        # instantiation of the template, i.e. if ION[ion] is minOccur=0
        # the converter should not ask for this field to be present !

        # hot fixed for now suggesting to implement as a new issue
        # NEW ISSUE: implement a functionality to return NX data type information
        # at this reader level so that values of a certain type family, like NX_UINT
        # get transformed into the specific datatype, like uint32 or uint64 e.g.

        # trg = "/ENTRY[entry]/atom_probe/"
        # implicit_int_to_uint32 \
        #     = [trg + "hit_multiplicity/hit_multiplicity",
        #        trg + "hit_multiplicity/pulses_since_last_ion",
        #        trg + "hit_multiplicity/pulse_id",
        #        trg + "ranging/peak_identification/ION[ion]/ion_type",
        #        trg + "ranging/peak_identification/ION[ion]/isotope_vector"]
        # for entry in implicit_int_to_uint32:
        #     template[entry] = np.uint32(template[entry])

        create_default_plottable_data(template)

        print('Add metadata from a nomadOASIS NXapm ELN yaml file...')
        # if 'json' in typed_files.keys():
        #     assert len(typed_files['json']) == 1, \
        #         'List of json files is ambiguous!'
        #     extract_data_from_json_file(typed_files['json'][0], template)
        if 'yaml' in typed_files.keys():
            assert len(typed_files['yaml']) == 1, \
                'List of yaml files is ambiguous!'
            extract_data_from_yaml_file(typed_files['yaml'][0], template)
        else:
            print('Unable to extract information from a lab notebook!')
            return {}

        # reporting of what has not been properly defined at the reader level
        print('\n\nDebugging...')
        for keyword in template.keys():
            # if template[keyword] is None:
            print(keyword + '...')
            print(template[keyword])
            # if template[keyword] is None:
            #     print("Entry: '" + keyword + " is not properly defined yet!")

        print('Returning and attempting the NXS creation...')

        return template


# This has to be set to allow the convert script to use this reader.
READER = ApmReader
