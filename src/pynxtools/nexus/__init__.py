# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""
Public API for the ``pynxtools.nexus`` sub-package.

Core objects
------------
NexusFileHandler
    Walks an HDF5/NeXus file and dispatches each node to a NexusVisitor.
NexusVisitor
    Abstract base class for node visitors.  Subclass to implement custom
    traversal logic (annotation, validation, NOMAD parsing, …).

Schema-tree nodes
-----------------
NexusNode
    Base tree node representing any NXDL concept.
NexusGroup
    Specialization for NXDL group elements.
NexusEntity
    Specialization for NXDL field / attribute elements.
NexusLink
    Specialization for NXDL link elements.
NexusChoice
    Specialization for NXDL choice elements.

Type aliases
------------
NexusType
    Literal union of all NeXus primitive type strings (``NX_FLOAT``, …).
NexusUnitCategory
    Literal union of all NeXus unit-category strings (``NX_ENERGY``, …).

Tree construction
-----------------
generate_tree_from(appdef)
    Build a NexusNode tree from an application-definition name.
populate_tree_from_parents(node)
    Augment a tree node with inherited definitions from parent NXDL base classes.
"""

# Lazy re-exports: avoids circular import between nexus.nexus_tree and
# dataconverter.helpers at package-initialization time.
# Direct submodule imports are always preferred for internal code.
_HANDLER = "pynxtools.nexus.handler"
_NEXUS_TREE = "pynxtools.nexus.nexus_tree"

_LAZY: dict[str, str] = {
    "NexusFileHandler": _HANDLER,
    "NexusVisitor": _HANDLER,
    "NexusNode": _NEXUS_TREE,
    "NexusGroup": _NEXUS_TREE,
    "NexusEntity": _NEXUS_TREE,
    "NexusLink": _NEXUS_TREE,
    "NexusChoice": _NEXUS_TREE,
    "NexusType": _NEXUS_TREE,
    "NexusUnitCategory": _NEXUS_TREE,
    "generate_tree_from": _NEXUS_TREE,
    "populate_tree_from_parents": _NEXUS_TREE,
}

__all__ = list(_LAZY)


def __getattr__(name: str):
    if name in _LAZY:
        import importlib

        module = importlib.import_module(_LAZY[name])
        value = getattr(module, name)
        # Cache in module globals so subsequent attribute access is O(1).
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
