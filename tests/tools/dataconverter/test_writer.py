"""Test cases for the Writer class used by the DataConverter"""

import os

import pytest
import h5py
import numpy as np

from nexusparser.tools.dataconverter.writer import Writer


@pytest.fixture(name="writer")
def fixture_writer(tmp_path):
    """pytest fixture to setup Writer object to be used by tests with dummy data."""
    writer = Writer(
        {
            ("/ENTRY[my_entry]/INSTRUMENT[our_instrument]/"
             "FERMI_CHOPPER[their_fermi_chopper]/energy"): "Value",
            ("/ENTRY[my_entry]/INSTRUMENT[our_instrument]/"
             "FERMI_CHOPPER[their_fermi_chopper]/energy/@units"): "units",
            ("/ENTRY[my_entry]/INSTRUMENT[our_instrument]/"
             "FERMI_CHOPPER[their_fermi_chopper]/numpy"): np.zeros(3)
        },
        "tests/data/dataconverter/NXspe.nxdl.xml",
        os.path.join(tmp_path, "test.nxs")
    )
    yield writer
    del writer


def test_init(writer):
    """Test to verify Writer's initialization works."""
    assert isinstance(writer, Writer)


def test_write(writer):
    """Test for the Writer's write function. Checks whether entries given above get written out."""
    writer.write()
    assert writer.nxdl_name == "NXspe"
    test_nxs = h5py.File(writer.output_path, "r")
    assert test_nxs["/my_entry/our_instrument/their_fermi_chopper/energy"].asstr()[...] == "Value"  # pylint: disable=no-member
    assert test_nxs["/my_entry/our_instrument/their_fermi_chopper/energy"].attrs["units"] == "units"
    assert test_nxs["/my_entry/our_instrument/their_fermi_chopper/numpy"].shape == (3,)  # pylint: disable=no-member
