# pynxtools architecture

This page explains the internal design of `pynxtools`. It is intended for developers who want to extend `pynxtools`, implement custom processing pipelines, or understand how the built-in tools work.

## Overview

`pynxtools` organizes its HDF5/NeXus processing around three collaborating layers:

| Layer | Key type | Role |
|---|---|---|
| **Schema** | `NexusNode` | In-memory representation of an NXDL application definition |
| **Traversal** | `NexusFileHandler` | Walks every node of an HDF5 file in order |
| **Processing** | `NexusVisitor` | Receives node events and implements the actual logic |

The separation is deliberate: traversal and I/O live in `NexusFileHandler`; all domain-specific behavior (annotation, validation, NOMAD parsing) lives in `NexusVisitor` implementations. This makes every processing mode independently testable and composable.

## The schema layer: `NexusNode`

`NexusNode` (in `pynxtools.nexus.nexus_tree`) is an in-memory tree that mirrors an NXDL application definition. Each node corresponds to one element defined in the XML schema: a definition root, a group, a field, an attribute, a choice, or a link.

### Node type hierarchy

| Class | `nx_type` | XSD type | Represents |
|---|---|---|---|
| `NexusDefinition` | `"definition"` | `definitionType` | NXDL file root — carries `category`, `symbols`, `ignore_extra_*` |
| `NexusGroup` | `"group"` | `groupType` | An HDF5 group / NeXus class instance |
| `NexusField` | `"field"` | `fieldType` | A dataset — carries `unit`, `long_name`, `interpretation`, and deprecated plotting hints |
| `NexusAttribute` | `"attribute"` | `attributeType` | An HDF5 attribute — type and enumeration only, no unit |
| `NexusChoice` | `"choice"` | `choiceType` | A `<choice>` element |
| `NexusLink` | `"link"` | — | A `<link>` element |

`NexusField` and `NexusAttribute` share a private base `_NexusEntityBase` for dtype, enumeration, and shape information.  The distinction matters because `unit` is a field-only concept in the NeXus XSD (`fieldType` has a `units` attribute; `attributeType` does not).

`NexusEntity` is a backward-compatible alias for `NexusField`.  Existing code importing `NexusEntity` continues to work; new code should import `NexusField` or `NexusAttribute` directly.

### What `NexusNode` provides

- **Optionality**: whether a concept is `required`, `recommended`, or `optional`.
- **Type information**: NeXus type (e.g. `NX_FLOAT`) and, for fields, the unit category (e.g. `NX_ENERGY`).
- **Enumeration values**: closed vs. open enumerations.
- **Inheritance chain traversal**: `get_inheritance_enums()` and `get_inheritance_concept_paths()` walk the full NeXus inheritance chain and return constraints from every contributing parent class, ordered from the concrete subclass to the most general base class.
- **Name resolution**: `best_child_for(name, node_type, nx_class)` selects the best-matching schema child for a given HDF5 instance name, applying NeXus name-fitting rules. Always returns the first of multiple equally-scoring matches.
- **Collection parent detection**: `has_nxcollection_parent()` checks whether a node lives inside an `NXcollection` group (which exempts it from required-field checks).

### `NexusDefinition` — the tree root

`generate_tree_from` returns a `NexusDefinition` node (not a generic `NexusGroup`).  It exposes the metadata declared at the top of every NXDL file:

| Attribute | Type | Source |
|---|---|---|
| `category` | `"base"` or `"application"` | `<definition category="...">` |
| `symbols` | `dict[str, str]` | `<symbols>/<symbol>` block |
| `ignore_extra_groups` | `bool` | `ignoreExtraGroups="true"` |
| `ignore_extra_fields` | `bool` | `ignoreExtraFields="true"` |
| `ignore_extra_attributes` | `bool` | `ignoreExtraAttributes="true"` |

### Generating a tree

```python
from pynxtools.nexus.nexus_tree import NexusDefinition, generate_tree_from

root: NexusDefinition = generate_tree_from("NXarpes")
print(root.category)   # "application"
print(root.symbols)    # {"nP": "...", ...}
```

`generate_tree_from` resolves the full inheritance chain at build time, so every child node already contains the merged constraints from all contributing base classes.

## The traversal layer: `NexusFileHandler`

`NexusFileHandler` (in `pynxtools.nexus.handler`) opens a NeXus/HDF5 file and performs a depth-first walk, dispatching each node to a `NexusVisitor`.

```python
from pynxtools.nexus.handler import NexusFileHandler

NexusFileHandler(file_path).process(visitor)
```

The handler owns file I/O and traversal order. It knows nothing about what to *do* with each node — that is entirely the visitor's responsibility.

### Dispatch order per node

For every node encountered during traversal:

1. `visitor.on_group(hdf_path, hdf_node)` **or** `visitor.on_field(hdf_path, hdf_node)`
2. `visitor.on_attribute(hdf_path, attr_name, attr_value, parent)` for every attribute of that node

After the full walk:

3. `visitor.on_complete(root)` — called once, with the open HDF5 file root

The root group itself is dispatched as a group with `hdf_path = ""`.

## The processing layer: `NexusVisitor`

`NexusVisitor` (in `pynxtools.nexus.handler`) is the extension point. It is an abstract base class (`ABC`) that declares four mandatory hooks and two optional hooks.

The four mandatory hooks must be implemented by every concrete subclass; implement hooks that are not meaningful as `pass`:

```python
from abc import ABC, abstractmethod
from pynxtools.nexus.handler import NexusVisitor
import h5py

class NexusVisitor(ABC):
    @abstractmethod
    def on_group(self, hdf_path: str, hdf_node: h5py.Group) -> None: ...
    @abstractmethod
    def on_field(self, hdf_path: str, hdf_node: h5py.Dataset) -> None: ...
    @abstractmethod
    def on_attribute(
        self,
        hdf_path: str,
        attr_name: str,
        attr_value,
        parent: h5py.Group | h5py.Dataset,
    ) -> None: ...
    @abstractmethod
    def on_complete(self, root: h5py.File) -> None: ...
```

Two optional hooks have default no-op implementations and may be overridden:

| Hook | When called |
|------|-------------|
| `on_broken_link(hdf_path, link)` | A soft or external link cannot be resolved; the broken node is skipped. |
| `on_external_link(hdf_path, link)` | An external link is encountered, *before* the handler opens the external file. |

### Built-in visitor implementations

| Visitor | Module | CLI tool | Purpose |
|---|---|---|---|
| `Annotator` | `pynxtools.annotator.annotator` | `pynx read` | Logs NXDL documentation for every node in a NeXus file |
| `ValidationVisitor` | `pynxtools.dataconverter.validation` | `pynx validate` | Checks every node against its NXDL constraints |
| `NomadVisitor` | `pynxtools.nomad.parsers.parser` | `nomad parse` | Populates the NOMAD archive from a NeXus file |

All built-in visitors are interchangeable in `NexusFileHandler`. Switching the visitor changes what happens to each node; the traversal is identical.

## Schema resolution: `NexusSchemaResolver` and `resolve_path`

Mapping a live HDF5 path to its schema `NexusNode` is a cross-cutting concern needed by every visitor.  `pynxtools.nexus.schema_resolver` provides the shared infrastructure so visitors do not each reimplement it.

### `resolve_path`

`resolve_path(root, path, node_type, *, nx_class_for, hint, _cache)` walks a `NexusNode` tree segment by segment, calling `best_child_for` at each step.  It is h5py-free: callers supply an optional `nx_class_for` callable that reads the `NX_class` HDF5 attribute for intermediate group segments, enabling deterministic disambiguation of variadic schema groups (e.g. `DETECTOR[NXdetector]`).

```python
from pynxtools.nexus.schema_resolver import resolve_path
from pynxtools.nexus.nexus_tree import generate_tree_from

tree = generate_tree_from("NXarpes")
node = resolve_path(tree, "ENTRY/INSTRUMENT/analyser", node_type="group")
```

### `NexusSchemaResolver`

`NexusSchemaResolver` is a visitor-agnostic helper class that wraps `resolve_path` with HDF5-aware appdef discovery and per-instance caching.  Any `NexusVisitor` implementation should hold one instead of re-implementing lookup logic.

```python
from pynxtools.nexus.schema_resolver import NexusSchemaResolver

class MyVisitor(NexusVisitor):
    def __init__(self):
        self._resolver = NexusSchemaResolver()

    def on_field(self, hdf_path, hdf_node):
        node = self._resolver.node_for(hdf_path, hdf_node)
        ...
```

Key methods:

| Method | Purpose |
|---|---|
| `appdef_for(hdf_node)` | Walk up the HDF5 tree to find the `NXentry/definition` value; returns `str` or `None` if no `NXentry` ancestor exists |
| `tree_for(appdef)` | Return (and cache) the `NexusNode` tree for a named application definition |
| `node_for(hdf_path, hdf_node, hint)` | Return the schema `NexusNode` for an HDF5 path, or `None` if not in schema |
| `attr_node_for(hdf_path, attr_name, parent_hdf)` | Return the schema `NexusNode` for an attribute |

### Caching

`NexusSchemaResolver` maintains two caches per instance:

- **`_tree_cache: dict[str, NexusNode | None]`** — maps application definition name (e.g. `"NXarpes"`) to its fully-resolved tree.  Building a tree requires parsing NXDL XML and walking the full inheritance chain; the cache ensures this is done at most once per appdef per file traversal.
- **`_node_cache: dict[str, NexusNode | None]`** — maps HDF5 path string to the corresponding schema `NexusNode` (or `None` for a confirmed miss).  Intermediate path segments are cached alongside final results, so paths sharing a common prefix (e.g. `/entry/instrument/detector/field1` and `.../field2`) avoid redundant tree traversals.

## How the CLI tools are built

### `pynx read` — the annotator

`pynx read` creates an `Annotator` visitor and passes it to `NexusFileHandler`.  The annotator holds a `NexusSchemaResolver` and uses it on every `on_field` / `on_attribute` callback to look up the matching `NexusNode`, then emits documentation, optionality, enumeration values, and inheritance information.

Three operating modes are supported:

- **Default**: annotate every node and print the default-plottable summary.
- **`-d` (documentation)**: annotate only the single node at a given HDF5 path.
- **`-c` (concept)**: find all HDF5 nodes that implement a given NXDL concept path.

### `pynx validate` — the validator

`validate` creates a `ValidationVisitor` and passes it to `NexusFileHandler`. The validator checks:

- required, recommended, and optional fields are present where expected,
- field values conform to their `NexusType` and unit category,
- enumeration values are in-range (warnings for closed enumerations, info for open),
- `NXdata` signal and axis dimensionality rules are satisfied,
- HDF5 links resolve correctly and carry a `@target` attribute; broken soft or external links are reported as `BrokenLink` problems,
- reserved suffixes and prefixes are used in valid contexts.

Validation state accumulates across callbacks and the summary report is emitted in `on_complete`.

## Data flow summary

```
HDF5 file
    │
    ▼
NexusFileHandler.process(visitor)
    │
    ├─ on_group  ─────────┐
    ├─ on_field  ──────────┤ NexusVisitor
    ├─ on_attribute ───────┤  (Annotator / NomadVisitor / custom)
    └─ on_complete ────────┘
              │
              │  node_for(hdf_path, hdf_node)
              ▼
    NexusSchemaResolver
    ├─ appdef_for(hdf_node) ──► NXentry/definition (str | None)
    ├─ tree_for(appdef)  ─────► NexusDefinition root (cached)
    │                           (built from NXDL via generate_tree_from)
    └─ resolve_path(tree, ...) ► NexusNode (cached per path)
```

## Extending pynxtools with a custom visitor

Because `NexusFileHandler` accepts any `NexusVisitor`, it is straightforward to add new processing modes without modifying pynxtools internals. See the [how-to guide on implementing a custom visitor](../../how-tos/pynxtools/implement-a-visitor.md) for a worked example.

## Relationship to the dataconverter

The dataconverter (write path) is independent of `NexusFileHandler` (read path). Readers produce a `Template` dictionary; the dataconverter validates the template against an NXDL tree (also built from `NexusNode`) and writes the HDF5 file.

See [Data conversion in pynxtools](dataconverter-and-readers.md) for the write-path architecture.
