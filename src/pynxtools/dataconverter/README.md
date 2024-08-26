# Dataconverter

This tool converts experimental data to NeXus/HDF5 files based on any provided [NXDL schemas](https://manual.nexusformat.org/nxdl.html#index-1).
It contains a set of [readers](readers/) to convert supported data files into a compliant NeXus file.

You can read specific README's of the readers and find usage examples [here](../../examples/).

## Installation

```console
user@box:~$ pip install pynxtools[convert]
```

## Usage

### Commands
- **convert**: This is the top-level command that allows you to use the converter. It can be called directly with ```dataconverter```.
- **generate-template**: This command generates a reader template dictionary for a given NXDL file. It can be called with ```dataconverter generate-template```.

```console
Usage: dataconverter [OPTIONS] COMMAND [ARGS]...

Commands:
  convert*           This command allows you to use the converter...
  generate-template  Generates and prints a template to use for your nxdl.

Info:
  You can see more options by using --help for specific commands. For example:
  dataconverter generate-template --help
```
#### Merge partial NeXus files into one

```console
user@box:~$ dataconverter --nxdl nxdl partial1.nxs partial2.nxs
```

#### Map an HDF5/JSON/(Python Dict pickled in a pickle file)

```console
user@box:~$ dataconverter --nxdl nxdl any_data.hdf5 --mapping my_custom_map.mapping.json
```

You can find actual examples with data files at [`examples/json_map`](../../examples/json_map/).


#### Use with multiple input files

```console
user@box:~$ dataconverter --nxdl nxdl metadata data.raw otherfile
```

## Writing a Reader

In case you want to write your own reader for a certain type of experiment, you can find documentation [here](https://fairmat-nfdi.github.io/pynxtools/how-tos/build-a-plugin.html)
