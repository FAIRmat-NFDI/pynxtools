This is a software for developing ontologies and instances of ontologies with
[NeXus](https://www.nexusformat.org/). The software serves two aims.

First, it offers users a tool with which they can
create specific data files packaging together numerical data and metadata from
experiments which can originate from technology partners and/or text file output
from an electronic lab notebook (ELN).

Second, the software is used in the German National Research Data Infrastructure
(German NFDI) project FAIRmat, here specifically in the NOMAD OASIS research data
management (RDM) system, to serve as a set of parsers which enable users of a NOMAD
Oasis instance to create data and metadata entries from experiments so that NOMAD Oasis
understands the specific logic and terminology of the scientific field.

The software tools are located inside the module subdirectory 'nexusutils'and they are
shipped with unit tests located in the subdirectory 'tests'.
Some examples with real datasets are also provided in the subdirectory 'examples'
in which Jupyter Notebooks are guiding through the process of converting instrument raw
data into the NeXus standard and then aloow the visualisation of the hierarchical contents
of the generated NeXus file in JupyterLab.

## Getting started
You should create a virtual environment. We tested on Ubuntu with Python 3.7.

If you don't have Python 3.7 installed on your computer, follow these commands:
```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7 python3-dev libpython3.7-dev python-numpy

```

You can now install your virtual environment with a python3.7 interpreter

```
mkdir <your-brand-new-folder>
cd <your-brand-new-folder>
pip install virtualenv
virtualenv --python=python3.7 .pyenv
source .pyenv/bin/activate
pip install pip-tools
```

This software can be used independently of a NOMAD or NOMAD Oasis instance.
Clone this project (or fork and then clone the fork).
Go into the cloned directory and directly run the parser from there:

Now you have to decide your role. Are you a user or a developer?

### I want to use nexusutils as a user
If you are a user you should install nexusutils as a standalone tool:
```
pip install nexusutils --extra-index-url https://gitlab.mpcdf.mpg.de/api/v4/projects/2187/packages/pypi/simple
```

### I am a developer and want to explore or contribute

Install package with its dependencies:

```
git clone https://github.com/nomad-coe/nomad-parser-nexus.git --branch master --recursive nexusutils
cd nexusutils
git submodule sync --recursive
git submodule update --init --recursive --jobs=4
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install -e .[dev]
```

To be able to run jupyerlab with the NeXus file viewer H5Web, you also need the foolwing packages

```
python -m pip install jupyterlab
python -m pip install jupyterlab_h5web[full]==6.0.1
```

## Test this software
Especially relevant for developers, there exists a basic test framework written in
[pytest](https://docs.pytest.org/en/stable/) which can be used as follows:

```
python -m pytest -sv tests
```

## Individual modules of this software and their functions

### **nyaml2nxdl**
This module is a tool which automatically converts YAML files containing specifications for NeXus
base classes and/or application definitions, i.e. data schemes, into specifically formatted XML files
that follow the conventions used in NeXus. The tool works in two directions: Either a YAML file can
be converted to a NXDL XML file or a NXDL XML file can be converted into a YAML.
NXDL XML files have an own XML and XSD rule set that was developed and is maintained
by the NeXus International Advisory Committee (NIAC). The nyaml2nxdl converter implements this rule set.

The main purpose of the tool is to support developers with a simplified
editing and writing experience when they wish to explore, modified, i.e. work with
NeXus base classes and application definitions.

```console
user@box:~$ nyaml2nxdl --help

Usage: nyaml2nxdl.py [OPTIONS]

Options:
   --input-file TEXT     The path to the input data file to read.
   --append TEXT         Parse xml NeXus file and append to specified base class,
                         write the base class name with no extension.
   --verbose             Addictional std output info is printed to help debugging.
   --help                Show this message and exit.
```

Further documentation: [README.md](nyaml2nxdl/README.md)


### **dataconverter**
This module is a tool which enables users to create instances of NeXus/HDF5 files.
The instances are specific for the experiment and technique.
Each instance supports a combination of specifically-versioned software components:
A NeXus application definition, an associated referred to set of base classes,
and an experiment/technique-specific dataconverter (aka parser).

The main purpose of these parsers is to create an instance of a NeXus/HDF5 file that is
formatted in accordance with the respective NeXus application definition.
This means the parser eventually transcodes and copies data and metadata within specifically
formatted file and representations, like ELNs, of a scientific community and/or
technology partner.

The dataconverter implements a concept of a generic parser, which internally calls
the above-mentioned experimental-method-specific parser.
Currently, the generic parser maintains one dictionary object in which all
data and metadata to be written are collected and exported to HDF5 afterwards.
The role of the generic parser is to resolve the structure of the NeXus application
definition and decorate the HDF5 files with attributes, fields, and groups
as it is required by NeXus, so that the dataconverter can yield a properly
formatted NeXus/HDF5 file.

The role of the specific parsers is to fill this dictionary. Parsers are separated
to avoid that a single parser becomes too complex in its implementation.

```console
user@box:~$ dataconverter --help

Usage: convert.py [OPTIONS]

Options:
  --input-file TEXT    The path to the input data file to read. (Repeat for
                       more than one file.)

  --reader TEXT        The reader to use.
  --nxdl TEXT          The name of the NXDL file to use without extension.  [required]
  --output TEXT        The path to the output NeXus file to be generated.
  --generate-template  Just print out the template generated from given NXDL
                       file.

  --help               Show this message and exit.
```

Further documentation: [README.md](dataconverter/README.md)

Inspect also specific README.md of the respective parser(s) you wish to use
or contribute to so that you can learn how these parser(s) work, which input data
they expect, and what which output they yield.

### **read_nexus**
This utility outputs a debug log for a given NeXus file by annotating the data and
metadata entries with the schema definitions from the respective base classes and
application definitions the file content is referring to.

```console
user@box:~$ read_nexus <path_to_nexus_file>
```

*The environmental variable called "NEXUS_DEF_PATH" can be set to
a directory, which contains the NeXus definitions as XML files. If this environmental
variable is not defined, the module will use the dinfitions in its bundle.*

An environmental variable can be set as follows:
```
export 'NEXUS_DEF_PATH'=<folder_path_that_contains_nexus_defs>
```

## Next steps

Our documentation provides several resources that might be interesting for developers of NOMAD (Oasis):
- [How to write a parser](https://nomad-lab.eu/prod/rae/docs/parser.html).
  Provides a more detailed tutorial on how to write a parser for NOMAD.
- [Introduction to the NOMAD Metainfo](https://nomad-lab.eu/prod/rae/docs/metainfo.html).
  This explains how the NOMAD data schema, the so-called NOMAD MetaInfo, can be extended
  and used within your parser. A contextualization of the NOMAD MetaInfo is available
  in the scientific literature https://doi.org/10.1038/s41524-017-0048-5.

## Questions, suggestions?
To ask further questions, to make suggestions how we can improve these tools, to
get advice on how to build on this work, or to get your parser included into NOMAD, you can:
- Open an issue on the [nexus-parser GitHub project](https://github.com/nomad-coe/nomad-parser-nexus/issues)
- Use our forums at [matsci.org](https://matsci.org/c/nomad/32)
- Write to [support@nomad-lab.eu](mailto:support@nomad-lab.eu)
