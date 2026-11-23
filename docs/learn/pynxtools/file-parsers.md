# File parsers

!!! info
    Here, we explain how file parsers recognize and read input files. For the steps to write a parser and to call it from your reader, see [How-tos > pynxtools > Write a file parser for your plugin](../../how-tos/pynxtools/write-a-file-parser.md).

A reader plugin often supports several file formats, or several versions of one format. Instead of each plugin writing its own detection and parsing logic, pynxtools offers three building blocks in `pynxtools.dataconverter.readers.parsers`:

- `FileProbe` (`probe.py`): a cheap, read-only view of one input file, shared by all parsers;
- `FileParser` (`file_parser.py`): the base class for a parser of one file format;
- `ParsedData` (`parsed_data.py`): a container for what a parser read, which the config file addresses with `@data:` and `@attrs:`.

## Recognizing a file: `FileProbe`

A reader creates one `FileProbe` per input file, with `FileProbe.from_path(path)`. Every parser looks at the same probe, and the probe reads each piece of the file at most once:

| Attribute | What it gives |
|---|---|
| `path`, `size`, `suffixes` | the file, its size in bytes, and its lower-case suffixes, e.g. `(".mtex", ".h5")` |
| `head` | the first 64 KiB as bytes |
| `text_head` | the head as text, or `None` for binary files |
| `has_suffix(suffix)` | whether the name ends with `suffix`, ignoring case, e.g. `.mtex.h5` |
| `is_hdf5`, `hdf5_root_keys`, `hdf5_root_attrs` | HDF5 detection, and the names and attributes of the root group (no data is read) |
| `is_zip` | zip detection |
| `is_tiff`, `tiff_tags` | TIFF detection, and the tags of the first page (no image is read) |

None of these checks raises for an unreadable or corrupt file: a broken HDF5 file gives no keys, a broken TIFF no tags. `text_head` covers only the head, so a parser that needs content further into the file reads `path` itself.

The table in [Tutorial > Bring your own data > Identify your format](../../tutorial/bring-your-own-data.md#identify-your-format) lists how common formats can be recognized; `FileProbe` already checks the HDF5, zip and TIFF signatures.

## Deciding whether a parser reads a file: `match`

`FileParser.match(probe)` checks, in this order:

1. the extension, against `supported_file_extensions`;
2. the content, with `matches_file`;
3. the version, with `detect_version` and `supported_versions`.

The content is checked before the version, so that a file of another format with the same extension (`.txt`, `.h5`, `.xml`) is rejected for its format, and `detect_version` only ever reads files of its own format.

`match` returns a `MatchResult` that is true if all checks passed. Otherwise it is false and its `reason` says why, for example:

```text
File 'scan.txt' has version 2.1, which SpectrumTextParser does not support. Supported versions: >= 1.0 and < 2.0.
```

`match` never raises. `matches_file` and `detect_version` are plugin code, so any error can occur in them; it becomes the reason, with its type, e.g. `KeyError: 'header'`. This way, one parser failing on another format's file does not stop the other parsers from being checked, and a reader can show the user why no parser accepted a file.

`match` and `detect_version` are class methods, so no parser is created and the file is not opened again until a parser is chosen. `parse(probe)` then calls the chosen parser's `_parse`, stores the returned entries in `data`, and sets the `source` of each entry to the parsed file, unless `_parse` set one.

## Primary and metadata parsers

A *primary* parser creates entries on its own. Some files only add metadata to the entries of another file, for example a quantification export next to the spectra. A parser for such a file names the parsers whose entries it adds to in `compatible_primary`, and sets `role = "metadata"` if it can do nothing else. A primary parser can set `compatible_primary` too, if its files can also add to another parser's entries.

`accepts_primary(primary, version=None)` says whether a parser can add to the entries of `primary`:

- `primary` must be one of `compatible_primary`, or a subclass of one;
- if `supported_primary_versions` is set and `version` is given (the version of the primary file that was read), that version must lie in `supported_primary_versions`;
- without `version`, `supported_primary_versions` must only overlap with the `supported_versions` of `primary`. That says the two parsers work together for some files, not for a given file, so pass `version` whenever a primary file is known.

## Reading parsed values: `ParsedData`

A `ParsedData` holds:

- `data`: the arrays, addressed by `@data:<key>`. Values can be numpy arrays (also `np.memmap`, to map large binary files instead of loading them), `xarray.DataArray`, or an `HDF5Reference(file, path)` for a dataset that stays in its source HDF5 file;
- `metadata`: flat key-value metadata with `/`-separated keys, addressed by `@attrs:<key>`;
- `dims`: the dimension names per data key, used to expand `*` in config files;
- `source`: the file it was read from.

`get_metadata(path)` finds a key exactly, or else the first key that ends with `"/" + path`. Empty values give `None`, and a `datetime` is returned as an ISO 8601 string. For example:

```python
from pynxtools.dataconverter.readers.parsers.parsed_data import ParsedData

entry = ParsedData(
    metadata={
        "instrument/analyser/energy/@units": "eV",
        "instrument/vendor": "My Instruments",
        "sample/name": "",
    }
)
entry.get_metadata("instrument/vendor")  # "My Instruments" (exact key)
entry.get_metadata("energy/@units")      # "eV" (key ending in "/energy/@units")
entry.get_metadata("sample/name")        # None (empty value)
entry.unused_metadata                    # set(): all three keys were looked up
```

If several keys end with `path`, a warning names them all; write the full key in the config file to pick another one. After the config file has been processed, `unused_metadata` lists the keys that no lookup used, which helps to find metadata the config file does not map yet.

## File parsers and the `MultiFormatReader`

The [`MultiFormatReader`](multi-format-reader.md) calls a handler for each input file, chosen by its extension, and fills the template from the config file through callbacks such as `get_data` and `get_attr`. File parsers fit into this as follows: the handler finds the parser whose `match` accepts the file and calls `parse`, and the callbacks return values from the resulting `ParsedData`. The [how-to](../../how-tos/pynxtools/write-a-file-parser.md#4-call-the-parsers-from-your-reader) shows such a reader. Currently, the MultiFormatReader chooses a handler by file extension only and does not know about file parsers, so your reader calls them from its handler, as in the how-to. 
