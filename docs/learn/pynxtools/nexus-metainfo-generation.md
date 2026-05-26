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

The existing `nexus_schema` entry point is untouched. Everything in Phase 1 is purely
additive.

---

## Architecture

```
NexusNode API
    │  generate_tree_from(nx_name)
    │  → NexusDefinition root with NexusGroup/NexusField/NexusAttribute children
    ▼
nxdl_to_metainfo.py             ← generator
    │  build_context(nx_name)   ← builds Jinja2 template context
    │  render(context)          ← Jinja2 + ruff
    │  write_base_class(nx_name)
    ▼
metainfo/base_classes/<stem>.py ← generated Python files (one per base class)
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
(`pynxtools.nexus.nexus_tree`). No raw XML attribute access happens inside the
generator.  This gives:

- **Inheritance resolution**: NexusNode follows the `extends` chain and merges attributes
  from parent classes. The generator never needs to know about inheritance.
- **Stable surface**: if the NXDL XML format changes, only `nexus_tree.py` needs to
  change; the generator and all generated files stay the same.
- **Testability**: unit tests target `NexusNode` properties, not generator output.

### `generate_tree_from()`

```python
from pynxtools.nexus.nexus_tree import generate_tree_from, NexusField, NexusAttribute

root = generate_tree_from("NXdetector")
print(root.nx_type)     # "definition"
print(root.category)    # "base"
print(root.deprecated)  # None  (or a deprecation string)
for child in root.children:
    print(child.nx_type, child.name)  # "field" "data", "group" "NXtransformations", ...
```

`generate_tree_from(nx_name)` is the single entry point into the NexusNode tree.  It:

1. Calls `get_nxdl_root_and_path(nx_name)` to load the primary XML element.
2. Builds the full inheritance chain via `get_all_parents_for()`.
3. Constructs a `NexusDefinition` root carrying definition-level metadata.
4. Recursively adds `NexusGroup`, `NexusField`, `NexusAttribute`, `NexusLink`, and
   `NexusChoice` children.

### Node class hierarchy

```
NexusNode (base)
├── NexusDefinition   — root of a generated tree; carries category, symbols, ignore_extra_*
├── NexusGroup        — group child; carries nx_class and occurrence_limits
├── NexusChoice       — choice element (multiple allowed types for one slot)
├── NexusLink         — link element
└── _NexusEntityBase  — shared base for field/attribute
    ├── NexusField    — field child; additionally carries unit, long_name, interpretation,
    │                   and deprecated plotting hints (signal, axis, axes, primary)
    └── NexusAttribute — attribute child; dtype/enum/shape only
```

### Key attributes per class

#### `NexusNode` (all subclasses inherit these)

| Attribute | Type | Source (NXDL) |
|-----------|------|--------------|
| `name` | `str` | element `@name` |
| `nx_type` | `str` | XML tag (`"definition"`, `"group"`, ...) |
| `name_type` | `str` | `@nameType` (default `"specified"`) |
| `optionality` | `str` | `@recommended`/`@required`/`@optional` |
| `variadic` | `bool` | derived from `name_type` |
| `deprecated` | `str \| None` | `@deprecated` |

#### `NexusDefinition`

| Attribute | Type | Source (NXDL) |
|-----------|------|--------------|
| `category` | `str` | `@category` (default `"base"`) |
| `ignore_extra_groups` | `bool` | `@ignoreExtraGroups` |
| `ignore_extra_fields` | `bool` | `@ignoreExtraFields` |
| `ignore_extra_attributes` | `bool` | `@ignoreExtraAttributes` |
| `symbols` | `dict[str, str]` | `<symbols>/<symbol>` elements |

#### `NexusGroup`

| Attribute | Type | Source (NXDL) |
|-----------|------|--------------|
| `nx_class` | `str` | `@type` |
| `occurrence_limits` | `tuple[int\|None, int\|None]` | `@minOccurs`/`@maxOccurs` |

#### `NexusField`

| Attribute | Type | Source (NXDL) |
|-----------|------|--------------|
| `dtype` | `str` | `@type` (default `"NX_CHAR"`) |
| `unit` | `str \| None` | `@units` |
| `shape` | `tuple \| None` | `<dimensions>` element |
| `dim_symbols` | `tuple \| None` | symbol names parallel to `shape` |
| `items` | `list[str] \| None` | `<enumeration>/<item>` |
| `open_enum` | `bool` | `<enumeration open="true">` |
| `long_name` | `str \| None` | `@long_name` |
| `interpretation` | `str \| None` | `@interpretation` |

#### `NexusAttribute`

Shares `dtype`, `shape`, `dim_symbols`, `items`, `open_enum` with `NexusField`.
Has no `unit`, `long_name`, `interpretation`, or plotting-hint attributes.

---

## Annotation models

Three `AnnotationModel` subclasses carry all NeXus-specific metadata on generated
sections and quantities.

### `NeXusDefinition`

Attached to `Section.m_def` of every top-level generated class.  Carries the NXDL
definition identity and class-level validation controls.

```python
class NeXusDefinition(AnnotationModel):
    nx_class: str
    category: Literal["base", "application", "contributed"] = "base"
    restricts: bool = False
    ignore_extra_groups: bool = False
    ignore_extra_fields: bool = False
    ignore_extra_attributes: bool = False
    symbols: dict[str, str] | None = None
    deprecated: str | None = None
```

### `NeXusGroup`

For top-level classes this annotation lives on the **named concept class `m_def`**
rather than on the `SubSection`. For cross-file group references (where no named
concept class is generated in the same file) it lives on the `SubSection`.

Carries the occurrence context: how a group of a given class appears inside its parent.

```python
class NeXusGroup(AnnotationModel):
    nx_class: str
    name: str | None = None
    name_type: Literal["specified", "any", "partial"] = "specified"
    optionality: Literal["required", "recommended", "optional"] = "optional"
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
    annotations.py              # NeXusDefinition + NeXusGroup + NeXusQuantity + registration
    converters/
        __init__.py
        _naming.py              # nxdl_to_class_name, BASESECTIONS_MAP, type mapping
        nxdl_to_metainfo.py     # generator: NexusNode → .py via Jinja2
        templates/
            base_class.py.j2    # Jinja2 template
    metainfo/
        __init__.py             # public: build_package()
        _package.py             # assembles NOMAD Package
        base_classes/           # generated .py files (one per NXDL base class)
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
from nomad.datamodel.metainfo import basesections
from nomad.datamodel.metainfo.basesections import BaseSection
from pynxtools.nomad.annotations import NeXusDefinition, NeXusGroup, NeXusQuantity
from pynxtools.nomad.metainfo.base_classes.object import Object
from pynxtools.nomad.metainfo.base_classes.user import User

class Entry(Object, basesections.Measurement):
    """Description of a complete, self-consistent measurement."""

    m_def = Section(
        a_nexus_definition=NeXusDefinition(
            nx_class="NXentry",
            category="base",
        ),
    )

    # Cross-file SubSection: a_nexus_group lives on the SubSection itself
    # because Detector is defined in a separate file.
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

    # Named concept SubSection: clean — a_nexus_group lives on EntryUser.m_def.
    user = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.entry.EntryUser",
        repeats=True,
        variable=True,
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

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class EntryUser(User):
    """A user contributing to this entry."""

    m_def = Section(
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXuser",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
```

### Named concepts vs. cross-file SubSections

A named concept class is generated only when the group defines **its own quantities** that
differ from the generic class — changed optionality, extra fields, or different
type/units/enumeration.  Groups that exist purely for occurrence context (e.g. a
`backgroundBACKGROUND` group with no additional fields) point their `SubSection` directly
at the generic class; no named concept class is generated.  This rule also prevents
circular imports since every class transitively extends `Object` (the generated `NXobject`
class).

| SubSection target | `a_nexus_group` location |
|---|---|
| Class defined in **this same file** (named concept) | On the concept class `m_def` |
| Class defined in **another file** (cross-file reference) | On the `SubSection` |

This means: named concept classes fully self-describe their occurrence context.
Cross-file SubSections carry the occurrence context because the target class is generic
and may appear in multiple parent contexts.

---

## Shape representation

NXDL `<dimensions>` elements map to `shape` on the generated `Quantity`. Concrete
integer sizes are preserved as-is.  Unbounded or symbolically-named dimensions (e.g.
`nP`, `nz`) become the wildcard `"*"` — NOMAD does not interpret NeXus symbol names.
Symbol definitions from the NXDL `<symbols>` block are preserved in
`NeXusDefinition.symbols` on the class `m_def`.

```python
# NXDL: <dimensions rank="2"><dim index="1" value="nP"/><dim index="2" value="3"/></dimensions>
data = Quantity(
    type=np.float64,
    shape=["*", 3],
    ...
)
```

---

## Additive-only generation

The generator never removes or renames existing members. When a file already exists:

- If `force=False` (default): the file is rewritten only if the new source contains
  members not yet present in the existing file.
- If `force=True`: the file is always overwritten.
- In `dry_run` mode: returns `True` if the file would differ; no disk write occurs.

Custom `normalize()` methods added directly to generated files are preserved because the
`ast.parse()` check compares member *names*, not content.

---

## CLI

```bash
# Generate one class
pynx nomad generate-metainfo --nx-class NXentry

# Generate all base classes in topological (dependency) order
pynx nomad generate-metainfo --all

# CI check: fail if committed files differ from what the generator would produce
pynx nomad generate-metainfo --all --dry-run

# Force regeneration (overwrite existing files)
pynx nomad generate-metainfo --all --force
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

## Inheritance chain

Every generated class extends its **NeXus parent** class (the Python class generated from
the NXDL `extends` attribute) and — where a semantic match exists — additionally inherits
from the corresponding NOMAD base section:

```python
class Object(BaseSection): ...             # NXobject → root
class Entry(Object, basesections.Measurement): ...
class Process(Object, basesections.ActivityStep): ...
class Sample(Component, basesections.CompositeSystem): ...
class SampleComponent(Component, basesections.Component): ...
class Data(Object, basesections.ActivityResult): ...
```

The NOMAD base section is imported **as the module** (`from nomad.datamodel.metainfo import
basesections`) and used as `basesections.Measurement` in the class signature. This avoids
name collisions when the generated NeXus class and the NOMAD base share the same Python
name (e.g. both `Component`).

The secondary NOMAD base is only added when the NeXus `extends` chain does not already
provide it — preventing duplicate entries in the MRO.

| NXDL class | Generated class signature |
|-----------|--------------------------|
| `NXobject` | `Object(BaseSection)` |
| `NXentry` | `Entry(Object, basesections.Measurement)` |
| `NXprocess` | `Process(Object, basesections.ActivityStep)` |
| `NXsample` | `Sample(Component, basesections.CompositeSystem)` |
| `NXsample_component` | `SampleComponent(Component, basesections.Component)` |
| `NXfabrication` | `Fabrication(Object, basesections.Instrument)` |
| `NXdata` | `Data(Object, basesections.ActivityResult)` |
| all others | `<Class>(Object)` |

---

## Naming conventions

### Class names

`nxdl_to_class_name("NXmicrostructure_ipf")` → `"MicrostructureIPF"`

Domain-specific abbreviations (`xrd`, `xps`, `arpes`, `mpes`, `em`, `apm`, `xas`, `afm`, `stm`, `sem`, `tem`, `spm`, `ipf`) are upper-cased; other words are title-cased.

### Quantity names

Field and attribute names are kept as-is (NeXus convention uses snake_case throughout).
Attributes are emitted without the `@` prefix. Python reserved words and a small set of NOMAD basesections-reserved names get a `_field` suffix (e.g. `name` → `name_field`). 

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

- [Learn > pynxtools > NOMAD integration](nomad-integration.md)
