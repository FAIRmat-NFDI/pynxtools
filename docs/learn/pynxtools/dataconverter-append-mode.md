# Dataconverter append mode

There are cases where users wish to compose a NeXus/HDF5 file with data from multiple sources. Typical examples include:

- A file should contain multiple `NXentry` instances where each instance applies a different application definition.
- Content under `NXentry` instances is composed from running a specific pynxtools parser plugin plus additional content
  that is injected via software that might not be written in Python.

Enabling such use cases while minimizing data copying is the idea behind the append mode of the dataconverter. It is activated by
passing the `--append` flag during [command line invocation](../../tutorial/converting-data-to-nexus.md).

**The append mode must not be understood as a functionality that allows overwriting data.** Convinced that data should be immutable,
once generated, the append mode feature works with the following key assumptions:

- Only groups, datasets, or attributes not yet existent can be added when in append mode.
  The implementation catches attempts of overwriting existent such type of HDF5 objects,
  emitting respective logging messages.
- When in append mode, the internal validation of the `template` dictionary is switched off,
  irrespective if `--skip-verify` is passed or not.
  Instead, users should validate [the HDF5 file a posteriori](../../how-tos/pynxtools/validate-nexus-files.md).
- Despite the HDF5 library offers the functionality, a reshaping of HDF5 datasets is not supported.

