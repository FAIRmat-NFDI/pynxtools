# Validation of NeXus files in pynxtools

!!! info "This page explains how validation works in `pynxtools`. For step-by-step usage of the CLI tools, see the [how-to guide](../../how-tos/pynxtools/validate-nexus-files.md)."

Validation checks that the structure, concepts, and data of an HDF5 file conform to a specific NeXus application definition. The output is a categorized list of deviations — missing fields, type mismatches, invalid enumeration values — from which a boolean validity verdict can be derived.

Valid NeXus files are foundational to FAIR data: they guarantee that key contextual information (experiment type, units, acquisition parameters, measurement location) is present, correctly named, and structured in a way any compliant tool can parse.

## How validation works in pynxtools

### The `ValidationVisitor`

Validation in pynxtools is implemented as a `NexusVisitor` subclass called `ValidationVisitor` (in `pynxtools.dataconverter.validation`). It receives node events from `NexusFileHandler` and checks each node against the `NexusNode` tree built from the file's declared application definition.

```
HDF5 file  ──▶  NexusFileHandler  ──▶  ValidationVisitor
                   (traversal)            (checks each node)
                                               │
                                          NexusNode tree
                                    (built from NXDL schema)
```

For a conceptual overview of the visitor architecture, see [pynxtools architecture](architecture.md).

### What is checked

**Required concepts**
: Warnings are logged when a required group, field, or attribute defined in the application definition is absent from the file. This applies to required concepts inside recommended or optional groups as well.

**Name fitting**
: NeXus allows instance names to differ from schema concept names (e.g. `my_detector` for an `NXdetector` group). Each instance name is matched against the schema using NeXus name-fitting rules (see [NeXus naming rules](../nexus/nexus-rules.md#name-resolution)). Errors are raised if a group or field uses the name defined for a *different* NeXus concept type. Unmatched names produce a warning.

**Field and attribute values**

- *Enumerations*: closed enumerations produce a warning if the value is not in the allowed set; open enumerations produce an info message.
- *Data types*: values are checked against the declared [`NexusType`](https://manual.nexusformat.org/nxdl-types.html#index-0) (e.g. `NX_FLOAT`, `NX_CHAR`). Mismatches produce warnings.
- *Units*: units are validated using [`pint`](https://pint.readthedocs.io) by confirming that the given unit's dimensionality matches the field's declared [`NexusUnitCategory`](https://manual.nexusformat.org/nxdl-types.html#unit-categories-allowed-in-nxdl-specifications) (e.g. `NX_ENERGY`). Missing units and orphaned unit attributes are also flagged.
- *Orphaned attributes*: an attribute with no corresponding group or field produces a warning.

**`NXdata` rules**
: The [`NXdata`](https://manual.nexusformat.org/classes/base_classes/NXdata.html) group is the container for plottable data and carries specific structural requirements. The validator checks for the required `@signal` and `@axes` attributes and verifies that signal and axis dimensionality is consistent.

**HDF5 links**
: Links are resolved before checking. The validator also checks for the required `@target` attribute on linked nodes.

**Undocumented concepts**
: NeXus permits additional data beyond what the application definition specifies. Each such addition produces a warning to catch accidental misspellings of field names.

**Reserved suffixes and prefixes**
: NeXus defines [reserved suffixes](https://manual.nexusformat.org/datarules.html#index-6) (e.g. `_set`) and [reserved prefixes](https://manual.nexusformat.org/datarules.html#index-4) that may only be used in specific contexts. The validator flags misuse of either.

## Validation use cases

### During data conversion (write path)

When the `dataconverter` produces an HDF5 file, it validates the `Template` dictionary against the target NXDL before writing. Because the template uses a combined instance-plus-concept notation (`ENTRY[entry]/INSTRUMENT[instrument]/DETECTOR[detector]`), the validator also checks that instance names and concept names are consistent.

As a convenience, the dataconverter automatically:

- removes entries that would produce an invalid file (e.g. a field named the same as a group in the schema),
- silently coerces values to the declared type when safe (e.g. int → float, `"true"` → `True`).

### Validating existing files with `validate_nexus`

For NeXus files produced by other tools, `pynxtools` provides the `validate_nexus` CLI. It applies the same `ValidationVisitor` to any existing HDF5 file and reports deviations.

```bash
validate_nexus path/to/file.nxs
```

Validation of existing files is more direct than template validation: the type of every group, field, and attribute is determined from the file's own structure, so no additional disambiguation is needed.

See the [validation how-to guide](../../how-tos/pynxtools/validate-nexus-files.md) for a worked example and usage details.

### Annotating files with `read_nexus`

`read_nexus` is the companion annotation tool. Where `validate_nexus` checks *conformance*, `read_nexus` surfaces *documentation*: it annotates every node in a NeXus file with the schema description, optionality string, data type, unit category, and inheritance chain from the matching `NexusNode`. It is useful for debugging files and exploring what a given application definition requires.

Both `validate_nexus` and `read_nexus` are backed by the same `NexusFileHandler` traversal; they differ only in the `NexusVisitor` they use (`ValidationVisitor` vs. `Annotator`).

## Limitations

Some NeXus features are not yet fully enforced:

- **Symbols and dimensionality**: inconsistencies in how symbols are defined across base classes mean that some dimensional checks cannot be applied reliably.
- **`NXchoice`**: seldomly used in practice; not fully validated.

These limitations reflect open issues in the NeXus standard itself. Resolution is expected in collaboration with the NeXus community.

## Other validation tools

Several third-party tools can also validate NeXus files:

1. [cnxvalidate — NeXus validation tool written in C](https://github.com/nexusformat/cnxvalidate)
2. [punx — Python Utilities for NeXus HDF5 files](https://github.com/prjemian/punx)
3. [nexpy/nxvalidate — a Python API for validating NeXus files](https://github.com/nexpy/nxvalidate)

See the [dedicated how-to page](../../how-tos/pynxtools/validate-nexus-files-other-tools.md) for a comparison.
