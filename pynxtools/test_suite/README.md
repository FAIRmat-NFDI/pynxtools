# Generalized Test stuff for pynxtools plugin
This pynxtools sub-package is to be utilized to write automated test for pynxtools plugins without having deeper knowledge of the pynxtools internal architecture. The tool mainly supports for generalised test for all the reader plugins disregarding the technical details of file reader and internal design of the plugin (It is assumed that the plugin has followed the [plugin template](https://github.com/FAIRmat-NFDI/pynxtools-plugin-template)).

## Why it is needed
To test plugin integration with the `pynxtools` core system. The integration test comes in two ways.
1. Test the plugin's integration with `pynxtools` from the plugin's ci/cd.
2. Test from pynxtools as pynxtools's ci/cd if plugin has been integrated with `pynxtools` properly.

## How to write integration test from the reader plugin

It is very simple to write a test to verify the plugin integration with `pynxtools` from plugin tests directory. The developer can write the test where they want, only they need to use the provided test interface from `pynxtools`. An example test for `pynxtools-FOO` (a demo plugin name) plugin as follows:

```python
# test_plugin.py

import os

from pynxtools_foo.reader import FOOReader
import pytest
from pynxtools.test_suite.reader_plugin import ReaderTest

# e.g. module_dir = /pynxtools-foo/tests
module_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.parametrize(
    "nxdl,reader,files_or_dir",
    [
        ("NXfoo", FOOReader, f"{module_dir}/../examples/test_data_dir_1"),
        ("NXfoo", FOOReader, f"{module_dir}/../examples/test_data_dir_2"),
        ("NXfoo", FOOReader, f"{module_dir}/data/test_data_dir_2"),
    ],
)
def test_foo_reader(nxdl, reader, files_or_dir, tmp_path, caplog):
    """Test for the FooReader or foo reader plugin.

    Parameters
    ----------
    nxdl : str
        Name of the NXDL file e.g. NXfoo from NXfoo.nxdl.xml.
    reader : sts
        _description_
    files_or_dir : class
        Name of the class of the reader.
    tmp_path : pytest.fixture
        Pytest fixture parameters.
    caplog : pytest.fixture
        Log capture from pytest.
    """
    # test plugin reader
    test = ReaderTest(nxdl, reader, files_or_dir, tmp_path, caplog)
    test.convert_to_nexus()
    test.check_reproducibility_of_nexus()
```

Alonside with the examples in the `examples`, it is also possible to add other examples inside the test directory of the plugin.
