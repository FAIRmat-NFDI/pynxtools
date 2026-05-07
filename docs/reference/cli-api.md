# API for command line tools

`pynxtools` provides a unified `pynx` entry point with subcommands for all CLI operations. This page documents the current API.

The legacy entry points (`dataconverter`, `validate_nexus`, `read_nexus`, `generate_eln`) are still installed as deprecated aliases — they continue to work but emit a deprecation warning.

## Data conversion — `pynx convert`

Converts experimental data to NeXus/HDF5 files. Internally uses the reader pipeline described in [Learn > pynxtools > Data conversion in pynxtools](../learn/pynxtools/dataconverter-and-readers.md).

::: mkdocs-click
    :module: pynxtools.dataconverter.cli
    :command: run
    :prog_name: pynx convert
    :depth: 1
    :style: table

### Sub-commands

::: mkdocs-click
    :module: pynxtools.dataconverter.cli
    :command: convert
    :prog_name: pynx convert
    :depth: 2
    :style: table
    :list_subcommands: True

!!! info

    Note that simply calling `pynx convert` defaults to `pynx convert run`.

## NeXus file validation — `pynx validate`

Validates an existing HDF5/NeXus file against the NeXus application definition it declares in `NXentry/definition`.

See [Learn > pynxtools > Validation of NeXus files](../learn/pynxtools/nexus-validation.md) for a conceptual explanation, and the [how-to guide](../how-tos/pynxtools/validate-nexus-files.md) for usage examples.

::: mkdocs-click
    :module: pynxtools.dataconverter.cli
    :command: validate
    :prog_name: pynx validate
    :depth: 2
    :style: table
    :list_subcommands: True

## NeXus file annotator — `pynx read`

Annotates every node in a NeXus/HDF5 file with NXDL documentation, optionality, data types, unit categories, and inheritance paths. Backed by `Annotator` in `pynxtools.nexus.annotation`.

Three operating modes:

- **Default**: annotate all nodes and print the default-plottable summary.
- **`-d` (documentation)**: annotate the single node at a given HDF5 path.
- **`-c` (concept)**: find all HDF5 nodes that implement a given NXDL concept path.

!!! note
    Only one of `-d` and `-c` is accepted at a time.

::: mkdocs-click
    :module: pynxtools.nexus.cli
    :command: read
    :prog_name: pynx read
    :depth: 2
    :style: table
    :list_subcommands: True

## ELN schema generation — `pynx generate_eln`

Generates an ELN YAML template from a NeXus application definition. The resulting file can be filled in to provide metadata for the `dataconverter`.

::: mkdocs-click
    :module: pynxtools.eln_mapper.cli
    :command: generate_eln
    :prog_name: pynx generate-eln
    :depth: 2
    :style: table
    :list_subcommands: True

## Application definition inspector

Lists the concept paths defined in a NeXus application.

::: mkdocs-click
    :module: pynxtools.nexus.cli
    :command: inspect_appdef
    :prog_name: pynx inspect-appdef
    :depth: 1
    :style: table
