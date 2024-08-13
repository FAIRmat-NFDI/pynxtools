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

Options:
  --help                          Show this message and exit.
  --input-file TEXT               Deprecated: Please use the positional file
                                  arguments instead. The path to the input
                                  data file to read. (Repeat for more than one
                                  file.)
  --reader [example|json_map|json_yml]
                                  The reader to use. default="example"
  --nxdl TEXT                     The name of the NXDL file to use without
                                  extension.This option is required if no '--
                                  params-file' is supplied.
  --output TEXT                   The path to the output NeXus file to be
                                  generated.
  --params-file FILENAME          Allows to pass a .yaml file with all the
                                  parameters the converter supports.
  --ignore-undocumented           Ignore all undocumented fields during
                                  validation.
  --fail                          Fail conversion and don't create an output
                                  file if the validation fails.
  --skip-verify                   Skips the verification routine during
                                  conversion.
  --mapping TEXT                  Takes a <name>.mapping.json file and
                                  converts data from given input files.

Commands:
  convert*           This command allows you to use the converter...
  generate-template  Generates and prints a template to use for your nxdl.

Info:
  You can see more options by using --help for specific commands. For example:
  dataconverter generate-template --help
```

<img src="./convert_routine.svg" />

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

In case you want to write your own reader for a certain type of experiment, you can find documentation [here](https://fairmat-nfdi.github.io/pynxtools/how-tos/build_a_reader.html)
