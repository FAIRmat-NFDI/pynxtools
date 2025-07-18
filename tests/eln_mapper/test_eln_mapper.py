"""This test is dedicated to the generate_eln converter tool."""

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

import os

import yaml
from click import testing

from pynxtools.eln_mapper import eln_mapper


def check_keys_from_two_dict(dict1: dict, dict2: dict, path: str = ""):
    """Compare keys of two dicts and report all differences.

    Parameters
    ----------
    dict1 : dict
        First dictionary to compare.
    dict2 : dict
        Second dictionary to compare.
    path : str, optional
        Current key path being checked (used for recursive calls).
    """
    differences: list[tuple[str, str]] = []

    keys1 = set(dict1.keys())
    keys2 = set(dict2.keys())

    # Find missing and extra keys
    missing_in_dict2 = keys1 - keys2
    missing_in_dict1 = keys2 - keys1

    for key in missing_in_dict2:
        differences.append((f"{path}.{key}".lstrip("."), "Missing in dict2"))

    for key in missing_in_dict1:
        differences.append((f"{path}.{key}".lstrip("."), "Missing in dict1"))

    # Check common keys recursively
    for key in keys1 & keys2:
        val1, val2 = dict1[key], dict2[key]
        if isinstance(val1, dict) and isinstance(val2, dict):
            check_keys_from_two_dict(val1, val2, path=f"{path}.{key}".lstrip("."))

    # Raise error if there are differences
    if differences:
        error_message = "Key mismatches found:\n" + "\n".join(
            f"- {key}: {msg}" for key, msg in differences
        )
        raise AssertionError(error_message)


def test_reader_eln(tmp_path):
    """Test eln that goes with reader.

    Parameters
    ----------
    tmp_path : pathlib.Path
        A temporary path that is created for pytest
    """

    local_dir = os.path.abspath(os.path.dirname(__file__))
    ref_file = os.path.join(local_dir, "../data/eln_mapper/scan.eln_data.yaml")

    test_file = os.path.join(tmp_path, "scan.eln_data.yaml")
    cli_run = testing.CliRunner()
    cli_run.invoke(
        eln_mapper.get_eln,
        [
            "--nxdl",
            "NXscan",
            "--skip-top-levels",
            0,
            "--output-file",
            test_file,
            "--eln-type",
            "reader",
        ],
    )

    with open(ref_file, encoding="utf-8") as ref_f:
        ref_dict = yaml.safe_load(ref_f)

    with open(test_file, encoding="utf-8") as test_f:
        test_dict = yaml.safe_load(test_f)

    check_keys_from_two_dict(ref_dict, test_dict)


def test_scheme_eln(tmp_path):
    """Test Eln that goes in Nomad

    Parameters
    ----------
    tmp_path : pathlib.Path
        A temporary path that is created for pytest
    """

    local_dir = os.path.abspath(os.path.dirname(__file__))
    ref_file = os.path.join(local_dir, "../data/eln_mapper/scan.scheme.archive.yaml")

    test_file = os.path.join(tmp_path, "scan.scheme.archive.yaml")
    cli_run = testing.CliRunner()
    cli_run.invoke(
        eln_mapper.get_eln,
        ["--nxdl", "NXscan", "--output-file", test_file, "--eln-type", "schema"],
    )
    with open(ref_file, encoding="utf-8") as ref_f:
        ref_dict = yaml.safe_load(ref_f)

    with open(test_file, encoding="utf-8") as test_f:
        test_dict = yaml.safe_load(test_f)

    check_keys_from_two_dict(ref_dict, test_dict)
