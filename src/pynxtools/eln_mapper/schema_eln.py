"""Generate schema ELN files which can be passed to NOMAD to define an ELN."""

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

import re
from typing import Union

from pynxtools.dataconverter.nexus_tree import NexusEntity, NexusGroup, NexusNode
from pynxtools.eln_mapper.eln import ElnGenerator

NEXUS_TO_NOMAD_QUANTITY: dict[str, tuple[str, str]] = {
    "NX_BINARY": ("bytes", "NumberEditQuantity"),
    "NX_BOOLEAN": ("bool", "BoolEditQuantity"),
    "NX_CHAR": ("str", "StringEditQuantity"),
    "NX_CHAR_OR_NUMBER": ("np.float64", "NumberEditQuantity"),
    "NX_COMPLEX": ("numpy.complex64", "NumberEditQuantity"),
    "NX_DATE_TIME": ("Datetime", "DateTimeEditQuantity"),
    "NX_FLOAT": ("np.float64", "NumberEditQuantity"),
    "NX_INT": ("int", "NumberEditQuantity"),
    "NX_NUMBER": ("np.float64", "NumberEditQuantity"),
    "NX_POSINT": ("int", "NumberEditQuantity"),
    "NX_UINT": ("int", "NumberEditQuantity"),
}

DEFAULT_UNITS: dict[str, Union[str, None]] = {
    "NX_ANGLE": "degree",
    "NX_ANY": None,
    "NX_AREA": "m**2",
    "NX_CHARGE": "C",
    "NX_COUNT": None,
    "NX_CROSS_SECTION": "m**2",
    "NX_CURRENT": "A",
    "NX_DIMENSIONLESS": None,
    "NX_EMITTANCE": "m * rad",
    "NX_ENERGY": "eV",
    "NX_FLUX": "1 / (m**2 * s)",
    "NX_FREQUENCY": "Hz",
    "NX_LENGTH": "m",
    "NX_MASS": "kg",
    "NX_MASS_DENSITY": "kg / m**3",
    "NX_MOLECULAR_WEIGHT": "g / mol",
    "NX_PERIOD": "s",
    "NX_PER_AREA": "1 / m**2",
    "NX_PER_LENGTH": "1 / m",
    "NX_POWER": "W",
    "NX_PRESSURE": "Pa",
    "NX_PULSES": None,
    "NX_SCATTERING_LENGTH_DENSITY": "m / m**3",
    "NX_SOLID_ANGLE": "sr",
    "NX_TEMPERATURE": "K",
    "NX_TIME": "s",
    "NX_TIME_OF_FLIGHT": "s",
    "NX_TRANSFORMATION": None,  # Unit is either m or degree or None
    "NX_UNITLESS": "",  # Explicitly unitless
    "NX_VOLTAGE": "V",
    "NX_VOLUME": "m**3",
    "NX_WAVELENGTH": "nm",
    "NX_WAVENUMBER": "1 / m",
}

DEFAULT_READER: dict[str, str] = {
    "NXafm": "spm",
    "NXapm": "apm",
    "NXellipsometry": "ellips",
    "NXem": "em",
    "NXmpes": "mpes",
    "NXraman": "raman",
    "NXspm": "spm",
    "NXstm": "spm",
    "NXsts": "spm",
    "NXxps": "xps",
    "NXxrd": "xrd",
}


def construct_description(node: NexusNode, concept_dict: dict) -> None:
    """Collect doc from concept doc (and inherited docs)."""
    inherited_docstrings = node.get_docstring()

    for key, doc in list(inherited_docstrings.items())[::-1]:
        if doc is not None:
            doc = re.sub(r"\s+", " ", doc).strip()
            concept_dict["description"] = doc
            break


class NomadElnGenerator(ElnGenerator):
    """Class for creating NOMAD ELN schemas from NeXus application definitions."""

    def _generate_output_file_name(self, output_file: str):
        """
        Generate the output file name of the schema ELN generator.

        The output file name will be:
        - <output_file>.scheme.archive.yaml or
        - <output_file> if output_file already ends on scheme.archive.yaml

        If no output_file is given, the output will be <nxdl_name>.scheme.archive.yaml,
        where <nxdl_name> is the name of the application definition without the leading NX
        (e.g., for NXmpes, the file is called mpes.scheme.archive.yaml).

        """
        file_parts: list = []
        out_file_ext = "scheme.archive.yaml"
        raw_name = ""
        out_file = ""

        if self.output_file is None:
            out_file = ".".join([self.nxdl[2:], out_file_ext])
        else:
            if output_file.endswith(out_file_ext):
                out_file = self.output_file
            else:
                file_parts = output_file.split(".")
                if len(file_parts) == 1:
                    raw_name = file_parts[0]
                    out_file = ".".join([raw_name, out_file_ext])
                elif len(file_parts) == 4 and ".".join(file_parts[1:]) == out_file_ext:
                    out_file = output_file
                else:
                    raise ValueError(
                        "Check for correct NeXus definition and output file name."
                    )

        return out_file

    def _generate_eln_header(self) -> dict:
        """Generate the header for the NOMAD ELN"""

        # Basic building blocks of ELN
        self.recursive_dict["definitions"] = {
            "name": f"{self.nxdl.lstrip('NX')} ELN data schema",
            "sections": {},
        }
        sections = self.recursive_dict["definitions"]["sections"]

        root_name = f"ELN for {self.nxdl.lstrip('NX')}"
        sections[root_name] = {}

        # Note for later: create a new function to handle root part
        sections[root_name].update(
            {
                "base_sections": [
                    "pynxtools.nomad.dataconverter.NexusDataConverter",
                    "nomad.datamodel.data.EntryData",
                ]
            }
        )

        reader = DEFAULT_READER.get(self.nxdl, "<READER_NAME>")

        m_annotations: dict = {
            "m_annotations": {
                "template": {"reader": reader, "nxdl": self.nxdl},
                "eln": {"hide": []},
            }
        }
        sections[root_name].update(m_annotations)

        return sections[root_name]

    def _construct_group_structure(
        self, node: NexusGroup, recursive_dict: dict, recursion_level: int
    ) -> None:
        """Handle NeXus group, to construct group structure as follows:
        <group_name>:
            section:
                m_annotations:
                    eln:
                        overview: true

        Parameters
        ----------
        node: NexusGroup
            NeXus group to recurse
        recursive_dict : dict
            dict into which the group is recursively added
        recursion_level: int
            Recursion level in the tree, used to (optionally) skip upper levels like NXentry
        """
        if not super()._construct_group_structure(
            node, recursive_dict, recursion_level
        ):
            return
        # if subsections is None:
        if "sub_sections" not in recursive_dict:
            recursive_dict["sub_sections"] = {}
        subsections = recursive_dict["sub_sections"]

        m_annotations = {"m_annotations": {"display": {"visible": True}}}

        group_name = node.name
        if node.name_type == "any":
            group_name = group_name.lower()  # this is just a suggestion for easier use

        subsections[group_name] = {}
        group_dict = subsections[group_name]

        # add section in group
        group_dict["section"] = {}
        section = group_dict["section"]
        if node.variadic:
            section["repeats"] = True
        section.update(m_annotations)

        # handle description and link
        construct_description(node, section)
        section["links"] = [node.get_link()]

        # pass the grp elment for recursive search
        self._recurse_tree(node, section, recursion_level + 1)

    def _construct_entity_structure(
        self, node: NexusEntity, recursive_dict: dict, recursion_level: int
    ):
        """Handle NeXus field or attribute, to construct structure like:
        <entity_name>:
            type: np.float64 (matching with the node's type)
            unit: <some-unit> (matching with the node's unit)
            m_annotations:
                eln:
                component: NumberEditQuantity (matching with the node's type)
                defaultDisplayUnit: <some-unit> (matching with the node's unit)
            description: node docs

        Parameters
        ----------
        node: NexusEntity
            NeXus field/attribute to recurse
        recursive_dict : dict
            dict into which the entity is recursively added
        recursion_level: int
            Recursion level in the tree, used to (optionally) skip upper levels like NXentry
        """
        if not super()._construct_entity_structure(
            node, recursive_dict, recursion_level
        ):
            return

        if "quantities" not in recursive_dict:
            recursive_dict["quantities"] = {}
        quantities_dict = recursive_dict["quantities"]

        entity_name = node.name
        if node.variadic:
            if node.name_type == "any":
                entity_name = (
                    entity_name.lower()
                )  # this is just a suggestion for easier use

        quantities_dict[entity_name] = {}
        entity_dict = quantities_dict[entity_name]

        # handle type
        default_types = ("str", "StringEditQuantity")
        entity_type, component_name = NEXUS_TO_NOMAD_QUANTITY.get(
            node.dtype, default_types
        )

        unit = None
        if node.unit:
            unit = DEFAULT_UNITS.get(node.unit)

        entity_dict["type"] = entity_type

        display_dict: dict[str, Union[bool, str]] = {"visible": True}
        if unit:
            entity_dict["unit"] = unit
            display_dict["unit"] = unit

        m_annotations = {
            "m_annotations": {
                "eln": {
                    "component": component_name,
                },
                "display": display_dict,
            }
        }

        entity_dict.update(m_annotations)

        construct_description(node, entity_dict)
        entity_dict["links"] = [node.get_link()]

        self._recurse_tree(node, entity_dict, recursion_level + 1)
