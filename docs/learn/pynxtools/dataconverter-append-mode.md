# Dataconverter append mode

There are cases where users wish to compose a NeXus/HDF5 file with data from multiple sources. Typical examples include:

- A file should contain multiple `NXentry` instances where each instance applies a different application definition.
- Content under `NXentry` instances is composed from running a specific pynxtools parser plugin plus additional content
  that is injected via software other than `pynxtools` or not even software that is written in Python.

Enabling such use cases while minimizing data copying is the idea behind the append mode of the dataconverter. It is activated by
passing the `--append` flag during [command line invocation](../../tutorial/converting-data-to-nexus.md).

## Possibilities and limitations

**The append mode must not be understood as a functionality that allows an overwriting of existent data.**
We are convinced that written data should be immutable. Therefore, using the append mode demands to accept the following assumptions:

- Only groups, datasets, or attributes not yet existent can be added when in append mode.
  The implementation catches attempts of overwriting existent HDF5 objects,
  emitting respective logging messages.
- When in append mode, the internal validation of the `template` dictionary is switched off,
  irrespective if `--skip-verify` is passed or not.
  Instead, users should validate [the HDF5 file](../../how-tos/pynxtools/validate-nexus-files.md) when having the file compositing completed.
- The HDF5 library's functionality to reshape existent HDF5 datasets is not supported by `pynxtools`.

## Interpreting root level attributes

Note that `pynxtools` sets several attributes at the root level of a NeXus/HDF5 file. These values are defined by whichever tool writes them first.
A subsequent writing to the HDF5 file in append mode does not modify these. This makes the interpretation of the following attributes ambiguous
`NeXus_repository`, `NeXus_release`, `HDF5_Version`, `h5py_version`, `creator`, `creator_version`, `file_time` and `file_update_time`.

When in append mode, `pynxtools` adds the root level attribute `append_mode = "True"` which flags the file as an artifact that was composed
from at least one pynxtools tool running in append mode. Note that the absence of this flag does not guarantee that the file was written
by `pynxtools` or its plugins, as also other software could have written the NeXus file.

Until the NeXus standard allows users to link or define these attributes at the HDF5 object level, i.e. for groups, datasets, and attributes, separately,
we advise to no mix tools that write content that adheres to different versions of the NeXus definitions. Note that the `validate` functionality
of `pynxtools` can currently not detect which objects within an HDF5 file were written with which NeXus or tool version. The validation concludes from
the combination of the `ENTRY/definition`, `ENTRY/definition/@version`, and `/@NeXus_version` attributes.

## Time-stamped HDF5 objects

Note that the HDF5 library has the low-level feature to timestamp individual HDF5 objects. By default though, this feature is deactivated
as per decision of the HDF5 Consortium. The choice was made to prevent that changing timestamp values change the hash of the entire file content.
Note that the `pynxtools-em` plugin includes a [`hfive_base` parser](https://github.com/FAIRmat-NFDI/pynxtools-em/blob/main/src/pynxtools_em/parsers/hfive_base.py)
that can compute hashes from the content of individual HDF5 objects. Users are advised to blacklist timestamp attributes like `file_time`, and `file_update_time`
when comparing the binary content of two HDF5 files using this parser. 

