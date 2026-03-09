# Implement a custom NexusVisitor

!!! info "This guide assumes familiarity with the visitor pattern in pynxtools. Read [pynxtools architecture](../../learn/pynxtools/architecture.md) first."

`NexusFileHandler` accepts any `NexusVisitor`, making it straightforward to add new HDF5 processing modes without modifying pynxtools internals. This guide walks through implementing a minimal custom visitor.

## When to write a custom visitor

Write a custom visitor when you need to process every node of a NeXus file in a way that is not covered by the built-in `Annotator` or `ValidationVisitor`. Common use cases:

- Collecting statistics over all fields (e.g. value ranges, missing data)
- Extracting a specific subset of nodes for further processing
- Implementing a custom export or transformation
- Linting files against local conventions beyond what `validate_nexus` checks

## The visitor interface

Every visitor implements four hooks (all optional — default to no-ops):

```python
from pynxtools.nexus.handler import NexusVisitor
import h5py

class NexusVisitor:
    def on_group(self, hdf_path: str, hdf_node: h5py.Group) -> None: ...
    def on_field(self, hdf_path: str, hdf_node: h5py.Dataset) -> None: ...
    def on_attribute(
        self,
        hdf_path: str,
        attr_name: str,
        attr_value,
        parent: h5py.Group | h5py.Dataset,
    ) -> None: ...
    def on_complete(self, root: h5py.File) -> None: ...
```

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

    def on_field(self, hdf_path: str, hdf_node: h5py.Dataset) -> None:
        value = hdf_node[()]
        # Only store scalars and short arrays for this example
        if np.ndim(value) == 0 or (np.ndim(value) == 1 and len(value) <= 10):
            self.fields[hdf_path] = value

    def on_complete(self, root: h5py.File) -> None:
        print(f"Collected {len(self.fields)} fields.")


# Usage
visitor = FieldCollector()
handler = NexusFileHandler("path/to/file.nxs", visitor)
handler.process()

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
    """
    Example visitor that looks up the NexusNode for every field
    and logs its optionality and declared unit category.
    """

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


# Usage
logging.basicConfig(level=logging.INFO)
visitor = SchemaAwareVisitor("NXarpes")
handler = NexusFileHandler("path/to/arpes_file.nxs", visitor)
handler.process()
```

## Registering schema information

If your visitor needs to resolve the application definition from the file itself (rather than receiving it as a constructor argument), look it up in `on_group` when `hdf_path == ""` (the root):

```python
def on_group(self, hdf_path: str, hdf_node: h5py.Group) -> None:
    if hdf_path == "":
        # Root group — inspect NXentry children for definition field
        for entry_name in hdf_node:
            entry = hdf_node[entry_name]
            if isinstance(entry, h5py.Group):
                definition = entry.get("definition")
                if definition is not None:
                    appdef = definition[()].decode() if isinstance(definition[()], bytes) else definition[()]
                    self._root_node = generate_tree_from(appdef)
                    break
```

## Design notes

- **Accumulate state in the visitor, not in callbacks.** Callbacks return `None`; state should be stored as instance attributes and read in `on_complete` or after `handler.process()` returns.
- **The handler owns the file.** Do not open or close the HDF5 file yourself; `on_complete` gives you access to the open root for any final reads you need.
- **One visitor per call to `process`.** Visitors are not reset between calls; instantiate a new visitor for each file.
- **Node caching is your responsibility.** `NexusNode.find_node_at_path` accepts a `_cache` dict; passing the same dict across calls amortizes repeated lookups across callbacks.
