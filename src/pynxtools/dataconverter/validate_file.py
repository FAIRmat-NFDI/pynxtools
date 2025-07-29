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
from typing import Union

import click
from h5py import File, is_hdf5

from pynxtools.dataconverter import helpers
from pynxtools.dataconverter.validation import validate_hdf_group_against

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _get_def_map(file: str) -> dict[str, str]:
    """
    Extract the application definitions used by each NXentry in a NeXus HDF5 file.

    Args:
        file (str): Path to the NeXus HDF5 file.

    Returns:
        dict[str, str]: A mapping from NXentry names to their corresponding
                        NXDL (NeXus Definition Language) application definitions.
    """
    def_map: dict[str, str] = {}
    with File(file, "r") as h5file:
        for entry_name, dataset in h5file.items():
            if (
                helpers.clean_str_attr(dataset.attrs.get("NX_class")) == "NXentry"
                and f"/{entry_name}/definition" in h5file
            ):
                def_map.update(
                    {entry_name: h5file[f"/{entry_name}/definition"][()].decode("utf8")}
                )

    return def_map


def validate(file: str, ignore_undocumented: bool = False):
    """
    Validate a NeXus HDF5 file against its declared application definitions.

    Args:
        file (str): Path to the NeXus HDF5 file.
        ignore_undocumented (bool): If True, ignore undocumented concepts during validation.

    Raises:
        click.FileError: If the file does not exist, is not a file, or is not a valid HDF5 file.
    """
    if not path.exists(file):
        raise click.FileError(file, hint=f'File "{file}" does not exist.')

    if not path.isfile(file):
        raise click.FileError(file, hint=f'"{file}" is not a file.')

    if not is_hdf5(file):
        raise click.FileError(file, hint=f'"{file}" is not a valid HDF5 file.')

    def_map = _get_def_map(file)

    if not def_map:
        logger.warning(f"Could not find any valid entry in file {file}")

    with File(file, "r") as h5file:
        for entry, nxdl in def_map.items():
            is_valid = validate_hdf_group_against(
                nxdl,
                h5file[entry],
                file,
                ignore_undocumented,
            )

            if is_valid:
                logger.info(
                    f"The entry `{entry}` in file `{file}` is valid"
                    f" according to the `{nxdl}` application definition.",
                )
            else:
                logger.info(
                    f"Invalid: The entry `{entry}` in file `{file}` is NOT valid"
                    f" according to the `{nxdl}` application definition.",
                )


@click.command()
@click.argument(
    "file",
    type=click.Path(exists=True),
)
@click.option(
    "--ignore-undocumented",
    is_flag=True,
    default=False,
    help="Ignore all undocumented concepts during validation.",
)
def validate_cli(file: str, ignore_undocumented: bool = False):
    """
    Validates a NeXus HDF5 file.

    FILE: The path to the NeXus file to validate.
    """
    validate(file, ignore_undocumented)
