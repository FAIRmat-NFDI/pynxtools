![](https://github.com/FAIRmat-NFDI/pynxtools/actions/workflows/pytest.yml/badge.svg)
![](https://github.com/FAIRmat-NFDI/pynxtools/actions/workflows/pylint.yml/badge.svg)
![](https://github.com/FAIRmat-NFDI/pynxtools/actions/workflows/publish.yml/badge.svg)
![](https://img.shields.io/pypi/pyversions/pynxtools)
![](https://img.shields.io/pypi/l/pynxtools)
![](https://img.shields.io/pypi/v/pynxtools)
![](https://coveralls.io/repos/github/FAIRmat-NFDI/pynxtools/badge.svg?branch=master)

`pynxtools` is a tool designed for making your experimental data FAIR.
It allows to develop ontologies and to create ontological instances based on the [NeXus format](https://www.nexusformat.org/).

# Installation

It is recommended to use python 3.8 with a dedicated virtual environment for this package.
Learn how to manage [python versions](https://github.com/pyenv/pyenv) and
[virtual environments](https://realpython.com/python-virtual-environments-a-primer/).

Install this package with

```shell
pip install git+https://github.com/FAIRmat-NFDI/pynxtools.git
```

for the latest development version.

# Scope

`pynxtools` (previously called `nexusutils`) is intended as a parser for combining various instrument output formats and electronic lab notebook (ELN) formats to an hdf5 file according to NeXus application definitions.

Additionally, the software is used in the research data management system NOMAD for
making experimental data searchable and publishable.
NOMAD is developed by the FAIRMAT consortium, as a part of the German National Research Data Infrastructure
(NFDI).

The software tools are located inside [`pynxtools`](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/pynxtools) and they are
shipped with unit tests located in [`tests`](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/tests).
Some examples with real datasets are provided in [`examples`](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/examples).
It guides you through the process of converting instrument raw
data into the NeXus standard and visualising the files content.

# Command line tools

- [**nyaml2nxdl**](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/pynxtools/nyaml2nxdl/README.md): Converts, easy to read, YAML [NeXus schemas](https://nexusformat.org) into NeXus XML definition language (NXDL).
- [**dataconverter**](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/pynxtools/dataconverter/README.md): Creates compliant instances of NeXus/HDF5 files to [NeXus schemas](https://nexusformat.org).
- [**read_nexus**](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/pynxtools/nexus/README.md): Outputs a debug log for a given NeXus file.

# Contributing

## Development install

Install the package with its dependencies:

```shell
git clone https://github.com/FAIRmat-NFDI/pynxtools.git \\
    --branch master \\
    --recursive pynxtools
cd pynxtools
git submodule sync --recursive
git submodule update --init --recursive --jobs=4
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install -e ".[dev]"
```

## Test this software

Especially relevant for developers, there exists a basic test framework written in
[pytest](https://docs.pytest.org/en/stable/) which can be used as follows:

```shell
python -m pytest -sv tests
```

## Run examples

A number of examples exist which document how the tools can be used. For a standalone
usage convenient jupyter notebooks are available for each tool. To use them jupyter
and related tools have to be installed in the development environment as follows:

```shell
python -m pip install jupyter
python -m pip install jupyterlab
python -m pip install jupyterlab_h5web
```

# Questions, suggestions?

To ask further questions, to make suggestions how we can improve these tools, to get advice
on how to build on this work, or to get your parser included into NOMAD, you can:

- Open an issue on the [pynxtools GitHub](https://github.com/FAIRmat-NFDI/pynxtools/issues)
- Use our forums at [matsci.org](https://matsci.org/c/nomad/32)
- Write to [support@nomad-lab.eu](mailto:support@nomad-lab.eu)
- Contact directly the lead developers of the individual parsers.

### Does this software require NOMAD or NOMAD OASIS ?

No. The data files produced here can be uploaded to Nomad. Therefore, this acts like the framework to design schemas and instances of data within the NeXus universe.
