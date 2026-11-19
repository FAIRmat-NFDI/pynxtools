# Write a file parser for your plugin

A reader plugin often supports several file formats, or several versions of one format. pynxtools offers three building blocks so that each plugin doesn't have to write its own:

- `FileProbe` (in `pynxtools.dataconverter.readers.parsers.probe`): a cheap, read-only view of one input file;
- `FileParser` (in `pynxtools.dataconverter.readers.parsers.file_parser`): the base class for a parser of one file format;
- `ParsedData` (in `pynxtools.dataconverter.readers.parsers.parsed_data`): what a parser read for one NeXus entry.

This guide shows how to write a parser with them and how to call it from your reader.

## A minimal parser

The example reads text files that start with a line like `SPECTRUM 1.2`, followed by one number per line:

```python
import numpy as np

from pynxtools.dataconverter.readers.parsers.file_parser import FileParser
from pynxtools.dataconverter.readers.parsers.parsed_data import ParsedData
from pynxtools.dataconverter.readers.parsers.versioning import normalize_version


class SpectrumTextParser(FileParser):
    supported_file_extensions = (".txt", ".dat")
    supported_versions = (((1, 0), (2, 0)),)  # 1.0 up to, but not including, 2.0
    supported_vendor = "My Instruments"

    @classmethod
    def matches_file(cls, probe):
        return (probe.text_head or "").startswith("SPECTRUM")

    @classmethod
    def detect_version(cls, probe):
        first_line = probe.text_head.splitlines()[0]
        words = first_line.split()
        return normalize_version(words[1]) if len(words) > 1 else None

    def _parse(self, probe, **options):
        lines = probe.path.read_text().splitlines()[1:]
        self._data["entry"] = ParsedData(
            data={"counts": np.array([float(line) for line in lines])},
            metadata={"instrument/vendor": self.supported_vendor},
            dims={"counts": ["channel"]},
        )
```

A subclass sets `supported_file_extensions` and implements `matches_file` and `_parse`. A version-aware parser also sets `supported_versions` and implements `detect_version`.

`matches_file` and `detect_version` must be class methods that take a `FileProbe`. `supported_file_extensions` must be a tuple of non-empty strings. Both are checked when the class is defined, so a mistake raises a `TypeError` as soon as the plugin is imported.

## Recognizing your files

A reader creates one `FileProbe` per input file, with `FileProbe.from_path(path)`. Every parser looks at the same probe, and the probe reads each piece of the file at most once:

| Attribute | What it gives |
|---|---|
| `path`, `size`, `suffixes` | the file, its size in bytes, and its lower-case suffixes, e.g. `(".mtex", ".h5")` |
| `head` | the first 64 KiB as bytes |
| `text_head` | the head as text, or `None` for binary files |
| `has_suffix(suffix)` | whether the name ends with `suffix`, ignoring case; compound suffixes such as `.mtex.h5` work |
| `is_hdf5`, `hdf5_root_keys`, `hdf5_root_attrs` | HDF5 detection, and the names and attributes of the root group (no data is read) |
| `is_zip` | zip detection |
| `is_tiff`, `tiff_tags` | TIFF detection, and the tags of the first page (no image is read) |

`matches_file` should recognize the format from its content, for example a header line, HDF5 keys or TIFF tags, not only from the file name. Keep it cheap: it runs for every input file and every parser. It doesn't need to catch exceptions, because `match` does that.

## Declaring supported versions

`detect_version` returns the file's version as a tuple, or `None` if the file has none. Use `normalize_version` to turn a version string into a tuple. How to choose `supported_versions` is described in [Declare which file-format versions a parser supports](declare-file-format-versions.md).

## Checking whether a parser reads a file

`match(probe)` decides whether a parser reads a file. It checks, in this order:

1. the extension, against `supported_file_extensions`;
2. the content, with `matches_file`;
3. the version, with `detect_version` and `supported_versions`.

It returns a `MatchResult` that is true if all checks passed. Otherwise it is false and its `reason` says why, for example:

```text
File 'scan.txt' has version 2.1, which SpectrumTextParser does not support. Supported versions: 1.0 – 2.0.
```

`match` never raises: an error in `matches_file` or `detect_version` becomes the reason. Show the reasons to the user when no parser reads a file.

## Parsing into `ParsedData`

`parse(probe, **options)` clears `data`, calls your `_parse` and sets the `source` of every entry to the parsed file, unless `_parse` set one. It does not repeat the checks of `match`, so call it only for files that matched.

In `_parse`, fill `self._data` with one `ParsedData` per NeXus entry, keyed by the entry name:

- `data`: the arrays, addressed by `@data:<key>` in the config file. Values can be numpy arrays (also `np.memmap`, to map large binary files instead of loading them), `xarray.DataArray`, or an `HDF5Reference(file, path)` for a dataset that should stay in its source HDF5 file.
- `metadata`: flat key-value metadata with `/`-separated keys, addressed by `@attrs:<key>`.
- `dims`: the dimension names per data key.

`ParsedData.get_metadata(path)` finds a key exactly, or else the first key that ends with `"/" + path`. If several keys end with it, a warning names them all; write the full key in the config file to pick another one. After the config file has been processed, `unused_metadata` lists the keys that no lookup used.

## Metadata parsers

Some files only add metadata to the entries of another file, for example a quantification export next to the spectra. A parser for such a file sets:

```python
class SpectrumResultsParser(FileParser):
    role = "metadata"
    compatible_primary = (SpectrumTextParser,)
    supported_primary_versions = (((1, 5), None),)  # files of version 1.5 and newer
    supported_file_extensions = (".csv",)
    ...
```

`SpectrumResultsParser.accepts_primary(SpectrumTextParser, version=version)` says whether it can add to the entries read by `SpectrumTextParser` from a file of that version. Pass the primary file's version from `SpectrumTextParser.detect_version(probe)`. Without `version`, only the declared ranges are compared, which says that the two parsers work together for some files, not for a given file.

## Using the parsers in your reader

Until the `MultiFormatReader` chooses parsers by itself, call them from your reader:

```python
from pynxtools.dataconverter.readers.parsers.probe import FileProbe

PARSERS = (SpectrumTextParser,)


def parse_file(path):
    probe = FileProbe.from_path(path)
    results = {parser: parser.match(probe) for parser in PARSERS}
    matching = [parser for parser, result in results.items() if result]
    if len(matching) != 1:
        reasons = "\n".join(
            f"  - {parser.__name__}: {result.reason}"
            for parser, result in results.items()
        )
        raise ValueError(f"No single parser reads '{probe.path.name}':\n{reasons}")
    parser = matching[0]()
    parser.parse(probe)
    return parser.data
```

## Testing your parsers

- For each example file, check that `match` accepts it for its own parser and rejects it for all others, so no two parsers claim the same file.
- Check the reasons for typical wrong files, e.g. an unsupported version.
- Check `parse` against the values you expect in `data` and `metadata`.
