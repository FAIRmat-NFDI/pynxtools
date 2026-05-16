# NeXus Metainfo Generation (Phase 1)

!!! warning "In development"
    This page describes a new code generation system currently under active development.
    The API, file layout, and generated output may change before this feature is
    officially released.

---

## Overview

The existing pynxtools NOMAD integration compiles all NXDL base classes and
application definitions from raw XML at import time inside `nomad/schema_packages/schema.py`.
This approach works but tightly couples NXDL parsing to schema registration, makes the
generated schema hard to inspect or extend, and produces no persistent Python artifacts
that domain plugins can build on.

Phase 1 of the NeXus–NOMAD Metainfo refactor introduces a **code generator** that reads
the NeXus definitions through the `NexusNode` API and writes one Python file per NXDL
base class.  Each generated file is a normal importable Python module containing a single
NOMAD `Section` class that carries structured annotations connecting every quantity and
group back to its NXDL definition.

The existing `nexus_schema` entry point is untouched.  Everything in Phase 1 is purely
additive.

---

## Architecture

```
NexusNode API
    │  build_base_class_node(nx_name)
    │  → NexusGroup with pre-populated children
    ▼
nxdl_to_metainfo.py             ← generator
    │  build_context(nx_name)   ← builds Jinja2 template context
    │  render(context)          ← Jinja2 + black
    │  write_base_class(nx_name)
    ▼
metainfo/base_classes/<stem>.py ← generated Python files (142 total)
    ▼
metainfo/_package.py            ← assembles NOMAD Package
    │  build_package()
    ▼
NOMAD Package (section_definitions[])
```

---

## The NexusNode layer

### Why NexusNode, not raw XML

All NXDL attribute reading goes through the `NexusNode` API
(`pynxtools.dataconverter.nexus_tree`).  No raw XML attribute access happens inside the
generator.  This gives:

- **Inheritance resolution**: NexusNode follows the `extends` chain and merges attributes
  from parent classes.  The generator never needs to know about inheritance.
- **Stable surface**: if the NXDL XML format changes, only `nexus_tree.py` needs to
  change; the generator and all generated files stay the same.
- **Testability**: unit tests target `NexusNode` properties, not generator output.

### `build_base_class_node()`

```python
from pynxtools.dataconverter.nexus_tree import build_base_class_node

root = build_base_class_node("NXdetector")
print(root.nx_class)        # "NXdetector"
print(root.category)        # "base"
print(root.deprecated)      # None  (or a deprecation string)
for child in root.children:
    print(child.nx_type, child.name)  # "field" "data", "group" "NXtransformations", ...
```

`build_base_class_node(nx_name)` is the single entry point into the NexusNode tree for
base classes.  It:

1. Calls `get_nxdl_root_and_path(nx_name)` to load the primary XML element.
2. Builds the full inheritance chain via `get_all_parents_for()`.
3. Constructs a `NexusGroup` root with the chain as `.inheritance`.
4. Calls `populate_direct_children()` to add all first-level children
   (fields, groups, attributes, links) without recursing.
5. For each field child, calls `populate_direct_children()` again so
   field-level attributes are accessible as `field.children`.

### New NexusNode attributes (Phase 1 additions)

The following typed class attributes were added to support the generator.
All are set in `__init__` via a `_set_*()` method that reads from `self.inheritance[0]`.

#### `NexusNode`

| Attribute | Type | Source (NXDL) |
|-----------|------|--------------|
| `deprecated` | `str \| None` | `@deprecated` |

#### `NexusGroup`

| Attribute | Type | Source (NXDL) |
|-----------|------|--------------|
| `category` | `str` | `@category` (default `"base"`) |
| `restricts` | `bool` | `@restricts` |
| `ignore_extra_groups` | `bool` | `@ignoreExtraGroups` |
| `ignore_extra_fields` | `bool` | `@ignoreExtraFields` |
| `ignore_extra_attributes` | `bool` | `@ignoreExtraAttributes` |
| `symbols` | `dict[str, str] \| None` | `<symbols>/<symbol>` elements |

#### `NexusEntity` (field / attribute)

| Attribute | Type | Source (NXDL) |
|-----------|------|--------------|
| `interpretation` | `str \| None` | `@interpretation` |
| `long_name` | `str \| None` | `@long_name` |

---

## Annotation models

Two `AnnotationModel` subclasses carry all NeXus-specific metadata on generated
sections and quantities.

### `NeXusGroup`

Attached to `Section.m_def` for every generated class and to `SubSection` instances
for every group child.

```python
class NeXusGroup(AnnotationModel):
    nx_class: str
    name: str | None = None
    name_type: Literal["specified", "any", "partial"] = "specified"
    category: Literal["base", "application", "contributed"] = "base"
    optionality: Literal["required", "recommended", "optional"] = "optional"
    restricts: bool = False
    ignore_extra_groups: bool = False
    ignore_extra_fields: bool = False
    ignore_extra_attributes: bool = False
    symbols: dict[str, str] | None = None
    min_occurs: int | None = None
    max_occurs: int | None = None
    deprecated: str | None = None
```

### `NeXusQuantity`

Attached to every `Quantity` for field and attribute children.

```python
class NeXusQuantity(AnnotationModel):
    kind: Literal["field", "attribute"]
    name: str
    type: str = "NX_CHAR"
    name_type: Literal["specified", "any", "partial"] = "specified"
    optionality: Literal["required", "recommended", "optional"] = "optional"
    units: str | None = None
    enumeration: list[str] | None = None
    open_enum: bool = False
    parent_field: str | None = None
    interpretation: str | None = None
    long_name: str | None = None
    deprecated: str | None = None
```

---

## Generated file layout

```
src/pynxtools/nomad/
    annotations.py              # NeXusGroup + NeXusQuantity definition + registration
    converters/
        __init__.py
        _naming.py              # nxdl_to_class_name, BASESECTIONS_MAP, type mapping
        nxdl_to_metainfo.py     # generator: NexusNode → .py via Jinja2
        templates/
            base_class.py.j2    # Jinja2 template
    metainfo/
        __init__.py             # public: build_package()
        _package.py             # assembles NOMAD Package
        base_classes/           # 142 generated .py files
            __init__.py
            entry.py
            sample.py
            detector.py
            ...
        applications/           # Phase 2
        contributed/            # Phase 2
```

### Example generated file (`entry.py`, excerpt)

```python
class Entry(Measurement):
    """Description of a complete, self-consistent measurement."""

    m_def = Section(
        a_nexus_group=NeXusGroup(
            nx_class="NXentry",
            category="base",
            optionality="optional",
        ),
    )

    detector = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.detector.Detector",
        repeats=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdetector",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    start_time = Quantity(
        type=Datetime,
        a_nexus_quantity=NeXusQuantity(
            kind="field",
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="recommended",
        ),
    )
```

---

## Additive-only generation

The generator never removes or renames existing members.  When a file already exists:

- If `force=False` (default): the file is rewritten only if the new source contains
  members that are not yet present in the existing file.
- If `force=True`: the file is always overwritten.
- In `dry_run` mode: returns `True` if the file would differ; no disk write occurs.

Custom `normalize()` methods added directly to generated files are preserved because the
`ast.parse()` check compares member *names*, not content.

---

## CLI

```bash
# Generate one class
pynx generate-metainfo --nx-class NXentry

# Generate all base classes in topological (dependency) order
pynx generate-metainfo --all

# CI check: fail if committed files differ from what the generator would produce
pynx generate-metainfo --all --dry-run

# Force regeneration (overwrite existing files)
pynx generate-metainfo --all --force
```

---

## Package assembly

`metainfo/_package.py` imports all generated base class modules and assembles a single
NOMAD `Package`:

```python
from pynxtools.nomad.metainfo._package import build_package

pkg = build_package()
print(len(pkg.section_definitions), "sections")
```

During `build_package()`, `__init_metainfo__()` resolves all `SubSection.section_def`
string FQNs into live class references.

!!! note "Phase 1 limitation"
    Some base classes reference groups from the contributed definitions
    (e.g. `NXphase` → `NXmicrostructure_ipf`).  Those contributed classes are not
    generated in Phase 1, so the corresponding `SubSection` references remain
    unresolved.  `build_package()` emits a warning and continues rather than raising.
    These cross-category references are resolved in Phase 2.

---

## Base section mapping

Generated classes inherit from NOMAD `basesections` where a semantic match exists:

| NXDL class | Python base class |
|-----------|------------------|
| `NXobject` | `BaseSection` |
| `NXentry` | `Measurement` |
| `NXprocess` | `ActivityStep` |
| `NXsample` | `CompositeSystem` |
| `NXsample_component` | `Component` |
| `NXfabrication` | `Instrument` |
| `NXdata` | `ActivityResult` |
| all others | `BaseSection` |

---

## Naming conventions

### Class names

`nxdl_to_class_name("NXmicrostructure_ipf")` → `"MicrostructureIPF"`

Domain-specific abbreviations (`xrd`, `xps`, `arpes`, `mpes`, `em`, `apm`, `xas`, `afm`, `stm`, `sem`, `tem`, `spm`, `ipf`) are upper-cased; other words are title-cased.

### Quantity names

Field and attribute names are kept as-is (NeXus convention uses snake_case throughout).
Python reserved words and a small set of NOMAD basesections-reserved names get a
`_field` suffix (e.g. `name` → `name_field`).

### Subsection names

Group children with a fixed name use the NXDL name directly
(e.g. `instrument` → `instrument`).  Variadic groups (name type `any`/`partial`) use
the class stem in lower-case (e.g. any `NXdetector` group → `detector`).

### Field-attribute quantities

Attributes that belong to a specific field (e.g. the `units` attribute of `data`) are
emitted as quantities with a double-underscore-separated name:

```python
data__units = Quantity(
    ...,
    a_nexus_quantity=NeXusQuantity(
        kind="attribute",
        name="units",
        parent_field="data",
        ...
    ),
)
```

---

## Relation to existing schema

The generated `metainfo/` package co-exists with `nomad/schema_packages/schema.py`.
Phase 1 does not touch the existing code path.  Once Phase 1 is complete and validated,
Phase 3 will bridge the two by making `schema.py` import from the generated classes
rather than building its own section tree.

---

## Further reading

- [Learn → pynxtools → NOMAD integration](nomad-integration.md)
- `src/pynxtools/nomad/converters/nxdl_to_metainfo.py`
- `src/pynxtools/nomad/annotations.py`
- `src/pynxtools/dataconverter/nexus_tree.py`
