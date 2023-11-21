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
##### Details on the [mapping.json](/pynxtools/dataconverter/readers/json_map/README.md#the-mappingjson-file) file.

## How to run these examples?

### Automatically merge partial NeXus files
```console
user@box:~$ dataconverter --nxdl NXiv_temp --input-file voltage_and_temperature.nxs --input-file current.nxs --output auto_merged.nxs
```

### Map and copy over data to new NeXus file
```console
user@box:~$ dataconverter --nxdl NXiv_temp --mapping merge_copied.mapping.json --input-file voltage_and_temperature.nxs --input-file current.nxs --output merged_copied.nxs
```

### Map and link over data to new NeXus file
```console
user@box:~$ dataconverter --nxdl NXiv_temp --mapping merge_linked.mapping.json --input-file voltage_and_temperature.nxs --input-file current.nxs --output merged_linked.nxs
```

## Contact person in FAIRmat for this reader
Sherjeel Shabih
