The tools of the NOMAD parser for [NEXUS](https://www.nexusformat.org/) can also be used
without a NOMAD OASIS installation. There are two main use cases:
- Use the DATACONVERTER/em_spctrscpy for transcoding vendor and community files to 
  NeXus files so that these are compliant with a specific NeXus application definition
  [NEXUS-FAIRMAT-PROPOSAL](https://fairmat-experimental.github.io/nexus-fairmat-proposal/).
  In this example NXem.
- Use the YAML2NXDL converter during editing and developing
  NeXus base classes and application definitions.

## Getting started - prepare your environment

It is recommended to install the tool in an own virtual environment as
some installation steps will install specific versions of packages which
might be in conflict with existent ones in your environment.
You can install the tools as standalone tools. We make the following assumptions:
- You have a python in version 3.7 installed. Higher versions can be used but might
  need modifications for specific packages on which nomad-parser-nexus depends.
- You can but do not need to be inside a conda environment.

```
pip install virtualenv && virtualenv --python=python3.7 .nexusenv && source .nexusenv/bin/activate
pip install --upgrade pip==22.2.2 && pip install --upgrade nodejs==0.1.1
pip install jupyterlab_h5web[full]==6.0.1
```

## Getting started - install the nomad-parser-nexus tool

```
git clone https://github.com/nomad-coe/nomad-parser-nexus.git --recursive
cd nomad-parser-nexus/
git branch -a
pip install -e .
```

With these two steps the installation is complete.

### Using the tool

The tool can be used as a command line application or started within jupyter lab:

```
jupyter lab
```

If you are using a Linux operating system, a browser tab should open up
which shows the running jupyter lab instance. If you are on Windows and use WSL2,
																	 
this command into the command line will leave you with a message in the
console reading:

```
...
Jupyter Server <<some version>> is running at.
http://localhost:8888/lab?token=<<some hash value / token>>
...

```

You should copy this localhost address into your browser, so that you can also
see the running jupyter lab instance and interact with it graphically.
													   
If you are on Windows and use WSL2 an error will follow after the localhost address,
which can be ignored though.

It can happen that H5Web visualizations show differences across web browsers.
We observed that for some configurations the H5Web plots are displayed
cleaner for the chrome browser than for firefox.

### Calling the DATACONVERTER

There is a jupyter notebook (ipynb) for each technique which you should
use to interact with the tool.

## Where should one place the files
For the dataconverter, you can find the respective notebooks in

```
tests/data/tools/dataconverter/readers/em-spctrscpy/
```

Go one directory deeper to explore the specific jupyter notebook for your method of choice.

