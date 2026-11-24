# Write a file parser for your plugin

!!! info
    This guide shows the steps to write a parser for one file format and to call it from your reader. How file parsers work, what a `FileProbe` offers and how `ParsedData` looks up metadata is explained in [Learn > pynxtools > File parsers](../../learn/pynxtools/file-parsers.md).

    You need a reader plugin to start from, see [Build your own `pynxtools` plugin](build-a-plugin.md). Step 4 uses a reader based on the `MultiFormatReader`, see [Use the `MultiFormatReader`](use-multi-format-reader.md).

The example parser reads text files that start with a line like `SPECTRUM 1.2`, followed by one number per line.

## 1. Write the parser

Subclass `FileParser`, set the extensions it reads, and implement `matches_file` and `_parse`:

```python
import numpy as np

from pynxtools.dataconverter.readers.parsers.file_parser import FileParser
from pynxtools.dataconverter.readers.parsers.parsed_data import ParsedData


class SpectrumTextParser(FileParser):
    supported_file_extensions = (".txt", ".dat")
    supported_versions = (((1, 0), (2, 0)),)  # 1.0 up to, but not including, 2.0
    supported_vendor = "My Instruments"

    @classmethod
    def matches_file(cls, probe):
        # Every file of this example format starts with "SPECTRUM <version>".
        return (probe.text_head or "").startswith("SPECTRUM")

    @classmethod
    def detect_version(cls, probe):
        words = probe.text_head.splitlines()[0].split()
        return words[1] if len(words) > 1 else None

    def _parse(self, probe, **options):
        lines = probe.path.read_text().splitlines()[1:]
        return {
            "entry": ParsedData(
                data={"counts": np.array([float(line) for line in lines])},
                metadata={"instrument/vendor": self.supported_vendor},
                dims={"counts": ["channel"]},
            )
        }
```

- `matches_file` and `detect_version` must be class methods that take a `FileProbe`. `supported_file_extensions` must be a tuple of non-empty strings. A mistake raises a `TypeError` as soon as the plugin is imported.
- In `matches_file`, recognize the format from its content, for example a header line in `probe.text_head`, `probe.hdf5_root_keys` or `probe.tiff_tags`, not only from the file name. It runs for every input file and every parser, so keep it cheap.
- `_parse` returns a dict of `ParsedData`, one per entry, keyed by a name you choose. Arrays go into `data`, flat metadata with `/`-separated keys into `metadata`, and dimension names into `dims`.

## 2. Declare the supported versions

If your format carries a version, set `supported_versions` and implement `detect_version`, as above. `detect_version` returns the version as written in the file (here `"1.2"`), a version tuple, or `None` if the file has none. A string is converted with `normalize_version`.

How to choose `supported_versions` is described in [Declare which file-format versions a parser supports](declare-file-format-versions.md).

## 3. Add a parser for metadata files (optional)

If a file only adds metadata to the entries of another file, for example a quantification export next to the spectra, write a second parser for it and name the parsers whose entries it adds to:

```python
class SpectrumResultsParser(FileParser):
    role = "metadata"
    compatible_primary = (SpectrumTextParser,)
    supported_primary_versions = (((1, 5), None),)  # version 1.5 and newer
    supported_file_extensions = (".csv",)

    @classmethod
    def matches_file(cls, probe):
        return (probe.text_head or "").startswith("RESULTS")

    def _parse(self, probe, **options):
        rows = [line.split(",") for line in probe.path.read_text().splitlines()[1:]]
        return {"entry": ParsedData(metadata={f"results/{k}": v for k, v in rows})}
```

Before you combine its entries with those of a primary file, check that it works with that file's version:

```python
from pynxtools.dataconverter.readers.parsers.probe import FileProbe

probe = FileProbe.from_path("spectrum.txt")
version = SpectrumTextParser.detect_version(probe)
result = SpectrumResultsParser.accepts_primary(SpectrumTextParser, version=version)
if not result:
    print(result.reason)
```

A parser with `role = "primary"` can set `compatible_primary` as well, if its files can also add metadata to another parser's entries.

## 4. Call the parsers from your reader

Put your parsers into a `ParserRegistry`. For each input file, `identify` returns the one parser that reads it:

```python
from pynxtools.dataconverter.readers.parsers.probe import FileProbe
from pynxtools.dataconverter.readers.parsers.registry import ParserRegistry

REGISTRY = ParserRegistry([SpectrumTextParser, SpectrumResultsParser])

probe = FileProbe.from_path("spectrum.txt")
parser = REGISTRY.identify(probe)  # SpectrumTextParser
```

If no parser accepts the file, `identify` raises an `UnsupportedFileError` that lists every parser's reason, so the user sees why their file was rejected. If two parsers accept it, it raises an `AmbiguousFormatError`; see [Learn > pynxtools > File parsers](../../learn/pynxtools/file-parsers.md#choosing-a-parser-parserregistry) for how the registry decides.

In a reader based on the `MultiFormatReader`, call the registry from a handler for your file extensions, and let `get_data`, `get_attr` and `get_data_dims` return the parsed values. The config file then addresses them with `@data:counts` and `@attrs:instrument/vendor`:

```python
from typing import Any

from pynxtools.dataconverter.readers.multi.reader import MultiFormatReader


class SpectrumReader(MultiFormatReader):
    supported_nxdls = ["NXsimple"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parsed: dict[str, Any] = {}
        self.extensions = {
            ".txt": self.handle_parser_file,
            ".dat": self.handle_parser_file,
            ".csv": self.handle_parser_file,
            ".json": self.set_config_file,
        }

    def handle_parser_file(self, file_path: str) -> dict[str, Any]:
        probe = FileProbe.from_path(file_path)
        parser = REGISTRY.identify(probe)()
        parser.parse(probe)
        self.parsed[parser.role] = parser.data["entry"]
        return {}

    def get_attr(self, key: str, path: str) -> Any:
        for entry in self.parsed.values():
            value = entry.get_metadata(path)
            if value is not None:
                return value
        return None

    def get_data(self, key: str, path: str) -> Any:
        return self.parsed["primary"].get_data(path)

    def get_data_dims(self, key: str, path: str) -> list[str]:
        return self.parsed["primary"].get_dims(path)
```

To find the parsers that can add metadata to a primary file, ask the registry with that file's version:

```python
REGISTRY.metadata_parsers_for(SpectrumTextParser, version="1.6")  # [SpectrumResultsParser]
REGISTRY.metadata_parsers_for(SpectrumTextParser, version="1.2")  # []
```

## 5. Test your parsers

- Check that no two parsers claim the same example file. `ambiguities` returns every file that more than one parser accepts, so for your example files it should return nothing:

    ```python
    from pathlib import Path


    def test_no_two_parsers_claim_the_same_file():
        assert REGISTRY.ambiguities(Path("tests/data").rglob("*")) == {}
    ```

- For each example file, check that `REGISTRY.identify` returns its own parser.
- Check the reasons for typical wrong files, for example an unsupported version.
- Check `parse` against the values you expect in `data` and `metadata`.
