# FAIRmat-supported `pynxtools` plugins

There are a number of plugins available for `pynxtools` that are maintained within FAIRmat. These are extensions of `pynxtools` used for reading data of specific experimental techniques and/or file formats.

## Photoemission spectroscopy


| Repository  | Description | Docs | PyPI |
|-----------------|-------------|:----:|:----:|
| [pynxtools-mpes](https://github.com/FAIRmat-NFDI/pynxtools-mpes/) | Reader plugin for multi-dimensional photoelectron spectroscopy (MPES) data. | | [📦](https://pypi.org/project/pynxtools-mpes/) |
| [pynxtools-xps](https://github.com/FAIRmat-NFDI/pynxtools-xps/) | Reader plugin for X-ray photoelectron spectroscopy (XPS) data from various vendors/sources. | [📚](https://fairmat-nfdi.github.io/pynxtools-xps/) | [📦](https://pypi.org/project/pynxtools-xps/) |
<!-- | [pynxtools-focus](https://github.com/FAIRmat-NFDI/pynxtools-focus/) | A reader plugin for MPES data obtained with a [FOCUS GmbH](https://www.focus-gmbh.com//) instrument. | [📚]() | [📦]() | -->

## Electron microscopy

| Repository  | Description | Docs | PyPI |
|-----------------|-------------|:----:|:----:|
| [pynxtools-em](https://github.com/FAIRmat-NFDI/pynxtools-em/) | Reader plugin for electron microscopy (EM) data from various vendors/sources. | [📚](https://fairmat-nfdi.github.io/pynxtools-em/) | [📦](https://pypi.org/project/pynxtools-em/) |

## Atom probe microscopy/tomography

| Repository  | Description | Docs | PyPI |
|-----------------|-------------|:----:|:----:|
| [pynxtools-apm](https://github.com/FAIRmat-NFDI/pynxtools-apm/) | Reader plugin for atom probe microscopy (APM) as well as related field ion microscopy (FIM) data. | [📚](https://fairmat-nfdi.github.io/pynxtools-apm/) | [📦](https://pypi.org/project/pynxtools-apm/) |

## Optical spectroscopy

| Repository  | Description | Docs | PyPI |
|-----------------|---------------------------------|:----:|:----:|
| [pynxtools-ellips](https://github.com/FAIRmat-NFDI/pynxtools-ellips/) | Reader plugin for ellipsometry data. | [📚](https://fairmat-nfdi.github.io/pynxtools-ellips/) | [📦](https://pypi.org/project/pynxtools-ellips/) |
| [pynxtools-raman](https://github.com/FAIRmat-NFDI/pynxtools-raman/) | Reader plugin for Raman data. | | [📦](https://pypi.org/project/pynxtools-raman/) |

## Scanning probe microscopy

| Repository  | Description | Docs | PyPI |
|-----------------|-------------|:----:|:----:|
| [pynxtools-spm](https://github.com/FAIRmat-NFDI/pynxtools-spm/) | Reader plugin for scanning probe microscopy (SPM). | [📚](https://fairmat-nfdi.github.io/pynxtools-spm/) | [📦](https://pypi.org/project/pynxtools-spm/) |

## X-ray diffraction

| Repository  | Description | Docs | PyPI |
|-----------------|-------------|:----:|:----:|
| [pynxtools-xrd](https://github.com/FAIRmat-NFDI/pynxtools-xrd/) | pynxtools reader plugin for X-ray diffraction data. | | [📦](https://pypi.org/project/pynxtools-xrd/) 

## Others

| Repository  | Description | Docs | PyPI |
|-----------------|-------------|:----:|:----:|
| [pynxtools-igor](https://github.com/FAIRmat-NFDI/pynxtools-igor/) | A general reader plugin for [Igor Pro](https://www.wavemetrics.com/) Binary Wave data. | [📚](https://fairmat-nfdi.github.io/pynxtools-igor/) | [📦](https://pypi.org/project/pynxtools-igor/) |

## Installation

You can install each of the plugins together with `pynxtools` by passing the name of the plugin as an extra to the pip install call. For example, for the `pynxtools-mpes` plugin:

=== "uv"

    ```bash
    uv pip install pynxtools[mpes]
    ```

=== "pip"

    ```bash
    pip install pynxtools[mpes]
    ```

In addition, you can also install all of the pynxtools reader plugins which are maintained by FAIRmat by passing the `[convert]` extra to the pip install call:

=== "uv"

    ```bash
    uv pip install pynxtools[convert]
    ```

=== "pip"

    ```bash
    pip install pynxtools[convert]
    ```

<!-- There is also a [cookiecutter template](https://github.com/FAIRmat-NFDI/pynxtools-plugin-template) available for creating your own pynxtools plugin.-->
