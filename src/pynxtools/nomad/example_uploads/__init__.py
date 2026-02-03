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

try:
    from nomad.config.models.plugins import ExampleUploadEntryPoint
except ImportError as exc:
    raise ImportError(
        "Could not import nomad package. Please install the package 'nomad-lab'."
    ) from exc

simple_nexus_example = ExampleUploadEntryPoint(
    title="Simple NeXus Example",
    category="NeXus Experiment Examples",
    description="""
        Sensor Scan - IV Temperature Curve
        This example shows how experimental data can be mapped to a Nexus application definition.
        Here, data from an IV Temperature measurements as taken by a Python framework is
        converted to [`NXiv_temp`](https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXiv_temp.html).
        We also demonstrate the use of Nexus ELN features of NOMAD to add further details
        which were not provided by the data acquisition software.
        This example demonstrates how
        - a NOMAD ELN can be built and its content can be written to an RDM platform agnostic yaml format
        - NOMAD ELN can be used to combine ELN data with experiment data and export them to NeXus
        - NeXus data is represented as an Entry with searchable quantities in NOMAD
        - NORTH tools can be used to work with data in NOMAD uploads
    """,
    plugin_package="pynxtools",
    resources=["nomad/example_uploads/iv_temp_example/*"],
)
