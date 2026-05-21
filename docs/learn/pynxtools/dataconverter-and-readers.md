# Data conversion in pynxtools

One of the main motivations for pynxtools is to develop a tool for combining various instrument output formats and electronic lab notebook (ELN) into a file according to [NeXus application definitions](https://fairmat-nfdi.github.io/nexus_definitions/classes/index.html). 

The `pynx convert` command in pynxtools provides exactly that: it converts experimental as well as simulation data, together with the results from analysis of such data, to NeXus files based on any provided [NXDL schemas](https://manual.nexusformat.org/nxdl.html#index-1). Here, we are using [HDF5](https://support.hdfgroup.org/HDF5/) as the serialization format.

The dataconverter currently has essentially three functionalities:

1. Read in experimental data using ```readers```
2. Validate the data and metadata against a NeXus application definition of choice (i.e., check that the output data matches all existence, shape, and format constraints of application definition)
3. Write a valid NeXus/HDF5 file

A set of readers has been developed which the converter calls to read in a set of experiment/method-specific file(s) and for a specific set of application definitions (NXDL XML file). These data files can be in a proprietary format, or of a certain format used in the respective scientific community, or text files. Only in combination, these files hold all the required pieces of information which the application definition demands and which are thus required to make a NeXus/HDF5 file compliant. Users can store additional pieces of information in an NeXus/HDF5 file. In this case readers will issue a warning that these data are not properly documented from the perspective of NeXus.

There exists two different subsets of readers:

1. [Built-in readers](../../reference/built-in-readers.md), which are implemented directly in pynxtools and are typically used either as superclasses for new reader implementations or for generic reading purposes not directly related to any specific technique.
2. [Reader plugins](../../reference/plugins.md) for `pynxtools, which are used for reading data of specific experimental techniques and are typically available as their own Python packages.

## Matching to NeXus application definitions

The purpose of the dataconverter is to create NeXus/HDF5 files with content that matches a specific NeXus application definition. Such application definitions are useful for collecting a set of pieces of information about a specific experiment in a given scientific field. The pieces of information are numerical and categorical (meta)data. The application definition is used to provide these data in a format that serves a data delivery contract: The HDF5 file, or so-called NeXus file, delivers all those pieces of information which the application definition specifies. Required and optional pieces of information are distinguished. NeXus classes can recommend the inclusion of certain pieces of information. Recommended data are essentially optional. The idea is that flagging these data as recommended motivates users to collect these, but does not require to write dummy or nonsense data if the recommended data is not available.

## Getting started

You should start by installing `pynxtools` and (if needed) one or more of its supported plugins.

- [Installation](../../tutorial/installation.md)

## Usage

See [Reference > API for command line tools > pynx convert](../../reference/cli-api.md#data-conversion-pynx-convert) for the documentation of the `pynx convert` API.

### Discover installed readers

Before converting data, you need to know which readers are available in your environment. Use `pynx convert get-readers` to list them:

```console
pynx convert get-readers
```

Once you know which reader to use, `pynx convert reader-info` shows the NXDL application definitions and file extensions it supports:

```console
pynx convert reader-info <reader-name>
```

### Inspect an application definition

To understand what fields a given NXDL application definition requires before converting your data, use `pynx inspect-appdef`:

```console
pynx inspect-appdef NXmynxdl
pynx inspect-appdef NXmynxdl --level optional
```

The `--level` flag controls how much of the definition is shown: `required` (default), `recommended`, or `optional`. For the full list of paths suitable for filling in directly, use `pynx convert generate-template` instead.

### Use with multiple input files

```console
pynx convert metadata data.raw otherfile --nxdl nxdl --reader <reader-name>
```

### Merge partial NeXus files into one

```console
pynx convert --nxdl nxdl partial1.nxs partial2.nxs
```

### Map an HDF5 file/JSON file

```console
pynx convert --nxdl nxdl any_data.hdf5 --mapping my_custom_map.mapping.json
```

You can find actual examples with data files at [`examples/json_map`](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/examples/json_map/).

## Example data for testing and development purposes

Before using your own data we strongly encourage you to download a set of open-source test data for testing the pynxtools readers and reader  plugins. For this purpose, pynxtools and its plugins come with `examples` and `test` directories including reader-specific examples. These examples can be used for downloading test data and use specific readers as a standalone converter to translate given data into a NeXus/HDF5 file.

Once you have practiced with these tools how to convert these examples, feel free to use the tools for converting your own data. You should feel invited to contact the respective corresponding author(s) of each reader if you run into issues with the reader or feel there is a necessity to include additional data into the NeXus file for your respective application.

We are looking forward to learning from your experience and learn from your use cases. You can find the contact persons [here](../../contact.md) or in the respective documentation of each reader (plugin).
