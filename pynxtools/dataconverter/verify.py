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
"""Verifies a nxs file"""

import logging
import os
import sys
import xml.etree.ElementTree as ET
from os import path
from typing import Dict, Union

import click
from h5py import Dataset, File, Group, is_hdf5

from pynxtools.dataconverter import helpers
from pynxtools.dataconverter.template import Template
from pynxtools.definitions.dev_tools.utils.nxdl_utils import get_nexus_definitions_path

logger = logging.getLogger(__name__)

DEBUG_TEMPLATE = 9
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


def _replace_group_names(class_map: Dict[str, str], path: str):
    for class_path, nx_class in class_map.items():
        if f"/{class_path}/" in path or path.startswith(f"{class_path}/"):
            path = path.replace(f"{class_path}/", f"{nx_class}[{class_path}]/")
    return path


def _get_def_map(file: str) -> Dict[str, str]:
    def_map: Dict[str, str] = {}
    with File(file, "r") as h5file:
        for entry_name, dataset in h5file.items():
            if (
                helpers.clean_str_attr(dataset.attrs.get("NX_class")) == "NXentry"
                and f"/{entry_name}/definition" in h5file
            ):
                def_map.update(
                    {
                        entry_name: (
                            definition := h5file[f"/{entry_name}/definition"][
                                ()
                            ].decode("utf8")
                        )
                    }
                )
                logger.debug("Reading entry '%s': '%s'", entry_name, definition)

    return def_map


def _get_nxdl_root(nxdl: str) -> ET.Element:
    definitions_path = get_nexus_definitions_path()
    nxdl_path = os.path.join(
        definitions_path, "contributed_definitions", f"{nxdl}.nxdl.xml"
    )
    if not os.path.exists(nxdl_path):
        nxdl_path = os.path.join(definitions_path, "applications", f"{nxdl}.nxdl.xml")
    if not os.path.exists(nxdl_path):
        raise FileNotFoundError(f"The nxdl file, {nxdl}, was not found.")

    return ET.parse(nxdl_path).getroot()


@click.command()
@click.argument("file")
def verify(file: str):
    """Verifies a nexus file"""

    if not path.exists(file):
        raise click.FileError(file, hint=f'File "{file}" does not exist.')

    if not path.isfile(file):
        raise click.FileError(file, hint=f'"{file}" is not a file.')

    if not is_hdf5(file):
        raise click.FileError(file, hint=f'"{file}" is not a valid HDF5 file.')

    def collect_entries(name: str, dataset: Union[Group, Dataset]):
        clean_name = _replace_group_names(class_map, name)
        if isinstance(dataset, Group) and (
            nx_class := helpers.clean_str_attr(dataset.attrs.get("NX_class"))
        ):
            entry_name = name.rsplit("/", 1)[-1]
            clean_nx_class = nx_class[2:].upper()

            is_variadic = True
            clean_name = _replace_group_names(class_map, name)
            for ref_entry in ref_template:
                if ref_entry.startswith(f"{entry_path}/{clean_name}"):
                    is_variadic = False
                    break

            if is_variadic:
                class_map[entry_name] = clean_nx_class
            logger.debug("Adding class %s to %s", clean_nx_class, entry_name)

        if isinstance(dataset, Dataset):
            logger.debug("Adding field %s/%s", entry_path, clean_name)
            if isinstance(read_data := dataset[()], bytes):
                read_data = read_data.decode("utf-8")
            data_template[f"{entry_path}/{clean_name}"] = read_data

        for attr_name, val in dataset.attrs.items():
            if attr_name == "NX_class":
                continue
            logger.debug(
                "Adding attribute %s/%s/@%s", entry_path, clean_name, attr_name
            )
            data_template[f"{entry_path}/{clean_name}/@{attr_name}"] = val

    def_map = _get_def_map(file)

    if not def_map:
        logger.info("Could not find any valid entry in file %s", file)

    for entry, nxdl in def_map.items():
        data_template = Template()
        class_map: Dict[str, str] = {}
        entry_path = f"/ENTRY[{entry}]"

        ref_template = Template()
        nxdl_root = _get_nxdl_root(nxdl)
        helpers.generate_template_from_nxdl(nxdl_root, ref_template)
        logger.log(DEBUG_TEMPLATE, "Reference template: %s", ref_template)

        with File(file, "r") as h5file:
            h5file[f"/{entry}"].visititems(collect_entries)

        logger.debug("Class map: %s", class_map)
        logger.log(DEBUG_TEMPLATE, "Processed template %s", data_template)
        is_valid = helpers.validate_data_dict(
            ref_template, Template(data_template), nxdl_root
        )

        if is_valid:
            logger.info(
                f"The entry `{entry}` in file `{file}` is a valid file"
                f" according to the `{nxdl}` application definition.",
            )
        else:
            logger.info(
                f"Invalid: The entry `{entry}` in file `{file}` is NOT a valid file"
                f" according to the `{nxdl}` application definition.",
            )
