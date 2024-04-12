# Generalized Test stuff for pynxtools plugin
This pynxtools sub-package is to be utilized to write automated test for pynxtools plugins without having deep knowledge of the pynxtools architecture. The tool mainly supports for generalised test for all the reader plugins disregarding the technical details of file reader and internal desing of the plugin.
## Why it is needed
To test plugin integartion with `pynxtools` core system. The integration test could come in two ways.
1. Test is plugin's integration with `pynxtools` from the plugin itself.
2. Test if plugin has been integrated with pynxtools properly from pynxtools.

## How to setup integration test from plugin
To setup the integration test from plugin itself one has to follow a definite directory structure in plugin. The plugin test also needs to include a specific test for that hooks from `test_suite` subpackage. Here, the discussion will be extended elaborately.

`Folder structure` for `pynstools-FOO` plugin

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

This hierarchical structure allows `pynxtools` to set up the integration for plugin test from its own test script. Plugin can add multiple example for multiple version and type of the raw data files from an experiment techniques. Plugin developers can wish to put other raw files related to the plugin owned test as they want (though usually they go to test/data/ dir).

**TODO**:
**1. Think about to store the pynxtools versions in a file of plugin which sinifies of the plugin integration in pynxtools.**


