# Dataconverter

This tool converts experimental data to NeXus/HDF5 files based on any provided [NXDL schemas](https://manual.nexusformat.org/nxdl.html#index-1). It contains a set of [readers](readers/) to convert supported data files into a compliant NeXus file.

You can find usage examples [here](../../examples/).

## Usage
`pynxtools` has a number of command line tools that can be used to convert data and verify NeXus files. You can more information about the API [here](https://fairmat-nfdi.github.io/pynxtools/reference/cli-api.html).

## Documentation
In order to understand the dataconverter, these pages might be particularly helpful:

- [Learn : The dataconverter in pynxtools](https://fairmat-nfdi.github.io/pynxtools/learn/dataconverter-and-readers.html)
- [Tutorial: Converting research data to NeXus](https://fairmat-nfdi.github.io/pynxtools/tutorial/converting-data-to-nexus.html)
- [Built-in readers of pynxtools](https://fairmat-nfdi.github.io/pynxtools/reference/built-in-readers.html)
- [Existing reader plugins for different experimental techniques](https://fairmat-nfdi.github.io/pynxtools/reference/plugins.html)
- [How-to guide for writing your own reader/plugin](https://fairmat-nfdi.github.io/pynxtools/how-tos/build-a-plugin.html)
