# Generalized Test stuff for pynxtools plugin
This pynxtools sub-package is to be utilized to write automated test for pynxtools plugins without having deep knowledge of the pynxtools architecture. The tool mainly supports for generalised test for all the reader plugins disregarding the technical details of file reader and internal desing of the plugin.
## Why it is needed
To test plugin integartion with `pynxtools` core system. The integration test could come in two ways.
1. Test is plugin's integration with `pynxtools` from the plugin itself.
2. Test if plugin has been integrated with pynxtools properly from pynxtools.

## How to setup integration test from plugin
To setup the integration test from plugin itself one has to follow a definite directory structure in plugin. The plugin test also needs to include a specific test for that hooks from `test_suite` subpackage. Here, the discussion will be extended elaborately.

Directory structure for `pynstools-FOO` plugin

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
       |---plugin_test.py
```

This hierarchical structure allows `pynxtools` to set up the integration for plugin test from its own test script. Plugin can add multiple example for multiple version and type of the raw data files from an experiment techniques. Plugin developers can wish to put other raw files related to the plugin owned test as they want (though usually they go to test/data/ dir). The `examples` folder must have one or multiple sub-directory where each directory represents a single example of input files (e.g. eln.yaml, raw_file.ext) to launch the plugin reader and a output file of `.nxs` extension genrated by reader from the given banch of input files. Beside the input files, a `test_config.json` file must be defined with the information of `nxdl` (e.g. `NXsts`, `NXmpes`), `reader` (e.g. `STMReader`, `MPESReader`), `plugin_name` (e.g. `pynxtools-stm`, `pynxtools-mpes`) and `example_dir` (e.g. `*`, `*_1`, `example_1`). Note that to define the value of the `exmaple_dir` unix style pathname pattern expansion (also used in [glob](https://docs.python.org/3/library/glob.html) lib), still we recomand to use simply the name of the example directory. A few examples forn `test_condig.json` has been added bellow.

The `test_config.json` can be defined to run on all available example.

```json
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
**Note** : There might be a case, a specific `exmaple` directory might be intended for a specific `nxdl`. In that case the value of the `nxdl` the be desired name of `nxdl`.

## Test in plugin

**TODO: Add how to create the package of the plugin of pynxtools.**


