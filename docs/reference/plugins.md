# Plugins
There are a number of plugins available for pynxtools that are maintained within FAIRmat. These are extensions of pynxtools used for reading data of specific experimental techniques and/or file formats.

### Photoemission spectroscopy
- [**pynxtools-mpes**](https://github.com/FAIRmat-NFDI/pynxtools-mpes): A reader for multi-dimensional photoelectron spectroscopy (MPES) data.
- [**pynxtools-xps**](https://github.com/FAIRmat-NFDI/pynxtools-xps): A reader for X-ray photoelectron spectroscopy (XPS) data from various vendors. Documentation can be found [here](https://fairmat-nfdi.github.io/pynxtools-xps/).
<!-- - [**pynxtools-focus**](https://github.com/FAIRmat-NFDI/pynxtools-focus): A reader for MPES data obtained with a [FOCUS GmbH](https://www.focus-gmbh.com//) instrument.-->

### Electron microscopy
- [**pynxtools-em**](https://github.com/FAIRmat-NFDI/pynxtools-em): A reader for electron microscopy data from various vendors. Documentation can be found [here](https://fairmat-nfdi.github.io/pynxtools-em/).

### Atom probe tomography
- [**pynxtools-apm**](https://github.com/FAIRmat-NFDI/pynxtools-apm): A reader for atom probe as well as related field ion microscopy data. Documentation can be found [here](https://fairmat-nfdi.github.io/pynxtools-apm/).

### Optical spectroscopy
- [**pynxtools-ellips**](https://github.com/FAIRmat-NFDI/pynxtools-ellips): A reader for ellipsometry data. Documentation can be found [here](https://fairmat-nfdi.github.io/pynxtools-ellips/).
- [**pynxtools-raman**](https://github.com/FAIRmat-NFDI/pynxtools-raman): A reader for Raman data.

### Scanning probe microscopy
- [**pynxtools-stm**](https://github.com/FAIRmat-NFDI/pynxtools-stm): A reader for scanning tunneling microscopy (SPM) and spectroscopy (STS) data.

### X-ray diffraction
- [**pynxtools-xrd**](https://github.com/FAIRmat-NFDI/pynxtools-xrd): A reader for X-ray diffraction data.

### Others
- [**pynxtools-igor**](https://github.com/FAIRmat-NFDI/pynxtools-igor): A general reader for [Igor Pro](https://www.wavemetrics.com/) Binary Wave data.




## Installation

You can install each of the plugins together with pynxtools by passing the name of the plugin as an extra to the pip install call. For example, for the `pynxtools-mpes` plugin:

```console
pip install pynxtools[mpes]
```

In addition, you can also install all of the pynxtools reader plugins which are maintained by FAIRmat by passing the `[convert]` extra to the pip install call:

```console
pip install pynxtools[convert]
```

<!-- There is also a [cookiecutter template](https://github.com/FAIRmat-NFDI/pynxtools-plugin-template) available for creating your own pynxtools plugin.-->
