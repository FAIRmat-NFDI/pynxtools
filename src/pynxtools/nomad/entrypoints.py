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
    from nomad.config.models.plugins import (
        ParserEntryPoint,
        SchemaPackageEntryPoint,
        ExampleUploadEntryPoint,
    )
except ImportError as exc:
    raise ImportError(
        "Could not import nomad package. Please install the package 'nomad-lab'."
    ) from exc


class NexusParserEntryPoint(ParserEntryPoint):
    def load(self):
        from pynxtools.nomad.parser import NexusParser

        return NexusParser(**self.dict())


class NexusSchemaEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from pynxtools.nomad.schema import nexus_metainfo_package

        return nexus_metainfo_package


class NexusDataConverterEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from pynxtools.nomad.dataconverter import m_package

        return m_package


nexus_schema = NexusSchemaEntryPoint(
    name="NeXus",
    description="The NeXus metainfo package.",
)

nexus_data_converter = NexusDataConverterEntryPoint(
    name="NeXus Dataconverter",
    description="The NeXus dataconverter to convert data into the NeXus format.",
)

nexus_parser = NexusParserEntryPoint(
    name="pynxtools parser",
    description="A parser for nexus files.",
    mainfile_name_re=r".*\.nxs",
    mainfile_mime_re="application/x-hdf5",
)

iv_temp_example = ExampleUploadEntryPoint(
    title="Sensor Scan - IV Temperature Curve",
    category="FAIRmat examples",
    description="""
        This example shows users how to take data from a Python framework and map it out to a Nexus application definition for IV Temperature measurements, [`NXiv_temp`](https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXiv_temp.html).
        We use the Nexus ELN features of NOMAD to generate a Nexus file.
    """,
    plugin_package="pynxtools",
    resources=["nomad/examples/iv_temp/*"],
)
