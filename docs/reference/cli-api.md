# API for command line tools

`pynxtools` supports a number of command line applications. This page provides documentation for their current API.

## Data conversion

Note that simply calling `dataconverter` defaults to `dataconverter convert`.

::: mkdocs-click
    :module: pynxtools.dataconverter.convert
    :command: main_cli
    :prog_name: dataconverter
    :depth: 2
    :style: table
    :list_subcommands: True

## NeXus file validation

::: mkdocs-click
    :module: pynxtools.dataconverter.validate_file
    :command: validate_cli
    :prog_name: validate_nexus
    :depth: 2
    :style: table
    :list_subcommands: True

## NeXus annotator

::: mkdocs-click
    :module: pynxtools.nexus.nexus
    :command: main
    :prog_name: read_nexus
    :depth: 2
    :style: table
    :list_subcommands: True

NOTE: Only one option from (`-d` and `-c`) is acceptable.

## ELN generation

::: mkdocs-click
    :module: pynxtools.eln_mapper.eln_mapper
    :command: get_eln
    :prog_name: generate_eln
    :depth: 2
    :style: table
    :list_subcommands: True