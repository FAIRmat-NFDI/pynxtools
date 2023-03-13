![](https://github.com/nomad-coe/nomad-parser-nexus/actions/workflows/pytest.yml/badge.svg?event=push)
![](https://github.com/nomad-coe/nomad-parser-nexus/actions/workflows/pylint.yml/badge.svg?event=push)
![](https://img.shields.io/badge/python-3.8-green.svg)

<br/>

This is a software for developing ontologies and instances of ontologies with
[NeXus](https://www.nexusformat.org/).

# Installation

It is recommended to use Python version 3.8 with this package. You can learn how to manage Python versions [here](https://github.com/pyenv/pyenv).

It is also recommended to use a fresh virtual environment to install all dependencies. You can learn more [here](https://realpython.com/python-virtual-environments-a-primer/).

Install this package:

```console
pip install git+https://github.com/nomad-coe/nomad-parser-nexus.git
```

<br/>

# Individual modules of this software and their functions

### **nyaml2nxdl**

This is a tool which converts, easy to read, YAML NeXus schemas into NXDL NeXus schemas. [NeXus Schemas](https://nexusformat.org)

Further documentation: [README.md](nexusutils/nyaml2nxdl/README.md)

### **dataconverter**

This is a tool which enables users to create compliant instances of NeXus/HDF5 files to [NeXus Schemas](https://nexusformat.org).

Further documentation: [README.md](nexusutils/dataconverter/README.md)

### **read_nexus**
This utility outputs a debug log for a given NeXus file.

Further documentation: [README.md](nexusutils/nexus/README.md)

<br/>

# Details
The software serves two aims.

First, it offers users a tool with which users can
create specific data files packaging together numerical data and metadata from
experiments which can originate from technology partners and/or text file output
from an electronic lab notebook (ELN).

Second, the software is used in the German National Research Data Infrastructure
(German NFDI) project FAIRmat, here specifically in the NOMAD OASIS research data
management (RDM) system, to serve as a set of parsers which enable users of a NOMAD
Oasis instance to create data and metadata entries from experiments so that NOMAD Oasis
understands the specific logic and terminology of the scientific field.

The software tools are located inside the module subdirectory [nexusutils](nexusutils/) and they are
shipped with unit tests located in the subdirectory [tests](tests/).
Some examples with real datasets are also provided in the subdirectory [examples](examples/)
in which Jupyter Notebooks are guiding through the process of converting instrument raw
data into the NeXus standard and then aloow the visualisation of the hierarchical contents
of the generated NeXus file in JupyterLab.

<br/>

# I am a developer and want to explore or contribute

Install the package with its dependencies:

```
git clone https://github.com/nomad-coe/nomad-parser-nexus.git --branch master --recursive nexusutils
cd nexusutils
git submodule sync --recursive
git submodule update --init --recursive --jobs=4
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install -e .[dev]
```
<br/>

# Test this software

Especially relevant for developers, there exists a basic test framework written in
[pytest](https://docs.pytest.org/en/stable/) which can be used as follows:

```
python -m pytest -sv tests
```

<br/>

# Questions, suggestions?

To ask further questions, to make suggestions how we can improve these tools, to get advice
on how to build on this work, or to get your parser included into NOMAD, you can:

- Open an issue on the [nexus-parser GitHub project](https://github.com/nomad-coe/nomad-parser-nexus/issues)
- Use our forums at [matsci.org](https://matsci.org/c/nomad/32)
- Write to [support@nomad-lab.eu](mailto:support@nomad-lab.eu)
- Contact directly the lead developers of the individual parsers.

<br/>

### Does this software require NOMAD or NOMAD OASIS ?

No. The data files produced here can be uploaded to Nomad. Therefore, this acts like the framework to design schemas and instances of data within the NeXus universe.
