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
"""Wrapping multiple parsers for vendor files with reconstructed dataset files."""

# pylint: disable=no-member

import numpy as np

from ifes_apt_tc_data_modeling.apt.apt6_reader import ReadAptFileFormat

from ifes_apt_tc_data_modeling.pos.pos_reader import ReadPosFileFormat

from ifes_apt_tc_data_modeling.epos.epos_reader import ReadEposFileFormat


def extract_data_from_pos_file(file_name: str, prefix: str, template: dict) -> dict:
    """Add those required information which a POS file has."""
    print(f"Extracting data from POS file: {file_name}")
    posfile = ReadPosFileFormat(file_name)

    trg = f"{prefix}reconstruction/"
    xyz = posfile.get_reconstructed_positions()
    template[f"{trg}reconstructed_positions"] \
        = {"compress": np.array(xyz.typed_value, np.float32), "strength": 1}
    template[f"{trg}reconstructed_positions/@units"] = xyz.unit
    del xyz

    trg = f"{prefix}mass_to_charge_conversion/"
    m_z = posfile.get_mass_to_charge_state_ratio()
    template[f"{trg}mass_to_charge"] \
        = {"compress": np.array(m_z.typed_value, np.float32), "strength": 1}
    template[f"{trg}mass_to_charge/@units"] = m_z.unit
    del m_z
    return template


def extract_data_from_epos_file(file_name: str, prefix: str, template: dict) -> dict:
    """Add those required information which an ePOS file has."""
    print(f"Extracting data from EPOS file: {file_name}")
    eposfile = ReadEposFileFormat(file_name)

    trg = f"{prefix}reconstruction/"
    xyz = eposfile.get_reconstructed_positions()
    template[f"{trg}reconstructed_positions"] \
        = {"compress": np.array(xyz.typed_value, np.float32), "strength": 1}
    template[f"{trg}reconstructed_positions/@units"] = xyz.unit
    del xyz

    trg = f"{prefix}mass_to_charge_conversion/"
    m_z = eposfile.get_mass_to_charge_state_ratio()
    template[f"{trg}mass_to_charge"] \
        = {"compress": np.array(m_z.typed_value, np.float32), "strength": 1}
    template[f"{trg}mass_to_charge/@units"] = m_z.unit
    del m_z

    # there are inconsistencies in the literature as to which units these
    # quantities have, so we skip exporting the following quantities for now
    # the following source code has not been tested with the current NXapm version
    # but should be kept for making additions in the future easier
    # -->
    # trg = f"{prefix}voltage_and_bowl_correction/"
    # raw_tof = eposfile.get_raw_time_of_flight()
    # template[f"{trg}raw_tof"] = raw_tof.value
    # template[f"{trg}raw_tof/@units"] = raw_tof.unit
    # # this somehow calibrated ToF is not available from an EPOS file
    # template[f"{trg}calibrated_tof"] = raw_tof.value
    # template[f"{trg}calibrated_tof/@units"] = raw_tof.unit
    # # is this really a raw ToF, if so, raw wrt to what?
    # # needs clarification from Cameca/AMETEK how this is internally computed
    # # especially when scientists write APT files and transcode them
    # # to EPOS using APSuite
    # del raw_tof

    # trg = f"{prefix}pulser/"
    # dc_voltage = eposfile.get_standing_voltage()
    # template[f"{trg}standing_voltage"] = dc_voltage.value
    # template[f"{trg}standing_voltage/@units"] = dc_voltage.unit
    # del dc_voltage

    # pu_voltage = eposfile.get_pulse_voltage()
    # template[f"{trg}pulsed_voltage"] = pu_voltage.value
    # template[f"{trg}pulsed_voltage/@units"] = pu_voltage.unit
    # del pu_voltage

    # trg = f"{prefix}ion_impact_positions/"
    # hit_positions = eposfile.get_hit_positions()
    # template[f"{trg}hit_positions"] = hit_positions.value
    # template[f"{trg}hit_positions/@units"] = hit_positions.unit
    # del hit_positions

    # trg = f"{prefix}hit_multiplicity/"
    # # little bit more discussion with e.g. F. M. M. at MPIE required

    # # currently npulses is "number of pulses since last event detected"
    # npulses = eposfile.get_number_of_pulses()
    # template[f"{trg}hit_multiplicity"] = npulses.value
    # template[f"{trg}hit_multiplicity/@units"] = npulses.unit
    # del npulses

    # ions_per_pulse = eposfile.get_ions_per_pulse()
    # # currently ions_per_pulse is "ions per pulse, 0 after the first ion"
    # template[f"{trg}pulses_since_last_ion"] = ions_per_pulse.value
    # template[f"{trg}pulses_since_last_ion/@units"] \
    # = ions_per_pulse.unit
    # del ions_per_pulse
    # -->

    return template


def extract_data_from_apt_file(file_name: str, prefix: str, template: dict) -> dict:
    """Add those required information which a APT file has."""
    print(f"Extracting data from APT file: {file_name}")
    aptfile = ReadAptFileFormat(file_name)

    trg = f"{prefix}reconstruction/"
    xyz = aptfile.get_named_quantity("Position")
    template[f"{trg}reconstructed_positions"] \
        = {"compress": np.array(xyz.typed_value, np.float32), "strength": 1}
    template[f"{trg}reconstructed_positions/@units"] = xyz.unit
    del xyz

    trg = f"{prefix}mass_to_charge_conversion/"
    m_z = aptfile.get_named_quantity("Mass")
    template[f"{trg}mass_to_charge"] \
        = {"compress": np.array(m_z.typed_value, np.float32), "strength": 1}
    template[f"{trg}mass_to_charge/@units"] = m_z.unit
    del m_z

    # all less explored optional branches in an APT6 file can also already
    # be accessed via the aptfile.get_named_quantity function
    # but it needs to be checked if this returns reasonable values
    # and specifically what these values logically mean, interaction with
    # Cameca as well as the community is vital here
    return template


class ApmReconstructionParser:  # pylint: disable=too-few-public-methods
    """Wrapper for multiple parsers for vendor specific files."""

    def __init__(self, file_name: str, entry_id: int):
        self.file_format = "none"
        self.file_name = file_name
        index = file_name.lower().rfind(".")
        if index >= 0:
            mime_type = file_name.lower()[index + 1::]
            if mime_type in ["pos", "epos", "apt"]:
                self.file_format = mime_type
        self.entry_id = entry_id

    def report(self, template: dict) -> dict:
        """Copy data from self into template the appdef instance.

        Paths in template are prefixed by prefix and have to be compliant
        with the application definition.
        """
        prfx = f"/ENTRY[entry{self.entry_id}]/atom_probe/"
        if self.file_name != "" and self.file_format != "none":
            if self.file_format == "pos":
                extract_data_from_pos_file(
                    self.file_name, prfx, template)
            if self.file_format == "epos":
                extract_data_from_epos_file(
                    self.file_name, prfx, template)
            if self.file_format == "apt":
                extract_data_from_apt_file(
                    self.file_name, prfx, template)
        return template
