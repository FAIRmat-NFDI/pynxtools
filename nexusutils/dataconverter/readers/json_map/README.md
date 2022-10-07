# JSON Map Reader

This reader allows you to convert either data from a .json file or an xarray exported as a .pickle using a flat .mapping.json file.

It accepts any NXDL file that you like as long as your mapping file contains all the fields.
Please use the --generate-template function of the dataconverter to create a .mapping.json file.

```console
user@box:~$ python convert.py --nxdl NXmynxdl --generate-template > mynxdl.mapping.json
```

There are some example files you can use:


[data.mapping.json](/tests/data/tools/dataconverter/readers/json_map/data.mapping.json)

[data.json](/tests/data/tools/dataconverter/readers/json_map/data.json)

```console
user@box:~$ python convert.py --nxdl NXtest --input-file data.json --input-file data.mapping.json --reader json_map
```

## Contact person in FAIRmat for this reader
Sherjeel Shabih