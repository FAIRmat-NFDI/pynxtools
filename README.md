[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![](https://github.com/FAIRmat-NFDI/pynxtools/actions/workflows/pytest.yml/badge.svg)
![](https://github.com/FAIRmat-NFDI/pynxtools/actions/workflows/pylint.yml/badge.svg)
![](https://github.com/FAIRmat-NFDI/pynxtools/actions/workflows/publish.yml/badge.svg)
![](https://img.shields.io/pypi/pyversions/pynxtools)
![](https://img.shields.io/pypi/l/pynxtools)
![](https://img.shields.io/pypi/v/pynxtools)
[![Coverage Status](https://coveralls.io/repos/github/FAIRmat-NFDI/pynxtools/badge.svg?branch=master&kill_cache=1)](https://coveralls.io/github/FAIRmat-NFDI/pynxtools?branch=master)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1323437.svg)](https://doi.org/10.5281/zenodo.13862042)

`pynxtools` is a tool designed for making your experimental data FAIR.
It allows to develop ontologies and to create ontological instances based on the [NeXus format](https://www.nexusformat.org/).

# Scope

`pynxtools` is a parser for combining various instrument output formats and electronic lab notebook (ELN) formats into an [HDF5](https://support.hdfgroup.org/HDF5/) file according to NeXus application definitions.

Additionally, the software can be used as a plugin in the research data management system NOMAD for
making experimental data searchable and publishable. NOMAD is developed by the FAIRmat consortium which is a consortium of the German National Research Data Infrastructure (NFDI).

# Installation

It is recommended to use python 3.11 with a dedicated virtual environment for this package.
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

# Documentation
Documentation can be found [here](https://fairmat-nfdi.github.io/pynxtools/).

# Repository structure

The software tools are located inside [`src/pynxtools`](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/src/pynxtools). They are shipped with unit tests located in [`tests`](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/tests).
Some examples from the scientific community are provided in [`examples`](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/examples). They guide you through the process of converting instrument data into the NeXus standard and visualising the files' content.

# NOMAD integration

## Does this software require NOMAD or NOMAD OASIS?

No. The data files produced here can be uploaded to NOMAD. Therefore, this tool acts as the framework to design schemas and instances of data within the NeXus universe. It can, however, be used as a NOMAD plugin to parse nexus files, please see the section below for details.

## How to use pynxtools with NOMAD

To use pynxtools with NOMAD, simply install it in the same environment as the `nomad-lab` package.
NOMAD will recognize pynxtools as a plugin automatically and offer automatic parsing of `.nxs` files. In addition, NOMAD will install a schema for NeXus application definitions.
By default, `pynxtools` is already included in the NOMAD [production]https://nomad-lab.eu/prod/v1/gui/ and [staging](https://nomad-lab.eu/prod/v1/staging/gui/) deployments.

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
usage convenient jupyter notebooks are available for each tool. To use these notebooks, jupyter
and related tools have to be installed in the development environment as follows:

```shell
python -m pip install jupyter
python -m pip install jupyterlab
python -m pip install jupyterlab_h5web
```
# Troubleshooting

Please check this [guide](https://fairmat-nfdi.github.io/pynxtools/tutorial/troubleshooting.html) for any issues you face with the tool. If you don't find a solution there, please make a new [Github Issue](https://github.com/FAIRmat-NFDI/pynxtools/issues/new?template=bug.yaml).

# Questions, suggestions?

To ask further questions, to make suggestions how we can improve these tools, to get advice
on how to build on this work, or to get your parser included into NOMAD, you can:

- Open an issue on the [pynxtools GitHub](https://github.com/FAIRmat-NFDI/pynxtools/issues)
- Use our forums at [matsci.org](https://matsci.org/c/nomad/32)
- Write to [support@nomad-lab.eu](mailto:support@nomad-lab.eu)
- Contact directly the lead developers of the individual parsers.