The tools of the NOMAD parser for [NEXUS](https://www.nexusformat.org/) can also be used
without having a NOMAD OASIS installation. There are two main use cases:
* Use the DATACONVERTER for transcoding vendor and community files to NeXus files so that these
  are compliant with specific NeXus application definitions for [NEXUS-FAIRMAT-PROPOSAL](https://fairmat-experimental.github.io/nexus-fairmat-proposal/).
* Use the YAML2NXDL converter to support writing NeXus base classes and application definitions.

## Getting started

It is recommended to install the tool in an own virtual environment as
some installation steps will install specific version of packages that
might conflict with existent versions. You can install the tools as
standalone tools. We make the following assumptions:
* You have a Python3.7 installed. Higher versions can be used but might need
  modifications for specific packages on which nomad-parser-nexus depends.
* You do not need to be inside a conda environment.

```
pip install virtualenv && virtualenv --python=python3.7 .nexusenv && source .nexusenv/bin/activate
pip install --upgrade pip==22.2.2 && pip install --upgrade nodejs==0.1.1
pip install jupyterlab_h5web[full]==6.0.1
```

So much about the environment. Let's continue with installing the tools:

```
git clone https://github.com/nomad-coe/nomad-parser-nexus.git --recursive
cd nomad-parser-nexus/
git branch -a
pip install -e .
```

With this the installation is complete.

### Using the tool

The tool can be started with jupyter:

```
jupyter lab
```

If you are using a Linux operating system, a browser tab should open up
which shows the running jupyter lab instance.
If you are on Windows and use WSL2, typing the above command into the
console will leave you with a message in the console reading:

```
...
Jupyter Server <<some version>> is running at.
http://localhost:8888/lab?token=<<some hash value / token>>
...

```

You should copy this localhost address into your browser,
so that you can also see the running jupyter lab instance
and interact with it graphically. If you are on Windows
and use WSL2 an error will follow after the localhost address,
which can be ignored though.

It can happen that H5Web visualizations show differences across web browsers.

### Calling the DATACONVERTER

There is a jupyter notebook (ipynb) for each technique which you should
use to interact with the tool.

## where should one place the files
For the dataconverter, you can find the respective notebooks in

```
tests/data/tools/dataconverter/readers/em-spctrscpy/
```

Go one directory deeper to explore the specific
jupyter notebook for your method of choice.

