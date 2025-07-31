import os
import tempfile
from datetime import datetime, timedelta

import h5py
import numpy as np
import pytest

from pynxtools.dataconverter.hdfdict import LazyHdfDict, dump, load


@pytest.fixture
def sample_data():
    return {
        "int": 42,
        "float": 3.14,
        "str": "hello",
        "list": [1, 2, 3],
        "datetime": datetime(2020, 1, 1, 12, 0, 0),
        "datetimes": [datetime(2020, 1, 1) + timedelta(days=i) for i in range(3)],
        "yaml_obj": {"a": 1, "b": [2, 3]},
        "nested": {"x": 5, "y": "world"},
    }


@pytest.fixture
def hdf_file_path():
    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as f:
        yield f.name
    os.remove(f.name)


def test_dump_and_load_nonlazy(sample_data, hdf_file_path):
    dump(sample_data, hdf_file_path)
    result = load(hdf_file_path, lazy=False)

    assert isinstance(result, dict)
    assert result["int"] == sample_data["int"]
    assert result["float"] == sample_data["float"]
    assert result["str"] == sample_data["str"]
    assert result["list"] == sample_data["list"]
    assert result["datetime"] == sample_data["datetime"]
    assert result["datetimes"] == sample_data["datetimes"]
    assert result["yaml_obj"] == sample_data["yaml_obj"]
    assert result["nested"]["x"] == sample_data["nested"]["x"]
    assert result["nested"]["y"] == sample_data["nested"]["y"]


def test_lazy_loading_unpacks_on_access(sample_data, hdf_file_path):
    dump(sample_data, hdf_file_path)
    result = load(hdf_file_path, lazy=True)

    assert isinstance(result, LazyHdfDict)
    # Initially, result stores h5py.Dataset objects internally,
    # but accessing keys triggers unpacking
    int_value = result["int"]
    assert isinstance(int_value, np.integer)
    assert int_value == sample_data["int"]

    dt_value = result["datetime"]
    assert isinstance(dt_value, datetime)
    assert dt_value == sample_data["datetime"]

    nested_value = result["nested"]
    assert isinstance(nested_value, LazyHdfDict)
    assert nested_value["x"] == sample_data["nested"]["x"]
    assert nested_value["y"] == sample_data["nested"]["y"]


def test_unlazy_method(sample_data, hdf_file_path):
    dump(sample_data, hdf_file_path)
    result = load(hdf_file_path, lazy=False)

    # After unlazying, all keys return plain Python objects
    assert isinstance(result["float"], float)
    assert isinstance(result["datetimes"], list)
    assert isinstance(result["yaml_obj"], dict)
    assert result["yaml_obj"]["b"] == [2, 3]


def test_attributes_storage_and_access(hdf_file_path):
    data = {"array": [1, 2, 3]}
    dump(data, hdf_file_path)

    with h5py.File(hdf_file_path, "a") as f:
        f["array"].attrs["unit"] = "eV"

    loaded = load(hdf_file_path, lazy=False)
    # Attribute keys end with '@'
    assert "array" in loaded
    assert loaded["array"] == [1, 2, 3]


def test_dataset_unpacking_yaml_object(hdf_file_path):
    data = {"custom": {"x": 1, "y": [1, 2]}}
    dump(data, hdf_file_path)

    result = load(hdf_file_path, lazy=False)
    assert isinstance(result["custom"], dict)
    assert result["custom"]["x"] == 1
    assert result["custom"]["y"] == [1, 2]


def test_nested_dicts_loaded_correctly(hdf_file_path):
    nested = {"outer": {"inner": {"val": 123}}}
    dump(nested, hdf_file_path)

    result = load(hdf_file_path, lazy=False)
    assert result["outer"]["inner"]["val"] == 123


def test_ipython_key_completions(sample_data, hdf_file_path):
    dump(sample_data, hdf_file_path)
    result = load(hdf_file_path, lazy=True)

    keys = result._ipython_key_completions_()
    assert isinstance(keys, tuple)
    # Should contain top-level keys
    assert "int" in keys
    assert "nested" in keys
