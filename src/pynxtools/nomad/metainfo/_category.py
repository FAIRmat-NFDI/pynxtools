#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
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
