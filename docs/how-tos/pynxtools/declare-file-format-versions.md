# Declare which file-format versions a parser supports

Many instrument file formats carry a version string in their header, for example `4.75`, `2019R2` or `v3_1`. A parser can declare which of these versions it has been tested with, so that files it cannot read are rejected with a clear message instead of being parsed wrongly.

The helpers for this live in `pynxtools.dataconverter.readers.parsers.versioning`.

## When to use it

Declaring supported versions is recommended: it makes clear which files a parser supports. Only declare ranges if you know how the format's versioning scheme works and which versions you have actually seen. If you are unsure, leave the ranges empty. Then every file is accepted, including files without a version.

Keep in mind that this can lead to unexpected failures: a file in a version the parser was never tested with is parsed anyway and may fail later or give wrong results. Log an info message in that case, see [below](#telling-the-user-what-was-decided).

## From version string to version tuple

`normalize_version` turns a version string into a tuple that can be compared:

| Version string | Tuple |
|---|---|
| `"4.75"` | `(4, 75)` |
| `"4"` | `(4,)` |
| `"2019R2"` | `(2019, "R", 2)` |
| `"v3_1"` | `("V", 3, 1)` |
| `"3-2"` | `(3, 2)` |

Digits become integers, letters become upper-case strings, and everything else separates the parts.

```python
from pynxtools.dataconverter.readers.parsers.versioning import normalize_version

version = normalize_version(header["version"])
```

## Declaring ranges

Supported versions are a tuple of half-open ranges `(lower, upper)`. The lower bound is included and the upper bound is excluded. `upper=None` means "and everything above".

```python
supported_versions = (
    ((1, 1), (4, 0)),   # 1.1 up to, but not including, 4.0
    ((4, 1), (4, 130)), # 4.1 up to, but not including, 4.130
)
```

To accept only some versions, declare one range per version, up to the next one:

```python
supported_versions = (
    ((1, 2), (1, 3)),  # 1.2
    ((1, 5), (1, 6)),  # 1.5
)
```

There is no way to list single versions exactly: `((1, 2), (1, 3))` also accepts `1.2.7`, but not `1.3` or `1.10`. For most formats that is what you want, because patch releases of a tested version are read the same way.

Check a file's version with `is_version_supported(version, supported_versions)`:

- **no ranges declared** → every file is accepted, also files without a version;
- **ranges declared** → a file without a version (`None`) is rejected, because it cannot fall into any range.

```python
from pynxtools.dataconverter.readers.parsers.versioning import is_version_supported

supported_versions = (((1, 1), (4, 0)),)

is_version_supported((2, 5), supported_versions)  # True
is_version_supported((4, 0), supported_versions)  # False: the upper bound is excluded
is_version_supported(None, supported_versions)  # False: the file has no version
is_version_supported(None, ())  # True: no ranges declared
```

## How versions are compared

- **Trailing zeros don't matter.** `4`, `4.0` and `4.0.0` are the same version. A file that says `4` is therefore *not* inside `[1.1, 4.0)`, but it is inside `[4.0, 5.0)`.
- **Numbers sort before letters.** Numbers and letters at the same position can't be compared in a meaningful way, so pynxtools uses a fixed order instead of failing: `(3,) < ("V", 3)` and `(2019, 1) < (2019, "R", 2)`. This order is a fallback, not a statement about which version is newer. Whenever this fallback decides a version check, pynxtools logs an info message. If a format mixes both kinds of versions, for example `2019.1` and `2019R2`, declare separate ranges for each kind rather than one range that spans both:

  ```python
  supported_versions = (
      ((2019, 1), (2019, 9)),            # numeric releases 2019.1 - 2019.8
      ((2019, "R", 1), (2019, "R", 5)),  # R releases 2019R1 - 2019R4
  )
  ```

## Metadata parsers

A metadata parser can declare which versions of its primary files it works with, in `supported_primary_versions`. For example, the primary parser reads versions 1.0 up to 2.0, and the metadata parser only works with version 1.5 and newer:

```python
from pynxtools.dataconverter.readers.parsers.versioning import (
    is_version_supported,
    version_ranges_overlap,
)

primary_versions = (((1, 0), (2, 0)),)
required_versions = (((1, 5), None),)

version_ranges_overlap(primary_versions, required_versions)  # True
is_version_supported((1, 2), required_versions)  # False
is_version_supported((1, 7), required_versions)  # True
```

- `version_ranges_overlap` answers "can the two parsers work together for some files?". Here they can, for the primary files of version 1.5 up to 2.0.
- `is_version_supported` answers "does this one primary file work?". A file of version 1.2 doesn't, a file of version 1.7 does.

`FileParser.accepts_primary(primary, version=version)` picks the right check for you: with the version of a primary file it checks that file, without one it checks the overlap. See [Write a file parser for your plugin](write-a-file-parser.md#2-add-a-parser-for-metadata-files-optional).

## Telling the user what was decided

`format_version` turns a tuple back into a readable string, e.g. `(2019, "R", 2)` → `"2019.R.2"`, and `format_version_ranges` does the same for a set of ranges, e.g. `(((1, 0), (2, 0)),)` → `">= 1.0 and < 2.0"`. Use them in error and log messages so users see which version their file has and which ranges are supported. `FileParser.match` already does this in its reasons.

If the parser declares no ranges, every file is accepted without a version check. Log an info message in that case, so that a later failure can be traced back to an untested version:

```python
from pynxtools import logger

if not supported_versions:
    logger.info(
        f"{parser_name} declares no supported versions, so the version of "
        f"'{file_name}' was not checked."
    )
```

Comparisons that rely on the numbers-before-letters fallback are logged by `is_version_supported` and `version_ranges_overlap` themselves.
