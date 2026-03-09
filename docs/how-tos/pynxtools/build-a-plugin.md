# Build your own pynxtools plugin

The `pynxtools` [dataconverter](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/src/pynxtools/dataconverter) converts experimental data to NeXus/HDF5 files based on any provided [NXDL schema](https://manual.nexusformat.org/nxdl.html). New data formats are supported by writing *readers*, either directly in pynxtools or as separate *plugins*.

There are [built-in readers](../../reference/built-in-readers.md) for generic use cases and [reader plugins](../../reference/plugins.md) for specific experimental techniques. If your data is not yet covered, this guide shows how to write your own.

## Repository structure

Start with a clean repository using this structure (for a plugin called `pynxtools-myplugin`):

```
pynxtools-myplugin/
├── .github/workflows/
├── docs/
│   ├── explanation/
│   ├── how-tos/
│   ├── reference/
│   └── tutorial/
├── src/
│   └── pynxtools_myplugin/
│       └── reader.py
├── tests/
│   └── data/
├── LICENSE
├── mkdocs.yaml
└── pyproject.toml
```

## Registering the plugin

To make `pynxtools` discover your reader, declare an entry point in `pyproject.toml`:

```toml title="pyproject.toml"
[project.entry-points."pynxtools.reader"]
myplugin = "pynxtools_myplugin.reader:MyDataReader"
```

The key (`myplugin`) is the name passed to `--reader` on the command line. If your plugin ships multiple readers, each needs its own entry point.

## Choosing a base class

| Base class | Use when |
|---|---|
| `MultiFormatReader` | You need to handle multiple file formats, use a config/mapping file, or want built-in ELN/metadata callbacks. **Recommended for almost all new readers.** |
| `BaseReader` | Your format is unusual enough that the `MultiFormatReader` pipeline does not apply. Maximum flexibility, minimum scaffolding. |

## Option A — Building off `MultiFormatReader` (recommended)

`MultiFormatReader` provides a structured pipeline: file dispatch by extension, template setup, object handling, config parsing, and post-processing. All new FAIRmat readers extend it.

```python title="reader.py"
from typing import Any

from pynxtools.dataconverter.readers.multi.reader import MultiFormatReader


class MyDataReader(MultiFormatReader):
    """Reader for my instrument format."""

    supported_nxdls = ["NXmynxdl"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extensions = {
            ".yaml": self.handle_eln_file,
            ".json": self.set_config_file,
            # add handlers for your instrument format here
        }

    # Override only the pipeline hooks you need:
    # setup_template, handle_objects, post_process,
    # get_attr, get_data, get_eln_data, get_data_dims

READER = MyDataReader
```

See the [MultiFormatReader how-to guide](./use-multi-format-reader.md) for a full worked example, and [The MultiFormatReader](../../learn/pynxtools/multi-format-reader.md) for an in-depth explanation of each pipeline stage.

## Option B — Building off `BaseReader`

When `MultiFormatReader` is too prescriptive, implement `read` directly:

```python title="reader.py"
from typing import Any

from pynxtools.dataconverter.readers.base.reader import BaseReader


class MyDataReader(BaseReader):
    """Reader for my instrument format."""

    supported_nxdls = ["NXmynxdl"]

    def read(
        self,
        template: dict = None,
        file_paths: tuple[str] = None,
        objects: tuple[Any] = None,
    ) -> dict:
        """Read input files and return the filled template."""
        # Example:
        # template["/ENTRY[entry]/instrument/name"] = "my_instrument"
        return template

READER = MyDataReader
```

### The `Template` dictionary

The `template` parameter is a [`Template`](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/dataconverter/template.py) object pre-populated with `None` values for all keys defined in the target NXDL. Keys follow the NXDL bracket notation:

```python
# Simple field
template["/ENTRY[entry]/instrument/name"] = "my_instrument"

# Field with units
template["/ENTRY[entry]/instrument/source/energy"] = 12.5
template["/ENTRY[entry]/instrument/source/energy/@units"] = "keV"

# Attribute
template["/ENTRY[entry]/instrument/@version"] = "1.0"

# HDF5 link
template["/ENTRY[entry]/data/raw"] = {"link": "/entry/instrument/detector/data"}
```

Generate an empty template to see all available keys:

```bash
dataconverter generate-template --nxdl NXmynxdl
```

#### Group naming

When the NXDL does not fix the group name, the template uses uppercase concept notation:

```json
{ "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[my_source]/type": null }
```

You may use any name instead of the suggested lowercase one. This also enables repeating groups defined in the NXDL.

#### Units

Every field with a unit category in the NXDL requires a corresponding `/@units` entry:

```json
{
  "/ENTRY[my_entry]/instrument/source/energy": null,
  "/ENTRY[my_entry]/instrument/source/energy/@units": null
}
```

A warning is shown during conversion if the units entry is missing.

## Running the reader

```bash
dataconverter --reader myplugin --nxdl NXmynxdl --output out.nxs input.dat
```

The `--reader` value must match the entry point key in `pyproject.toml`. The NXDL name must correspond to a valid XML file in `pynxtools.definitions`.

For the full CLI reference, see [here](../../reference/cli-api.md#data-conversion).

## Testing

Use the `pynxtools` testing framework to write round-trip tests for your reader:

- [Using the pynxtools test framework](./using-pynxtools-test-framework.md)
- [Running tests in parallel](./run-tests-in-parallel.md)
