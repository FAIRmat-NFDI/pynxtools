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

"""Keep pytest from collecting the converter golden files as test modules.

The goldens are named after the modules the converter generates (``test.py`` for
NXtest, ``test_extended.py`` for NXtest_extended), and ``test_extended.py``
matches pytest's default ``test_*.py`` discovery pattern. They are reference
data, not tests: importing them would require the generated metainfo packages to
be importable, which is not what this suite checks. ``collect_ignore_glob`` is
pytest's supported hook for excluding files from collection in a directory.
"""

collect_ignore_glob = ["*.py"]
