# Validate and inspect NeXus files

!!! info "This is a how-to guide for using `validate_nexus` and `pynx read`. To understand how validation works internally, see the [explanation page](../../learn/pynxtools/nexus-validation.md)."

This guide shows how to use the two pynxtools CLI tools for inspecting existing NeXus/HDF5 files:

- **`pynx validate`** — checks conformance with the declared application definition.
- **`pynx read`** — annotates every node with NXDL documentation and schema information.

- **As part of the dataconverter**: During [data conversion](../../learn/pynxtools/dataconverter-and-readers.md) within `pynxtools`, before writing the HDF5 file, the data is first checked against the provided application definition.

- **`pynx read`**: CLI tool to annotate and debug existing NeXus/HDF5 files.

- **`pynx validate`**: CLI tool to validate existing NeXus/HDF5 files.

In this how-to, we will learn how to use the `pynx validate` and `pynx read` command line tools.

!!! note "Legacy commands"
    The old entry points `validate_nexus` and `read_nexus` are still installed as deprecated aliases. They continue to work but emit a deprecation warning. Prefer `pynx validate` and `pynx read` for new usage.

<!-- ??? info "Using a different set of NeXus definitions"

    The environment variable "NEXUS_DEF_PATH" can be set to a directory which contains the NeXus definitions as NXDL XML files. If this environment variable is not defined, the module will use the definitions in its bundle (see `src/pynxtools/definitions`)._

    The environment variable can be set as follows:
    ```
    export 'NEXUS_DEF_PATH'=<folder_path_that_contains_nexus_defs>
    ``` -->

!!! info "Dataset"
    You can download the example dataset used in this guide here:

    [201805_WSe2_arpes.nxs](https://raw.githubusercontent.com/FAIRmat-NFDI/pynxtools/master/src/pynxtools/data/201805_WSe2_arpes.nxs){:target="_blank" .md-button }

    This is an angular-resolved photoelectron spectroscopy (ARPES) file structured according to the [`NXarpes`](https://manual.nexusformat.org/classes/applications/NXarpes.html) application definition.

You will need `pynxtools` installed. See the [installation tutorial](../../tutorial/installation.md).

## **`pynx validate`**

After installation, you can invoke the `--help` call of the `pynx validate` tool from the command line:

```bash exec="on" source="material-block" result="ini"
pynx validate --help
```

Run the validator on the example file:

```bash exec="on" source="material-block" result="text"
pynx validate --ignore-undocumented src/pynxtools/data/201805_WSe2_arpes.nxs
```

The output shows a number of issues in this file:

- Some units do not match the NeXus unit categories defined for the corresponding fields.
- Reserved suffixes are used without a corresponding base field.
- Some field values do not match the enumeration in the application definition.

This means the `NXentry` in this file is not fully compliant with `NXarpes`. The validation output is the starting point for fixing the file's creation routine.

!!! note "The `--ignore-undocumented` flag"
    This flag suppresses warnings for fields, groups, and attributes that are present in the file but not defined in the application definition. NeXus allows such additional content, but it can also be a sign of misspelled concept names. Remove the flag to see the full output:

??? example "Show full output including undocumented concepts"
    ```bash exec="on" source="material-block" result="text"
    pynx validate src/pynxtools/data/201805_WSe2_arpes.nxs
    ```

## **`pynx read`**

While `pynx validate` is used as a tool for _validating_ a NeXus file, `pynx read` is an _annotator_ tool. It outputs a debug log for a given NeXus file by annotating the data and metadata entries with the definitions from the respective NeXus base classes and application definitions to which the file refers to. This can be helpful to extract documentation and understand the concept defined in the NeXus application definition.

You can invoke the help call of the `pynx read` tool from the command line:

```bash exec="on" source="material-block" result="ini"
pynx read --help
```

??? info "A note for Windows users"

    If you run `pynx read` from `git bash`, you need to set the environmental variable
    `MSYS_NO_PATHCONV` to avoid the [path translation in Windows Git MSys](https://stackoverflow.com/questions/7250130/how-to-stop-mingw-and-msys-from-mangling-path-names-given-at-the-command-line#34386471).
    The easiest way is to prefix the `pynx read` call with `MSYS_NO_PATHCONV=1`:

    ```
    MSYS_NO_PATHCONV=1 pynx read src/pynxtools/data/201805_WSe2_arpes.nxs -c /NXarpes/ENTRY/INSTRUMENT/analyzer
    ```

### Default mode — annotate the whole file

```bash
pynx read src/pynxtools/data/201805_WSe2_arpes.nxs 
```

??? example "Show full output"
    ```bash exec="on" source="material-block" result="text"
    pynx read src/pynxtools/data/201805_WSe2_arpes.nxs 
    ```

In the output, several concepts are reported as "NOT IN SCHEMA". These are exactly those fields that we ignored with the `ignore-undocumented` flag about. NeXus allows to add additional groups/fields/attributes to NeXus files. However, such reports from the `pynx validate` or `pynx read` tools can also be indicators that a given part of the file is not compliant with the application definition as expected (e.g., because its name does not fit with the name of the intended NeXus concept).

### `-d` mode — document a single node

Aside from producing the full annotator log for the NeXus file, `pynx read` can also be used with the `-c` (or `--concept` option). This helps you to find out all instances in the file that correspond to a given concept path. If you want to find all groups in the file that implement the `analyser` group within `/NXarpes/ENTRY/INSTRUMENT`, you can run:

```bash
pynx read src/pynxtools/data/201805_WSe2_arpes.nxs -c /NXarpes/ENTRY/INSTRUMENT/analyser
```

??? example "Show output"
    ```bash exec="on" source="material-block" result="text"
    pynx read src/pynxtools/data/201805_WSe2_arpes.nxs -c /NXarpes/ENTRY/INSTRUMENT/analyser
    ```

### The `-d` option

Additionally, `pynx read` can also be used with the `-d` (or `--documentation` option). Here, the input is the path in the HDF file.

This helps you to find the NeXus definition for a given path in the HDF5 file. If you want to understand which NeXus concept the HDF5 group `/entry/instrument/analyser` corresponds to and how it is documented, you can run:

```bash
pynx read src/pynxtools/data/201805_WSe2_arpes.nxs -d /entry/instrument/analyser
```

??? example "Show output"
    ```bash exec="on" source="material-block" result="text"
    pynx read src/pynxtools/data/201805_WSe2_arpes.nxs -d /entry/instrument/analyser
    ```

### `-c` mode — find all instances of a concept

The `-c` (concept) option finds all HDF5 nodes in the file that implement a given NXDL concept path. Input is the NXDL path.

```bash
pynx read -f src/pynxtools/data/201805_WSe2_arpes.nxs -c /NXarpes/ENTRY/INSTRUMENT/analyser
```

??? example "Show output"
    ```bash exec="on" source="material-block" result="text"
    pynx read -f src/pynxtools/data/201805_WSe2_arpes.nxs -c /NXarpes/ENTRY/INSTRUMENT/analyser
    ```

## Other approaches

The [official NeXus website](https://manual.nexusformat.org/validation.html) lists additional programs for NeXus validation:

1. [cnxvalidate — NeXus validation tool written in C](https://github.com/nexusformat/cnxvalidate)
2. [punx — Python Utilities for NeXus HDF5 files](https://github.com/prjemian/punx)
3. [nexpy/nxvalidate — a Python API for validating NeXus files](https://github.com/nexpy/nxvalidate)

!!! info "For a comparison of these tools, see the [dedicated how-to page](validate-nexus-files-other-tools.md)."
