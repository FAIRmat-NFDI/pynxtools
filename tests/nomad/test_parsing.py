"""This tests that the nexus parsing still works."""

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

import os

import pytest

try:
    from nomad.datamodel import EntryArchive
    from nomad.units import ureg
    from nomad.utils import get_logger
except ImportError:
    pytest.skip("nomad not installed", allow_module_level=True)

from typing import Any

from pynxtools.nomad.parser import NexusParser
from pynxtools.nomad.schema import nexus_metainfo_package
from pynxtools.nomad.utils import _rename_nx_for_nomad as rename_nx_for_nomad


def test_nexus_example():
    archive = EntryArchive()

    example_data = "src/pynxtools/data/201805_WSe2_arpes.nxs"
    NexusParser().parse(example_data, archive, get_logger(__name__))
    arpes_obj = archive.data

    assert arpes_obj.ENTRY[0].SAMPLE[0].pressure__field == ureg.Quantity(
        "3.27e-10*millibar"
    )

    instrument = arpes_obj.ENTRY[0].INSTRUMENT[0]
    assert instrument.nx_name == "instrument"
    assert instrument.monochromator.energy__field == ureg.Quantity(
        "36.49699020385742*electron_volt"
    )
    assert instrument.analyser.entrance_slit_size__field == ureg.Quantity(
        "750 micrometer"
    )
    # good ENUM - x-ray
    assert instrument.SOURCE[0].probe__field == "x-ray"
    # wrong inherited ENUM - Burst (accepted for open enum)
    assert instrument.SOURCE[0].mode__field == "Burst"
    # wrong inherited ENUM for extended field - 'Free Electron Laser' (accepted for open enum)
    assert instrument.SOURCE[0].type__field == "Free Electron Laser"
    data = arpes_obj.ENTRY[0].DATA[0]
    assert len(data.AXISNAME__field) == 3
    # there is still a bug in the variadic name resolution, so skip these
    assert data.delays__field is not None
    assert data.angles__field.check("1/Å")
    # ToDo: if AXISNAME and DATA can be resolved properly, extend this!
    # assert data.delays__field.check("fs")
    # but the following still works
    assert data.energies__field is not None
    assert data.energies__field.check("eV")
    # manual name resolution
    assert data.AXISNAME__field["angles__field"] is not None
    assert data.AXISNAME__max["angles__max"].value == 2.168025463513032
    assert (1 * data.AXISNAME__field["angles__field"].unit).check("1/Å")
    assert (1 * data.AXISNAME__field["delays__field"].unit).check("fs")
    assert data.___axes == "['angles', 'energies', 'delays']"
    # testing attributes
    assert (
        data.AXISNAME__field["angles__field"].attributes.get("m_nx_data_path")
        == "/entry/data/angles"
    )
    assert (
        data.m_get_quantity_attribute("angles__field", "m_nx_data_path")
        == "/entry/data/angles"
    )
    assert data.m_attributes.get("m_nx_data_path") == "/entry/data"


def test_same_name_field_and_group():
    archive = EntryArchive()
    example_data = "tests/data/parser/SiO2onSi.ellips.nxs"
    NexusParser().parse(example_data, archive, get_logger(__name__))
    archive.m_to_dict(with_out_meta=True)


def test_nexus_example_with_renamed_groups():
    archive = EntryArchive()

    lauetof_data = os.path.join(
        os.path.dirname(__file__), "../data/nomad/NXlauetof.hdf5"
    )
    NexusParser().parse(lauetof_data, archive, get_logger(__name__))
    lauetof_obj = archive.data

    assert lauetof_obj.ENTRY[0].name__group.time_of_flight__field == ureg.Quantity(
        "1.0*second"
    )
    assert lauetof_obj.ENTRY[0].sample.name__field == "SAMPLE-CHAR-DATA"
