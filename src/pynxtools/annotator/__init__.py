# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0
"""
Public API for the ``pynxtools.annotator`` sub-package.

Annotator
    NexusVisitor implementation that annotates every node in an HDF5/NeXus
    file with NXDL documentation, optionality, data types, unit categories,
    and inheritance paths.  Used by the ``pynx read`` CLI command.
"""

from pynxtools.annotator.annotator import Annotator

__all__ = ["Annotator"]
