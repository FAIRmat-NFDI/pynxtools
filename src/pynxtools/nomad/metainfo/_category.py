# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

"""
Entry data category for generated NeXus metainfo classes.

Applied to the ``m_def`` of every generated class that is itself entry-creatable
(``Entry`` and every ``category="application"`` class, all of which inherit
``EntryData`` via ``Entry``), so that they are grouped under one label in the
"Create new entry from schema" dialog in NOMAD Oasis.
"""

from __future__ import annotations

from nomad.datamodel.data import EntryDataCategory
from nomad.metainfo import Category


class ExperimentCategory(EntryDataCategory):
    """
    A category for entry-creatable classes generated from NeXus definitions
    in `pynxtools` (``Entry`` and all application definitions).
    """

    m_def = Category(label="Experiment", categories=[EntryDataCategory])
