# NeXus verification
!!! info "Work in progress"

One of the main advantages of using pynxtools is that it comes with its own verification. That is, it can be used to verify that a given NeXus/HDF5 file is compliant with a NeXus application definition.

## As part of the dataconverter
During [data conversion](./dataconverter-and-readers.md), before writing the HDF5 file, the data is first checked against the provided application definition.

<!--## verify-nexus: Testing existing NeXus/HDF5 files
This CLI tool can be used to verify _existing_ HDF5 files that claim to be NeXus-compliant. See [here](reference/cli-api.html#verify-nexus) for the API documentation.-->

## read-nexus: NeXus file reader and debugger

This utility outputs a debug log for a given NeXus file by annotating the data and metadata entries with the schema definitions from the respective NeXus base classes and application definitions to which the file refers to. See [here](reference/cli-api.html#verify-nexus) for the API documentation.

The following example dataset can be used to test the `read_nexus` module: [src/pynxtools/data/201805_WSe2_arpes.nxs](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/data/201805_WSe2_arpes.nxs).

This is an angular-resolved photoelectron spectroscopy (ARPES) dataset and it is formatted according to
the [NXarpes application definition of NeXus](https://manual.nexusformat.org/classes/applications/NXarpes.html#nxarpes).

### Using a different set of NeXus definitions
The environmental variable called "NEXUS_DEF_PATH" can be set to
a directory, which contains the NeXus definitions as XML files. If this environmental
variable is not defined, the module will use the definitions in its bundle._

An environmental variable can be set as follows:

```
export 'NEXUS_DEF_PATH'=<folder_path_that_contains_nexus_defs>
```

### A note to Windows users
If you run `read_nexus` from `git bash`, you need to set the environmental variable
`MSYS_NO_PATHCONV` to avoid the [path translation in Windows Git MSys](https://stackoverflow.com/questions/7250130/how-to-stop-mingw-and-msys-from-mangling-path-names-given-at-the-command-line#34386471).
The easiest way is to prefix the `read_nexus` call with `MSYS_NO_PATHCONV=1`:

```
MSYS_NO_PATHCONV=1 read_nexus -c /NXarpes/ENTRY/INSTRUMENT/analyser
```

## Other approaches (not part of pynxtools)
Aside from the tools we developed within FAIRmat, the [official NeXus website](https://manual.nexusformat.org/validation.htm) listed two more programs for the verification and validation of NeXus files:

1. nxvalidate
2. punx