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
"""Utility functions for generation of atom probe NeXus datasets for dev purposes."""

# pylint: disable=E1101, R0801, R0902, W0201

import hashlib

import datetime

from typing import List

import numpy as np

from ase.lattice.cubic import FaceCenteredCubic
from ase.data import atomic_numbers, atomic_masses, chemical_symbols

from ifes_apt_tc_data_modeling.utils.utils \
    import create_isotope_vector, isotope_vector_to_nuclid_list, \
    isotope_vector_to_human_readable_name
from ifes_apt_tc_data_modeling.utils.definitions \
    import MAX_NUMBER_OF_ATOMS_PER_ION, MQ_EPSILON

from nexusutils.dataconverter.readers.apm.utils.apm_versioning \
    import NX_APM_ADEF_NAME, NX_APM_ADEF_VERSION, NX_APM_EXEC_NAME, NX_APM_EXEC_VERSION

from nexusutils.dataconverter.readers.apm.utils.apm_ranging_io \
    import add_unknown_iontype

# parameter affecting reconstructed positions and size
CRYSTAL_ORIENTATION = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
# MK::add analysis how large aggregate has to be
RECON_SIZE = (50, 50, 300)
RECON_ATOM_SPACING = 5.
RECON_HEIGHT = 300.  # angstroem
RECON_RADIUS = 50.  # angstroem
MAX_COMPONENTS = 5  # how many different molecular ions in one dataset/entry
MAX_ATOMS = 10  # determine power-law fraction of n_atoms per ion
MULTIPLES_FACTOR = 0.6  # controls how likely multiple ions are synthesized
# the higher this factor the more uniformly and more likely multiplicity > 1
MAX_CHARGE = 4  # highest allowed charge of ion
MAX_ATOMIC_NUMBER = 94  # do not include heavier atoms than Plutonium
MAX_USERS = 4


class ApmCreateExampleData:
    """A synthesized dataset meant to be used for development purposes only!."""

    def __init__(self, synthesis_id):
        # assure deterministic behaviour of the PRNG
        np.random.seed(seed=synthesis_id)

        self.n_entries = 1
        print("Generating one random example NXem entry...")
        self.entry_id = 1
        # reconstructed dataset and mass-to-charge state ratio values
        # like what is traditionally available via the POS file format
        self.xyz: List[float] = []
        self.m_z: List[float] = []

        # synthesizing realistic datasets for atom probe tomography
        # would require a physical model of the field evaporation process,
        # a model of the detector, and the reconstruction and ranging algorithms.
        # A cutting edge view of such simulations is described here
        # https://arxiv.org/abs/2209.05997, this demands very costly HPC computing
        # As this goes beyond what is numerically feasible, strong assumptions are made:
        # we are interested in having positions on a grid (real specimen geometry)
        #     details do not matter, positions are assumed exact without noise
        # reflect that signal comes from elementary and molecular ions
        #     details do not matter but sample from the entire periodic table
        # we wish to have a histogram of mass-to-charge-state ratio values
        # this is called a mass spectrum in the field of atom probe microscopy
        #     no tails in peaks are modelled as this depends on the pulser, physics
        #     and is in fact not yet well understood physically for general materials

    def create_reconstructed_positions(self):
        """Create aggregate of specifically oriented

        crystallographic unit cells and take the positions
        in this lattice to carve out a portion of the
        point cloud representing the reconstruction positions."""
        # https://wiki.fysik.dtu.dk/ase/ase/lattice.html#module-ase.lattice
        # ase length units in angstroem!
        # https://wiki.fysik.dtu.dk/ase/ase/units.html#units

        # assumptions:
        # identity orientation, no periodic boundary conditions
        xyz = np.asarray(FaceCenteredCubic(directions=CRYSTAL_ORIENTATION,
                                           size=RECON_SIZE, symbol="Cu",
                                           latticeconstant=RECON_ATOM_SPACING,
                                           pbc=(0, 0, 0)).get_positions(), np.float32)
        # Cu will be ignored, only the lattice with positions is relevant
        centre_of_mass = np.asarray([np.mean(xyz[:, 0]),
                                     np.mean(xyz[:, 1]),
                                     np.mean(xyz[:, 2])], np.float32)
        # print("Centre of mass of ASE lattice is (with coordinates in angstroem)")
        # print(centre_of_mass)
        xyz = xyz - centre_of_mass
        centre_of_mass = np.asarray([np.mean(xyz[:, 0]),
                                     np.mean(xyz[:, 1]),
                                     np.mean(xyz[:, 2])], np.float32)
        # print("Updated centre of mass")
        # print(centre_of_mass)
        # axis_aligned_bbox = np.asarray([np.min(xyz[:, 0]), np.max(xyz[:, 0]),
        #                                 np.min(xyz[:, 1]), np.max(xyz[:, 1]),
        #                                 np.min(xyz[:, 2]), np.max(xyz[:, 2])])
        # displace origin
        origin = centre_of_mass
        # print("Building a cylinder of radius " + str(RECON_RADIUS * 0.1) + " nm"
        #       + " and height " + str(RECON_HEIGHT * 0.1) + " nm")
        mask = None
        mask = xyz[:, 2] <= (origin[2] + 0.5 * RECON_HEIGHT)
        mask &= xyz[:, 2] >= (origin[2] - 0.5 * RECON_HEIGHT)
        mask &= ((xyz[:, 0] - origin[0])**2
                 + (xyz[:, 1] - origin[1])**2) <= RECON_RADIUS**2
        self.xyz = xyz[mask]
        shift = [0., 0., 0.5 * RECON_HEIGHT]
        for idx in np.arange(0, 3):
            self.xyz[:, idx] += shift[idx]
        self.xyz *= 0.1  # from angstroem to nm
        print("Created a geometry for a reconstructed dataset, shape is")
        print(np.shape(self.xyz))
        # self.aabb3d = np.asarray([np.min(self.xyz[:, 0]), np.max(self.xyz[:, 0]),
        #                           np.min(self.xyz[:, 1]), np.max(self.xyz[:, 1]),
        #                           np.min(self.xyz[:, 2]), np.max(self.xyz[:, 2])])

    def place_atoms_from_periodic_table(self):
        """Sample elements from the periodic table

        create (hypothetical) charged molecular ions from them
        and evaluate their mass-to-charge-state ratio to be used
        as values in the example dataset."""

        # uniform random model for how many different ions
        # !! warning: for real world datasets this depends on real specimen composition
        self.n_components = int(np.random.uniform(low=1, high=MAX_COMPONENTS))
        # print("Number of ions in the composition is " + str(self.n_components))

        # power law model for multiplicity of molecular ions
        # !! warning: for real world datasets depends on evaporation physics
        self.n_ivec = np.asarray(np.linspace(1,
                                             MAX_ATOMS,
                                             num=MAX_ATOMS,
                                             endpoint=True), np.float64)
        accept_reject = MULTIPLES_FACTOR**self.n_ivec
        accept_reject = np.cumsum(accept_reject) / np.sum(accept_reject)
        unifrnd = np.random.uniform(low=0., high=1., size=(self.n_components,))
        self.multiplicity = np.ones((self.n_components,))
        for idx in np.arange(0, len(accept_reject) - 1):
            mask = unifrnd[:] >= accept_reject[idx]
            mask &= unifrnd[:] < accept_reject[idx + 1]
            self.multiplicity[mask] = self.n_ivec[idx]
        self.multiplicity = np.asarray(self.multiplicity, np.uint32)

        # uniform model for distribution of charge states
        # !! warning: for real world datasets actual ion charge depends
        # on (evaporation) physics, very complicated in fact a topic of current research
        self.charge_state = np.asarray(np.random.uniform(low=1,
                                                         high=MAX_CHARGE,
                                                         size=(self.n_components,)),
                                       np.uint32)

        # compose for each component randomly sampled hypothetical molecular ions
        # uniform random model which elements to pick from periodic table of elements
        # !! warning: for real world datasets molecular ions found research dependant
        # !! often research in many groups is strongly focused on specific
        # materials and abundance, toxic nature of some elements forbids
        # experiments with these, like Plutonium or, also reason for synthetic data
        value_to_pse_symbol_lookup = {}
        for key, val in atomic_numbers.items():
            if key != "X":
                value_to_pse_symbol_lookup[val] = key

        composition = []  # list of tuples, one for each composition
        for idx in np.arange(0, self.n_components):
            isotope_vector = []
            mass_sum = 0.
            # sample atoms for building the ion
            sampled_elements = np.asarray(
                np.random.uniform(low=1, high=MAX_ATOMIC_NUMBER,
                                  size=(self.multiplicity[idx],)), np.uint32)

            for val in sampled_elements:
                symbol = value_to_pse_symbol_lookup[val]
                isotope_vector.append(symbol)
                mass_sum += atomic_masses[atomic_numbers[symbol]]

            composition.append((isotope_vector,
                                self.charge_state[idx],
                                mass_sum / self.charge_state[idx],
                                np.float64(np.random.uniform(low=1, high=100))))

        weighting_factor_sum = 0.
        for idx in np.arange(0, self.n_components):
            weighting_factor_sum += composition[idx][3]

        # normalize all compositions
        # (weighting_factor_sum)
        self.nrm_composition = []
        # print(composition)
        for idx in np.arange(0, self.n_components):
            self.nrm_composition.append((
                composition[idx][0],
                composition[idx][1],
                composition[idx][2],
                composition[idx][3] / weighting_factor_sum))

        self.nrm_composition.sort(key=lambda a: a[3])  # sort asc. for composition
        accept_reject = [0.]
        for idx in self.nrm_composition:
            accept_reject.append(idx[3])
        accept_reject = np.cumsum(accept_reject)
        assert self.xyz != [], \
            "self.xyz must not be an empty dataset, create a geometry first!"
        # print("Accept/reject sampling m/q values for "
        #       + str(np.shape(self.xyz)[0]) + " ions")

        unifrnd = np.random.uniform(low=0., high=1., size=(np.shape(self.xyz)[0],))
        self.m_z = np.empty((np.shape(self.xyz)[0],))
        self.m_z[:] = np.nan
        for idx in np.arange(0, len(accept_reject) - 1):
            mask = unifrnd[:] >= accept_reject[idx]
            mask &= unifrnd[:] < accept_reject[idx + 1]
            self.m_z[mask] = self.nrm_composition[idx][2]
            # print(self.nrm_composition[idx])
            # print(np.sum(mask) / np.shape(self.xyz)[0])
        # print(np.shape(self.m_z))
        # assert np.sum(self.m_z == np.nan) == 0, "Not all m/q values defined!"

    def composition_to_ranging_definitions(self, template: dict) -> dict:
        """Create ranging definitions based on composition."""
        assert len(self.nrm_composition) > 0, "Composition is not defined!"
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/atom_probe/ranging/"
        template[trg + "program"] = "synthetic"
        template[trg + "program/@version"] = "synthetic data"
        template[trg + "number_of_ion_types"] = np.uint32(0)
        # template[trg + "number_of_ion_types/@units"] = ""
        template[trg + "maximum_number_of_atoms_per_molecular_ion"] = np.uint32(32)
        template[trg + "maximum_number_of_atoms_per_molecular_ion/@units"] = ""

        trg = "/ENTRY[entry" + str(self.entry_id) + "]/atom_probe/ranging/peak_identification/"
        template[trg + "program"] = "synthetic"
        template[trg + "program/@version"] = "synthetic"

        add_unknown_iontype(template, self.entry_id)

        ion_id = 1
        for tpl in self.nrm_composition:
            path = trg + "ION[ion" + str(ion_id) + "]/"
            ivec = create_isotope_vector(tpl[0])
            template[path + "isotope_vector"] \
                = np.reshape(np.asarray(ivec, np.uint16),
                             (1, MAX_NUMBER_OF_ATOMS_PER_ION))
            # template[path + "isotope_vector/@units"] = ""
            template[path + "charge_state"] = np.int8(tpl[1])
            template[path + "charge_state/@units"] = "eV"
            template[path + "mass_to_charge_range"] \
                = np.reshape(np.asarray(
                             [tpl[2], tpl[2] + MQ_EPSILON], np.float32), (1, 2))
            template[path + "mass_to_charge_range/@units"] = "Da"
            nuclid_list = np.zeros([2, 32], np.uint16)
            nuclid_list = isotope_vector_to_nuclid_list(ivec)
            template[path + "nuclid_list"] = np.asarray(nuclid_list, np.uint16)
            # template[path + "nuclid_list/@units"] = ""
            template[path + "name"] = isotope_vector_to_human_readable_name(ivec, tpl[1])
            ion_id += 1

        trg = "/ENTRY[entry" + str(self.entry_id) + "]/atom_probe/ranging/"
        template[trg + "number_of_ion_types"] = np.uint32(ion_id)
        # template[trg + "number_of_ion_types/@units"] = ""
        return template

    def emulate_entry(self, template: dict) -> dict:
        """Copy data in entry section."""
        # check if required fields exists and are valid
        # print("Parsing entry...")
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/"
        template[trg + "definition"] = NX_APM_ADEF_NAME
        template[trg + "@version"] = NX_APM_ADEF_VERSION
        template[trg + "program"] = NX_APM_EXEC_NAME
        template[trg + "program/@version"] = NX_APM_EXEC_VERSION
        template[trg + "start_time"] = datetime.datetime.now().astimezone().isoformat()
        template[trg + "end_time"] = datetime.datetime.now().astimezone().isoformat()
        msg = '''
              WARNING: These are mocked data !!
              They are meant to be used exclusively
              for verifying NOMAD search capabilities.
              '''
        template[trg + "experiment_description"] = msg
        experiment_identifier \
            = "R" + str(np.random.choice(100, 1)[0]) \
            + "-" + str(np.random.choice(100000, 1)[0])
        template[trg + "experiment_identifier"] = experiment_identifier
        template[trg + "run_number"] \
            = experiment_identifier.split("-")[1]
        template[trg + "operation_mode"] \
            = str(np.random.choice(["apt", "fim", "apt_fim"], 1)[0])
        return template

    def emulate_user(self, template: dict) -> dict:
        """Copy data in user section."""
        # check if required fields exists and are valid
        # print("Parsing user...")
        prefix = "/ENTRY[entry" + str(self.entry_id) + "]/"
        user_names = np.unique(
            np.random.choice(["Sherjeel", "MarkusK", "Dierk", "Baptiste",
                              "Alexander", "Lorenz", "Sophie", "Stefan",
                              "Katharina", "Florian", "Daniel", "Sandor",
                              "Carola", "Andrea", "Hampus", "Pepe", "Lauri",
                              "MarkusS", "Christoph", "Claudia"],
                             1 + np.random.choice(MAX_USERS, 1)))
        user_id = 1
        for name in user_names:
            trg = prefix + "USER[user" + str(user_id) + "]/"
            template[trg + "name"] = str(name)
            user_id += 1
        return template

    def emulate_specimen(self, template: dict) -> dict:
        """Copy data in specimen section."""
        # check if required fields exists and are valid
        # print("Parsing specimen...")
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/specimen/"
        assert len(self.nrm_composition) > 0, "Composition list is empty!"
        unique_elements = set()
        for tpl in self.nrm_composition:
            symbol_lst = tpl[0]
            for symbol in symbol_lst:
                assert isinstance(symbol, str), "symbol is not a string!"
                if (symbol in chemical_symbols) & (symbol != "X"):
                    unique_elements.add(str(symbol))
        print("Unique elements are")
        print(list(unique_elements))
        template[trg + "atom_types"] = ", ".join(list(unique_elements))

        specimen_name = "Mocked atom probe specimen " \
            + str(np.random.choice(1000, 1)[0])
        template[trg + "name"] = specimen_name
        template[trg + "sample_history"] = "n/a"
        template[trg + "preparation_date"] \
            = datetime.datetime.now().astimezone().isoformat()
        template[trg + "short_title"] \
            = specimen_name.replace("Mocked atom probe specimen ", "")
        template[trg + "description"] = "n/a"
        return template

    def emulate_control_software(self, template: dict) -> dict:
        """Copy data in control software section."""
        # print("Parsing control software...")
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/atom_probe/control_software/"
        template[trg + "program"] = "IVAS"
        template[trg + "program/@version"] = "3." \
            + str(np.random.choice(9, 1)[0]) + "." \
            + str(np.random.choice(9, 1)[0])
        return template

    def emulate_instrument_header(self, template: dict) -> dict:
        """Copy data in instrument_header section."""
        # check if required fields exists and are valid
        # print("Parsing instrument header...")
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/atom_probe/"
        template[trg + "instrument_name"] \
            = "test instrument " + str(np.random.choice(100, 1)[0])
        template[trg + "flight_path_length"] \
            = np.float64(np.random.normal(loc=1.0, scale=0.05))
        template[trg + "flight_path_length/@units"] = "m"
        return template

    def emulate_fabrication(self, template: dict) -> dict:
        """Copy data in fabrication section."""
        # print("Parsing fabrication...")
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/atom_probe/FABRICATION[fabrication]/"
        template[trg + "vendor"] \
            = str(np.random.choice(["AMETEK/Cameca", "customized"], 1)[0])
        template[trg + "model"] \
            = str(np.random.choice(["LEAP3000", "LEAP4000", "LEAP5000",
                  "LEAP6000", "OxCart", "MTAP", "FIM"], 1)[0])
        template[trg + "identifier"] \
            = str(hashlib.sha256("IVAS".encode("utf-8")).hexdigest())
        template[trg + "capabilities"] = ""
        return template

    def emulate_analysis_chamber(self, template: dict) -> dict:
        """Copy data in analysis_chamber section."""
        # print("Parsing analysis chamber...")
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/atom_probe/analysis_chamber/"
        template[trg + "pressure"] = np.float64(
            np.random.normal(loc=1.0e-10, scale=0.2e-11))
        template[trg + "pressure/@units"] = "torr"
        return template

    def emulate_reflectron(self, template: dict) -> dict:
        """Copy data in reflectron section."""
        # print("Parsing reflectron...")
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/atom_probe/REFLECTRON[reflectron]/"
        template[trg + "applied"] = bool(np.random.choice([0, 1], 1)[0])
        return template

    def emulate_local_electrode(self, template: dict) -> dict:
        """Copy data in local_electrode section."""
        # print("Parsing local electrode...")
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/atom_probe/local_electrode/"
        template[trg + "name"] \
            = "electrode " + str(np.random.choice(1000, 1)[0])
        return template

    def emulate_detector(self, template: dict) -> dict:
        """Copy data in ion_detector section."""
        # print("Parsing detector...")
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/atom_probe/ion_detector/"
        detector_model_type = str(np.random.choice(["cameca", "mcp", "custom"], 1)[0])
        template[trg + "type"] = detector_model_type
        template[trg + "name"] = detector_model_type
        template[trg + "model"] = detector_model_type
        template[trg + "serial_number"] = hashlib.sha256(
            detector_model_type.encode("utf-8")).hexdigest()
        return template

    def emulate_stage_lab(self, template: dict) -> dict:
        """Copy data in stage lab section."""
        # print("Parsing stage lab...")
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/atom_probe/stage_lab/"
        template[trg + "base_temperature"] = np.float64(10 + np.random.choice(50, 1)[0])
        template[trg + "base_temperature/@units"] = "K"
        return template

    def emulate_specimen_monitoring(self, template: dict) -> dict:
        """Copy data in specimen_monitoring section."""
        # print("Parsing specimen monitoring...")
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/atom_probe/specimen_monitoring/"
        eta = np.min((np.random.normal(loc=0.6, scale=0.1), 1.))
        template[trg + "detection_rate"] = np.float64(eta)
        # template[trg + "detection_rate/@units"] = ""
        template[trg + "initial_radius"] = np.float64(RECON_RADIUS * 0.1)
        template[trg + "initial_radius/@units"] = "nm"
        template[trg + "shank_angle"] = np.float64(0.)  # = np.random.choice(10, 1)[0]
        template[trg + "shank_angle/@units"] = "degree"
        return template

    def emulate_pulser(self, template: dict) -> dict:
        """Copy data in pulser section."""
        # print("Parsing pulser...")
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/atom_probe/pulser/"
        pulse_mode = str(np.random.choice(
            ["laser", "voltage", "laser_and_voltage"], 1)[0])
        template[trg + "pulse_mode"] = pulse_mode
        template[trg + "pulse_fraction"] \
            = np.float64(np.random.normal(loc=0.1, scale=0.02))
        # template[trg + "pulse_fraction/@units"] = ""
        template[trg + "pulse_frequency"] \
            = np.float64(np.random.normal(loc=250, scale=10))
        template[trg + "pulse_frequency/@units"] = "kHz"
        if pulse_mode != "voltage":
            trg = "/ENTRY[entry" + str(self.entry_id) + "]/atom_probe/pulser/laser_gun/"
            template[trg + "name"] = "laser"
            template[trg + "wavelength"] \
                = np.float64((30 + np.random.choice(30, 1)) * 1.0e-8)
            template[trg + "wavelength/@units"] = "m"
            template[trg + "pulse_energy"] \
                = np.float64(np.random.normal(loc=1.2e-11, scale=0.2e-12))
            template[trg + "pulse_energy/@units"] = "J"
            template[trg + "power"] \
                = np.float64(np.random.normal(loc=2.0e-8, scale=0.2e-9))
            template[trg + "power/@units"] = "W"
        return template

    def emulate_reconstruction(self, template: dict) -> dict:
        """Copy data in reconstruction section."""
        # print("Parsing reconstruction...")
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/atom_probe/reconstruction/"
        src = "/ENTRY[entry" + str(self.entry_id) + "]/atom_probe/control_software/"
        template[trg + "program"] = template[src + "program"]
        template[trg + "program/@version"] = template[src + "program/@version"]
        template[trg + "protocol_name"] \
            = str(np.random.choice(["bas", "geiser", "gault", "cameca", "other"], 1)[0])
        template[trg + "parameter"] = "n/a"
        template[trg + "crystallographic_calibration"] = "n/a"
        return template

    def emulate_ranging(self, template: dict) -> dict:
        """Copy data in ranging section."""
        # print("Parsing ranging...")
        trg = "/ENTRY[entry" + str(self.entry_id) + "]/atom_probe/ranging/"
        src = "/ENTRY[entry" + str(self.entry_id) + "]/atom_probe/control_software/"
        template[trg + "program"] = template[src + "program"]
        template[trg + "program/@version"] = template[src + "program/@version"]
        return template

    def emulate_random_input_from_eln(self, template: dict) -> dict:
        """Emulate random input as could come from an ELN."""
        self.emulate_entry(template)
        self.emulate_user(template)
        self.emulate_specimen(template)

        self.emulate_control_software(template)
        # above call will set program and program/@version used later

        self.emulate_instrument_header(template)
        self.emulate_fabrication(template)
        self.emulate_analysis_chamber(template)
        self.emulate_reflectron(template)
        self.emulate_local_electrode(template)
        self.emulate_detector(template)
        self.emulate_stage_lab(template)
        self.emulate_specimen_monitoring(template)

        self.emulate_pulser(template)
        self.emulate_reconstruction(template)
        self.emulate_ranging(template)

        return template

    def synthesize(self, template: dict) -> dict:
        """Hand-over instantiated dataset to dataconverter template."""
        # heavy data, synthetic/mocked dataset
        for entry_id in np.arange(1, self.n_entries + 1):
            self.entry_id = entry_id
            print("Generating entry" + str(self.entry_id) + "...")

            self.xyz = []
            self.m_z = []
            self.create_reconstructed_positions()
            self.place_atoms_from_periodic_table()
            self.composition_to_ranging_definitions(template)

            # metadata
            self.emulate_random_input_from_eln(template)

            # heavy numerical data, here the synthesized "measurement" data
            prefix = "/ENTRY[entry" + str(self.entry_id) + "]/atom_probe/"
            trg = prefix + "reconstruction/"
            template[trg + "reconstructed_positions"] \
                = {"compress": np.asarray(self.xyz, np.float32), "strength": 1}
            template[trg + "reconstructed_positions/@units"] = "nm"

            trg = prefix + "mass_to_charge_conversion/"
            template[trg + "mass_to_charge"] \
                = {"compress": np.asarray(self.m_z, np.float32), "strength": 1}
            template[trg + "mass_to_charge/@units"] = "Da"

        return template
