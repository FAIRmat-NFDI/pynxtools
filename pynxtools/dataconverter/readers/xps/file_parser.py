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

# pylint: disable=too-many-lines

"""
Generic Classes for reading XPS files into python dictionary.
"""

from typing import List, Dict

from pynxtools.dataconverter.readers.xps.phi.spe_pro_phi import MapperPhi
from pynxtools.dataconverter.readers.xps.sle.sle_specs import SleMapperSpecs

# from pynxtools.dataconverter.readers.xps.slh.slh_specs import SlhMapperSpecs
from pynxtools.dataconverter.readers.xps.txt.txt_scienta import TxtMapperScienta

# from pynxtools.dataconverter.readers.xps.txt.txt_specs import TxtMapperSpecs
from pynxtools.dataconverter.readers.xps.txt.txt_vamas_export import (
    TxtMapperVamasExport,
)
from pynxtools.dataconverter.readers.xps.vms.vamas import VamasMapper
from pynxtools.dataconverter.readers.xps.xy.xy_specs import XyMapperSpecs
from pynxtools.dataconverter.readers.xps.xml.xml_specs import XmlMapperSpecs


class XpsDataFileParser:
    """Class intended for receiving any type of XPS data file."""

    __prmt_file_ext__ = ["pro", "sle", "spe", "txt", "vms", "xml", "xy"]
    __prmt_metadata_file_ext__ = ["slh"]
    __vendors__ = ["kratos", "phi", "scienta", "specs", "unkwown"]
    __prmt_vndr_cls: Dict[str, Dict] = {
        "pro": {"phi": MapperPhi},
        "sle": {"specs": SleMapperSpecs},
        "spe": {"phi": MapperPhi},
        # "slh": {"specs": SlhMapperSpecs},
        "txt": {
            "scienta": TxtMapperScienta,
            # 'specs': TxtMapperSpecs,
            "unknown": TxtMapperVamasExport,
        },
        "vms": {"unkwown": VamasMapper},
        "xml": {"specs": XmlMapperSpecs},
        "xy": {"specs": XyMapperSpecs},
    }

    __file_err_msg__ = (
        "Need an XPS data file with the following extension: " f"{__prmt_file_ext__}"
    )

    __vndr_err_msg__ = (
        "Need an XPSdata file from the following vendors: " f"{__vendors__}"
    )

    def __init__(self, file_paths: List) -> None:
        """
        Receive XPS file path.

        Parameters
        ----------
        file_paths : List
            XPS file path.
        """
        if isinstance(file_paths, str):
            file_paths = [file_paths]

        self.files = file_paths
        self.config_file = None

        if not self.files:
            raise ValueError(XpsDataFileParser.__file_err_msg__)

    def get_dict(self, **kwargs) -> dict:
        """
            Return python dict fully filled data from xps file.
        Returns
        -------
        python dictionary
        """
        for file in self.files:
            file_ext = file.rsplit(".")[-1]
            if file_ext in XpsDataFileParser.__prmt_file_ext__:
                vendor = XpsDataFileParser.check_for_vendors(file)
                try:
                    parser_class = XpsDataFileParser.__prmt_vndr_cls[file_ext][vendor]
                    parser_obj = parser_class()
                    parser_obj.parse_file(file, **kwargs)
                    self.config_file = parser_obj.config_file
                    return parser_obj.data_dict

                except ValueError as val_err:
                    raise ValueError(XpsDataFileParser.__vndr_err_msg__) from val_err
                except KeyError as key_err:
                    raise KeyError(XpsDataFileParser.__vndr_err_msg__) from key_err
            else:
                raise ValueError(XpsDataFileParser.__file_err_msg__)
        return {}

    @classmethod
    def check_for_vendors(cls, file: str) -> str:
        """
        Check for the vendor name of the XPS data file.

        """
        file_ext = file.rsplit(".")[-1]

        vendor_dict = XpsDataFileParser.__prmt_vndr_cls[file_ext]

        if len(vendor_dict) == 1:
            return list(vendor_dict.keys())[0]
        if file_ext == "txt":
            return cls._check_for_vendors_txt(file)
        return None

    @classmethod
    def _check_for_vendors_txt(cls, file: str) -> str:
        """
        Search for a vendor names in a txt file

        Parameters
        ----------
        file : str
            XPS txt file.

        Returns
        -------
        vendor
            Vendor name if that name is in the txt file.

        """
        vendor_dict = XpsDataFileParser.__prmt_vndr_cls["txt"]

        with open(file, encoding="utf-8") as txt_file:
            contents = txt_file.read()

        for vendor in vendor_dict:
            vendor_options = [vendor, vendor.upper(), vendor.capitalize()]

            if any(vendor_opt in contents for vendor_opt in vendor_options):
                return vendor
        return "unknown"
