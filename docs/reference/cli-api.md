# API for command line tools

`pynxtools` provides a unified `pynx` entry point with subcommands for all CLI operations. This page documents the current API.

The legacy entry points (`dataconverter`, `validate_nexus`, `read_nexus`, `generate_eln`) are still installed as deprecated aliases — they continue to work but emit a deprecation warning.

## Data conversion

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

## NeXus file validation

::: mkdocs-click
    :module: pynxtools.dataconverter.cli
    :command: validate
    :prog_name: pynx validate
    :depth: 2
    :style: table
    :list_subcommands: True

## NeXus annotator

::: mkdocs-click
    :module: pynxtools.nexus.cli
    :command: read
    :prog_name: pynx read
    :depth: 2
    :style: table
    :list_subcommands: True

## ELN generation

::: mkdocs-click
    :module: pynxtools.eln_mapper.cli
    :command: generate_eln
    :prog_name: pynx generate-eln
    :depth: 2
    :style: table
    :list_subcommands: True

## Application definition inspector

::: mkdocs-click
    :module: pynxtools.nexus.cli
    :command: inspect_appdef
    :prog_name: pynx inspect-appdef
    :depth: 1
    :style: table