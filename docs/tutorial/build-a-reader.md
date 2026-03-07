# Workshop: Build your own pynxtools reader

## Introduction

In this workshop you will build a working pynxtools reader from scratch.
By the end you will have a reader that converts instrument data from an HDF5 file
and user-provided metadata from a YAML file into a fully validated NeXus/HDF5 file
that conforms to the `NXsimple` application definition.

The workflow you will follow is the standard pattern used by all pynxtools plugins
in production (e.g. pynxtools-xps, pynxtools-mpes):

```
instrument file (.h5)  ─┐
ELN file (.yaml)        ├─▶  reader.py  ─▶  config file (.json)  ─▶  output.nxs
                        ─┘
```

## Prerequisites

- Basic Python knowledge
- `git` installed
- `uv` or `pip` available
- A terminal and a code editor

## Setup

### 1. Create your plugin from the template

The workshop uses a special branch of the pynxtools plugin template that already
contains the reader scaffold, example data, and the correct application definition.

```bash
pip install cookiecutter
cookiecutter gh:FAIRmat-NFDI/pynxtools-plugin-template --checkout workshop
```

When prompted, enter:

| Prompt | Value |
|---|---|
| `reader_name` | `myreader` |
| `supported_nxdl` | `NXsimple` |
| `short_description` | `My first pynxtools reader` |

This creates a directory `pynxtools-myreader/`. Enter it:

```bash
cd pynxtools-myreader
```

### 2. Install pynxtools from the workshop branch

The `NXsimple` application definition is only available in the pynxtools `workshop`
branch, which is what makes the converter and validator aware of it:

```bash
pip install "pynxtools @ git+https://github.com/FAIRmat-NFDI/pynxtools.git@workshop"
```

### 3. Install your plugin in editable mode

```bash
pip install -e ".[dev]"
```

### 4. Verify the setup

```bash
dataconverter --help
```

You should see the dataconverter CLI without errors.

---

## The data you will work with

The template ships with example data in `tests/data/workshop-example/`:

| File | Description |
|---|---|
| `mock_data.h5` | Instrument HDF5 output — signal data + instrument metadata |
| `eln_data.yaml` | Electronic lab notebook — user and sample metadata |
| `config_file.json` | Mapping config — **you will write this in Exercise 6** |
| `NXsimple.nxdl.xml` | The target application definition (for reference) |

### HDF5 file structure

Open `mock_data.h5` in any HDF5 viewer (e.g. `h5ls -r tests/data/workshop-example/mock_data.h5`)
or run the following in Python:

```python
import h5py

with h5py.File("tests/data/workshop-example/mock_data.h5", "r") as f:
    def show(name, obj):
        print(name, "=", obj[()] if isinstance(obj, h5py.Dataset) else "")
    f.visititems(show)
```

The structure is:

```
data/
  x_values          → float64 array (100,)   [eV]
  y_values          → float64 array (100,)   [counts_per_second]
  x_units           → b"eV"
  y_units           → b"counts_per_second"
metadata/
  instrument/
    version         → 1.0
    detector/
      name          → b"my_gaussian_detector"
      count_time    → 1.2
      count_time_units → b"s"
```

### ELN file structure

`eln_data.yaml` contains the metadata you would typically fill in through a lab
notebook or web form:

```yaml title="eln_data.yaml"
title: My experiment
user:
  name: John Doe
  address: 123 Science Rd, Data City, DC
sample:
  name: my_sample
  physical_form: powder
  temperature:
    value: 300
    unit: K
```

---

## The target application definition

`NXsimple` defines what a valid output file must contain.
Open `tests/data/workshop-example/NXsimple.nxdl.xml` and identify which fields are:

- **required** (default — no `optional` or `recommended` attribute)
- **recommended** (should be provided if possible)
- **optional** (may be omitted)

You can also generate a template to see all expected keys:

```bash
dataconverter generate-template --nxdl NXsimple
```

The template lists every path that `NXsimple` expects, together with whether it is
required. Keep this output open — you will need it when writing the config file.

---

## Part 1 — Reading the instrument file

Open `src/pynxtools_myreader/reader.py`.
You will see that `MyreaderReader` extends `MultiFormatReader`.
The `extensions` dict in `__init__` already maps each file extension to a handler method.
All handler methods currently contain `# TODO` stubs.

### Exercise 1: `handle_hdf5_file`

Implement `handle_hdf5_file` so that it reads the entire HDF5 file into a flat
dictionary `self.hdf5_data`.

The keys should be slash-separated paths matching the HDF5 hierarchy, e.g.:

```python
{
    "data/x_values": array([...]),
    "data/y_values": array([...]),
    "data/x_units": b"eV",
    "metadata/instrument/version": 1.0,
    ...
}
```

**Requirements:**
- Use `h5py.File(file_path, "r")`
- Recursively traverse groups
- Store each `h5py.Dataset` value (call `item[()]` to get the numpy value)
- Return `{}` — the template will be filled later via the config file

??? success "Solution"

    ```python
    import h5py

    def handle_hdf5_file(self, file_path: str) -> dict[str, Any]:
        def recursively_read_group(group, path=""):
            result = {}
            for key, item in group.items():
                new_path = f"{path}/{key}" if path else key
                if isinstance(item, h5py.Group):
                    result.update(recursively_read_group(item, new_path))
                elif isinstance(item, h5py.Dataset):
                    result[new_path] = item[()]
            return result

        with h5py.File(file_path, "r") as hdf:
            self.hdf5_data = recursively_read_group(hdf)

        return {}
    ```

    Don't forget to add `import h5py` at the top of `reader.py` and add `h5py` to your
    `dependencies` in `pyproject.toml`.

---

## Part 2 — Reading the ELN file

### Exercise 2a: `CONVERT_DICT`

The `CONVERT_DICT` at the top of `reader.py` tells `parse_yml` how to rename
YAML path components when building NeXus template keys.

Without it, a YAML key like `user/name` would become `/ENTRY[entry]/user/name`,
but NeXus requires it to be `/ENTRY[entry]/USER[user]/name`.

Add the following mappings to `CONVERT_DICT`:

| YAML key | NeXus template key |
|---|---|
| `user` | `USER[user]` |
| `instrument` | `INSTRUMENT[instrument]` |
| `detector` | `DETECTOR[detector]` |
| `sample` | `SAMPLE[sample]` |

??? success "Solution"

    ```python
    CONVERT_DICT: dict[str, str] = {
        "unit": "@units",
        "version": "@version",
        "user": "USER[user]",
        "instrument": "INSTRUMENT[instrument]",
        "detector": "DETECTOR[detector]",
        "sample": "SAMPLE[sample]",
    }
    ```

### Exercise 2b: `handle_eln_file`

Implement `handle_eln_file` to parse `eln_data.yaml` into a flat dictionary
of NeXus template paths stored in `self.eln_data`.

Use `pynxtools.dataconverter.readers.utils.parse_yml`:

```python
from pynxtools.dataconverter.readers.utils import parse_yml
```

Pass:
- `convert_dict=CONVERT_DICT`
- `parent_key="/ENTRY[entry]"` so all keys start with the correct NeXus path

??? success "Solution"

    ```python
    from pynxtools.dataconverter.readers.utils import parse_yml

    def handle_eln_file(self, file_path: str) -> dict[str, Any]:
        self.eln_data = parse_yml(
            file_path,
            convert_dict=CONVERT_DICT,
            parent_key="/ENTRY[entry]",
        )
        return {}
    ```

    After this runs, `self.eln_data` will look like:

    ```python
    {
        "/ENTRY[entry]/title": "My experiment",
        "/ENTRY[entry]/USER[user]/name": "John Doe",
        "/ENTRY[entry]/USER[user]/address": "123 Science Rd, Data City, DC",
        "/ENTRY[entry]/SAMPLE[sample]/name": "my_sample",
        "/ENTRY[entry]/SAMPLE[sample]/physical_form": "powder",
        "/ENTRY[entry]/SAMPLE[sample]/temperature": 300,
        "/ENTRY[entry]/SAMPLE[sample]/temperature/@units": "K",
    }
    ```

---

## Part 3 — Callback methods

The `MultiFormatReader` uses a JSON config file (see Part 4) to populate the NeXus
template. Config values starting with `@attrs:`, `@eln`, or `@data:` trigger
callbacks — the methods you implement now.

### Exercise 3: `get_attr`

Implement `get_attr` to retrieve instrument metadata from `self.hdf5_data`.

It is called for config entries like `"@attrs:metadata/instrument/version"`.
The `path` argument will be `"metadata/instrument/version"`.

??? success "Solution"

    ```python
    def get_attr(self, key: str, path: str) -> Any:
        if self.hdf5_data is None:
            return None
        return self.hdf5_data.get(path)
    ```

### Exercise 4: `get_eln_data`

Implement `get_eln_data` to retrieve user and sample metadata from `self.eln_data`.

It is called for config entries like `"@eln"`. The `key` argument is the full NeXus
template path (e.g. `"/ENTRY[entry]/USER[user]/name"`), which already matches the
keys in `self.eln_data` because of how `parse_yml` was called.

??? success "Solution"

    ```python
    def get_eln_data(self, key: str, path: str) -> Any:
        if self.eln_data is None:
            return None
        return self.eln_data.get(key)
    ```

### Exercise 5: `get_data`

Implement `get_data` to return measurement arrays from `self.hdf5_data`.

It is called for config entries like `"@data:x_values"` and `"@data:y_values"`.
The `path` argument will be `"x_values"` or `"y_values"`.

The arrays are stored under `"data/x_values"` and `"data/y_values"` in
`self.hdf5_data`.

??? success "Solution"

    ```python
    def get_data(self, key: str, path: str) -> Any:
        if self.hdf5_data is None:
            return None
        data = self.hdf5_data.get(f"data/{path}")
        if data is None:
            logger.warning(f"No data found at path 'data/{path}'.")
        return data
    ```

---

## Part 4 — Writing the config file

The config file (`config_file.json`) maps concepts from the NXsimple application
definition to the data sources you have read in. It is a JSON file where:

- Keys are NeXus template paths (matching the output of `generate-template`)
- Values use `@`-prefixes to route to the right callback:
  - `@eln` → `get_eln_data` (user and sample metadata from YAML)
  - `@attrs:<hdf5-path>` → `get_attr` (instrument metadata from HDF5)
  - `@data:<hdf5-path>` → `get_data` (measurement arrays from HDF5)

### Exercise 6: Write `config_file.json`

Write a config file that fills the following fields of `NXsimple`:

| NeXus path | Source |
|---|---|
| `/ENTRY/title` | ELN |
| `/ENTRY/USER[user]/name` | ELN |
| `/ENTRY/USER[user]/address` | ELN |
| `/ENTRY/INSTRUMENT[instrument]/@version` | HDF5 `metadata/instrument/version` |
| `/ENTRY/INSTRUMENT[instrument]/DETECTOR[detector]/count_time` | HDF5 `metadata/instrument/detector/count_time` |
| `/ENTRY/INSTRUMENT[instrument]/DETECTOR[detector]/count_time/@units` | HDF5 `metadata/instrument/detector/count_time_units` |
| `/ENTRY/SAMPLE[sample]/name` | ELN |
| `/ENTRY/SAMPLE[sample]/physical_form` | ELN |
| `/ENTRY/SAMPLE[sample]/temperature` | ELN |
| `/ENTRY/SAMPLE[sample]/temperature/@units` | ELN |
| `/ENTRY/data/@axes` | Fixed value `["x_values"]` |
| `/ENTRY/data/@signal` | Fixed value `"data"` |
| `/ENTRY/data/data` | HDF5 `data/y_values` |
| `/ENTRY/data/x_values` | HDF5 `data/x_values` |

Create this file at `tests/data/workshop-example/my_config.json`.

!!! tip "Nested vs flat keys"
    Config keys can be nested JSON objects **or** flat slash-separated strings.
    Both are equivalent — use whichever you find clearer.

??? success "Solution"

    ```json title="my_config.json"
    {
      "/ENTRY/title": "@eln",
      "/ENTRY/USER[user]": {
        "name": "@eln",
        "address": "@eln"
      },
      "/ENTRY/INSTRUMENT[instrument]": {
        "@version": "@attrs:metadata/instrument/version",
        "DETECTOR[detector]": {
          "count_time": "@attrs:metadata/instrument/detector/count_time",
          "count_time/@units": "@attrs:metadata/instrument/detector/count_time_units"
        }
      },
      "/ENTRY/SAMPLE[sample]": {
        "name": "@eln",
        "physical_form": "@eln",
        "temperature": "@eln",
        "temperature/@units": "@eln"
      },
      "/ENTRY/data": {
        "@axes": ["x_values"],
        "@signal": "data",
        "data": "@data:y_values",
        "x_values": "@data:x_values"
      }
    }
    ```

---

## Part 5 — Running the converter

Now that your reader is implemented and your config file is written, run the
dataconverter:

```bash
dataconverter \
    tests/data/workshop-example/mock_data.h5 \
    tests/data/workshop-example/eln_data.yaml \
    tests/data/workshop-example/my_config.json \
    --reader myreader \
    --nxdl NXsimple \
    --output output.nxs
```

If everything is correct, you will see a `output.nxs` file in your working directory.

The converter automatically validates the output against `NXsimple` and reports any
missing required fields.

### Inspect the output

```python
import h5py

with h5py.File("output.nxs", "r") as f:
    def show(name, obj):
        if isinstance(obj, h5py.Dataset):
            print(f"{name} = {obj[()]}")
    f.visititems(show)
```

Or use any HDF5 viewer such as [HDFView](https://www.hdfgroup.org/downloads/hdfview/)
or [NeXpy](https://nexpy.github.io/nexpy/).

---

## Summary

You have built a complete pynxtools reader that:

1. Reads instrument data from an HDF5 file (`handle_hdf5_file`)
2. Reads ELN metadata from a YAML file (`handle_eln_file`)
3. Routes HDF5 metadata queries via `get_attr`
4. Routes ELN queries via `get_eln_data`
5. Routes measurement data queries via `get_data`
6. Maps everything to a NeXus application definition via a JSON config file

This is the same pattern used in all production pynxtools reader plugins.
To support a new technique, you adapt:

- The **application definition** (NXDL) to your technique's concepts
- The **handler** to read your file format(s)
- The **config file** to map your data to that definition

## Further reading

- [How-to: Use the MultiFormatReader](../how-tos/pynxtools/use-multi-format-reader.md)
- [How-to: Build a plugin](../how-tos/pynxtools/build-a-plugin.md)
- [How-to: Write a NeXus application definition](../how-tos/nexus/writing-an-appdef.md)
- [How-to: Test your reader](../how-tos/pynxtools/using-pynxtools-test-framework.md)
- [Learn: The MultiFormatReader in detail](../learn/pynxtools/multi-format-reader.md)
