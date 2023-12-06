# JSON Map Reader

## What is this reader?

This reader is designed to allow users of pynxtools to convert their existing data with the help of a map file. The map file tells the reader what to pick from your data files and convert them to FAIR NeXus files. The following formats are supported as input files:
* HDF5 (any extension works i.e. h5, hdf5, nxs, etc)
* JSON
* Python Dict Objects Pickled with [pickle](https://docs.python.org/3/library/pickle.html). These can contain [xarray.DataArray](https://docs.xarray.dev/en/stable/generated/xarray.DataArray.html) objects as well as regular Python types and Numpy types.

It accepts any NXDL file that you like as long as your mapping file contains all the fields.
Please use the --generate-template function of the dataconverter to create a .mapping.json file.

```console
user@box:~$ dataconverter --nxdl NXmynxdl --generate-template > mynxdl.mapping.json
```

There are some example files you can use:

[data.mapping.json](/tests/data/dataconverter/readers/json_map/data.mapping.json)

[data.json](/tests/data/dataconverter/readers/json_map/data.json)

```console
user@box:~$ dataconverter --nxdl NXtest --input-file data.json --mapping data.mapping.json
```

##### [Example](/examples/json_map/) with HDF5 files.

## The mapping.json file

This file is designed to let you fill in the requirements of a NeXus Application Definition without writing any code. If you already have data in the formats listed above, you just need to use this mapping file to help the dataconverter pick your data correctly.

The mapping files will always be based on the Template the dataconverter generates. See above on how to generate a mapping file.
The right hand side values of the Template keys are what you can modify.

Here are the three different ways you can fill the right hand side of the Template keys:
* Write the nested path in your datafile. This is indicated by a leading `/` before the word `entry` to make `/entry/data/current_295C` below. 
Example:

```json
  "/ENTRY[entry]/DATA[data]/current_295C": "/entry/data/current_295C",
  "/ENTRY[entry]/NXODD_name/posint_value": "/a_level_down/another_level_down/posint_value",
```

* Write the values directly in the mapping file for missing data from your data file. 

```json

  "/ENTRY[entry]/PROCESS[process]/program": "Bluesky",
  "/ENTRY[entry]/PROCESS[process]/program/@version": "1.6.7"
```

* Write JSON objects with a link key. This follows the same link mechanism that the dataconverter implements. In the context of this reader, you can only use external links to your data files. In the example below, `current.nxs` is an already existing HDF5 file that we link to in our new NeXus file without copying over the data. The format is as follows: 
`"link": "<filename>:<path_in_file>"`
Note: This only works for HDF5 files currently.

```json
  "/ENTRY[entry]/DATA[data]/current_295C": {"link": "current.nxs:/entry/data/current_295C"},
  "/ENTRY[entry]/DATA[data]/current_300C": {"link": "current.nxs:/entry/data/current_300C"},
```

## Contact person in FAIRmat for this reader
Sherjeel Shabih
