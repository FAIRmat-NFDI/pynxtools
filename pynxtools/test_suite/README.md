# Generalized Test stuff for pynxtools plugin
This pynxtools sub-package is to be utilized to write automated test for pynxtools plugins without having deep knowledge of the pynxtools architecture. The tool mainly supports for generalised test for all the reader plugins disregarding the technical details of file reader and internal desing of the plugin.
## Why it is needed
To test plugin integration with the `pynxtools` core system. The integration test comes in two ways.
1. Test the plugin's integration with `pynxtools` from the plugin itself.
2. Test if plugin has been integrated with pynxtools properly from pynxtools.

## How integration test from `pynxtools` is build for reader plugins
To setup the integration test in `pynxtools`, one has to follow a specific directory structure in the plugin. The integration test also needs to be included by the test belongs to the plugin that utilize the test interface from `test_suite` subpackage (discussed in the next section). See below for an elaboreate explanation.

Directory structure for `pynstools-FOO` (a demo) plugin

```bash
pynxtools-FOO
 |
 |---examples
 |     |
 |     |---example_1
 |     |     |
 |     |     |---input_file_1.ext
 |     |     |---input_file_2.ext
 |     |     |---out_file.nxs
 |     |---example_2
 |           |
 |           |---input_file_1.ext
 |           |---input_file_2.ext
 |           |---out_file.nxs
 |---pynxtools-FOO
 |     |---<pynxtools-FOO package stuffs>
 |---pyproject.toml
 |---test
       |---data/<test_data>
       |---test_plugin.py
```

This hierarchical structure allows `pynxtools` to set up the integration test for plugin from its own test script. The plugin can add multiple examples for multiple version and type of the raw data files from different experiment techniques. Plugin developers can wish to put other raw files related to the plugin owned test as they want (though usually they go to pynxtools-FOO/test/data/ dir). The `examples` folder must have one or multiple sub-directory where each directory represents a single example of input files (e.g. eln.yaml, raw_file.ext) to launch the plugin reader and a output file of `.nxs` extension genrated by reader from the given banch of input files. Beside the input files, a `test_config.json` (discussed below) file must be defined with the information of `nxdl` (e.g. `NXsts`, `NXmpes`), `reader` (e.g. `STMReader`, `MPESReader`), `plugin_name` (e.g. `pynxtools-stm`, `pynxtools-mpes`) and `example_dir` (e.g. `*`, `*_1`, `example_1`). Therfore, the `test_config.json` gives the content for reader where the test data and other infos. Note that to define the value of the `exmaple_dir` unix style pathname pattern expansion (also used in [glob](https://docs.python.org/3/library/glob.html) lib) can be used, still we recomand to use simply the name of the example directory. A few examples forn `test_condig.json` have been added bellow.

The `test_config.json` can be defined to run on all available example.

```json
# test_config.json
{"launch_data":
    [
        {"nxdl": "NXfoo",
        "reader": "FOOReader",
        "plugin_name": "pynxtools-FOO",
        "example_dir": "*"}
    ]
}
```
The `test_config.json` file can be expanded as
```json
# test_config.json
{"launch_data":
    [
        {"nxdl": "NXfoo",
        "reader": "FOOReader",
        "plugin_name": "pynxtools-FOO",
        "example_dir": "example_1"},
        {"nxdl": "NXfoo",
        "reader": "FOOReader",
        "plugin_name": "pynxtools-FOO",
        "example_dir": "example_2"}
    ]
}
```
**Note** : There might be a case, a specific `example` directory might be intended for a specific `nxdl`. In that case the value of the `nxdl` must be the desired name of `nxdl`.

## How to write integration test from the reader plugin

It is very simple to write a test to verify the plugin integration with `pynxtools` from plugin tests folder. The developer can write the test where they want, only they need to use the provided test interface from `pynxtools`. An example test for `pynxtools-FOO` (a demo) plugin as follows:

```python
# test_plugin.py

import os

from pynxtools_foo.reader import FOOReader
import pytest
from pynxtools.test_suite.reader_plugin import ReaderTest

# /pynxtools-foo/tests dir
module_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.parametrize(
    "nxdl,reader,files_or_dir",
    [
        ("NXfoo", FOOReader, f"{module_dir}/../examples/example_1"),
        ("NXfoo", FOOReader, f"{module_dir}/../examples/example_2"),
        ("NXfoo", FOOReader, f"{module_dir}/data/example_3"),
    ],
)
def test_foo_reader(nxdl, reader, files_or_dir, tmp_path, caplog):
    # test plugin reader
    test = ReaderTest(nxdl, reader, files_or_dir, tmp_path, caplog)
    test.convert_to_nexus()
    test.check_reproducibility_of_nexus()
```

Alonside with the examples in the `examples`, it is also possible to add other examples inside the test directory of the plugin.
