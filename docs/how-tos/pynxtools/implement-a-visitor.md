# Implement a custom NexusVisitor

!!! info "This guide assumes familiarity with the visitor pattern in pynxtools. Read [pynxtools architecture](../../learn/pynxtools/architecture.md) first."

`NexusFileHandler` accepts any `NexusVisitor`, making it straightforward to add new HDF5 processing modes without modifying `pynxtools` internals. This guide walks through implementing a minimal custom visitor.

## When to write a custom visitor

Write a custom visitor when you need to process every node of a NeXus file in a way that is not covered by the built-in `Annotator`. Common use cases:

- Collecting statistics over all fields (e.g. value ranges, missing data)
- Extracting a specific subset of nodes for further processing
- Implementing a custom export or transformation
- Linting files against local conventions

## The visitor interface

`NexusVisitor` is an abstract base class. Concrete subclasses must implement all four hooks; implement hooks that are not needed as `pass`:

```python
from pynxtools.nexus.handler import NexusVisitor
import h5py

class MyVisitor(NexusVisitor):
    def on_group(self, hdf_path: str, hdf_node: h5py.Group) -> None: pass
    def on_field(self, hdf_path: str, hdf_node: h5py.Dataset) -> None: pass
    def on_attribute(
        self,
        hdf_path: str,
        attr_name: str,
        attr_value,
        parent: h5py.Group | h5py.Dataset,
    ) -> None: pass
    def on_complete(self, root: h5py.File) -> None: pass
```

Two additional optional hooks have default no-op implementations and may be overridden:

| Hook | When called | Default |
|------|-------------|---------|
| `on_broken_link(hdf_path, link)` | A soft or external link cannot be resolved. The broken node is then skipped. | no-op |
| `on_external_link(hdf_path, link)` | An external link is first encountered, *before* the handler opens the external file. | no-op |

The `link` argument is an `h5py.SoftLink` or `h5py.ExternalLink`. Inspect its type to distinguish the two cases. Nodes from a successfully resolved external file are visited with the same `hdf_path` prefix as the link itself; for example, a link at `"entry/ext"` whose target is a group containing `"value"` results in `on_field("entry/ext/value", ...)`.

!!! note "Hard links"
    Hard links are followed transparently. A built-in cycle guard prevents infinite recursion when a hard-linked descendant aliases an ancestor.

## Worked example: collecting all field paths and values

This visitor collects every field path and its scalar value into a flat dictionary.

```python
from __future__ import annotations

import h5py
import numpy as np

from pynxtools.nexus.handler import NexusFileHandler, NexusVisitor


class FieldCollector(NexusVisitor):
    """Collect all scalar HDF5 fields and their values."""

    def __init__(self) -> None:
        self.fields: dict[str, object] = {}

    def on_group(self, hdf_path: str, hdf_node: h5py.Group) -> None:
        pass

    def on_field(self, hdf_path: str, hdf_node: h5py.Dataset) -> None:
        value = hdf_node[()]
        if np.ndim(value) == 0 or (np.ndim(value) == 1 and len(value) <= 10):
            self.fields[hdf_path] = value

    def on_attribute(self, hdf_path: str, attr_name: str, attr_value, parent) -> None:
        pass

    def on_complete(self, root: h5py.File) -> None:
        print(f"Collected {len(self.fields)} fields.")


# Usage
visitor = FieldCollector()
NexusFileHandler("path/to/file.nxs").process(visitor)
print(visitor.fields)
```

## Worked example: schema-aware visitor using `NexusNode`

A more powerful visitor queries the `NexusNode` tree to correlate HDF5 nodes with their schema definition.

```python
from __future__ import annotations

import logging
from typing import Optional

import h5py

from pynxtools.nexus.handler import NexusFileHandler, NexusVisitor
from pynxtools.nexus.nexus_tree import NexusNode, generate_tree_from


class SchemaAwareVisitor(NexusVisitor):
    """Look up the NexusNode for every field and log its optionality and unit category."""

    def __init__(self, appdef: str) -> None:
        self.logger = logging.getLogger(__name__)
        self._root_node: Optional[NexusNode] = generate_tree_from(appdef)
        self._node_cache: dict[str, Optional[NexusNode]] = {}

    def _node_for(self, hdf_path: str) -> Optional[NexusNode]:
        if hdf_path in self._node_cache:
            return self._node_cache[hdf_path]
        node = self._root_node.find_node_at_path(hdf_path, _cache=self._node_cache)
        self._node_cache[hdf_path] = node
        return node

    def on_group(self, hdf_path: str, hdf_node: h5py.Group) -> None:
        pass

    def on_field(self, hdf_path: str, hdf_node: h5py.Dataset) -> None:
        node = self._node_for(hdf_path)
        if node is None:
            self.logger.debug("%s — not in schema", hdf_path)
            return
        self.logger.info(
            "%s — optionality=%s, unit_category=%s",
            hdf_path,
            node.optionality,
            node.unit_category,
        )

    def on_attribute(self, hdf_path: str, attr_name: str, attr_value, parent) -> None:
        pass

    def on_complete(self, root: h5py.File) -> None:
        pass


# Usage
logging.basicConfig(level=logging.INFO)
visitor = SchemaAwareVisitor("NXarpes")
NexusFileHandler("path/to/arpes_file.nxs").process(visitor)
```

## Handling broken and external links

Override `on_broken_link` and `on_external_link` to react to links that cannot be resolved or to external files that are traversed inline.

```python
from __future__ import annotations

import h5py

from pynxtools.nexus.handler import NexusFileHandler, NexusVisitor


class LinkAwareVisitor(NexusVisitor):
    """Report broken links and track which external files were opened."""

    def __init__(self) -> None:
        self.broken: list[tuple[str, str]] = []   # (hdf_path, link_target)
        self.external_files: set[str] = set()

    def on_group(self, hdf_path: str, hdf_node: h5py.Group) -> None:
        pass

    def on_field(self, hdf_path: str, hdf_node: h5py.Dataset) -> None:
        pass

    def on_attribute(self, hdf_path: str, attr_name: str, attr_value, parent) -> None:
        pass

    def on_complete(self, root: h5py.File) -> None:
        pass

    def on_broken_link(self, hdf_path: str, link) -> None:
        target = getattr(link, "path", str(link))
        self.broken.append((hdf_path, target))
        print(f"BROKEN LINK at {hdf_path!r} → {target!r}")

    def on_external_link(self, hdf_path: str, link: h5py.ExternalLink) -> None:
        self.external_files.add(link.filename)
        print(f"External file opened: {link.filename!r} for node {hdf_path!r}")


# Usage
visitor = LinkAwareVisitor()
NexusFileHandler("path/to/file.nxs").process(visitor)
print(f"Broken links: {visitor.broken}")
print(f"External files referenced: {visitor.external_files}")
```

`on_broken_link` is called for both broken soft links (`h5py.SoftLink`) and broken external links (`h5py.ExternalLink`); inspect `type(link)` to distinguish them.  `on_external_link` fires only for external links, immediately before the external file is opened. It does not fire again for nodes inside the external subtree.

## Resolving the application definition from the file

If your visitor needs to resolve the application definition from the file itself rather than receiving it as a constructor argument, read it in `on_group` when `hdf_path == ""` (the root group):

```python
def on_group(self, hdf_path: str, hdf_node: h5py.Group) -> None:
    if hdf_path == "":
        for entry_name in hdf_node:
            entry = hdf_node[entry_name]
            if isinstance(entry, h5py.Group):
                definition = entry.get("definition")
                if definition is not None:
                    raw = definition[()]
                    appdef = raw.decode() if isinstance(raw, bytes) else raw
                    self._root_node = generate_tree_from(appdef)
                    break
```

## Design notes

- **Accumulate state in the visitor, not in callbacks.** Callbacks return `None`; read accumulated state after `process()` returns or in `on_complete`.
- **The handler owns the file.** Do not open or close the HDF5 file yourself; `on_complete` gives you access to the open root for any final reads you need.
- **One visitor per call to `process`.** Visitors are not reset between calls; instantiate a new visitor for each file.
- **Node caching is your responsibility.** `NexusNode.find_node_at_path` accepts a `_cache` dict; passing the same dict across callbacks amortizes repeated lookups.
