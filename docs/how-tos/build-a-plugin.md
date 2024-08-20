# Build your own pynxtools plugin

Your current data is not supported yet by the [built-in pynxtools readers](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/src/pynxtools/dataconverter/readers) or any of the officially supported [pynxtools plugins](../reference/plugins.md)? 

Don't worry, the following how-to will guide you how to write a reader your own data.


## Getting started
You should start by creating a clean repository that implements the following structure (for a plugin called ```pynxtools-plugin```):
```
pynxtools-plugin
├── .github/workflows
├── docs
│   ├── explanation
│   ├── how-tos
│   ├── reference
│   ├── tutorial
├── src
│   ├── pynxtools_plugin
│       ├── reader.py
├── tests
│   └── data
├── LICENSE
├── mkdocs.yaml
├── dev-requirements.txt
└── pyproject.toml
```

To identify `pynxtools-plugin` as a plugin for pynxtools, an entry point must be established:
```
[project.entry-points."pynxtools.reader"]
mydatareader = "pynxtools_plugin.reader:MyDataReader"
```

Here, we will focus mostly on the `reader.py` file and how to build a reader. For guidelines on how to build the other parts of your plugin, you can have a look here:

- [Documentation writing guide](https://nomad-lab.eu/prod/v1/staging/docs/writing_guide.html)
- [Plugin testing framework](using-pynxtools-test-framework.md)

<!-- Note: There is also a [cookiecutter template](https://github.com/FAIRmat-NFDI/pynxtools-plugin-template) available for creating your own pynxtools plugin, but this is currently not well-maintained.-->


## Writing a Reader

After you have established the main structure, you can start writing your reader. The new reader shall be placed in `reader.py`.

Then implement the reader function:

```python
"""MyDataReader implementation for the DataConverter to convert mydata to NeXus."""
from typing import Tuple, Any

from pynxtools.dataconverter.readers.base.reader import BaseReader

class MyDataReader(BaseReader):
    """MyDataReader implementation for the DataConverter to convert mydata to NeXus."""

    def read(
        self,
        template: dict = None,
        file_paths: Tuple[str] = None,
        objects: Tuple[Any] = None
    ) -> dict:
        """Reads data from given file and returns a filled template dictionary"""
        # Fill the template
        for path in file_paths:
            print(path)

        template["/entry/instrument/scan"] = raw_scan_data

        return template


# This has to be set to allow the convert script to use this reader. Set it to "MyDataReader".
READER = MyDataReader



```
### The reader template dictionary

The read function takes a [`Template`](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/dataconverter/template.py) dictionary, which is used to map from the measurement (meta)data to the concepts defined in the application definition. It contains keys based on the provided NXDL file (you can get an empty template by using `dataconverter generate-template`).

The returned template dictionary should contain keys that exist in the template as defined below. The values of these keys have to be data objects to populate the output NeXus file.
They can be lists, numpy arrays, numpy bytes, numpy floats, numpy ints, ... . Practically you can pass any value that can be handled by the `h5py` package.

Example for a template entry:

```json
{
  "/entry/instrument/source/type": "None"
}
```

For a given NXDL schema, you can generate an empty template with the command
```console
user@box:~$ dataconverter generate-template` --nxdl NXmynxdl
```

#### Naming of groups
In case the NXDL does not define a `name` for the group the requested data belongs to, the template dictionary will list it as `/NAME_IN_NXDL[name_in_output_nexus]`
You can choose any name you prefer instead of the suggested name (see [here](../learn/nexus-rules.md) for the naming conventions). This allows the reader function to repeat groups defined in the NXDL to be outputted to the NeXus file.

```json
{
  "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[my_source]/type": "None"
}
```

#### Attributes
For attributes defined in the NXDL, the reader template dictionary will have the assosciated key with a "@" prefix to the attributes name at the end of the path:

```json
{
  "/entry/instrument/source/@attribute": "None"
}
```

#### Units
If there is a field defined in the NXDL, the converter expects a filled in /data/@units entry in the template dictionary corresponding to the right /data field unless it is specified as NX_UNITLESS in the NXDL. Otherwise, you will get an exception.

```json
{
  "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[my_source]/data": "None",
  "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[my_source]/data/@units": "Should be set to a string value"
}
```

#### Links
You can also define links by setting the value to sub dictionary object with key `link`:

```python
template["/entry/instrument/source"] = {"link": "/path/to/source/data"}
```

### Building off the BaseReader
When building off the [`BaseReader`](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/dataconverter/readers/base/reader.py), the developer has the most flexibility. Any new reader must implement the `read` function, which must return a filled template object.


### Building off the MultiFormatReader
While building on the ```BaseReader``` allows for the most flexibility, in most cases it is desirable to implement a reader that can read in multiple file formats and then populate the template based on the read data. For this purpose, `pynxtools` has the [**`MultiFormatReader`**](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/dataconverter/readers/multi/reader.py), which can be readily extended for your own data.

You can find an extensive how-to guide to build off the `MultiFormatReader` [here](./use-multi-format-reader.md).


## Calling the reader from the command line

The pynxtools converter allows extending support to other data formats by allowing extensions called readers.
The converter provides a dev platform to build a NeXus compatible reader by providing checking against a chosen NeXus Application Definition.

The dataconverter can be executed using:
```console
user@box:~$ dataconverter --reader mydatareader --nxdl NXmynxdl --output path_to_output.nxs
```
Here, the ``--reader`` flag must match the reader name defined in `[project.entry-points."pynxtools.reader"]` in the pyproject.toml file. The NXDL name passed to ``--nxdl``must be a valid NeXus NXDL/XML file in `pynxtools.definitions`.

Aside from this default structure, there are many more flags that can be passed to the dataconverter call. Here is an ouput if its ```help``` call:
```console
Usage: dataconverter [OPTIONS] COMMAND [ARGS]...

Options:
  --help                          Show this message and exit.
  --input-file TEXT               Deprecated: Please use the positional file
                                  arguments instead. The path to the input
                                  data file to read. (Repeat for more than one
                                  file.)
  --reader [example|json_map|json_yml]
                                  The reader to use. default="example"
  --nxdl TEXT                     The name of the NXDL file to use without
                                  extension.This option is required if no '--
                                  params-file' is supplied.
  --output TEXT                   The path to the output NeXus file to be
                                  generated.
  --params-file FILENAME          Allows to pass a .yaml file with all the
                                  parameters the converter supports.
  --ignore-undocumented           Ignore all undocumented fields during
                                  validation.
  --fail                          Fail conversion and don't create an output
                                  file if the validation fails.
  --skip-verify                   Skips the verification routine during
                                  conversion.
  --mapping TEXT                  Takes a <name>.mapping.json file and
                                  converts data from given input files.

Commands:
  convert*           This command allows you to use the converter...
  generate-template  Generates and prints a template to use for your nxdl.

Info:
  You can see more options by using --help for specific commands. For example:
  dataconverter generate-template --help
```