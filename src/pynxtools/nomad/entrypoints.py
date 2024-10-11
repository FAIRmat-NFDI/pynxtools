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

apm_example = ExampleUploadEntryPoint(
    title="Atom Probe Microscopy",
    category="FAIRmat examples",
    description="""
        This example presents the capabilities of the NOMAD platform to store and standardize atom probe data.
        It shows the generation of a NeXus file according to the
        [NXapm](https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXapm.html#nxapm)
        application definition and a successive analysis of an example data set.
        The example contains a small atom probe dataset from an experiment with a LEAP instrument to get you started
        and keep the size of your NOMAD installation small. Once started, we recommend changing the respective
        input file in the NOMAD Oasis ELN to run the example with your own datasets.
    """,
    url="https://download-directory.github.io/?url=https://github.com/FAIRmat-NFDI/pynxtools-apm/tree/main/examples/nomad",
    local_path="examples/data/uploads/apm.zip",
)

ellips_example = ExampleUploadEntryPoint(
    title="Ellipsometry",
    category="FAIRmat examples",
    description="""
        This example presents the capabilities of the NOMAD platform to store and standardize ellipsometry data.
      It shows the generation of a NeXus file according to the [NXellipsometry](https://manual.nexusformat.org/classes/contributed_definitions/NXellipsometry.html#nxellipsometry)
      application definition and a successive analysis of a SiO2 on Si Psi/Delta measurement.
    """,
    url="https://download-directory.github.io/?url=https://github.com/FAIRmat-NFDI/pynxtools-ellips/tree/main/examples/nomad",
    local_path="examples/data/uploads/ellips.zip",
)

em_example = ExampleUploadEntryPoint(
    title="Electron Microscopy",
    category="FAIRmat examples",
    description="""
        This example presents the capabilities of the NOMAD platform to store and standardize electron microscopy.
        It shows the generation of a NeXus file according to the
        [NXem](https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXem.html#nxem)
        application definition.
        The example contains a small set of electron microscopy datasets to get started and keep the size of your
        NOMAD installation small. Ones started, we recommend to change the respective input file in the NOMAD Oasis
        ELN to run the example with your own datasets.
    """,
    url="https://download-directory.github.io/?url=https://github.com/FAIRmat-NFDI/pynxtools-em/tree/main/examples/nomad",
    local_path="examples/data/uploads/em.zip",
)

iv_temp_example = ExampleUploadEntryPoint(
    title="Sensor Scan - IV Temperature Curve",
    category="FAIRmat examples",
    description="""
        This example shows users how to take data from a Python framework and map it out to a Nexus application definition for IV Temperature measurements, [NXiv_temp](https://fairmat-experimental.github.io/nexus-fairmat-proposal/1c3806dba40111f36a16d0205cc39a5b7d52ca2e/classes/contributed_definitions/NXiv_temp.html#nxiv-temp).
        We use the Nexus ELN features of Nomad to generate a Nexus file.
    """,
    path="nomad/examples/iv_temp",
    local_path="examples/data/uploads/iv_temp.zip",
)

stm_example = ExampleUploadEntryPoint(
    title="Scanning Tunneling Microscopy (STM)",
    category="FAIRmat examples",
    description="""
    This example is for two types of experiments: Scanning Tunneling Microscopy (STM) and Scanning Tunneling Spectroscopy (STS) from Scanning Probe Microscopy.
    It can transform the data from files generated by a the nanonis software into the NeXus application definition NXsts.
    The example contains data files from the two specific nanonis software versions generic 5e and generic 4.5.
    """,
    url="https://download-directory.github.io/?url=https://github.com/FAIRmat-NFDI/pynxtools-stm/tree/main/examples/nomad/stm",
    local_path="examples/data/uploads/stm.zip",
)

sts_example = ExampleUploadEntryPoint(
    title="Scanning Tunneling Spectroscopy (STS)",
    category="FAIRmat examples",
    description="""
        This example is for two types of experiments: Scanning Tunneling Microscopy (STM) and Scanning Tunneling Spectroscopy (STS) from Scanning Probe Microscopy.
        It can transform the data from files generated by a the nanonis software into the NeXus application definition NXsts.
        The example contains data files from the two specific nanonis software versions generic 5e and generic 4.5.
    """,
    url="https://download-directory.github.io/?url=https://github.com/FAIRmat-NFDI/pynxtools-stm/tree/main/examples/nomad/sts",
    local_path="examples/data/uploads/sts.zip",
)

xps_example = ExampleUploadEntryPoint(
    title="X-ray Photoelectron Spectroscopy (XPS)",
    category="FAIRmat examples",
    description="""
        This example presents the capabilities of the NOMAD platform to store and standardize X-ray Photoelectron Spectroscopy XPS data.
        It shows the generation of a NeXus file according to the
        [NXmpes](https://manual.nexusformat.org/classes/contributed_definitions/NXmpes.html#nxmpes)
        application definition and a successive analysis of an example data set.
    """,
    url="https://download-directory.github.io/?url=https://github.com/FAIRmat-NFDI/pynxtools-xps/tree/main/examples/nomad",
    local_path="examples/data/uploads/xps.zip",
)
