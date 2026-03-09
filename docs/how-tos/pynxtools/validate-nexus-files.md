# Validate and inspect NeXus files

!!! info "This is a how-to guide for using `validate_nexus` and `read_nexus`. To understand how validation works internally, see the [explanation page](../../learn/pynxtools/nexus-validation.md)."

This guide shows how to use the two pynxtools CLI tools for inspecting existing NeXus/HDF5 files:

- **`validate_nexus`** — checks conformance with the declared application definition.
- **`read_nexus`** — annotates every node with NXDL documentation and schema information.

Both tools are backed by the same `NexusFileHandler` traversal; they differ only in the visitor they use. See [pynxtools architecture](../../learn/pynxtools/architecture.md) for details.

!!! info "Dataset"
    You can download the example dataset used in this guide here:

    [201805_WSe2_arpes.nxs](https://raw.githubusercontent.com/FAIRmat-NFDI/pynxtools/master/src/pynxtools/data/201805_WSe2_arpes.nxs){:target="_blank" .md-button }

    This is an angular-resolved photoelectron spectroscopy (ARPES) file structured according to the [`NXarpes`](https://manual.nexusformat.org/classes/applications/NXarpes.html) application definition.

You will need `pynxtools` installed. See the [installation tutorial](../../tutorial/installation.md).

## `validate_nexus`

`validate_nexus` applies the `ValidationVisitor` to an existing HDF5 file and reports deviations from the application definition declared in `NXentry/definition`.

```bash exec="on" source="material-block" result="ini"
validate_nexus --help
```

Run the validator on the example file:

```bash exec="on" source="material-block" result="text"
validate_nexus --ignore-undocumented src/pynxtools/data/201805_WSe2_arpes.nxs
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
    validate_nexus src/pynxtools/data/201805_WSe2_arpes.nxs
    ```

## `read_nexus`

`read_nexus` annotates every node in a NeXus file with the corresponding NXDL documentation, optionality, data type, unit category, and inheritance chain from the matching `NexusNode`. It is useful for debugging a file and exploring what a given application definition requires.

```bash exec="on" source="material-block" result="ini"
read_nexus --help
```

??? info "A note for Windows users"

    When running `read_nexus` from Git Bash, prefix the command with `MSYS_NO_PATHCONV=1` to avoid path mangling:

    ```bash
    MSYS_NO_PATHCONV=1 read_nexus -c /NXarpes/ENTRY/INSTRUMENT/analyzer
    ```

### Default mode — annotate the whole file

```bash
read_nexus -f src/pynxtools/data/201805_WSe2_arpes.nxs
```

??? example "Show full output"
    ```bash exec="on" source="material-block" result="text"
    read_nexus -f src/pynxtools/data/201805_WSe2_arpes.nxs
    ```

Nodes reported as `NOT IN SCHEMA` are those flagged by `--ignore-undocumented` in `validate_nexus`. They may represent genuinely additional content or misspelled concept names.

### `-d` mode — document a single node

The `-d` (documentation) option limits the output to a single HDF5 node, showing which NXDL concept it corresponds to and how that concept is documented. Input is the HDF5 path.

```bash
read_nexus -f src/pynxtools/data/201805_WSe2_arpes.nxs -d /entry/instrument/analyser
```

??? example "Show output"
    ```bash exec="on" source="material-block" result="text"
    read_nexus -f src/pynxtools/data/201805_WSe2_arpes.nxs -d /entry/instrument/analyser
    ```

### `-c` mode — find all instances of a concept

The `-c` (concept) option finds all HDF5 nodes in the file that implement a given NXDL concept path. Input is the NXDL path.

```bash
read_nexus -f src/pynxtools/data/201805_WSe2_arpes.nxs -c /NXarpes/ENTRY/INSTRUMENT/analyser
```

??? example "Show output"
    ```bash exec="on" source="material-block" result="text"
    read_nexus -f src/pynxtools/data/201805_WSe2_arpes.nxs -c /NXarpes/ENTRY/INSTRUMENT/analyser
    ```

## Other approaches

The [official NeXus website](https://manual.nexusformat.org/validation.html) lists additional programs for NeXus validation:

1. [cnxvalidate — NeXus validation tool written in C](https://github.com/nexusformat/cnxvalidate)
2. [punx — Python Utilities for NeXus HDF5 files](https://github.com/prjemian/punx)
3. [nexpy/nxvalidate — a Python API for validating NeXus files](https://github.com/nexpy/nxvalidate)

!!! info "For a comparison of these tools, see the [dedicated how-to page](validate-nexus-files-other-tools.md)."
