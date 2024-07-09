# Plugins
There are a number of plugins available for pynxtools that are maintained within FAIRmat. These are extensions of pynxtools used for reading data of specific experimental techniques.

- [**pynxtools-mpes**](https://github.com/FAIRmat-NFDI/pynxtools-mpes): A reader for multi-dimensional photoelectron spectroscopy data.
- [**pynxtools-stm**](https://github.com/FAIRmat-NFDI/pynxtools-stm): A reader for scanning tunneling microscopy (SPM) and spectroscopy (STS) data.
- [**pynxtools-xps**](https://github.com/FAIRmat-NFDI/pynxtools-xps): A reader for X-ray photoelectron spectroscopy (XPS) data. Documentation can be found [here](https://fairmat-nfdi.github.io/pynxtools-xps/).
- [**pynxtools-apm**](https://github.com/FAIRmat-NFDI/pynxtools-apm): A reader for atom probe as well as related field ion microscopy data. Documentation can be found [here](https://fairmat-nfdi.github.io/pynxtools-apm/).
- [**pynxtools-em**](https://github.com/FAIRmat-NFDI/pynxtools-em): A reader for electron microscopy data. Documentation can be found [here](https://fairmat-nfdi.github.io/pynxtools-em/).
- [**pynxtools-ellips**](https://github.com/FAIRmat-NFDI/pynxtools-ellips): A reader for ellipsometry data. Documentation can be found [here](https://fairmat-nfdi.github.io/pynxtools-ellips/).

## Installation

You can install each of the plugins together with pynxtools by passing the name of the plugin as an extra to the pip install call. For example, for the pynxtools-mpes plugin:

```
pip install pynxtools[mpes]
```

In addition, you can also install all of the pynxtools reader plugins which are maintained by FAIRmat by passing the [convert] extra to the pip install call:

```
pip install pynxtools[convert]
```

There is also a [cookiecutter template](https://github.com/FAIRmat-NFDI/pynxtools-plugin-template) available for creating your own pynxtools plugin.
