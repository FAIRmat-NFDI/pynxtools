# JSON Map Reader

## What is this reader?

This reader converts existing data files to FAIR NeXus files using a configuration file
that maps paths in your data to NeXus paths. The following input formats are supported:

* HDF5 (any extension: `.h5`, `.hdf5`, `.nxs`, etc.)
* JSON
* Python Dict Objects pickled with [pickle](https://docs.python.org/3/library/pickle.html),
  which may contain [xarray.DataArray](https://docs.xarray.dev/en/stable/generated/xarray.DataArray.html)
  objects as well as regular Python and NumPy types.

It accepts any NXDL file as long as your configuration file supplies all required fields.

Use `--generate-template` to scaffold a configuration file:

```console
user@box:~$ dataconverter --nxdl NXmynxdl --generate-template > mynxdl.config.json
```

You can find details on the config file format in the documentation at [Reference > Built-in pynxtools readers > The JsonMapReader > The config file](https://fairmat-nfdi.github.io/pynxtools/reference/built-in-readers.html#the-jsonmapreader) and below.


## How to run these examples?

### Map and copy data into a new NeXus file

```console
user@box:~$ dataconverter --reader json_map --nxdl NXiv_temp \
    -c merge_copied.config.json \
    voltage_and_temperature.nxs current.nxs \
    --output merged_copied.nxs
```

### Map and link data into a new NeXus file

```console
user@box:~$ dataconverter --reader json_map --nxdl NXiv_temp \
    -c merge_linked.config.json \
    voltage_and_temperature.nxs current.nxs \
    --output merged_linked.nxs
```

## Config file format

Values in the config file can use the following tokens:

| Format | Description |
|--------|-------------|
| `"@data:some/nested/path"` | Read from the loaded data at the given path |
| `"literal value"` | Written as-is into the NeXus file |
| `{"link": "file.nxs:/path/in/file"}` | HDF5 hard link into another file |

## Deprecated: `.mapping.json` format

> **Warning**: Passing a `.mapping.json` file (via `--mapping` or as a positional argument)
> is deprecated and will be removed in a future release.
> Migrate to a `.config.json` file using `@data:` tokens and pass it with `-c`.

The old mapping format used bare `/data/path` strings as values. Replace them with
`@data:data/path` tokens in your new config file.

## Contact person in FAIRmat for this reader

Sherjeel Shabih
