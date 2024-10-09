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
    path="nomad/examples/apm",
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
    path="nomad/examples/ellips",
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
    path="nomad/examples/em",
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

mpes_example = ExampleUploadEntryPoint(
    title="Multidimensional photoemission spectroscopy (MPES)",
    category="FAIRmat examples",
    description="""
        This example presents the capabilities of the NOMAD platform to store and standardize multidimensional photoemission spectroscopy (MPES) experimental data. It contains three major examples:

      - Taking a pre-binned file, here stored in a h5 file, and converting it into the standardized MPES NeXus format.
        There exists a [NeXus application definition for MPES](https://manual.nexusformat.org/classes/contributed_definitions/NXmpes.html#nxmpes) which details the internal structure of such a file.
      - Binning of raw data (see [here](https://www.nature.com/articles/s41597-020-00769-8) for additional resources) into a h5 file and consecutively generating a NeXus file from it.
      - An analysis example using data in the NeXus format and employing the [pyARPES](https://github.com/chstan/arpes) analysis tool to reproduce the main findings of [this paper](https://arxiv.org/pdf/2107.07158.pdf).
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
    path="nomad/examples/sts/stm",
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
    path="nomad/examples/sts/sts",
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
    path="nomad/examples/sts/sts",
    local_path="examples/data/uploads/sts.zip",
)
