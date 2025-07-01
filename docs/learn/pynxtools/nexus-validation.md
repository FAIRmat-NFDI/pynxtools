# Validation of NeXus file

!!! info "This page is intended to give more information about the validation tools that are part of `pynxtools`. Please also have a look at our comprehensive [how-to guide](../../how-tos/pynxtools/validate-nexus-file.md) on NeXus validation."

One of the main advantages of using pynxtools is that it comes with its own validation tools. That is, it can be used to validate that a given NeXus/HDF5 file is compliant with a NeXus application definition.

## As part of the dataconverter

During [data conversion](./dataconverter-and-readers.md), before writing the HDF5 file, the data is first checked against the provided application definition.

<!--## verify-nexus: Testing existing NeXus/HDF5 files
This CLI tool can be used to validate _existing_ HDF5 files that claim to be NeXus-compliant. See [here](reference/cli-api.md#verify-nexus) for the API documentation.-->

## read_nexus: NeXus file reader and debugger

This utility outputs a debug log for a given NeXus file by annotating the data and metadata entries with the schema definitions from the respective NeXus base classes and application definitions to which the file refers to. See [here](../../reference/cli-api.md#nexus-file-validation) for the API documentation.

The following example dataset can be used to test the `read_nexus` module: [src/pynxtools/data/201805_WSe2_arpes.nxs](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/data/201805_WSe2_arpes.nxs). This is an angular-resolved photoelectron spectroscopy (ARPES) dataset that is formatted according to the [NXarpes application definition of NeXus](https://manual.nexusformat.org/classes/applications/NXarpes.html#nxarpes).

!!! info "Using a different set of NeXus definitions"

    The environment variable "NEXUS_DEF_PATH" can be set to a directory which contains the NeXus definitions as NXDL XML files. If this environment variable is not defined, the module will use the definitions in its bundle (see `src/pynxtools/definitions`)._

    The environment variable can be set as follows:
    ```
    export 'NEXUS_DEF_PATH'=<folder_path_that_contains_nexus_defs>
    ```

!!! info "A note to Windows users"

    If you run `read_nexus` from `git bash`, you need to set the environmental variable
    `MSYS_NO_PATHCONV` to avoid the [path translation in Windows Git MSys](https://stackoverflow.com/questions/7250130/how-to-stop-mingw-and-msys-from-mangling-path-names-given-at-the-command-line#34386471).
    The easiest way is to prefix the `read_nexus` call with `MSYS_NO_PATHCONV=1`:

    ```
    MSYS_NO_PATHCONV=1 read_nexus -c /NXarpes/ENTRY/INSTRUMENT/analyzer
    ```

    This workaround was tested with Windows 11, but should very likely also work with Windows 10 and lower.

## Other approaches (not part of pynxtools)

Aside from the tools we developed within FAIRmat, the [official NeXus website](https://manual.nexusformat.org/validation.html) lists additional programs for the validation of NeXus files:

1. [cnxvalidate: NeXus validation tool written in C](https://github.com/nexusformat/cnxvalidate)
2. [punx: Python Utilities for NeXus HDF5 files](https://github.com/prjemian/punx)
3. [nexpy/nxvalidate: A python API for validating NeXus file](https://github.com/nexpy/nxvalidate)

We will not discuss the details of these programs here, but you can find some information about the in the how-to guide linked above.