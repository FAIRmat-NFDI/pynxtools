## Getting started
Here, we provide examples of how you can convert your data (raw data, numerical data, metadata),
from your acquisition software or electronic lab notebook (ELN), into a NeXus/HDF5 file
using the [built-in readers of pynxtools](https://fairmat-nfdi.github.io/pynxtools/reference/built-in-readers.html).

There is also [documentation](https://fairmat-nfdi.github.io/pynxtools/learn/dataconverter-and-readers.html) of the [dataconverter](../src/pynxtools/dataconverter/README.md) available. You can write a reader plugin if the data for your experimental technique is not supported yet, see documentation [here](https://fairmat-nfdi.github.io/pynxtools/how-tos/build-a-plugin.html).

Note that `pynxtools` offers a number of FAIRmat-supported parsers/readers/data extractors for various experimental techniques via
technique specific plugins. You can find the list [here](https://fairmat-nfdi.github.io/pynxtools/reference/plugins.html). You can find
examples for using each of them in the individual repositories and in their documentation.

For giving feedback to specific parsers/readers/data extractors, please checkout the domain-specific `pynxtools` plugins and their examples
or contact the respective developers directly.
