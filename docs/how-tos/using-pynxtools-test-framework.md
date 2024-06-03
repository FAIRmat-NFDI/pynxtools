# Generalized Test Functionality for `pynxtools` plugins
The `pynxtools` sub-package `testing` is to be utilized to write automated tests for pynxtools reader plugins without requiring in-depth knowledge of the pynxtools internal architecture. The tool supports generalised a general test for all reader plugins, irrespective of the technical details of the raw data files and the internal design of the plugin (note: it is assumed that the plugin was built from the [plugin template](https://github.com/FAIRmat-NFDI/pynxtools-plugin-template) or has the same structure internally).
## Why it is needed
To test integration of a plugin with the `pynxtools` core system, we need to:  
1. Test the plugin's integration with `pynxtools` from the plugin's CI/CD.  
2. Test in the pynxtools's CI/CD if the plugin has been integrated with `pynxtools` properly.
## How to write an integration test for a reader plugin with `pynxtools.testing`
It is very simple to write a test to verify the plugin integration with `pynxtools` within the plugin's tests directory. The developer can place the test where they want, but they need to use the provided test interface from `pynxtools`. An example test for `pynxtools-FOO` (a demo plugin) plugin is given below:

```python
# test_plugin.py

import os

import pytest
from pynxtools.testing.nexus_conversion import ReaderTest

# e.g. module_dir = /pynxtools-foo/tests
module_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.parametrize(
    "nxdl,reader_name,files_or_dir",
    [
        ("NXfoo", "foo", f"{module_dir}/../test/data/test_data_dir_1"),
        ("NXfoo", "foo", f"{module_dir}/../test/data/test_data_dir_2")
    ],
)
def test_foo_reader(nxdl, reader_name, files_or_dir, tmp_path, caplog):
    """Test for the FooReader or foo reader plugin.

    Parameters
    ----------
    nxdl : str
        Name of the NXDL application definition that is to be tested by
        this reader plugin (e.g. NXfoo), without the file ending .nxdl.xml.
    reader_name : str
        Name of the class of the reader (e.g. "foo")
    files_or_dir : class
        Name of the class of the reader.
    tmp_path : pytest.fixture
        Pytest fixture variable, used to create temporary file and clean up the generated files
        after test.
    caplog : pytest.fixture
        Pytest fixture variable, used to capture the log messages during the test.
    """
    # test plugin reader
    test = ReaderTest(nxdl, reader_name, files_or_dir, tmp_path, caplog)
    test.convert_to_nexus()
    # Use `ignore_undocumented` to skip undocumented fields
    # test.convert_to_nexus(ignore_undocumented=True)
    test.check_reproducibility_of_nexus()
```

Alongside the test data in `test/data`, it is also possible to add other types of test data inside the test directory of the plugin.

You can also pass additional parameters to `test.convert_to_nexus`:

- `log_level` (str): Can be either "ERROR" (by default) or "warning". This parameter determines the level at which the caplog is set during testing. If it is "WARNING", the test will also fail if any warnings are reported by the reader.

- `ignore_undocumented` (boolean): If true, the test skipts the verification of undocumented keys. Otherwise, a warning massages for undocumented keys is raised
