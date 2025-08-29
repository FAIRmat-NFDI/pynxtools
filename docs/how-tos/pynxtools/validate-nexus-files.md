# Validation of NeXus files

!!! info "This is a how-to guide for using different tools to validate NeXus files. If you want to learn more about how validation is done in `pynxtools`, please visit the [explanation page](../../learn/pynxtools/nexus-validation.md)."

In this how-to guide, we will learn how to use `pynxtools` to validate existing NeXus files. As outlined in other parts of the documentation,
`pynxtools` can act as a framework for creating FAIR NeXus-compliant
files from experimental data.

In order to validate NeXus data, `pynxtools` comes with its own set of validation tools:

- **As part of the dataconverter**: During [data conversion](../../learn/pynxtools/dataconverter-and-readers.md) within `pynxtools`, before writing the HDF5 file, the data is first checked against the provided application definition.

- **`read_nexus`**: CLI tool to validate existing NeXus/HDF5 files.

- **`validate_nexus`**: Annotator and debugger CLI tool for NeXus/HDF5 files.

In this how-to, we will learn how to use the `validate_nexus` and `read_nexus` command line tools.

<!-- ??? info "Using a different set of NeXus definitions"

    The environment variable "NEXUS_DEF_PATH" can be set to a directory which contains the NeXus definitions as NXDL XML files. If this environment variable is not defined, the module will use the definitions in its bundle (see `src/pynxtools/definitions`)._

    The environment variable can be set as follows:
    ```
    export 'NEXUS_DEF_PATH'=<folder_path_that_contains_nexus_defs>
    ``` -->

!!! info "Dataset"
    You can download the dataset for following this how-to here:

    [201805_WSe2_arpes.nxs](https://raw.githubusercontent.com/FAIRmat-NFDI/pynxtools/master/src/pynxtools/data/201805_WSe2_arpes.nxs){:target="_blank" .md-button }

    This is an angular-resolved photoelectron spectroscopy (ARPES) dataset that is formatted according to the [`NXarpes`](https://manual.nexusformat.org/classes/applications/NXarpes.html#nxarpes) application definition.

Note that you will need to have `pynxtools` installed in a Python environment. Learn more about the installation procedure in the [installation tutorial](../../tutorial/installation.md).

## **`validate_nexus`**

After installation, you can envoke the help call of the `validate_nexus` tool from the command line:

```bash exec="on" source="material-block" result="ini"
validate_nexus --help
```

To see the results on the test file, run:

```bash exec="on" source="material-block" result="text"
validate_nexus --ignore-undocumented src/pynxtools/data/201805_WSe2_arpes.nxs
```

As you can see, the test file has a number of issues that are picked up during validation:

- Some of the units do not match those specified for the NeXus concepts.
- [Reserved suffixes](https://manual.nexusformat.org/datarules.html) are used without corresponding fields.
- The values of some fields do not match with those given in the enumeration in the NeXus application definition.

Therefore, we consider the `NXentry` instance in this file invalid. If you were writing such files, this would be the starting point to make some changes in the file creation routine to make your NeXus file compliant with `NXarpes`.

Note that here we are passing the `--ignore-undocumented` flag to the validation tool to ignore all additional content in the file which is not defined in the application definitions. We encourage you to test out the same call without the `--ignore-undocumented` flag to see the difference.

??? example "Show output including undocumented concepts"
    ```bash exec="on" source="material-block" result="text"
    validate_nexus src/pynxtools/data/201805_WSe2_arpes.nxs
    ```

## **`read_nexus`**

While `validate_nexus` is used as a tool for _validating_ a NeXus file, `read_nexus` is an _annotator_ tools. It outputs a debug log for a given NeXus file by annotating the data and metadata entries with the definitions from the respective NeXus base classes and application definitions to which the file refers to. This can be helpful to extract documentation and understand the concept defined in the NeXus application definition.

You can envoke the help call of the `read_nexus` tool from the command line:

```bash exec="on" source="material-block" result="ini"
read_nexus --help
```

??? info "A note to Windows users"

    If you run `read_nexus` from `git bash`, you need to set the environmental variable
    `MSYS_NO_PATHCONV` to avoid the [path translation in Windows Git MSys](https://stackoverflow.com/questions/7250130/how-to-stop-mingw-and-msys-from-mangling-path-names-given-at-the-command-line#34386471).
    The easiest way is to prefix the `read_nexus` call with `MSYS_NO_PATHCONV=1`:

    ```
    MSYS_NO_PATHCONV=1 read_nexus -c /NXarpes/ENTRY/INSTRUMENT/analyzer
    ```

    This workaround was tested with Windows 11, but should very likely also work with Windows 10 and lower.

To see the results on the test file, run:

```bash
read_nexus -f src/pynxtools/data/201805_WSe2_arpes.nxs 
```

??? example "Show full output"
    ```bash exec="on" source="material-block" result="text"
    read_nexus -f src/pynxtools/data/201805_WSe2_arpes.nxs 
    ```

In the output, several concepts are reported as "NOT IN SCHEMA". These are exactly those fields that we ignored with the `ignore-undocumented` flag about. NeXus allows to add additional groups/fields/attributes to NeXus files. However, such reports from the `validate_nexus`/`read_nexus` tools can also be indicators that a given part of the file is not compliant with the application definition as expected (e.g., because its name does not fit with the name of the intended NeXus concept).

### The `-c` option

Aside from producing the full anotator log for the NeXus file, `read_nexus` can also be used with the `-c` (or `--concept` option). This helps you to find out all instances in the file that correspond to a given concept path. If you want to find all groups in the file that implement the `analyser` group within `/NXarpes/ENTRY/INSTRUMENT`, you can run:

```bash
read_nexus -f src/pynxtools/data/201805_WSe2_arpes.nxs -c /NXarpes/ENTRY/INSTRUMENT/analyser
```

??? example "Show output"
    ```bash exec="on" source="material-block" result="text"
    read_nexus -f src/pynxtools/data/201805_WSe2_arpes.nxs -c /NXarpes/ENTRY/INSTRUMENT/analyser
    ```

### The `-d` option

Additionally, `read_nexus` can also be used with the `-d` (or `--documentation` option). Here, the input is the path in the HDF file.

This helps you to find the NeXus definition for a given path in the HDF5 file. If you want to understand which NeXus concept the HDF5 group `/entry/instrument/analyser` corresponds to and how it is documented, you can run:

```bash
read_nexus -f src/pynxtools/data/201805_WSe2_arpes.nxs -d /entry/instrument/analyser
```

??? example "Show output"
    ```bash exec="on" source="material-block" result="text"
    read_nexus -f src/pynxtools/data/201805_WSe2_arpes.nxs -d /entry/instrument/analyser
    ```

If you run this call, you get a smaller subset of the full annotation log that helps you to understand which NeXus concept a given HDF5 object corresponds to.

## Other approaches (not part of pynxtools)

Aside from the tools we develop within FAIRmat, the [official NeXus website](https://manual.nexusformat.org/validation.html) lists additional programs for the validation of NeXus files:

1. [cnxvalidate: NeXus validation tool written in C](https://github.com/nexusformat/cnxvalidate)
2. [punx: Python Utilities for NeXus HDF5 files](https://github.com/prjemian/punx)
3. [nexpy/nxvalidate: A python API for validating NeXus file](https://github.com/nexpy/nxvalidate)

!!! info "We will not discuss these tools here, but you can find some information about them on the [dedicated how-to page](validate-nexus-files-other-tools.md)."
