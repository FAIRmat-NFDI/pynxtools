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
"""Utility functions for generation of EM NeXus datasets for dev purposes."""

# pylint: disable=E1101, R0801

import hashlib

import datetime

import math

import numpy as np

# import matplotlib.pyplot as plt

import hyperspy.api as hs

from ase.data import chemical_symbols

from nexusutils.dataconverter.readers.em_spctrscpy.utils.em_versioning \
    import NX_EM_ADEF_NAME, NX_EM_ADEF_VERSION, NX_EM_EXEC_NAME, NX_EM_EXEC_VERSION

# parameter affecting reconstructed positions and size
# default parameter
MAX_USERS = 4
# compose hypothetical spectrum (ignoring background)
XRAY_ENERGY_DELTA = 0.01  # in keV
PEAK_WIDTH_SIGMA = 0.1  # stddev in keV assumed the same for all peaks
SIGNAL_YIELD = 1000.  # arbitrarily assumed signal intensity


class EmSpctrscpyCreateExampleData:
    """A synthesized dataset meant to be used for development purposes only!."""

    def __init__(self, synthesis_id):
        # assure deterministic behaviour of the PRNG
        np.random.seed(seed=synthesis_id)

        self.n_entries = 1
        print("Generating one random example NXem entry...")
        self.entry_id = 1
        self.elements_observed = []
        self.e_axis = []
        self.cnts_summary = []
        # synthesizing realistic datasets for electron microscopy requires a
        # physical model of the image formation process see e.g. Kirkland et al.
        # for an (incomplete) view of this large topic
        # https://doi.org/10.1007/978-3-030-33260-0
        # we are interested in having spectra and maybe some synthesized images
        # as this is already sufficient to explore search capabilities in e.g. OASIS

    def emulate_entry(self, template: dict) -> dict:
        """Copy data in entry section."""
        # check if required fields exists and are valid
        # print("Parsing entry...")
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/"
        template[trg + "definition"] = NX_EM_ADEF_NAME
        template[trg + "@version"] = NX_EM_ADEF_VERSION
        template[trg + "program"] = NX_EM_EXEC_NAME
        template[trg + "program/@version"] = NX_EM_EXEC_VERSION
        template[trg + "start_time"] = datetime.datetime.now().astimezone().isoformat()
        template[trg + "end_time"] = datetime.datetime.now().astimezone().isoformat()
        msg = '''WARNING: These are mocked data !!
              These are meant to be used exclusively
              for verifying NOMAD search capabilities.
              '''
        template[trg + "experiment_description"] = msg
        template[trg + "experiment_documentation"] = "free text field"
        experiment_identifier \
            = "EM" + str(np.random.choice(100, 1)[0]) \
            + "/" + str(np.random.choice(100000, 1)[0])
        template[trg + "experiment_identifier"] = experiment_identifier
        return template

    def emulate_user(self, template: dict) -> dict:
        """Copy data in user section."""
        # check if required fields exists and are valid
        # print("Parsing user...")
        prefix = f"/ENTRY[entry{self.entry_id}]/"
        user_names = np.unique(
            np.random.choice(["Sherjeel", "MarkusK", "Benedikt", "Johannes",
                              "Gerardo", "Kristiane", "Sabine", "Sophie", "Tom",
                              "Volker", "MarkusW", "PeterK", "Oonagh", "Annika",
                              "ChristophP", "Thomas", "Mariano", "Tilmann",
                              "ChristophF", "Niels", "Dieter", "Alexander",
                              "Katharina", "Florian", "Sebastian", "Sandor",
                              "Carola", "Chris", "Hampus", "Pepe", "Lauri",
                              "MarkusS", "Christoph", "Claudia"],
                             1 + np.random.choice(MAX_USERS, 1)))
        user_id = 1
        for name in user_names:
            trg = prefix + "USER[user" + str(user_id) + "]/"
            template[trg + "name"] = str(name)
            user_id += 1
        return template

    def emulate_sample(self, template: dict) -> dict:
        """Copy data in specimen section."""
        # check if required fields exists and are valid
        # print("Parsing sample...")
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/sample/"
        template[trg + "method"] = "simulation"

        self.elements_observed \
            = np.random.choice(np.asarray(np.linspace(1, 94, num=118, endpoint=True),
                                          np.uint32),
                               1 + int(np.random.uniform(low=0, high=5)))
        assert len(self.elements_observed) > 0, "List of assumed elements is empty!"
        unique_elements = set()
        for atomic_number in self.elements_observed:
            symbol = chemical_symbols[atomic_number]
            assert isinstance(symbol, str), "symbol is not a string!"
            if (symbol in chemical_symbols) & (symbol != "X"):
                unique_elements.add(symbol)
        print("Unique elements are")
        print(list(unique_elements))
        template[trg + "atom_types"] = ", ".join(list(unique_elements))

        specimen_name = "Mocked electron microscopy specimen " \
            + str(np.random.choice(1000, 1)[0])
        template[trg + "name"] = specimen_name
        template[trg + "sample_history"] = "n/a"
        template[trg + "preparation_date"] \
            = datetime.datetime.now().astimezone().isoformat()
        template[trg + "short_title"] \
            = specimen_name.replace("Mocked atom probe specimen ", "")
        template[trg + "description"] = "n/a"

        template[trg + "thickness"] \
            = np.float64(np.max((np.random.normal(loc=40., scale=5.0), 10.)))
        template[trg + "thickness/@units"] = "nm"
        template[trg + "density"] = 0.  # is optional
        # template[trg + "density/@units"] = "kg/m^3"
        return template

    def emulate_coordinate_system(self, template: dict) -> dict:
        """Define the coordinate systems to be used."""
        # print("Parsing coordinate system...")
        prefix = f"/ENTRY[entry{self.entry_id}]/"
        prefix += "COORDINATE_SYSTEM_SET[coordinate_system_set]/"
        # this is likely not yet matching how it should be in NeXus
        grpnm = prefix + "TRANSFORMATIONS[laboratory]/"
        cs_xyz = np.asarray(
            [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]], np.float64)
        cs_names = ["x", "y", "z"]
        for i in np.arange(0, 3):
            trg = grpnm + "AXISNAME[" + cs_names[i] + "]"
            template[trg] = cs_xyz[:, i]
            template[trg + "/@transformation_type"] = "translation"
            template[trg + "/@offset"] = np.asarray([0., 0., 0.], np.float64)
            template[trg + "/@offset_units"] = "m"
            template[trg + "/@depends_on"] = "."

        msg = '''
              This way of defining coordinate systems is an example
              how these can be defined. More discussion among members
              of FAIRmat Area A/B/C and members of the EM community
              plus more examples should be used to test how this
              feature of NeXus can be used.
              '''
        template[prefix + "@comment"] = msg
        return template

    def emulate_instrument_header(self, template: dict) -> dict:
        """Copy data in instrument header section."""
        # print("Parsing instrument header...")
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/em_lab/"
        instrument_name = np.random.choice(
            ["Some ThermoFisher", "Some JEOL", "Some Zeiss",
             "Some TEscan", "Some Hitachi"], 1 + np.random.choice(1, 1))[0]
        template[trg + "instrument_name"] = str(instrument_name)
        template[trg + "location"] = str(np.random.choice(
            ["Berlin", "Leipzig", "Dresden", "Düsseldorf", "Aachen", "Garching",
             "Aachen", "Leoben", "Jülich"], 1 + np.random.choice(1, 1))[0])
        trg = f"/ENTRY[entry{self.entry_id}]/em_lab/FABRICATION[fabrication]/"
        template[trg + "vendor"] = instrument_name.replace("Some ", "")
        template[trg + "model"] = "n/a"
        template[trg + "identifier"] = str(hashlib.sha256(
            instrument_name.replace("Some ", "").encode("utf-8")).hexdigest())
        template[trg + "capabilities"] = "n/a"
        return template

    def emulate_ebeam_column(self, template: dict) -> dict:
        """Copy data in ebeam_column section."""
        # print("Parsing ebeam column...")
        prefix = f"/ENTRY[entry{self.entry_id}]/em_lab/EBEAM_COLUMN[ebeam_column]/"
        trg = prefix + "electron_gun/"

        template[trg + "voltage"] \
            = np.float64(
                np.random.choice(np.linspace(10., 300., num=30, endpoint=True), 1)[0])
        template[trg + "voltage/@units"] = "kV"
        template[trg + "emitter_type"] \
            = str(np.random.choice(["thermionic", "schottky", "field_emission"], 1)[0])

        # apertures = [1]
        # aperture_id = 1
        # for aperture in apertures:
        trg = prefix + "APERTURE_EM[aperture_em" + str(1) + "]/"
        template[trg + "value"] \
            = np.uint32(
                np.random.choice(np.linspace(1, 5, num=5, endpoint=True), 1)[0])
        # template[trg + "value/@units"] = ""
        template[trg + "name"] = "aperture " + str(1)
        template[trg + "description"] = "n/a"
        # aperture_id += 1

        # the above-mentioned snippet is a blue-print for lenses also...

        # corrector
        trg = prefix + "aberration_correction/"
        template[trg + "applied"] = bool(np.random.choice([0, 1], 1)[0])
        return template

    def emulate_ibeam_column(self, template: dict) -> dict:
        """Copy data in ibeam_column section."""
        # print("Parsing ibeam column...")
        return template

    def emulate_ebeam_deflector(self, template: dict) -> dict:
        """Copy data in ebeam_deflector section."""
        # print("Parsing ebeam deflector...")
        return template

    def emulate_ibeam_deflector(self, template: dict) -> dict:
        """Copy data in ibeam_deflector section."""
        # print("Parsing ibeam deflector...")
        return template

    def emulate_optics(self, template: dict) -> dict:
        """Copy data in optical_system_em section."""
        # print("Parsing optics...")
        trg = f"/ENTRY[entry{self.entry_id}]/em_lab/OPTICAL_SYSTEM_EM[optical_system_em]/"
        template[trg + "beam_current_description"] = "undefined"
        template[trg + "camera_length"] \
            = np.float64(np.random.normal(loc=1.0, scale=0.05))
        template[trg + "camera_length/@units"] = "m"
        template[trg + "magnification"] \
            = np.float64(np.random.choice([100., 1000., 10000., 100000.], 1)[0])
        # template[trg + "magnification/@units"] = ""
        template[trg + "defocus"] = np.float64(np.random.normal(loc=1.0e-7, scale=0.1e-7))
        template[trg + "defocus/@units"] = "m"
        template[trg + "semi_convergence_angle"] \
            = np.float64(
                np.min((np.random.normal(loc=10., scale=1.), 1.0)))
        template[trg + "semi_convergence_angle/@units"] = "degree"
        template[trg + "working_distance"] \
            = np.float64(np.trunc(np.random.choice(np.linspace(5.,
                                                               20.,
                                                               num=15,
                                                               endpoint=True), 1)[0]))
        template[trg + "working_distance/@units"] = "cm"
        template[trg + "beam_current"] = np.float64(
            np.min((np.random.normal(loc=10., scale=2.), 1.0)))
        template[trg + "beam_current/@units"] = "pA"
        return template

    def emulate_detector(self, template: dict) -> dict:
        """Copy data in detector section."""
        # print("Parsing detector...")
        detectors = np.unique(np.random.choice(
            ["SE", "BSE", "EBSD", "EDX", "INLINE"],
            1 + np.random.choice(5, 1)))
        detector_id = 1
        for detector in detectors:
            trg = f"/ENTRY[entry{self.entry_id}]/em_lab/DETECTOR[detector{detector_id}]/"
            template[trg + "type"] = str(detector)
            detector_id += 1
        return template

    def emulate_stage_lab(self, template: dict) -> dict:
        """Copy data in stage lab section."""
        # print("Parsing stage lab...")
        trg = f"/ENTRY[entry{self.entry_id}]/em_lab/stage_lab/"
        stage_name = np.random.choice(
            ["side_entry", "top_entry", "single_tilt", "quick_change",
             "multiple_specimen", "bulk_specimen", "double_tilt", "tilt_rotate",
             "heating_chip", "atmosphere_chip", "electrical_biasing_chip",
             "liquid_cell_chip"], 1)[0]
        template[trg + "name"] = str(stage_name)
        return template

    def emulate_random_input_from_eln(self, template: dict) -> dict:
        """Emulate random input as could come from an ELN."""
        print("Parsing random input from ELN...")
        self.emulate_entry(template)
        self.emulate_user(template)
        self.emulate_sample(template)
        self.emulate_coordinate_system(template)
        self.emulate_instrument_header(template)
        self.emulate_ebeam_column(template)
        self.emulate_ibeam_column(template)
        self.emulate_ebeam_deflector(template)
        self.emulate_ibeam_deflector(template)
        self.emulate_optics(template)
        self.emulate_detector(template)
        self.emulate_stage_lab(template)

        return template

    def emulate_random_xray_spectrum(self, template: dict) -> dict:
        """Emulate one event data group for Xray spectroscopy."""
        # !! data meant exclusively to be used for verification purposes !!
        assert len(self.elements_observed > 0), "No elements were observed !"
        composition = np.random.uniform(
            low=0., high=1., size=(len(self.elements_observed),))
        composition = composition / np.sum(composition)
        signal_contributions = []
        idx = 0
        # sample hypothetically X-ray lines for each element observed
        for atomic_number in self.elements_observed:
            symbol = chemical_symbols[atomic_number]
            if symbol in hs.material.elements:
                if 'Atomic_properties' in hs.material.elements[symbol]:
                    if 'Xray_lines' in hs.material.elements[symbol].Atomic_properties:
                        lines = hs.material.elements[symbol].Atomic_properties.Xray_lines
                        for xline_name, xline_props in lines.as_dictionary().items():
                            # print(key + ", " + str(value["weight"]))
                            signal_contributions.append((atomic_number,
                                                         symbol,
                                                         composition[idx],
                                                         xline_name,
                                                         xline_props["energy (keV)"],
                                                         xline_props["weight"]))
            idx += 1
        # self.elements_observed = np.unique(symbols)

        xray_energy_max = 0.
        for tpl in signal_contributions:
            xray_energy_max = np.max((xray_energy_max, tpl[4]))
        # print(xray_energy_max)

        n_bins = int(np.ceil(
            (xray_energy_max + 3. * XRAY_ENERGY_DELTA + 1.)
            / XRAY_ENERGY_DELTA))  # covering [0., n_bins * XRAY_ENERGY_DELTA]
        self.e_axis = np.linspace(
            0.5 * XRAY_ENERGY_DELTA,
            0.5 * XRAY_ENERGY_DELTA + n_bins * XRAY_ENERGY_DELTA,
            num=n_bins, endpoint=True)

        self.cnts_summary = np.zeros((n_bins,), np.float64)
        for tpl in signal_contributions:
            # idx = np.abs(self.e_axis - tpl[4]).argmin()
            # integrate analytically, assume Gaussian peak with stddev PEAK_WIDTH_SIGMA
            cnts_tpl = np.zeros((n_bins, ), np.float64)
            for idx in np.arange(0, n_bins):
                cnts_tpl[idx] = SIGNAL_YIELD * tpl[2] * tpl[5] * 0.5 \
                    * (math.erf(1. / (np.sqrt(2.) * PEAK_WIDTH_SIGMA)
                       * (tpl[4] - (0. + idx * XRAY_ENERGY_DELTA)))
                       - math.erf(1. / (np.sqrt(2.) * PEAK_WIDTH_SIGMA)
                       * (tpl[4] - (XRAY_ENERGY_DELTA + idx * XRAY_ENERGY_DELTA))))
            self.cnts_summary = np.add(self.cnts_summary, cnts_tpl)
        # plt.plot(self.e_axis, self.cnts_summary)
        # plt.xlabel("energy (keV)")
        # plt.ylabel("cnts")
        # plt.xscale("log")

        trg = "/ENTRY[entry" + str(self.entry_id) + "]/"
        trg += "measurement/EVENT_DATA_EM[event_data_em1]/"
        trg += "SPECTRUM_SET_EM_XRAY[spectrum_set_em_xray1]/summary/"
        template[trg + "title"] = "Accumulated X-ray spectrum"
        # template[trg + "@long_name"] = "Xray"
        template[trg + "@signal"] = "data_counts"
        template[trg + "@axes"] = ["axis_photon_energy"]
        template[trg + "@AXISNAME_indices[axis_photon_energy_indices]"] = 0
        template[trg + "DATA[data_counts]"] \
            = {"compress": self.cnts_summary, "strength": 1}
        template[trg + "DATA[data_counts]/@units"] = ""
        template[trg + "DATA[data_counts]/@long_name"] = "Photon counts (1)"
        template[trg + "AXISNAME[axis_photon_energy]"] \
            = {"compress": self.e_axis, "strength": 1}
        template[trg + "AXISNAME[axis_photon_energy]/@units"] = "keV"
        template[trg + "AXISNAME[axis_photon_energy]/@long_name"] = "Photon energy (keV)"
        return template

    def synthesize(self, template: dict) -> dict:
        """Hand-over instantiated dataset to dataconverter template."""
        for entry_id in np.arange(1, self.n_entries + 1):
            self.entry_id = entry_id
            print("Generating entry" + str(self.entry_id) + "...")

            # metadata
            self.emulate_random_input_from_eln(template)

            # heavy numerical data, here the synthesized "measurement" data
            self.emulate_random_xray_spectrum(template)

        return template
