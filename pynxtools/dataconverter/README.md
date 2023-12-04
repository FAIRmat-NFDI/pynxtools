# Dataconverter

This tool contains a set of [readers](readers/) to convert supported data files into a compliant NeXus file.

You can read specific Readme's of the readers and find usage examples [here](../../examples/).

## Installation

```console
user@box:~$ pip install git+https://github.com/FAIRmat-NFDI/pynxtools.git
```

## Usage

Converts experimental data to NeXus/HDF5 files based on any provided NXDL.

```console
user@box:~$ dataconverter --help
Usage: dataconverter [OPTIONS]

  The CLI entrypoint for the convert function

Options:
  --input-file TEXT               The path to the input data file to read.
                                  (Repeat for more than one file.)
  --reader [apm|ellips|em_nion|em_om|em_spctrscpy|example|hall|json_map|json_yml|mpes|rii_database|sts|transmission|xps]
                                  The reader to use. default="example"
  --nxdl TEXT                     The name of the NXDL file to use without
                                  extension.
  --output TEXT                   The path to the output NeXus file to be
                                  generated.
  --generate-template             Just print out the template generated from
                                  given NXDL file.
  --fair                          Let the converter know to be stricter in
                                  checking the documentation.
  --params-file FILENAME          Allows to pass a .yaml file with all the
                                  parameters the converter supports.
  --undocumented                  Shows a log output for all undocumented
                                  fields
  --mapping TEXT                  Takes a <name>.mapping.json file and
                                  converts data from given input files.
  --help                          Show this message and exit.
```

#### Merge partial NeXus files into one

```console
user@box:~$ dataconverter --nxdl nxdl --input-file partial1.nxs --input-file partial2.nxs
```

#### Map an HDF5/JSON/(Python Dict pickled in a pickle file)

```console
user@box:~$ dataconverter --nxdl nxdl --input-file any_data.hdf5 --mapping my_custom_map.mapping.json
```

#### You can find actual examples with data files at [`examples/json_map`](../../examples/json_map/).


#### Use with multiple input files

```console
user@box:~$ dataconverter --nxdl nxdl --input_file metadata --input_file data.raw --input_file otherfile
```

## Writing a Reader

This converter allows extending support to other data formats by allowing extensions called readers.
The converter provides a dev platform to build a NeXus compatible reader by providing checking
against a chosen NeXus Application Definition.

Readers have to be placed in the **readers** folder in there own subfolder.
The reader folder should be named with the reader's name and contain a `reader.py`.\
For example: The reader `Example Reader` is placed under [`readers/example/reader.py`](readers/example/reader.py).

Copy and rename `readers/example/reader.py` to your own `readers/mydatareader/reader.py`.

Then implement the reader function:

```python
"""MyDataReader implementation for the DataConverter to convert mydata to NeXus."""
from typing import Tuple, Any

from dataconverter.readers.base.reader import BaseReader


class MyDataReader(BaseReader):
    """MyDataReader implementation for the DataConverter to convert mydata to NeXus."""

    def read(
        self,
        template: dict = None,
        file_paths: Tuple[str] = None,
        objects: Tuple[Any] = None
    ) -> dict:
        """Reads data from given file and returns a filled template dictionary"""
        # Fill the template
        for path in file_paths:
            print(path)

        template["/entry/instrument/scan"] = raw_scan_data

        return template


# This has to be set to allow the convert script to use this reader. Set it to "MyDataReader".
READER = MyDataReader

```

The read function takes a template dictionary based on the provided NXDL file (similar to `--generate-template`)
and the list of all the file paths the user provides with `--input`.
The returned dictionary should contain keys that exist in the template as defined below.
The values of these keys have to be data objects to be populated in the output NeXus file.
They can be lists, numpy arrays, numpy bytes, numpy floats, numpy ints. Practically you can pass any value
that can be handled by the `h5py` package.

The dataconverter can be executed using:

```console
user@box:~$ dataconverter --reader mydata --nxdl NXmynxdl --output path_to_output.nxs
```

### The reader template dictionary

Example:

```json
{
  "/entry/instrument/source/type": "None"
}
```

**Units**: If there is a field defined in the NXDL, the converter expects a filled in /data/@units entry in the template dictionary corresponding to the right /data field unless it is specified as NX_UNITLESS in the NXDL. Otherwise, you will get an exception.

```json
{
  "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[my_source]/data": "None",
  "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[my_source]/data/@units": "Should be set to a string value"
}
```

In case the NXDL does not define a `name` for the group the requested data belongs to, the template dictionary will list it as `/NAME_IN_NXDL[name_in_output_nexus]`
You can choose any name you prefer instead of the suggested name. This allows the reader function to repeat groups defined in the NXDL to be outputted to the NeXus file.

```json
{
  "/ENTRY[my_entry]/INSTRUMENT[my_instrument]/SOURCE[my_source]/type": "None"
}
```

For attributes defined in the NXDL, the reader template dictionary will have the assosciated key with a "@" prefix to the attributes name at the end of the path:

```json
{
  "/entry/instrument/source/@attribute": "None"
}
```

You can also define links by setting the value to sub dictionary object with key `link`:

```python
template["/entry/instrument/source"] = {"link": "/path/to/source/data"}
```

<img src="./convert_routine.svg" />
