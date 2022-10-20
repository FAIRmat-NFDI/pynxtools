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
"""Perkin Ellmer transmission file reader implementation for the DataConverter."""
from inspect import isfunction
from typing import Callable, List, Any, Dict
import pandas as pd

from nexusutils.dataconverter.readers.json_yml.reader import YamlJsonReader
import nexusutils.dataconverter.readers.transmission.metadata_parsers as mpars
from nexusutils.dataconverter.readers.utils import parse_json, parse_yml


# Dictionary mapping metadata in the asc file to the paths in the NeXus file.
# The entry can either be a function with one list parameter
# which is executed to fill the specific path or an
# integer which is used to get the value at the index of the metadata.
# If the value is a str this string gets inputed at the path.
METADATA_MAP: Dict[str, Any] = {
    "/ENTRY[entry]/SAMPLE[sample]/name": 8,
    "/ENTRY[entry]/start_time": mpars.read_start_date,
    "/ENTRY[entry]/instrument/sample_attenuator/attenuator_transmission":
        mpars.read_sample_attenuator,
    "/ENTRY[entry]/instrument/ref_attenuator/attenuator_transmission":
        mpars.read_ref_attenuator,
    "/ENTRY[entry]/instrument/spectrometer/GRATING[grating]/wavelength_range":
        mpars.read_uv_monochromator_range,
    "/ENTRY[entry]/instrument/spectrometer/GRATING[grating1]/wavelength_range":
        mpars.read_visir_monochromator_range,
    "/ENTRY[entry]/instrument/SOURCE[source]/type": "D2",
    "/ENTRY[entry]/instrument/SOURCE[source]/wavelength_range":
        mpars.get_d2_range,
    "/ENTRY[entry]/instrument/SOURCE[source1]/type": "halogen",
    "/ENTRY[entry]/instrument/SOURCE[source1]/wavelength_range":
        mpars.get_halogen_range
}
# Dictionary to map value during the yaml eln reading
# This is typically a mapping from ELN signifier to NeXus path
CONVERT_DICT: Dict[str, str] = {
    'Sample': 'SAMPLE[sample]',
    "unit": "@units"
}
# Dictionary to map nested values during the yaml eln reading
# This is typically a mapping from nested ELN signifiers to NeXus group
REPLACE_NESTED: Dict[str, str] = {
    'Sample[sample]/experiment_identifier': 'experiment_identifier'
}


def data_to_template(data: pd.DataFrame) -> Dict[str, Any]:
    """Builds the data entry dict from the data in a pandas dataframe

    Args:
        data (pd.DataFrame): The dataframe containing the data.

    Returns:
        Dict[str, Any]: The dict with the data paths inside NeXus.
    """
    template: Dict[str, Any] = {}
    template["/ENTRY[entry]/data/@axes"] = "wavelength"
    template["/ENTRY[entry]/data/type"] = "transmission"
    template["/ENTRY[entry]/data/@signal"] = "transmission"
    template["/ENTRY[entry]/data/wavelength"] = data.index.values
    template["/ENTRY[entry]/instrument/spectrometer/wavelength"] = data.index.values
    template["/ENTRY[entry]/data/wavelength/@units"] = "nm"
    template["/ENTRY[entry]/data/transmission"] = data.values[:, 0]
    template["/ENTRY[entry]/instrument/measured_data"] = data.values

    return template


def parse_detector_line(line: str, convert: Callable[[str], Any] = None) -> List[Any]:
    """Parses a detector line from the asc file.

    Args:
        line (str): The line to parse.

    Returns:
        List[Any]: The list of detector settings.
    """
    if convert is None:
        def convert(val):
            return val
    return [convert(s.split('/')[-1]) for s in line.split()]


# pylint: disable=too-many-arguments
def convert_detector_to_template(
        det_type: str,
        slit: str,
        time: float,
        gain: float,
        det_idx: int,
        wavelength_range: List[float]
) -> Dict[str, Any]:
    """Writes the detector settings to the template.

    Args:
        det_type (str): The detector type.
        slit (float): The slit width.
        time (float): The exposure time.
        gain (str): The gain setting.

    Returns:
        Dict[str, Any]: The dictionary containing the data readout from the asc file.
    """
    if det_idx == 0:
        path = '/ENTRY[entry]/instrument/DETECTOR[detector]'
    else:
        path = f'/ENTRY[entry]/instrument/DETECTOR[detector{det_idx}]'
    template: Dict[str, Any] = {}
    template[f"{path}/type"] = det_type
    template[f"{path}/response_time"] = time
    if gain is not None:
        template[f"{path}/gain"] = gain

    if slit == "servo":
        template[f"{path}/slit/type"] = "servo"
    else:
        template[f"{path}/slit/type"] = "fixed"
        template[f"{path}/slit/x_gap"] = float(slit)
        template[f"{path}/slit/x_gap/@units"] = "nm"

    template[f"{path}/wavelength_range"] = wavelength_range

    return template


def read_detectors(metadata: list) -> Dict[str, Any]:
    """Reads detector values from the metadata and writes them into a template
    with the appropriate NeXus path."""

    template: Dict[str, Any] = {}
    detector_slits = parse_detector_line(metadata[31])
    detector_times = parse_detector_line(metadata[32], float)
    detector_gains = parse_detector_line(metadata[35], float)
    detector_changes = [float(x) for x in metadata[43].split()]
    wavelength_ranges = \
        [mpars.MIN_WAVELENGTH] + detector_changes[::-1] + [mpars.MAX_WAVELENGTH]

    template.update(
        convert_detector_to_template(
            "PMT", detector_slits[2], detector_times[2],
            None, 2, [wavelength_ranges[0], wavelength_ranges[1]]
        )
    )

    for name, idx in zip(["PbS", "InGaAs"], [1, 0]):
        template.update(
            convert_detector_to_template(
                name,
                detector_slits[idx],
                detector_times[idx],
                detector_gains[idx],
                idx,
                [wavelength_ranges[2 - idx], wavelength_ranges[3 - idx]]
            )
        )

    return template


def parse_asc(file_path: str) -> Dict[str, Any]:
    """Parses a Perkin Ellmer asc file into metadata and data dictionary.

    Args:
        file_path (str): File path to the asc file.

    Returns:
        Dict[str, Any]: Dictionary containing the metadata and data from the asc file.
    """
    template: Dict[str, Any] = {}
    data_start_ind = "#DATA"

    with open(file_path, encoding="utf-8") as fobj:
        metadata = []
        for line in fobj:
            if line.strip() == data_start_ind:
                break
            metadata.append(line.strip())

        data = pd.read_csv(
            fobj, delim_whitespace=True, header=None, index_col=0
        )

    for path, val in METADATA_MAP.items():
        # If the dict value is an int just get the data with it's index
        if isinstance(val, int):
            template[path] = metadata[val]
        elif isinstance(val, str):
            template[path] = val
        elif isfunction(val):
            template[path] = val(metadata)
        else:
            print(
                f"WARNING: "
                f"Invalid type value {type(val)} of entry '{path}:{val}' in METADATA_MAP"
            )

    template.update(read_detectors(metadata))
    template.update(data_to_template(data))

    return template


def add_def_info() -> Dict[str, str]:
    """Creates a template with definition version information"""
    template: Dict[str, Any] = {}
    template["/@default"] = "entry"
    template["/ENTRY[entry]/@default"] = "data"
    template["/ENTRY[entry]/definition"] = "NXtransmission"
    template["/ENTRY[entry]/definition/@version"] = "v2022.06"
    template["/ENTRY[entry]/definition/@url"] = \
        "https://fairmat-experimental.github.io/nexus-fairmat-proposal/" + \
        "50433d9039b3f33299bab338998acb5335cd8951/index.html"

    return template


# pylint: disable=too-few-public-methods
class TransmissionReader(YamlJsonReader):
    """TransmissionReader implementation for the DataConverter
    to convert transmission data to Nexus."""

    supported_nxdls = ["NXtransmission"]
    extensions = {
        ".asc": parse_asc,
        ".json": parse_json,
        ".yml": lambda fname: parse_yml(fname, CONVERT_DICT, REPLACE_NESTED),
        ".yaml": lambda fname: parse_yml(fname, CONVERT_DICT, REPLACE_NESTED),
        "default": lambda _: add_def_info()
    }


READER = TransmissionReader
