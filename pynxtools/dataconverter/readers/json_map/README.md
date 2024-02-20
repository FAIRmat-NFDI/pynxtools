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

* Convert custom date and time string to Nexus-compliant ISO format. 
The following entry parses the date and time in a string array `/logs/logs` 
with items like `22/10/22 15:18:26.0164 - Starting...`. 

```json
  "/ENTRY[entry]/end_time": {
    "parse_string":  "/logs/logs",
    "index": "-1",
    "regexp": "[0-9.:/]+ [0-9.:/]+",
    "dateutil": "dmy",
    "timezone": "Europe/Berlin"
  }
```

The properties correspond to operations that are applied to input data, in the order given below.
The `datetime`, `dateutil` and `timestamp` properties are mutually exclusive.

    "parse_string": (required) Data path of the string (array) like for regular datasets.
    "index": (optional) Element index to extract from string array.
        The original data must be a string array.
        If this option is not specified, the original data must be a singular string.
    "regexp": (optional) Match regular expression, keeping only the matching part.
        If the expression contains groups, the result will be a space-delimited concatenation of the matching groups.
        If the expression does not contain explicit groups, the whole match is used.
    "datetime": (optional) Format string for datetime.datetime.strptime function.
        If specified, use datetime.datetime.strptime for date parsing.
    "dateutil": (optional) Date ordering for the dateutil.parser.parse function.
        Possible values 'YMD', 'MDY', 'DMY' (or lower case).
        The dateutil parsers recognizes many date and time formats, but may need the order of year, month and day.
        If specified, use dateutil.parser.parse for date parsing.
    "timestamp": (optional) Interpret the data item as POSIX timestamp.
    "timezone": (optional) Specify the time zone if the date-time string does not include a UTC offset.
        The time zone must be in a dateutil-supported format, e.g. "Europe/Berlin".
        By default, the local time zone is used.

The resulting string replaces the mapped value (dictionary) in the mapping dictionary.
If date parsing is enabled, the resulting string is ISO-formatted as required by the Nexus standard.


## Contact person in FAIRmat for this reader
Sherjeel Shabih
