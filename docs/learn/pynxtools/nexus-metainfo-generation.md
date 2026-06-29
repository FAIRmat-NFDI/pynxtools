# NeXus Metainfo Generation

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
- **Application definitions are Entry subclasses**: `Xps(Entry)` instead of a wrapper where `Xps` contains `XpsEntry` (see below).
- **Backward compatibility**: The old `nexus_schema` entry point is untouched; both systems coexist until we are sure the new schema works.

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
metainfo/<folder>/<stem>.py ← generated Python files (one per NeXus definition) 
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
generator. This gives:

- **Inheritance resolution**: NexusNode follows the `extends` chain and merges attributes
  from parent classes. The generator never needs to know about inheritance.
- **Stable surface**: if the NXDL XML format changes, only `nexus_tree.py` needs to
  change; the generator and all generated files stay the same.
- **Testability**: unit tests target `NexusNode` properties, not generator output.

### `generate_tree_from()`

```python
from pynxtools.nexus.nexus_tree import generate_tree_from
root = generate_tree_from("NXdetector")
print(root.nx_type)     # "definition"
print(root.category)    # "base"
print(root.deprecated)  # None  (or a deprecation string)
for child in root.children:
    print(child.nx_type, child.name)  # "field" "data", "group" "NXtransformations", ...
```

`generate_tree_from(nx_name)` is the single entry point into the NexusNode tree. It:

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
| `deprecated` | `str \ None` | `@deprecated` |

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
| `occurrence_limits` | `tuple[int\None, int\None]` | `@minOccurs`/`@maxOccurs` |

#### `NexusField`

| Attribute | Type | Source (NXDL) |
|-----------|------|--------------|
| `dtype` | `str` | `@type` (default `"NX_CHAR"`) |
| `unit` | `str \ None` | `@units` |
| `shape` | `tuple \ None` | `<dimensions>` element |
| `dim_symbols` | `tuple \ None` | symbol names parallel to `shape` |
| `items` | `list[str] \ None` | `<enumeration>/<item>` |
| `open_enum` | `bool` | `<enumeration open="true">` |
| `long_name` | `str \ None` | `@long_name` |
| `interpretation` | `str \ None` | `@interpretation` |

#### `NexusAttribute`

Shares `dtype`, `shape`, `dim_symbols`, `items`, `open_enum` with `NexusField`.
Has no `unit`, `long_name`, `interpretation`, or plotting-hint attributes.

---

## Annotation models

Six `AnnotationModel` subclasses (one per NXDL node kind) carry all NeXus-specific metadata on generated sections and quantities . Each annotation is queryable
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

Attached to every `Quantity` derived from a NXDL `<field>` element. Fields
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
group-level or field-level). Field-level attributes set `parent_field` to the
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
block. A choice allows exactly one NX class to occupy a named slot. One
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
        base_classes/           # 142 generated base class files
            __init__.py
            entry.py            # Entry(Object, basesections.Measurement)
            sample.py           # Sample(Object, basesections.CompositeSystem)
            detector.py
            ...
        applications/           # 85 generated application definition files
            __init__.py
            arpes.py            # Arpes(Entry) — application specialization of Entry
            xps.py              # Xps(Entry) — application specialization of Entry
            ...
```

---

## Application Definitions

### The design principle: `Xps(Entry)` not `Xps(Object, Measurement)`

In NeXus, every application definition (e.g. `NXxps.nxdl.xml`) wraps exactly one `NXentry` at
the root level. This is supposed to be a container pattern. However, in practice, no application definition has anything outside of its `NXentry` group. Therefore, application definitions can be understood as **constraint templates**
that describe what an `NXentry` looks like in a specific measurement context.

Therefore, in Python/NOMAD, application definitions inherit from `Entry` directly:

```python
class Xps(Entry):
    m_def = Section(
        a_nexus_definition=NeXusDefinition(nx_class="NXxps", category="application"),
    )
    # SubSections and Quantities from inside NXxps's NXentry group,
    # with XPS-specific optionality
```

- `Xps` **is** a specialized kind of Entry, not a wrapper around an entry.
- Parser logic is simpler: directly instantiate `Xps` when an HDF5 file's `NX_class` attribute says `"NXxps"`.
- Inheritance chain is clear: `Object → Entry → Xps`.
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
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry"
        ],
        categories=[ExperimentCategory],
        a_schema=SchemaAnnotation(label="Entry", enabled=False),
        a_nexus_definition=NeXusDefinition(
            nx_class="NXentry",
            category="base",
        ),
    )

    # Cross-file SubSection: a_nexus_group lives on the SubSection itself
    # because Detector is defined in a separate file.
    data = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=True,
        variable=True,
        description=(
            ...
        ),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    # Named concept SubSection: a_nexus_group lives on EntryThumbnail.m_def.
    thumbnail = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.entry.EntryThumbnail",
        repeats=False,
        description=(
            ...
        ),
    )

    start_time = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-start-time-field"
        ],
        description=("Starting time of measurement"),
        a_nexus_field=NeXusField(
            name="start_time",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
        ...


class EntryThumbnail(Note):
    """
    A small image that is representative of the entry. An example of this is a
    640x480 jpeg image automatically produced by a low resolution plot of the
    NXdata.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-thumbnail-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="thumbnail",
            name_type="specified",
            optionality="optional",
        ),
    )

    type = Quantity(
        type=MEnum(["image/*"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-thumbnail-type-attribute"
        ],
        description=("The mime type should be an ``image/*``"),
        a_nexus_attribute=NeXusAttribute(
            name="type",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            enumeration=["image/*"],
            deprecated="Use the `type` field instead",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="image/*",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
```

### Named concepts vs. cross-file SubSections

A named concept class is generated only when the group defines **its own quantities** that
differ from the generic class: changed optionality, extra fields, or different
type/units/enumeration. Groups that exist purely for occurrence context (e.g. a
`backgroundBACKGROUND` group with no additional fields) point their `SubSection` directly
at the generic class; no named concept class is generated. This rule also prevents
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
integer sizes are preserved as-is. Unbounded or symbolically-named dimensions (e.g.
`nP`, `nz`) become the wildcard `"*"`. NOMAD does not interpret NeXus symbol names.
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

## Units

A NXDL `<field>`'s `@units` category (e.g. `NX_ENERGY`) maps to `dimensionality`
(a pint-parseable dimensionality string) and `default_unit` on the generated
`Quantity`:

```python
# NXDL: <field name="energy" type="NX_FLOAT" units="NX_ENERGY">
energy = Quantity(
    type=np.float64,
    dimensionality="[mass] * [length] ** 2 / [time] ** 2",
    unit="joule",
    ...
)
```

`NX_ANY` is different: it means the field's unit is **not fixed by the
schema at all** — the actual unit varies per file/value. There is no
`dimensionality`/`unit` to assign, so instead the generated `Quantity` gets
`flexible_unit=True` — a first-class NOMAD `Quantity` parameter for exactly
this case ("this quantity may have a unit that is not the default unit");
NOMAD then stores the value in full-storage mode (`MQuantity`), preserving
whichever unit was actually written:

```python
# NXDL: <field name="resolution" type="NX_FLOAT" units="NX_ANY">
resolution = Quantity(
    type=np.float64,
    flexible_unit=True,
    ...
    a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
)
```

No special ELN handling is needed beyond the usual `NumberEditQuantity`: its
GUI implementation already supports typing a value together with any unit
(and a unit-selection dropdown) when the field has no fixed dimensionality —
exactly the `NX_ANY` case.

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

# Generate all base classes
pynx nomad generate-metainfo --all-base

# Generate all application definitions
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

### Base classes package

```python
from pynxtools.nomad.metainfo import build_base_classes_package

pkg_base = build_base_classes_package()
print(len(pkg_base.section_definitions), "base sections")  # 327 including named concepts
```

### Applications package

```python
from pynxtools.nomad.metainfo import build_applications_package

pkg_apps = build_applications_package()
print(len(pkg_apps.section_definitions), "application sections")  # 345 including named concepts
```

During package assembly, `__init_metainfo__()` resolves all `SubSection.section_def`
string FQNs into live class references.
---

## Inheritance chain

Every generated class extends its **NeXus parent** class (the Python class generated from
the NXDL `extends` attribute) and — where a semantic match exists — additionally inherits
from the corresponding NOMAD base section:

```python
class Object(BaseSection): ...            # NXobject → root
class Entry(Object, basesections.Measurement): ...
class Sample(Component, basesections.CompositeSystem): ...
class SampleComponent(Component, basesections.Component): ...
...
```

The NOMAD base section is imported **as the module** (`from nomad.datamodel.metainfo import
basesections`) and used as `basesections.Measurement` in the class signature. This avoids
name collisions when the generated NeXus class and the NOMAD base share the same Python
name (e.g. both `Component`).

The secondary NOMAD base is only added when the NeXus `extends` chain does not already
provide it;s preventing duplicate entries in the MRO.

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

!!! warning "In development"
    This mapping is still being refactored, alongside the refactoring of the Base Sections v2. `NXprocess`, `NXfabrication`, and `NXdata` are especially not mapped in a proper way; this still needs to be addressed later.

---

## Naming conventions

### Class names

Top-level classes — one per generated NXDL class — are camel-cased directly from
the NXDL name: `nxdl_to_class_name("NXmicrostructure_ipf")` → `"MicrostructureIpf"`.

**Named concept classes** are generated for a group occurrence that adds its own
quantities/children beyond its generic class (e.g. `MpesInstrument` for the
`INSTRUMENT` group inside `NXmpes`). They are are named `{ParentClassName}{Suffix}`,
where `Suffix` depends on the group's `name_type`, exactly like [Subsection
names](#subsection-names) below but CamelCased instead of lowercased:

- `name_type="specified"`: suffix from the NXDL name, e.g. `temperature_log` →
  `TemperatureLog` → `SampleTemperatureLog`.
- `name_type="any"`: suffix from `node.name` — the NXDL's explicit `name=`
  attribute if it has one (e.g. `name="BIAS_SWEEP"` → `BiasSweep` →
  `StsInstrumentBiasSweep`), otherwise the NX class itself (e.g. any `NXlog` →
  `Log` → `ObjectLog`).
- `name_type="partial"`: the lower-case prefix of the partial name is
  CamelCased (splitting on `_`, same as the "specified" case), then the
  upper-case marker is appended as-is — e.g. `peakPEAK` → `Peak` → `FitPeak`,
  or `voltage_sensorTAG` → `VoltageSensorTAG` →
  `SpmInstrumentVoltageSensorTAG` (not `Voltage_sensorTAG`, which is what a
  naive "just uppercase the first letter" rule would produce).

If the resulting name would equal the base class name itself (circular
inheritance, e.g. `NXapm_measurement`'s own `measurement` child resolving to
`ApmMeasurement` == its own base `ApmMeasurement`), it is re-prefixed with the
full type-based name instead — e.g. `ApmApmMeasurement`. This is intentional,
not a naming bug.

### Quantity names

Field and attribute names are kept as-is (NeXus convention uses snake_case
throughout). Two cases get a `_quantity` suffix instead:

- **Python keywords**, always — e.g. `lambda` → `lambda_quantity`.
- **An array-shaped field** named like a NOMAD `BaseSection` quantity
  (`name`, `datetime`, `lab_id`, `description`) — e.g. a `shape=["*"]` field
  literally named `name` → `name_quantity`.

A **scalar** field named like one of those four is *not* suffixed — NOMAD
allows a subclass to directly override an inherited quantity, replacing it
cleanly rather than merging or conflicting with it (confirmed by reading
`Section.__init_metainfo__()` in `nomad/metainfo/metainfo.py`: it only raises
`MetainfoError` when overriding properties are different *kinds* — Quantity
vs. SubSection — never for two Quantities of different type/shape; and
confirmed type-compatible — `str`/`Datetime` as appropriate — across every
occurrence of these four names in the whole NXDL corpus).

The array case is still suffixed even though NOMAD itself wouldn't object,
because `BaseSection`'s own `normalize()` and related logic
(`nomad/datamodel/metainfo/basesections.py`) treat `self.name`/
`self.datetime`/etc. as scalars throughout its inheritance chain (e.g.
`archive.metadata.entry_name = self.name`, `Workflow(name=self.name)`) — an
array there is accepted by NOMAD's metaclass but silently wrong at runtime,
which the generator has no way to rely on NOMAD to catch. This was a real
case, not hypothetical: `NXmicrostructure_score_config` had a field literally
named `name` holding a one-dimensional array of per-texture-component names
(one string per entry, deliberately — see
[nexus_definitions#428](https://github.com/FAIRmat-NFDI/nexus_definitions/pull/428),
rejected upstream because the array is intentional). That field has since
been renamed to `names` upstream, removing the collision at the source, but
the shape check stays as a general safeguard for any other such field.

Separately, when a field name collides with a same-class or ancestor
`SubSection` name, the field always gets `_quantity` regardless of shape
(groups always win the unqualified name — *that* collision genuinely can't
be resolved by overriding, see [Subsection names](#subsection-names) below).

### Subsection names

A group's Python attribute name is always derived from `node.name` — which
`NexusNode` populates with either the NXDL's explicit `name=` attribute, or
(when absent) the NeXus class stem in uppercase (e.g. `"USER"` for any `NXuser`).
The three `name_type` values differ only in *casing*, not in which name is
used:

- `name_type="specified"` (a fixed-name group, e.g. `instrument`): used as-is
  — NXDL convention already writes these in snake_case.
- `name_type="any"` (a variadic group; instances may use any actual HDF5
  name): `node.name` is lowercased. This covers both an anonymous
  group with no `name=` attribute at all (e.g. any `NXdetector` → `detector`)
  *and* an explicitly-named variadic group (e.g. `name="BIAS_SWEEP"` →
  `bias_sweep`).
- `name_type="partial"` (e.g. `peakPEAK`): used as-is, preserving the mixed
  case, so the lower-case fixed prefix and the upper-case user-chosen portion
  both stay visible in the generated code (consistent with the matching
  concept class name, e.g. `FitPeakPEAK`).

The `a_nexus_group(name=...)` annotation, separately, faithfully records what
NXDL actually declares: `None` only for a genuinely anonymous group (no
`name=` attribute at all), the literal NXDL name otherwise — so `name=None`
for any `NXuser`, but `name="BIAS_SWEEP"` for the explicitly-named variadic
group above, even though both get lowercased the same way for the Python
attribute name.

**One exception to "groups always win the unqualified name"**: a group
literally named `name`, `datetime`, `lab_id`, or `description` gets a
`_group` suffix instead (e.g. `name` → `name_group`). These four names take
precedence over any NXDL group because every single generated class — without
exception — inherits them first: `Object`, the universal root all generated
classes derive from, itself extends `basesections.BaseSection`, which defines
exactly these four quantities. By the time a NeXus-specific group is added,
the slot is already occupied by a `Quantity`, not optionally or
class-specifically but structurally, for every class in the hierarchy. A
`SubSection` can never override a same-named `Quantity` the way a *field* can
(see [Quantity names](#quantity-names) above) — they're different property
*kinds*, which NOMAD rejects outright with `MetainfoError: Cannot inherit
from different property types.` So while any NXDL *field* may safely reuse
one of these four names, a *group* using one of them always needs the
suffix — there is no field/group asymmetry here other than what NOMAD's
override mechanism itself allows.

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
While we are still working on the new schema/parser, we do not touch the existing code path. Once the new NOMAD integration is complete and validated, we will deprecate and eventually remove `schema.py` and `parser.py`.

---

## Further reading

- [Learn > pynxtools > NOMAD integration](nomad-integration.md)
