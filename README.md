[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
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

It is recommended to use python 3.10 with a dedicated virtual environment for this package.
Learn how to manage [python versions](https://github.com/pyenv/pyenv) and
[virtual environments](https://realpython.com/python-virtual-environments-a-primer/).

Install the latest stable version of this package from PyPI with

```shell
pip install pynxtools
```

You can also install the latest _development_ version with

```shell
pip install git+https://github.com/FAIRmat-NFDI/pynxtools.git
```

# Scope

`pynxtools` (previously called `nexusutils`) is intended as a parser for combining various instrument output formats and electronic lab notebook (ELN) formats to an hdf5 file according to NeXus application definitions.

Additionally, the software is used in the research data management system NOMAD for
making experimental data searchable and publishable.
NOMAD is developed by the FAIRMAT consortium, as a part of the German National Research Data Infrastructure
(NFDI).

The software tools are located inside [`pynxtools`](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/src/pynxtools) and they are
shipped with unit tests located in [`tests`](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/tests).
Some examples with real datasets are provided in [`examples`](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/examples).
It guides you through the process of converting instrument raw
data into the NeXus standard and visualising the files content.

# Command line tools

- [**dataconverter**](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/dataconverter/README.md): Creates compliant instances of NeXus/HDF5 files to [NeXus schemas](https://nexusformat.org).
- [**read_nexus**](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/nexus/README.md): Outputs a debug log for a given NeXus file.
- [**generate_eln**](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/src/pynxtools/eln_mapper/README.md): Outputs ELN files that can be used to add metadata to the dataconverter routine.

# Documentation
Documentation for the different tools can be found [here](https://fairmat-nfdi.github.io/pynxtools/).

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

There is also a [pre-commit hook](https://pre-commit.com/#intro) available
which formats the code and checks the linting before actually commiting.
It can be installed with
```shell
pre-commit install
```
from the root of this repository.

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

# Troubleshooting

Please check this [guide](TROUBLESHOOTING.md) for any issues you face with the tool. If you don't find a solution there, please make a new [Github Issue](https://github.com/FAIRmat-NFDI/pynxtools/issues/new?template=bug.yaml).

