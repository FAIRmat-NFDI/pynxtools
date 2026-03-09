# API for command line tools

`pynxtools` provides several command line tools for converting, validating, and annotating NeXus files. All tools are available after [installation](../tutorial/installation.md).

## Data conversion

Converts experimental data to NeXus/HDF5 files. Internally uses the reader pipeline described in [Data conversion in pynxtools](../learn/pynxtools/dataconverter-and-readers.md).

Note: calling `dataconverter` without a subcommand defaults to `dataconverter convert`.

::: mkdocs-click
    :module: pynxtools.dataconverter.convert
    :command: main_cli
    :prog_name: dataconverter
    :depth: 2
    :style: table
    :list_subcommands: True

## NeXus file validation — `validate_nexus`

Validates an existing HDF5/NeXus file against the NeXus application definition it declares in `NXentry/definition`. Backed by `ValidationVisitor` in `pynxtools.dataconverter.validation`.

See [Validation of NeXus files](../learn/pynxtools/nexus-validation.md) for a conceptual explanation, and the [how-to guide](../how-tos/pynxtools/validate-nexus-files.md) for usage examples.

::: mkdocs-click
    :module: pynxtools.dataconverter.validate_file
    :command: validate_cli
    :prog_name: validate_nexus
    :depth: 2
    :style: table
    :list_subcommands: True

## NeXus file annotator — `read_nexus`

Annotates every node in a NeXus/HDF5 file with NXDL documentation, optionality, data types, unit categories, and inheritance paths. Backed by `Annotator` in `pynxtools.nexus.annotation`.

Three operating modes:

- **Default**: annotate all nodes and print the default-plottable summary.
- **`-d` (documentation)**: annotate the single node at a given HDF5 path.
- **`-c` (concept)**: find all HDF5 nodes that implement a given NXDL concept path.

See the [how-to guide](../how-tos/pynxtools/validate-nexus-files.md#read_nexus) for usage examples.

!!! note
    Only one option from (`-d` and `-c`) is accepted at a time.

::: mkdocs-click
    :module: pynxtools.nexus.nexus
    :command: main
    :prog_name: read_nexus
    :depth: 2
    :style: table
    :list_subcommands: True

## ELN schema generation — `generate_eln`

Generates an ELN YAML template from a NeXus application definition. The resulting file can be filled in to provide metadata for the `dataconverter`.

::: mkdocs-click
    :module: pynxtools.eln_mapper.eln_mapper
    :command: get_eln
    :prog_name: generate_eln
    :depth: 2
    :style: table
    :list_subcommands: True
