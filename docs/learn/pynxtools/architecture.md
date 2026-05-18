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

`NexusNode` (in `pynxtools.nexus.nexus_tree`) is an in-memory tree that mirrors an NXDL application definition. Each node corresponds to one group, field, or attribute defined in the XML schema.

### What `NexusNode` provides

- **Optionality**: whether a concept is `required`, `recommended`, or `optional`.
- **Type information**: NeXus type (e.g. `NX_FLOAT`) and NeXus Unit category (e.g. `NX_ENERGY`).
- **Enumeration values**: closed vs. open enumerations.
- **Inheritance chain traversal**: `get_inheritance_docs()`, `get_inheritance_enums()`, and `get_inheritance_concept_paths()` walk the full NeXus inheritance chain and return documentation and constraints from every contributing base class, most-specific first.
- **Name resolution**: `best_child_for(name, node_type, nx_class)` selects the best-matching schema child for a given HDF5 instance name, applying NeXus name-fitting rules.
- **Full-path lookup**: `find_node_at_path(path, ...)` traverses the tree from a root, with an optional dict cache to amortize repeated lookups.
- **Collection parent detection**: `has_nxcollection_parent()` checks whether a node lives inside an `NXcollection` group (which exempts it from required-field checks).

### Generating a tree

```python
from pynxtools.nexus.nexus_tree import generate_tree_from

root: NexusNode = generate_tree_from("NXarpes")
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

`NexusVisitor` (in `pynxtools.nexus.handler`) is the extension point. It is an abstract base class (`ABC`) that declares four hooks. All four must be implemented by concrete subclasses; hooks that are not meaningful for a particular visitor should be implemented as `pass`.

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

### Built-in visitor implementations

| Visitor | Module | CLI tool | Purpose |
|---|---|---|---|
| `Annotator` | `pynxtools.annotator.annotator` | `pynx read` | Logs NXDL documentation for every node in a NeXus file |
| `NomadVisitor` | `pynxtools.nomad.parsers.parser` | `nomad parse` | Populates the NOMAD archive from a NeXus file |

All built-in visitors are interchangeable in `NexusFileHandler`. Switching the visitor changes what happens to each node; the traversal is identical.

## How the CLI tools are built

### `pynx read` — the annotator

`pynx read` creates an `Annotator` visitor and passes it to `NexusFileHandler`. The annotator resolves the application definition from the file's `NXentry/definition` field, builds a `NexusNode` tree for it. Thereafter, the annotator looks up on each `on_field` / `on_attribute` callback the matching `NexusNode` to emit documentation, optionality, enumeration values, and inheritance information.

Three operating modes are supported:

- **Default**: annotate every node and print the default-plottable summary.
- **`-d` (documentation)**: annotate only the single node at a given HDF5 path.
- **`-c` (concept)**: find all HDF5 nodes that implement a given NXDL concept path.

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
              │  NexusNode lookup (per node)
              ▼
         NexusNode tree
         (built from NXDL via generate_tree_from)
```

## Extending pynxtools with a custom visitor

Because `NexusFileHandler` accepts any `NexusVisitor`, it is straightforward to add new processing modes without modifying pynxtools internals. See the [how-to guide on implementing a custom visitor](../../how-tos/pynxtools/implement-a-visitor.md) for a worked example.

## Relationship to the dataconverter

The dataconverter (write path) is independent of `NexusFileHandler` (read path). Readers produce a `Template` dictionary; the dataconverter validates the template against an NXDL tree (also built from `NexusNode`) and writes the HDF5 file.

See [Data conversion in pynxtools](dataconverter-and-readers.md) for the write-path architecture.
