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
        AppEntryPoint,
        ExampleUploadEntryPoint,
        ParserEntryPoint,
        SchemaPackageEntryPoint,
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
    mainfile_mime_re="application/x-hdf*",
)

from nomad.config.models.ui import (
    App,
    Column,
    Menu,
    MenuItemHistogram,
    MenuItemPeriodicTable,
    MenuItemTerms,
    SearchQuantities,
)

schema = "pynxtools.nomad.schema.Root"

nexus_app = AppEntryPoint(
    name="NexusApp",
    description="Simple Generic NeXus app.",
    app=App(
        # Label of the App
        label="NeXus",
        # Path used in the URL, must be unique
        path="nexusapp",
        # Used to categorize apps in the explore menu
        category="Experiment",
        # Brief description used in the app menu
        description="A simple search app customized for generic NeXus data.",
        # Longer description that can also use markdown
        readme="This is a simple App to support basic search for NeXus based Experiment Entries.",
        # If you want to use quantities from a custom schema, you need to load
        # the search quantities from it first here. Note that you can use a glob
        # syntax to load the entire package, or just a single schema from a
        # package.
        search_quantities=SearchQuantities(
            include=[f"*#{schema}"],
        ),
        # Controls which columns are shown in the results table
        columns=[
            Column(quantity="entry_id", selected=True),
            Column(quantity=f"entry_type", selected=True),
            Column(
                title="definition",
                quantity=f"data.ENTRY[*].definition__field#{schema}",
                selected=True,
            ),
            Column(
                title="start_time",
                quantity=f"data.ENTRY[*].start_time__field#{schema}",
                selected=True,
            ),
            Column(
                title="title",
                quantity=f"data.ENTRY[*].title__field#{schema}",
                selected=True,
            ),
        ],
        # Dictionary of search filters that are always enabled for queries made
        # within this app. This is especially important to narrow down the
        # results to the wanted subset. Any available search filter can be
        # targeted here. This example makes sure that only entries that use
        # MySchema are included.
        filters_locked={"section_defs.definition_qualified_name": [schema]},
        # Controls the menu shown on the left
        menu=Menu(
            title="Material",
            items=[
                Menu(
                    title="elements",
                    items=[
                        MenuItemPeriodicTable(
                            quantity="results.material.elements",
                        ),
                        MenuItemTerms(
                            quantity="results.material.chemical_formula_hill",
                            width=6,
                            options=0,
                        ),
                        MenuItemTerms(
                            quantity="results.material.chemical_formula_iupac",
                            width=6,
                            options=0,
                        ),
                        MenuItemHistogram(
                            x="results.material.n_elements",
                        ),
                    ],
                )
            ],
        ),
        # Controls the default dashboard shown in the search interface
        dashboard={
            "widgets": [
                {
                    "type": "histogram",
                    "show_input": False,
                    "autorange": True,
                    "nbins": 30,
                    "scale": "linear",
                    "quantity": f"data.ENTRY.start_time__field#{schema}",
                    "title": "Start Time",
                    "layout": {
                        "lg": {"minH": 3, "minW": 3, "h": 4, "w": 12, "y": 0, "x": 0}
                    },
                },
                {
                    "type": "terms",
                    "show_input": False,
                    "scale": "linear",
                    "quantity": f"entry_type",
                    "title": "Entry Type",
                    "layout": {
                        "lg": {"minH": 3, "minW": 3, "h": 8, "w": 4, "y": 0, "x": 12}
                    },
                },
                {
                    "type": "terms",
                    "show_input": False,
                    "scale": "linear",
                    "quantity": f"data.ENTRY.definition__field#{schema}",
                    "title": "Definition",
                    "layout": {
                        "lg": {"minH": 3, "minW": 3, "h": 8, "w": 4, "y": 0, "x": 16}
                    },
                },
                {
                    "type": "periodic_table",
                    "scale": "linear",
                    "quantity": f"results.material.elements",
                    "layout": {
                        "lg": {"minH": 3, "minW": 3, "h": 4, "w": 12, "y": 4, "x": 0}
                    },
                },
            ]
        },
    ),
)

simple_nexus_example = ExampleUploadEntryPoint(
    title="Simple NeXus Example",
    category="NeXus Experiment Examples",
    description="""
        This example show 3 use cases on how NeXus experiment data can be handled in NOMAD.
        Example 1 - ELN Export
        This example shows how a simple ELN can be set up in NOMAD which can be then
        exported in to an RDM agnostic eln_data.yaml format. The example also shows how such
        eln file can be used together with some experiment data to be converted by pynxtools
        to a valid NeXus file.
        Example 2 - Interface for Data Conversion to NeXus Format
        This example shows how NOMAD GUI allows converting experiment data with
        attached eln notes to NeXus file.
        Example 3 - Sensor Scan - IV Temperature Curve
        This example shows how experimental data can be mapped to a Nexus application definition.
        Here, data from an IV Temperature measurements as taken by a Python framework is
        converted to [`NXiv_temp`](https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXiv_temp.html).
        We also demonstrate the use of Nexus ELN features of NOMAD to add further details
        which were not provided by the data acquisition software.
        This example combines Example 1, and 2, and demonstrates how a NOMAD ELN can be built
        to collect additional information, and combine it with experimental data to convert
        them into exportable NeXus file, which is also directly searchable in NOMAD.
    """,
    plugin_package="pynxtools",
    resources=["nomad/examples/*"],
)
