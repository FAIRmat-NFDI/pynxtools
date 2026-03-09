# Data conversion in pynxtools

One of the main motivations for pynxtools is to provide a principled tool for converting diverse instrument outputs and electronic lab notebook (ELN) data into NeXus-compliant HDF5 files. The `dataconverter` API does exactly that: it reads experimental data using *readers*, validates the result against a NeXus application definition, and writes a valid NeXus/HDF5 file.

## The three-step pipeline

```
Input files  ──▶  Reader  ──▶  Template  ──▶  Validator  ──▶  HDF5 writer
                 (fills)        (dict)        (checks)         (writes .nxs)
```

1. **Read** — one or more readers populate a `Template` dictionary whose keys are NXDL-style paths (e.g. `/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[my_source]/type`).
2. **Validate** — the `ValidationVisitor` checks the populated template against the `NexusNode` tree for the target application definition.
3. **Write** — the validated template is serialized to HDF5 using [`h5py`](https://www.h5py.org/).

The validation step uses the same `ValidationVisitor` that backs the standalone `validate_nexus` CLI. See [pynxtools architecture](architecture.md) for details.

## Readers

A reader is a Python class that takes input files and objects, and returns a populated `Template`. There are two levels to build from:

### `BaseReader` (maximum flexibility)

`BaseReader` is an abstract base class with an empty `read` method. Use it when the target format is unusual enough that none of the `MultiFormatReader` conveniences apply.

```python
from pynxtools.dataconverter.readers.base.reader import BaseReader

class MyDataReader(BaseReader):
    supported_nxdls = ["NXmynxdl"]

    def read(self, template=None, file_paths=None, objects=None, **kwargs):
        # fill template and return it
        return template

READER = MyDataReader
```

### `MultiFormatReader` (recommended)

`MultiFormatReader` is the recommended base class for all new readers. It provides a structured pipeline for handling multiple file formats, a config-file mapping mechanism, and built-in callbacks for data, metadata, and ELN files.

See [The MultiFormatReader](multi-format-reader.md) for an in-depth explanation, and the [how-to guide](../../how-tos/pynxtools/use-multi-format-reader.md) for a concrete implementation example.

## The `Template` dictionary

The `Template` object is the contract between readers and the dataconverter. Keys are NXDL-style paths that encode both the HDF5 instance path and the NeXus concept:

```
/ENTRY[entry]/INSTRUMENT[instrument]/SOURCE[my_source]/type
 \_concept_/\__instance__/\_concept__/\__instance__/ \field/
```

- `ENTRY` — concept name (uppercase, as in the NXDL)
- `entry` — instance name (the actual HDF5 group name)

Bracket notation (`CONCEPT[instance]`) is only required when the NXDL does not fix the group name. For application definitions that fix a name, the concept and instance are the same.

Keys in the template are pre-populated by the dataconverter from the target NXDL with `None` values. The reader fills in actual values. The `Template` also categorizes keys by optionality (`required`, `recommended`, `optional`, `undocumented`) so the validator knows what to enforce.

### Key conventions

| Syntax | Meaning |
|---|---|
| `/ENTRY[entry]/field` | field value |
| `/ENTRY[entry]/field/@units` | unit attribute for `field` |
| `/ENTRY[entry]/GROUP[name]/@NX_class` | NX_class attribute |
| `{"link": "/path/to/target"}` | HDF5 hard link |

### Generating an empty template

```bash
dataconverter generate-template --nxdl NXmynxdl
```

## Matching to NeXus application definitions

Application definitions specify which groups, fields, and attributes a valid NeXus entry must contain, with explicit optionality. The dataconverter validates the populated template against these rules before writing:

- **Required** concepts must be present.
- **Recommended** concepts produce a warning if absent.
- **Optional** concepts are silently ignored if absent.
- Values not defined in the NXDL land in the `undocumented` sub-dict and produce a warning.

## Usage

### Basic conversion

```bash
dataconverter --reader myreader --nxdl NXmynxdl input.dat --output out.nxs
```

### Multiple input files

```bash
dataconverter metadata.yaml data.raw --nxdl NXmynxdl --reader myreader
```

### Merging partial NeXus files

```bash
dataconverter --nxdl NXmynxdl partial1.nxs partial2.nxs
```

### Mapping an HDF5 or JSON file without a custom reader

```bash
dataconverter --nxdl NXmynxdl any_data.hdf5 --mapping my_map.mapping.json
```

The `--mapping` flag activates the built-in `JsonMapReader`. Examples are in [`examples/json_map`](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/examples/json_map/).

## Built-in readers

| Reader | Entry point name | Purpose |
|---|---|---|
| `MultiFormatReader` | — | Abstract base with full pipeline; recommended starting point |
| `BaseReader` | — | Abstract base; minimum interface only |
| `JsonMapReader` | `json_map` | No-code mapping from HDF5/JSON via a `.mapping.json` file |
| `YamlJsonReader` | `json_yml` | Reads YAML/JSON files directly into the template |
| `ExampleReader` | `example` | Minimal working example for developers |

See [Built-in readers](../../reference/built-in-readers.md) for full details.

## Reader plugins

Technique-specific readers are distributed as separate Python packages (e.g. `pynxtools-xps`, `pynxtools-mpes`). Each registers itself via an entry point:

```toml title="pyproject.toml"
[project.entry-points."pynxtools.reader"]
xps = "pynxtools_xps.reader:XPSReader"
```

See [FAIRmat-supported pynxtools plugins](../../reference/plugins.md) for the current list.
