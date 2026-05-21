# Note on versioning

Keeping track of versions is essential for every software and semantic data modeling activity. We follow [PEP440](https://peps.python.org/pep-0440/) when reporting versions, fetching metadata at run time using [`importlib.metadata`](https://docs.python.org/3/library/importlib.metadata.html). Several versions need to be distinguished. The version of `pynxtools`, the one of the `NeXus definitions`, and those of `h5py` and the `HDF5` library. All these are stored under the root group `/` of the NeXus/HDF5 file.

## `pynxtools`

For `pynxtools` these specifically are the

```
/@creator
/@creator_version
```

attributes.

## NeXus definitions

Each version of `pynxtools` comes bundled with a specific version of the NeXus definitions. Its version is fetched either from git tags or the `nexus-version.txt` artifact as a fallback resulting in the

```
/@NeXus_repository
/@NeXus_release
```

attributes set respectively.

## HDF5

As for `h5py` and `HDF5`, the version is documented via the

```
"/@h5py_version"
"/@HDF5_Version"
```

attributes.

## `pynxtools` plugins

Furthermore, we consider it best practice that each plugin of `pynxtools` writes its version as a `programID` instance of [`NXprogram`](https://github.com/FAIRmat-NFDI/nexus_definitions/blob/fairmat/base_classes/NXprogram.nxdl.xml). `ID` serves as a placeholder that can be either omitted or replaced by an integer if multiple programs need to be distinguished. Counting should start at one, i.e., `program` or `program1` are preferred options.
Specifically, the field `program` should store the distribution (package) name. The attribute `program/@version` should store a version string following PEP440.

## Benefit

With all these version information combined and comparing to the installed version of `pynxtools` and its plugins, it is possible to identify if a NeXus/HDF5 file was created locally or via NOMAD.

