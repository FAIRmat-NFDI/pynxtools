# Python API reference

This page documents the stable public API of `pynxtools`. All symbols listed here are importable from the sub-package shown. Symbols not listed are internal implementation details and may change without notice.

!!! note "Stability contract"
    Any public symbol follows [semantic versioning](https://semver.org/): breaking changes will be accompanied by a major-version bump and a deprecation period of at least one minor release.

---

## `pynxtools` — top-level

```python
import pynxtools
```

::: pynxtools
    options:
      members:
        - get_nexus_version
        - get_nexus_version_hash
        - get_definitions_url

---

## `pynxtools.nexus` — NeXus file traversal and schema tree

```python
from pynxtools.nexus import NexusFileHandler, NexusVisitor
from pynxtools.nexus import NexusNode, NexusGroup, NexusEntity
from pynxtools.nexus import generate_tree_from, NexusType, NexusUnitCategory
```

### File traversal

::: pynxtools.nexus.handler.NexusVisitor

::: pynxtools.nexus.handler.NexusFileHandler

### Schema tree nodes

::: pynxtools.nexus.nexus_tree.NexusNode
    options:
      members: false

::: pynxtools.nexus.nexus_tree.NexusGroup
    options:
      members: false

::: pynxtools.nexus.nexus_tree.NexusEntity
    options:
      members: false

::: pynxtools.nexus.nexus_tree.NexusLink
    options:
      members: false

::: pynxtools.nexus.nexus_tree.NexusChoice
    options:
      members: false

### Tree construction

::: pynxtools.nexus.nexus_tree.generate_tree_from

::: pynxtools.nexus.nexus_tree.populate_tree_from_parents

---

## `pynxtools.annotator` — NeXus file annotation

```python
from pynxtools.annotator import Annotator
```

::: pynxtools.annotator.annotator.Annotator

---

## `pynxtools.dataconverter` — data conversion and validation

```python
from pynxtools.dataconverter import (
    BaseReader, MultiFormatReader, JsonMapReader,
    Template, generate_template_from_nxdl,
    convert, get_reader, get_names_of_all_readers, ValidationFailed,
    validate_hdf_group_against, validate_dict_against,
)
```

### Reader interface

::: pynxtools.dataconverter.readers.base.reader.BaseReader

::: pynxtools.dataconverter.readers.multi.reader.MultiFormatReader

::: pynxtools.dataconverter.readers.json_map.reader.JsonMapReader

### Template

::: pynxtools.dataconverter.template.Template

::: pynxtools.dataconverter.helpers.generate_template_from_nxdl

### Conversion

::: pynxtools.dataconverter.convert.ValidationFailed

::: pynxtools.dataconverter.convert.convert

::: pynxtools.dataconverter.convert.get_reader

::: pynxtools.dataconverter.convert.get_names_of_all_readers

### Validation

::: pynxtools.dataconverter.validation.validate_hdf_group_against

::: pynxtools.dataconverter.validation.validate_dict_against

---

## `pynxtools.eln_mapper` — ELN schema generation

```python
from pynxtools.eln_mapper import ElnGenerator, ReaderElnGenerator, NomadElnGenerator
```

::: pynxtools.eln_mapper.eln.ElnGenerator

::: pynxtools.eln_mapper.reader_eln.ReaderElnGenerator

::: pynxtools.eln_mapper.schema_eln.NomadElnGenerator

---

## `pynxtools.testing` — reader plugin test utilities

```python
from pynxtools.testing import ReaderTest
```

::: pynxtools.testing.nexus_conversion.ReaderTest

### NOMAD example testing

!!! note "Requires nomad-lab"
    The following helpers are available only when `nomad-lab` is installed.
    The module guards itself with `pytest.skip` at import time if nomad is absent.

```python
from pynxtools.testing import get_file_parameter, parse_nomad_examples
```

::: pynxtools.testing.nomad_example.get_file_parameter

::: pynxtools.testing.nomad_example.parse_nomad_examples

::: pynxtools.testing.nomad_example.example_upload_entry_point_valid

---

## `pynxtools.nomad` — NOMAD integration

!!! warning "nomad-lab required"
    The symbols in this sub-package require `nomad-lab` to be installed:
    ```
    pip install pynxtools[nomad]
    ```

```python
from pynxtools.nomad.parsers import NomadVisitor, NexusParser
```

::: pynxtools.nomad.parsers.parser.NomadVisitor

::: pynxtools.nomad.parsers.parser.NexusParser

---

## `pynxtools.units` — NeXus unit validation

```python
from pynxtools.units import NXUnitSet
```

::: pynxtools.units.NXUnitSet
