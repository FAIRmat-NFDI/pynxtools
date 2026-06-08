# NeXus Metainfo Generation (Phases 1–2)

!!! warning "In development"
    This page describes a new code generation system currently under active development.
    The API, file layout, and generated output may change before this feature is
    officially released.

---

## Overview

The NeXus–NOMAD Metainfo refactor replaces the runtime XML compilation in `nomad/schema_packages/schema.py`
with a **persistent code generator** that reads the NeXus definitions through the `NexusNode` API
and writes one Python file per NXDL class. Each generated file is a normal importable Python module containing a single NOMAD `Section` class that carries structured annotations connecting every quantity and group back to its NXDL definition.

### What this provides

- **Importable, type-checkable Python classes**: Each NXDL class becomes a NOMAD `Section` class
  in a `.py` file, with structured annotations connecting every quantity and group back to NXDL.
- **Clean naming**: Quantities are named after their NXDL concept (`start_time`, not `start_time__field`).
- **Two entry points**: `nexus_base_classes` (142 base classes) and `nexus_applications` (85 application definitions).
- **Application definitions are Entry subclasses**: `Xps(Entry)` instead of wrappers — see [ADR-006](#adr-006-application-definitions).
- **Backward compatibility**: The old `nexus_schema` entry point is untouched; both systems coexist until Phase 3.

### Current status

- **Phase 1** (complete): 142 NXDL base classes (`category="base"`) generated and tested.
- **Phase 2** (complete): 85 application definitions (`category="application"`) generated; `nexus_applications` entry point active.

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

Six `AnnotationModel` subclasses carry all NeXus-specific metadata on generated
sections and quantities — one per NXDL node kind.  Each annotation is queryable
at runtime via `m_def.m_get_annotations("nexus_field")` etc.

### `NeXusDefinition`

Attached to `Section.m_def` of every top-level generated class.

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

On named concept class `m_def` (group with own quantities, same file) or on the
`SubSection` for cross-file group references.

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

### `NeXusField`

Attached to every `Quantity` derived from a NXDL `<field>` element.  Fields
carry typed data arrays and may have unit categories, interpretation hints,
and long names.

```python
class NeXusField(AnnotationModel):
    name: str
    type: str = "NX_CHAR"
    units: str | None = None
    name_type: Literal["specified", "any", "partial"] = "specified"
    optionality: Literal["required", "recommended", "optional"] = "optional"
    enumeration: list[str] | None = None
    open_enum: bool = False
    interpretation: str | None = None
    long_name: str | None = None
    deprecated: str | None = None
```

### `NeXusAttribute`

Attached to every `Quantity` derived from a NXDL `<attribute>` element (either
group-level or field-level).  Field-level attributes set `parent_field` to the
owning field name (e.g. `parent_field="energy"` for `energy__units`).

```python
class NeXusAttribute(AnnotationModel):
    name: str
    parent_field: str | None = None
    type: str = "NX_CHAR"
    name_type: Literal["specified", "any", "partial"] = "specified"
    optionality: Literal["required", "recommended", "optional"] = "optional"
    enumeration: list[str] | None = None
    open_enum: bool = False
    deprecated: str | None = None
```

### `NeXusLink`

Attached to a `Quantity(type=str)` derived from a NXDL `<link>` element.
The `target` is the schema-level default target path; the parser resolves the
actual HDF5 target at read time.

```python
class NeXusLink(AnnotationModel):
    name: str
    target: str
    optionality: Literal["required", "recommended", "optional"] = "optional"
    deprecated: str | None = None
```

### `NeXusChoice`

Attached to each `SubSection` representing one alternative in a NXDL `<choice>`
block.  A choice allows exactly one NX class to occupy a named slot.  One
SubSection is generated per alternative; all share the same `group_name`.

Naming: `{choice_name}_{class_suffix}` — e.g. `pixel_shape_off_geometry` and
`pixel_shape_cylindrical_geometry` for `<choice name="pixel_shape">`.

```python
class NeXusChoice(AnnotationModel):
    nx_class: str
    group_name: str
    optionality: Literal["required", "recommended", "optional"] = "optional"
    deprecated: str | None = None
```

### Summary: annotation placement

| NXDL element | Generated artifact | Annotation key |
|---|---|---|
| `<definition>` | top-level Section class `m_def` | `nexus_definition` |
| `<group>` (named concept) | concept class `m_def` | `nexus_group` |
| `<group>` (cross-file) | `SubSection` | `nexus_group` |
| `<field>` | `Quantity` | `nexus_field` |
| `<attribute>` | `Quantity` | `nexus_attribute` |
| `<link>` | `Quantity(type=str)` | `nexus_link` |
| `<choice>` alternative | `SubSection` | `nexus_choice` |

---

## Generated file layout

```
src/pynxtools/nomad/
    annotations.py              # NeXusDefinition + NeXusGroup + NeXusField + NeXusAttribute
                                #   + NeXusLink + NeXusChoice + registration
    converters/
        __init__.py
        _mapping.py             # nxdl_to_class_name, BASESECTIONS_MAP, type mapping
        nxdl_to_metainfo.py     # generator: NexusNode → .py via Jinja2
        templates/
            nexus.py.j2    # Jinja2 template
    metainfo/
        __init__.py             # public API: build_base_classes_package(), build_applications_package()
        _package.py             # assembles NOMAD Packages
        base_classes/           # Phase 1: 142 generated base class files
            __init__.py
            entry.py            # Entry(Object, basesections.Measurement)
            sample.py           # Sample(Object, basesections.CompositeSystem)
            detector.py
            ...
        applications/           # Phase 2: 85 generated application definition files
            __init__.py
            arpes.py            # Arpes(Entry) — application specialization of Entry
            xps.py              # Xps(Entry) — application specialization of Entry
            ...
```

---

## Application Definitions: The XpsEntry Decision {#adr-006-application-definitions}

### The design principle: `Xps(Entry)` not `Xps(Object, Measurement)`

In NeXus, every application definition (e.g. `NXxps.nxdl.xml`) wraps exactly one `NXentry` at
the root level. This is not a container pattern — application definitions are **constraint templates**
that describe what an `NXentry` looks like in a specific measurement context.

Therefore, in Python/NOMAD, application definitions inherit from `Entry` directly:

```python
# Phase 2: generated application definition
class Xps(Entry):
    m_def = Section(
        a_nexus_definition=NeXusDefinition(nx_class="NXxps", category="application"),
    )
    # SubSections and Quantities from inside NXxps's NXentry group,
    # with XPS-specific optionality
```

**Why this design** (see [ADR-006](../../data-modeling/nexus-metainfo/adr/ADR-006-application-definitions-are-entry-subclasses.md)):

- `Xps` **is** a specialized kind of Entry, not a wrapper around an entry.
- Parser logic is simpler: directly instantiate `Xps` when an HDF5 file's `NX_class` attribute says `"NXxps"`.
- Inheritance chain is clear: `BaseSection → Object → Entry → Xps`.
- 1:1 mapping of NXentry to NOMAD entry is preserved.

**Named concepts** in applications follow the same rule as base classes: a named concept class
is generated only when a group defines its own quantities. Inherited groups point directly at the
base class.

```python
# Generated only if CoordinateSystem has own quantities:
class XpsCoordinateSystem(CoordinateSystem):
    # XPS-specific changes to the coordinate_system group

# SubSection on Xps uses it if generated, else references the base:
coordinate_system = SubSection(section_def=XpsCoordinateSystem)
```

### Example generated file (`entry.py`, excerpt)

```python
from nomad.datamodel.metainfo import basesections
from nomad.datamodel.metainfo.basesections import BaseSection
from pynxtools.nomad.annotations import NeXusDefinition, NeXusField, NeXusGroup
from pynxtools.nomad.metainfo.base_classes.object import Object
from pynxtools.nomad.metainfo.base_classes.user import User

class Entry(Object, basesections.Measurement):
    """Description of a complete, self-consistent measurement."""

    m_def = Section(
        links=["https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry"],
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
        links=["https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-start-time-field"],
        a_nexus_field=NeXusField(
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
        links=["https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-user-group"],
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

The generator never removes hand-written additions. When a file already exists:

- If `force=False` (default): the file is rewritten whenever the generated source differs
  from the existing file **and** the existing file contains no user-added members (methods
  or quantities not present in the new output). This means generator-driven changes
  (descriptions, annotation values, new members) propagate automatically, while files with
  custom `normalize()` logic are protected.
- If `force=True`: the file is always overwritten.
- In `dry_run` mode: returns `True` if the file would differ; no disk write occurs.

User-added members are detected by comparing the set of names in the existing file against
the set the generator would produce. Any name present in the existing file but absent from
the new output is considered user-added.

---

## CLI

```bash
# Generate one class (base or application)
pynx nomad generate-metainfo --nxdl NXentry
pynx nomad generate-metainfo --nxdl NXarpes

# Generate all base classes (Phase 1)
pynx nomad generate-metainfo --all-base

# Generate all application definitions (Phase 2)
pynx nomad generate-metainfo --all-applications

# Generate all categories (apps first, then base --force for cross-refs)
pynx nomad generate-metainfo --all

# CI check: fail if committed files differ from what the generator would produce
pynx nomad generate-metainfo --all --dry-run

# Force regeneration (overwrite existing files)
pynx nomad generate-metainfo --all --force

# Generate into a different package (e.g. nomad-measurements)
pynx nomad generate-metainfo --all --output-dir ../nomad-measurements/nexus/metainfo/base_classes
```

---

## Package assembly

`metainfo/_package.py` imports all generated modules and assembles NOMAD `Package` objects:

### Base classes package (Phase 1)

```python
from pynxtools.nomad.metainfo import build_base_classes_package

pkg_base = build_base_classes_package()
print(len(pkg_base.section_definitions), "base sections")  # 327 including named concepts
```

### Applications package (Phase 2)

```python
from pynxtools.nomad.metainfo import build_applications_package

pkg_apps = build_applications_package()
print(len(pkg_apps.section_definitions), "application sections")  # 345 including named concepts
```

During package assembly, `__init_metainfo__()` resolves all `SubSection.section_def`
string FQNs into live class references.

!!! note "Phase 1 limitation"
    Some base classes reference groups from the contributed definitions
    (e.g. `NXphase` → `NXmicrostructure_ipf`).  Those contributed classes are not
    generated in Phase 1, so the corresponding `SubSection` references remain
    unresolved.  `build_base_classes_package()` emits a warning and continues rather than raising.
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
Attributes are emitted without the `@` prefix. A small set of NOMAD `BaseSection`-reserved names get a `_quantity` suffix (e.g. `name` → `name_quantity`). When a field name collides with a same-class or ancestor `SubSection` name, the field also gets `_quantity` (groups always win the unqualified name).

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
    a_nexus_attribute=NeXusAttribute(
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
