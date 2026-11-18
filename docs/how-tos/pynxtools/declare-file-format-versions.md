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

Check a file's version with `is_version_supported(version, supported_versions)`:

- **no ranges declared** → every file is accepted, also files without a version;
- **ranges declared** → a file without a version (`None`) is rejected, because it cannot fall into any range.

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

If a separate parser only works together with certain versions of a primary parser, `version_ranges_overlap(primary_ranges, required_ranges)` tells you whether two sets of ranges share at least one version. It uses the same comparison rules as above.

## Telling the user what was decided

`format_version` turns a tuple back into a readable string, e.g. `(2019, "R", 2)` → `"2019.R.2"`. Use it in error and log messages so users see which version their file has and which ranges are supported.


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
