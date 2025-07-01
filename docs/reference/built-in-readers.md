# Built-in readers
There exists a number of [readers](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/src/pynxtools/dataconverter/readers) directly in pynxtools. These are typically used either as superclasses for new reader implementations or for generic reading purposes not directly related to any specific technique.

## The [BaseReader](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/dataconverter/readers/base/reader.py)

This is the most simple reader, which is an abstract base class, on top of which a new reader implementation can build. It has an essentially empty read function and is thus only helpful for implementing the correct input/output design of the ```read``` function of any reader that is inheriting from this base reader.

## The [MultiFormatReader](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/dataconverter/readers/multi/reader.py)

Another reader that can act as the basis for any reader implementation is the `MultiFormatReader`, which can be used to implement a reader that can read in multiple file formats and then populate the NeXus file using the read data. Note that this reader has a lot of already built-in functionality, which is extensively described [here](../learn/pynxtools/multi-format-reader.md). There is also a [how-to guide](../how-tos/pynxtools/use-multi-format-reader.md) on how to implement a new reader off of the `MultiFormatReader` using a concrete example.

## The [JsonMapReader](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/dataconverter/readers/json_map/reader.py)

This reader is designed to allow users of `pynxtools` to convert their existing data with the help of a map file. The map file tells the reader which concept and instance data to pick from the data files and how to convert these to NeXus files. The following formats are supported as input files:

* HDF5
* JSON
* Python Dict Objects pickled with [pickle](https://docs.python.org/3/library/pickle.html). These can contain [xarray.DataArray](https://docs.xarray.dev/en/stable/generated/xarray.DataArray.html) objects as well as regular Python types and Numpy types. Note that while it is supported, we strongly recommend note to use pickle due to its known [security concerns](https://huggingface.co/docs/hub/security-pickle).

It accepts any XML file that follows the NXDL schema definition language file as long as your mapping file contains all the required fields.
Please use the `--generate-template` function of the `dataconverter` to create a `.mapping.json` file:

```console
user@box:~$ dataconverter --nxdl NXmynxdl --generate-template > mynxdl.mapping.json
```

### The mapping.json file

This file is designed to let you fill in the requirements of a NeXus Application Definition without writing any code. If you already have data in the formats listed above, you just need to use this mapping file to help the dataconverter pick your data correctly.

The mapping files will always be based on the template the dataconverter generates. See above on how to generate a mapping file. The right hand side values of the template keys are what you can modify. These keys are called NeXus template paths, because they combine the actual path that will be used in the HDF5 hierarchy with additional NeXus datatype hints to guide the dataconverter to add NX_class annotations.

Here are the three different ways you can fill the right hand side of the template keys:

* Write the nested path in your datafile. This is indicated by a leading `/` before the word `entry` to make `/entry/data/current_295C` below.
Example:

```json
  "/ENTRY[entry]/DATA[data]/current_295C": "/entry/data/current_295C",
  "/ENTRY[entry]/NXODD_name/posint_value": "/a_level_down/another_level_down/posint_value",
```

Here, `"/entry/data/current_295C"` is the path in the original HDF5 file, while the key shown here is the template path (see above).

* Write the values directly in the mapping file for missing data from your data file.

```json
  "/ENTRY[entry]/PROCESS[process]/program": "Bluesky",
  "/ENTRY[entry]/PROCESS[process]/program/@version": "1.6.7"
```

* Write JSON objects with a link key. This follows the same link mechanism that the dataconverter implements. In the context of this reader, you can only use external links to your data files. In the example below, `current.nxs` is an already existing HDF5 file that we link to in our new NeXus file without copying over the data. The format is as follows:
`"link": "<filename>:<path_in_file>"`
Note: This only works for HDF5 files currently.

```json
  "/ENTRY[entry]/DATA[data]/current_295C": {"link": "current.nxs:/entry/data/current_295C"},
  "/ENTRY[entry]/DATA[data]/current_300C": {"link": "current.nxs:/entry/data/current_300C"},
```

### Examples

#### Basic mappings

There are some example files you can use:

[data.mapping.json](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/tests/data/dataconverter/readers/json_map/data.mapping.json)

[data.json](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/tests/data/dataconverter/readers/json_map/data.json)

```console
user@box:~$ dataconverter --nxdl NXtest data.json --mapping data.mapping.json
```

#### Example with HDF5 files

You can find example data files for using the mapping with HDF5 files at [`examples/json_map`](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/examples/examples/json_map/).

The example can be run by calling

```console
user@box:~$ dataconverter --nxdl nxdl any_data.hdf5 --mapping my_custom_map.mapping.json
```

## The [YamlJsonReader](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/dataconverter/readers/json_yml/reader.py)

!!! danger "Work in progress"

## Installation

Each of the built-in readers are shipped/installed with the main `pynxtools` package. Hence, these readers are available after installation:

- [Installation](../tutorial/installation.md)