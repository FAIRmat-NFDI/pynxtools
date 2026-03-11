# Built-in `pynxtools` readers

There exists a number of [readers](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/src/pynxtools/dataconverter/readers) directly in `pynxtools`. These are typically used either as superclasses for new reader implementations or for generic reading purposes not directly related to any specific technique.

## The [BaseReader](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/dataconverter/readers/base/reader.py)

This is the most simple reader, which is an abstract base class, on top of which a new reader implementation can build. It has an essentially empty read function and is thus only helpful for implementing the correct input/output design of the ```read``` function of any reader that is inheriting from this base reader.

## The [MultiFormatReader](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/dataconverter/readers/multi/reader.py)

Another reader that can act as the basis for any reader implementation is the `MultiFormatReader`, which can be used to implement a reader that can read in multiple file formats and then populate the NeXus file using the read data. Note that this reader has a lot of already built-in functionality, which is extensively described [here](../learn/pynxtools/multi-format-reader.md). There is also a [how-to guide](../how-tos/pynxtools/use-multi-format-reader.md) on how to implement a new reader off of the `MultiFormatReader` using a concrete example.

## The [JsonMapReader](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/dataconverter/readers/json_map/reader.py)

This reader is designed to allow users of `pynxtools` to convert their existing data with the help of a config file. The config file tells the reader which concept and instance data to pick from the data files and how to convert these to NeXus files. The following formats are supported as input files:

* HDF5
* JSON
* YAML
* Python Dict Objects pickled with [pickle](https://docs.python.org/3/library/pickle.html). These can contain [xarray.DataArray](https://docs.xarray.dev/en/stable/generated/xarray.DataArray.html) objects as well as regular Python types and Numpy types. Note that while it is supported, we strongly recommend not to use pickle due to its known [security concerns](https://huggingface.co/docs/hub/security-pickle).

It accepts any NXDL application definition as long as your config file contains all the required fields.

### The config file

Pass the config file via the `-c` flag:

```console
user@box:~$ dataconverter --nxdl NXmynxdl data.json -c my_config.json
```

The config file is a JSON (or YAML) file that maps NeXus template paths to values. Use `--generate-template` to get the list of paths for your NXDL:

```console
user@box:~$ dataconverter --nxdl NXmynxdl --generate-template
```

There are four ways to fill the right-hand side of a template key:

#### 1. Data path (`@data:` token)

Use the `@data:` prefix to point at a path inside your data file:

```json
  "/ENTRY[entry]/DATA[data]/current_295C": "@data:entry/data/current_295C",
  "/ENTRY[entry]/NXODD_name/posint_value": "@data:a_level_down/another_level_down/posint_value"
```

The path after `@data:` is a `/`-separated key chain into your data dictionary or HDF5 group hierarchy (no leading `/`). This is the same convention used by all other `MultiFormatReader`-based plugins (mpes, xps, raman, …).

#### 2. Literal value

Write the value directly for data that is not in your file:

```json
  "/ENTRY[entry]/PROCESS[process]/program": "Bluesky",
  "/ENTRY[entry]/PROCESS[process]/program/@version": "1.6.7"
```

#### 3. Link / virtual dataset

Use a JSON object with a `"link"` callback to reference data in an existing HDF5 file without copying it:

```json
  "/ENTRY[entry]/DATA[data]/current_295C":"@link:current.nxs:/entry/data/current_295C",
  "/ENTRY[entry]/DATA[data]/current_300C":"@link:current.nxs:/entry/data/current_300C"
```

Note: linking only works for HDF5 files. A `"shape"` key may be added alongside `"link"` to select a slice (e.g. `"shape": "0:100, 0:50"`).

#### 4. ELN / attribute data

Other token prefixes allow pulling from ELN files or reader attributes:

```json
  "/ENTRY[entry]/title": "@eln:title",
  "/ENTRY[entry]/start_time/@units": "@attrs:start_time_units"
```

### Examples

#### Basic example

```console
user@box:~$ dataconverter --nxdl NXtest data.json -c my_config.json
```

#### Example with HDF5 files

You can find example data files for using the config with HDF5 files at [`examples/json_map`](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/examples/examples/json_map/).

### The `.mapping.json` format (deprecated)

!!! warning "Deprecated"
    The `.mapping.json` file format is deprecated and will be removed in a future release.
    Please migrate to the config file format described above (passed via the `-c` flag).

For backward compatibility, the reader still accepts `.mapping.json` files. In this format, data paths are written with a leading `/` instead of `@data:`:

```json
  "/ENTRY[entry]/DATA[data]/current_295C": "/entry/data/current_295C"
```

Using a `.mapping.json` file will emit a `DeprecationWarning`.

## The [YamlJsonReader](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/dataconverter/readers/json_yml/reader.py)

!!! warning "Deprecated"
    `YamlJsonReader` is deprecated and will be removed in a future release.
    Use `MultiFormatReader` directly — it provides identical functionality.

## Installation

Each of the built-in readers are shipped/installed with the main `pynxtools` package. Hence, these readers are available after installation:

- [Installation](../tutorial/installation.md)