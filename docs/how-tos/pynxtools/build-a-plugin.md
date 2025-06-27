# Build your own pynxtools plugin

The pynxtools [dataconverter](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/src/pynxtools/dataconverter) is used to convert experimental data to NeXus/HDF5 files based on any provided [NXDL schemas](https://manual.nexusformat.org/nxdl.html). The converter allows extending support to other data formats by allowing extensions called `readers`.  There exist a set of [built-in pynxtools readers](../reference/built-in-readers.md) as well as [pynxtools reader plugins](../reference/plugins.md) to convert supported data files for some experimental techniques into NeXus-compliant files.

Your current data is not supported yet by the built-in pynxtools readers or the officially supported pynxtools plugins?

Don't worry, the following how-to will guide you through the steps of writing a reader for your own data.

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

To identify `pynxtools-plugin` as a plugin for pynxtools, an entry point must be established (in the `pyproject.toml` file):

``` toml title="pyproject.toml"
[project.entry-points."pynxtools.reader"]
mydatareader = "pynxtools_plugin.reader:MyDataReader"
```

Note that it is also possible that your plugin contains multiple readers. In that case, each reader must have its unique entry point.

Here, we will focus mostly on the `reader.py` file and how to build a reader. For guidelines on how to build the other parts of your plugin, you can have a look here:

- [Documentation writing guide](https://nomad-lab.eu/prod/v1/staging/docs/writing_guide.html)
- [Plugin testing framework](using-pynxtools-test-framework.md)

<!-- Note: There is also a [cookiecutter template](https://github.com/FAIRmat-NFDI/pynxtools-plugin-template) available for creating your own pynxtools plugin, but this is currently not well-maintained.-->

## Writing a Reader

After you have established the main structure, you can start writing your reader. The new reader shall be placed in `reader.py`.

Then implement the reader function:

```python title="reader.py"
"""MyDataReader implementation for the DataConverter to convert mydata to NeXus."""
from typing import Any

from pynxtools.dataconverter.readers.base.reader import BaseReader

class MyDataReader(BaseReader):
    """MyDataReader implementation for the DataConverter to convert mydata to NeXus."""

    supported_nxdls = [
        "NXmynxdl" # this needs to be changed during implementation.
    ]

    def read(
        self,
        template: dict = None,
        file_paths: tuple[str] = None,
        objects: tuple[Any] = None
    ) -> dict:
        """Reads data from given file and returns a filled template dictionary"""
        # Here, you must provide functionality to fill the the template, see below.
        # Example:
        # template["/entry/instrument/name"] = "my_instrument"

        return template


# This has to be set to allow the convert script to use this reader. Set it to "MyDataReader".
READER = MyDataReader
```

### The reader template dictionary

The read function takes a [`Template`](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/dataconverter/template.py) dictionary, which is used to map from the measurement (meta)data to the concepts defined in the NeXus application definition. The template contains keys that match the concepts in the provided NXDL file.

The returned template dictionary should contain keys that exist in the template as defined below. The values of these keys have to be data objects to populate the output NeXus file.
They can be lists, numpy arrays, numpy bytes, numpy floats, numpy integers, ... . Practically you can pass any value that can be handled by the `h5py` package.

Example for a template entry:

```json
{
  "/entry/instrument/source/type": "None"
}
```

For a given NXDL schema, you can generate an empty template with the command

```console
user@box:~$ dataconverter generate-template --nxdl NXmynxdl
```

#### Naming of groups

In case the NXDL does not define a `name` for the group the requested data belongs to, the template dictionary will list it as `/NAME_IN_NXDL[name_in_output_nexus]`. You can choose any name you prefer instead of the suggested `name_in_output_nexus` (see [here](../learn/nexus-rules.md) for the naming conventions). This allows the reader function to repeat groups defined in the NXDL to be outputted to the NeXus file.

```json
{
  "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[my_source]/type": "None"
}
```

#### Attributes

For attributes defined in the NXDL, the reader template dictionary will have the associated key with a "@" prefix to the attributes name at the end of the path:

```json
{
  "/entry/instrument/source/@attribute": "None"
}
```

#### Units

If there is a field defined in the NXDL, the converter expects a filled in `/data/@units` entry in the template dictionary corresponding to the right `/data` field unless it is specified as `NX_UNITLESS` in the NXDL. Otherwise, a warning will be shown.

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

### Building off of the BaseReader

When building off the [`BaseReader`](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/dataconverter/readers/base/reader.py), the developer has the most flexibility. Any new reader must implement the `read` function, which must return a filled template object.

### Building off of the MultiFormatReader

While building on the ```BaseReader``` allows for the most flexibility, in most cases it is desirable to implement a reader that can read in multiple file formats and then populate the template based on the read data. For this purpose, `pynxtools` has the [**`MultiFormatReader`**](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/dataconverter/readers/multi/reader.py), which can be readily extended for your own data.

You can find an extensive how-to guide to build off the `MultiFormatReader` [here](./use-multi-format-reader.md).

## Calling the reader from the command line

The dataconverter can be executed using:

```console
user@box:~$ dataconverter --reader mydatareader --nxdl NXmynxdl --output path_to_output.nxs
```

Here, the ``--reader`` flag must match the reader name defined in `[project.entry-points."pynxtools.reader"]` in the pyproject.toml file. The NXDL name passed to ``--nxdl``must be a valid NeXus NXDL/XML file in `pynxtools.definitions`.

Aside from this default structure, there are many more flags that can be passed to the
dataconverter call. Here is its API:
::: mkdocs-click
    :module: pynxtools.dataconverter.convert
    :command: convert_cli
    :prog_name: dataconverter
    :depth: 2
    :style: table
    :list_subcommands: True
