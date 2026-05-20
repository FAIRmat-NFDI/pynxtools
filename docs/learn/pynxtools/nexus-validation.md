# Validation of NeXus files in pynxtools

!!! info "This page explains how validation works in `pynxtools`. For step-by-step usage of the CLI tools, see the [how-to guide](../../how-tos/pynxtools/validate-nexus-files.md)."

Validation checks that the structure, concepts, and data of an HDF5 file conform to a specific NeXus application definition. The output is a categorized list of deviations — missing fields, type mismatches, invalid enumeration values — from which a boolean validity verdict can be derived.

Valid NeXus files are foundational to FAIR data: they guarantee that key contextual information (experiment type, units, acquisition parameters, measurement location) is present, correctly named, and structured in a way any compliant tool can parse.

### What is checked during validation in pynxtools

**Required concepts**
: Warnings are logged when a required group, field, or attribute defined in the application definition is absent from the file. This applies to required concepts inside recommended or optional groups as well.

**Name fitting**
: NeXus allows instance names to differ from schema concept names (e.g. `my_detector` for an `NXdetector` group). Each instance name is matched against the schema using NeXus name-fitting rules (see [NeXus naming rules](../nexus/nexus-rules.md#name-resolution)). Errors are raised if a group or field uses the name defined for a *different* NeXus concept type. Unmatched names produce a warning.

**Field and attribute values**

- *Enumerations*: closed enumerations produce a warning if the value is not in the allowed set; open enumerations produce an info message.
- *Data types*: values are checked against the declared [`NexusType`](https://manual.nexusformat.org/nxdl-types.html#index-0) (e.g. `NX_FLOAT`, `NX_CHAR`). Mismatches produce warnings.
- *Units*: units are validated using [`pint`](https://pint.readthedocs.io) by confirming that the given unit's dimensionality matches the field's declared [`NexusUnitCategory`](https://manual.nexusformat.org/nxdl-types.html#unit-categories-allowed-in-nxdl-specifications) (e.g. `NX_ENERGY`). Missing units and orphaned unit attributes are also flagged.
- *Orphaned attributes*: an attribute with no corresponding group or field produces a warning.

- **NXDL symbol consistency**: Application definitions can declare [symbols](https://manual.nexusformat.org/nxdl_desc.html#symbolstype) to express that multiple fields share a common dimension size. After all fields in a group have been visited, the validator checks that every field that references the same symbol agrees on its size. A warning is emitted for each symbol where two or more fields report different sizes.
- **`NXdata`**: The [**`NXdata`**](https://manual.nexusformat.org/classes/base_classes/NXdata.html#nxdata) group plays a special rule in NeXus as it is used to define [the plottable data](https://manual.nexusformat.org/examples/python/plotting/index.html). Therefore, `NXdata` comes with a specific set of rules attributes (especially the presence of the `@signal` and `@data`) . The validator checks for the presence of these attributes and also ensures that the dimensionality of the signals and axes match.
- **Links**: When writing NeXus files in HDF5, any group or field can be replaced by an [HDF5 link](https://manual.nexusformat.org/design.html#links) to another group/field. In the validation, these links are resolved and the validity of the resolved object against the NeXus definition is checked. In addition, the presence of the `@target` attribute (which is supposed to be set when using links) is checked.
- **Undocumented concepts**: In NeXus, it is allowed to add additional data that are not defined in the NeXus definitions (e.g., additional fields). In order to prevent unintended use of this feature (arising, for example, from misspelling of instance names), warnings are logged for any such additional data.
- **Reserved suffixes and prefixes**: NeXus defines a number of [reserved suffixes](https://manual.nexusformat.org/datarules.html#index-6). These are suffixes for the name of fields that can only be used if the actual field exists as well (e.g., the suffix `_set` in the field `temperature_set` would be used to report the setpoint for the field `temperature`). If the associated field does not exist, a warning is logged. In addition, NeXus also has a number of [reserved prefixes](https://manual.nexusformat.org/datarules.html#index-4), which can only be used in certain contexts (e.g., in a specific application definition). If such a prefix is used anywhere else, the validation tool produces a warning message.

**HDF5 links**
: Links are resolved before checking. The validator also checks for the required `@target` attribute on linked nodes.

**Undocumented concepts**
: NeXus permits additional data beyond what the application definition specifies. Each such addition produces a warning to catch accidental misspellings of field names.

**Reserved suffixes and prefixes**
: NeXus defines [reserved suffixes](https://manual.nexusformat.org/datarules.html#index-6) (e.g. `_set`) and [reserved prefixes](https://manual.nexusformat.org/datarules.html#index-4) that may only be used in specific contexts. The validator flags misuse of either.

## Validation use cases

### During data conversion (write path)

In addition to the validation tools mentioned above, there is another utility in `pynxtools` called **`pynx read`** (available from the command line after installation). This tool outputs a debug log for a given NeXus file by annotating the data and metadata entries with the schema definitions from the respective NeXus base classes and application definitions to which the file refers to. Read more in [Reference > API for command line tools > pynx read](../../reference/cli-api.md#nexus-file-annotator-pynx-read).

When the `dataconverter` produces an HDF5 file, it validates the `Template` dictionary against the target NXDL before writing. Because the template uses a combined instance-plus-concept notation (`ENTRY[entry]/INSTRUMENT[instrument]/DETECTOR[detector]`), the validator also checks that instance names and concept names are consistent.

As a convenience, the dataconverter automatically:

- removes entries that would produce an invalid file (e.g. a field named the same as a group in the schema),
- silently coerces values to the declared type when safe (e.g. int → float, `"true"` → `True`).

### Validating existing files with `pynx validate`

While we encourage NeXus users to convert their data using the `pynxtools` data conversion pipeline, we also realize that a lot of NeXus files are created using other applications. For such use cases, `pynxtools` provides a **standalone validator** (`pynx validate`). This CLI tool can be used to validate _existing_ HDF5 files against the NeXus application definition they claim to be compliant with. Read more in the [API documentation](../../reference/cli-api.md#nexus-file-validation-pynx-validate).

File validation in pynxtools is implemented as a `NexusVisitor` subclass called `ValidationVisitor` (in `pynxtools.dataconverter.validation`). It receives node events from `NexusFileHandler` and checks each node against the `NexusNode` tree built from the file's declared application definition.

```
HDF5 file  ──▶  NexusFileHandler  ──▶  ValidationVisitor
                   (traversal)            (checks each node)
                                               │
                                          NexusNode tree
                                    (built from NXDL schema)
```

For a conceptual overview of the visitor architecture, see [pynxtools architecture](architecture.md).


The `pynx validate` CLI tool applies the `ValidationVisitor` to any existing HDF5 file and reports deviations.

```bash
pynx validate path/to/file.nxs
```

Validation of existing files is more direct than template validation: the type of every group, field, and attribute is determined from the file's own structure, so no additional disambiguation is needed.

See the [How-tos > pynxtools > Validate and inspect NeXus files](../../how-tos/pynxtools/validate-nexus-files.md) for a worked example and usage details.

### Annotating files with `pynx read`

`pynx read` is the companion annotation tool. Where `pynx validate` checks *conformance*, `pynx read` surfaces *documentation*: it annotates every node in a NeXus file with the schema description, optionality string, data type, unit category, and inheritance chain from the matching `NexusNode`. It is useful for debugging files and exploring what a given application definition requires.

Both `pynx validate` and `pynx read` are backed by the same `NexusFileHandler` traversal; they differ only in the `NexusVisitor` they use (`Annotator`, `ValidationVisitor`, or `NomadVisitor`).

## Limitations

While we try to cover most NeXus use cases in the validation, there are some checks that we do not apply consistently yet. These limitations are mostly due to inconsistencies in the standard or because a feature is seldomly used (like [NeXus choices](https://manual.nexusformat.org/nxdl_desc.html#choicetype)). We are looking forward to resolving such ambiguities with the NeXus community going forward, after which a more rigorous implementation in the validation software is possible.

- **`NXchoice`**: seldomly used in practice; not fully validated.
- **[`variants`](https://manual.nexusformat.org/datarules.html#variants)**: seldomly used in practice and only defined in the NeXus manual; not fully validated, not considered during annotation, unusable in data conversion and NOMAD parsing.

These limitations reflect open issues in the NeXus standard itself. Resolution is expected in collaboration with the NeXus community.

## Other validation tools

Several third-party tools can also validate NeXus files:

1. [cnxvalidate — NeXus validation tool written in C](https://github.com/nexusformat/cnxvalidate)
2. [punx — Python Utilities for NeXus HDF5 files](https://github.com/prjemian/punx)
3. [nexpy/nxvalidate — a Python API for validating NeXus files](https://github.com/nexpy/nxvalidate)

See the [dedicated how-to page](../../how-tos/pynxtools/validate-nexus-files-other-tools.md) for a comparison.
