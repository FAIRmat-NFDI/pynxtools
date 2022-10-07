The tools can be used with the following two main use cases:
- Use the DATACONVERTER/apm for transcoding vendor and community files to
  NeXus files so that these are compliant with a specific NeXus application definition
  [NEXUS-FAIRMAT-PROPOSAL](https://fairmat-experimental.github.io/nexus-fairmat-proposal/).
  In this example NXapm.
- Use the NYAML2NXDL converter during editing and developing
  NeXus base classes and application definitions.

## Getting started - prepare your environment

Please follow the **installation guide for developers** in the main README

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
