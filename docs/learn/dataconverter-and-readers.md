# Data conversion in pynxtools
One of the main motivations for pynxtools is to develop a tool for combining various instrument output formats and electronic lab notebook (ELN) into an [HDF5](https://support.hdfgroup.org/HDF5/) file according to [NeXus application definitions](https://fairmat-nfdi.github.io/nexus_definitions/classes/index.html).

The `dataconverter` API in pynxtools provides exactly that: it converts experimental data to NeXus/HDF5 files based on any provided [NXDL schemas](https://manual.nexusformat.org/nxdl.html#index-1).

The dataconverter has essentially three functionalities:

1. read in experimental data using ```readers```
2. validate the data and metadata against any of the NeXus application definitions
3. write a valid NeXus/HDF5 file

For step 1, a set of readers has been which the converter calls to accomplish this task for a specific set of application definition (NXDL XML file) plus a set of experiment/method-specific file(s). These files can be files in a proprietary format, or of a certain format used in the respective scientific community, or text files. Only in combination, these files hold all the required pieces of information which the application definition demands and which are thus required to make a NeXus/HDF5 file compliant. Users can store additional pieces of information in an NeXus/HDF5 file. In this case readers will issue a warning that these data are not properly documented from the perspective of NeXus.

There exists two different subsets of readers:

1. [Built-in readers](../reference/built-in-readers.md), which are implemented directly in pynxtools and are typically used either as superclasses for new reader implementations or for generic reading purposes not directly related to any specific technique.
2. [Reader plugins](../reference/plugins.md) for `pynxtools, which are used for reading data of specific experimental techniques and are typically available as their own Python packages.

## Matching to NeXus application definitions

The purpose of the dataconverter is to create NeXus/HDF5 files with content that matches a specific NeXus application definition. Such application definitions are useful for collecting a set of pieces of information about a specific experiment in a given scientific field. The pieces of information are metadata and numerical data. The application definition is used to provide these data in a format that serves a data delivery contract: The HDF5 file, or so-called NeXus file, delivers all those pieces of information which the application definition specifies. Required and optional pieces of information are distinguished. NeXus classes can recommend the inclusion of certain pieces of information. Recommended data are essentially optional. The idea is that flagging these data as recommended motivates users to collect them but does not require to write dummy
or nonsense data if the user is unable to collect recommended data.

## Getting started

Each of the built-in reader comes with the main `pynxtools` package, therefore they are avaible after pip installation:
```console
user@box:~$ pip install pynxtools
```

The different FAIRmat-supported plugins can be installed together with pynxtools by passing the name of the plugin as an extra to the pip install call. For example, for the `pynxtools-mpes` plugin:
```console
pip install pynxtools[mpes]
```

In addition, it is also possible to install all of the pynxtools reader plugins which are maintained by FAIRmat by passing the `[convert]` extra to the pip install call:

```console
pip install pynxtools[convert]
```

## Usage
See [here](../reference/cli-api.md#data-conversion) for the documentation of the `dataconverter` API.

### Use with multiple input files

```console
user@box:~$ dataconverter --nxdl nxdl metadata data.raw otherfile
```

### Merge partial NeXus files into one

```console
user@box:~$ dataconverter --nxdl nxdl partial1.nxs partial2.nxs
```

### Map an HDF5/JSON/(Python Dict pickled in a pickle file)

```console
user@box:~$ dataconverter --nxdl nxdl any_data.hdf5 --mapping my_custom_map.mapping.json
```

You can find actual examples with data files at [`examples/json_map`](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/examples/json_map/).


## Example data for testing and development purposes

Before using your own data we strongly encourage you to download a set of open-source test data for testing the plug-ins. For this purpose pynxtools comes with a tests directory with a data/dataconverter sub-directory including reader-specific jupyter-notebook examples. These examples can be used for downloading test data and use specific readers as a standalone converter to translate given data into a NeXus/HDF5 file.

Once you have practised with these tools how to convert these examples, feel free to use the tools for converting your own data. You should feel invited to contact the respective corresponding author(s) of each reader if you run into issues with the reader or feel there is a necessity to include additional data into the NeXus file for the respective application.

We are looking forward for learning from your experience and see the interesting use cases.
You can find the contact persons in the respective README.md of each reader.

You can read specific README's of the readers and find usage examples [here](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/examples/).