This is a NOMAD parser for [NEXUS](https://www.nexusformat.org/). It will read input in NEXUS format and output files and provide all information in NOMAD's unified Metainfo based Archive format.

## Getting started

Install the nexusparser as a standalone tool:
```
pip install nexusparser --extra-index-url https://gitlab.mpcdf.mpg.de/api/v4/projects/2187/packages/pypi/simple
```

This project also includes standalone tools that can be used without installing Nomad.

***If you want to use it as a Nomad parser, see [below](#using-the-project-as-a-parser-in-nomad).***

## YAML2NXDL

```console
user@box:~$ python -m nexusparser.tools.yaml2nxdl.yaml2nxdl

Usage: python yaml2nxdl.py [OPTIONS]

Options:
   --input-file TEXT     The path to the input data file to read.
   --append TEXT         Parse xml NeXus file and append to specified base class,
                         write the base class name with no extension.
   --verbose             Addictional std output info is printed to help debugging.
   --help                Show this message and exit.

```

Further documentation: [README.md](nexusparser/tools/yaml2nxdl/README.md)

## Dataconverter

Converts experimental data to Nexus/HDF5 files based on any provided NXDL.

```console
user@box:~$ python -m nexusparser.tools.dataconverter.convert --help
Usage: convert.py [OPTIONS]

Options:
  --input-file TEXT    The path to the input data file to read. (Repeat for
                       more than one file.)

  --reader TEXT        The reader to use.
  --nxdl TEXT          The name of the NXDL file to use without extension.  [required]
  --output TEXT        The path to the output Nexus file to be generated.
  --generate-template  Just print out the template generated from given NXDL
                       file.

  --help               Show this message and exit.
```

Further documentation: [README.md](nexusparser/tools/dataconverter/README.md)

## Nexus Checker

Outputs a debug log for a given Nexus file.

```console
user@box:~$ python -m nexusparser.tools.nexus <path_to_nexus_file>
```


# Using the project as a parser in Nomad
You should create a virtual environment. This is optional, but highly recommended as
the required nomad-lab pypi package requires many dependencies with specific versions
that might conflict with other libraries that you have installed. This was tested
with Python 3.7.

If you don't have Python 3.7 installed on your computer, follow these commands:
```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7 python3-dev libpython3.7-dev python-numpy

```

You can now install your virtual environment with python3.7 interpreter

```
mkdir <your-brand-new-folder>
cd <your-brand-new-folder>
pip install virtualenv
virtualenv --python=python3.7 .pyenv
source .pyenv/bin/activate
```

Simply install the nexusparser pypi package with all dependencies:
```
pip install --upgrade pip
pip install nexusparser[nomad] --extra-index-url https://gitlab.mpcdf.mpg.de/api/v4/projects/2187/packages/pypi/simple
```