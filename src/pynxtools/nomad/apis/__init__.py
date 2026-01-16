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

from nomad.config.models.plugins import APIEntryPoint


class MyAPIEntryPoint(APIEntryPoint):
    def load(self):
        from pynxtools.nomad.apis.ontology_service import app

        return app


ontology_service = MyAPIEntryPoint(
    name="ontology_service",
    description="A service to provide ontological information for a given NeXus class.",
    prefix="/ontology_service",
)
