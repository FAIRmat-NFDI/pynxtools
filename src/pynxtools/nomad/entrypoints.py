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
    MenuSizeEnum,
    SearchQuantities,
)

schema = "pynxtools.nomad.schema.Root"


nexus_app = AppEntryPoint(
    name="NeXus App",
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
        readme="This page allows to search for generic NeXus Experiment Entries. It is similar to the entries search, but with reduced filter set, modified menu on the left and different shown columns. The dashboard directly shows useful interactive statistics about the data",
        # If you want to use quantities from a custom schema, you need to load
        # the search quantities from it first here. Note that you can use a glob
        # syntax to load the entire package, or just a single schema from a
        # package.
        search_quantities=SearchQuantities(
            include=[f"*#{schema}"],
        ),
        # Controls which columns are shown in the results table
        columns=[
            Column(title="Entry ID", search_quantity="entry_id", selected=True),
            Column(
                title="File Name",
                search_quantity=f"mainfile",
                selected=True,
            ),
            Column(
                title="Start Time",
                search_quantity=f"data.datetime#{schema}",
                selected=True,
            ),
            Column(
                title="Start Times by Entry",
                search_quantity=f"data.ENTRY[*].start_time__field#{schema}",
                selected=False,
            ),
            Column(
                title="Description",
                search_quantity=f"data.ENTRY[*].experiment_description__field#{schema}",
                selected=True,
            ),
            Column(
                title="Author",
                search_quantity=f"data.ENTRY[*].USER[*].name__field#{schema}",
                selected=True,
            ),
            Column(
                title="Sample",
                search_quantity=f"data.ENTRY[*].SAMPLE[*].name__field#{schema}",
                selected=True,
            ),
            Column(
                title="Sample ID",
                search_quantity=f"data.ENTRY[*].SAMPLE[*].identifierNAME__field#{schema}",
                selected=False,
            ),
            Column(
                title="Definition",
                search_quantity=f"data.ENTRY[*].definition__field#{schema}",
                selected=True,
            ),
        ],
        # Dictionary of search filters that are always enabled for queries made
        # within this app. This is especially important to narrow down the
        # results to the wanted subset.
        filters_locked={"section_defs.definition_qualified_name": [schema]},
        # Controls the menu shown on the left
        menu=Menu(
            size=MenuSizeEnum.MD,
            title="Menu",
            items=[
                Menu(
                    title="Elements",
                    size=MenuSizeEnum.XXL,
                    items=[
                        MenuItemPeriodicTable(
                            search_quantity="results.material.elements",
                        ),
                        MenuItemTerms(
                            search_quantity="results.material.chemical_formula_hill",
                            width=6,
                            options=0,
                        ),
                        MenuItemTerms(
                            search_quantity="results.material.chemical_formula_iupac",
                            width=6,
                            options=0,
                        ),
                        MenuItemTerms(
                            search_quantity="results.material.chemical_formula_reduced",
                            width=6,
                            options=0,
                        ),
                        MenuItemTerms(
                            search_quantity="results.material.chemical_formula_anonymous",
                            width=6,
                            options=0,
                        ),
                        MenuItemHistogram(
                            x="results.material.n_elements",
                        ),
                    ],
                ),
                Menu(
                    title="Experiment type",
                    size=MenuSizeEnum.LG,
                    items=[
                        MenuItemTerms(
                            title="Entry Type",
                            search_quantity=f"entry_type",
                            width=12,
                            options=12,
                        ),
                        MenuItemTerms(
                            title="NeXus Class",
                            search_quantity=f"data.ENTRY.definition__field#{schema}",
                            width=12,
                            options=12,
                        ),
                    ],
                ),
                Menu(
                    title="Instruments",
                    size=MenuSizeEnum.LG,
                    items=[
                        MenuItemTerms(
                            title="Name",
                            search_quantity=f"data.ENTRY.INSTRUMENT.name__field#{schema}",
                            width=12,
                            options=12,
                        ),
                        MenuItemTerms(
                            title="Short Name",
                            search_quantity=f"data.ENTRY.INSTRUMENT.name___short_name#{schema}",
                            width=12,
                            options=12,
                        ),
                    ],
                ),
                Menu(
                    title="Samples",
                    size=MenuSizeEnum.LG,
                    items=[
                        MenuItemTerms(
                            title="Name",
                            search_quantity=f"data.ENTRY.SAMPLE.name__field#{schema}",
                            width=12,
                            options=12,
                        ),
                        MenuItemTerms(
                            title="Sample ID",
                            search_quantity=f"data.ENTRY.SAMPLE.identifierNAME__field#{schema}",
                            width=12,
                            options=12,
                        ),
                    ],
                ),
                Menu(
                    title="Authors / Origin",
                    size=MenuSizeEnum.LG,
                    items=[
                        MenuItemTerms(
                            title="Entry Author",
                            search_quantity=f"data.ENTRY.USER.name__field#{schema}",
                            width=12,
                            options=5,
                        ),
                        MenuItemTerms(
                            title="Upload Author",
                            search_quantity=f"authors.name",
                            width=12,
                            options=5,
                        ),
                        MenuItemTerms(
                            title="Affiliation",
                            search_quantity=f"data.ENTRY.USER.affiliation__field#{schema}",
                            width=12,
                            options=5,
                        ),
                    ],
                ),
                MenuItemHistogram(
                    title="Start Time",
                    x=f"data.datetime#{schema}",
                    autorange=True,
                ),
                MenuItemHistogram(
                    title="Start Time by Entry",
                    x=f"data.ENTRY.start_time__field#{schema}",
                    autorange=True,
                ),
                MenuItemHistogram(
                    title="Upload Creation Time",
                    x=f"upload_create_time",
                    autorange=True,
                ),
            ],
        ),
        # Controls the default dashboard shown in the search interface
        dashboard={
            "widgets": [
                {
                    "type": "periodic_table",
                    "scale": "linear",
                    "quantity": f"results.material.elements",
                    "layout": {
                        "sm": {"minH": 3, "minW": 3, "h": 5, "w": 8, "y": 0, "x": 0},
                        "md": {"minH": 3, "minW": 3, "h": 7, "w": 12, "y": 0, "x": 0},
                        "lg": {"minH": 3, "minW": 3, "h": 10, "w": 14, "y": 0, "x": 0},
                        "xl": {"minH": 3, "minW": 3, "h": 7, "w": 10, "y": 0, "x": 0},
                        "xxl": {"minH": 3, "minW": 3, "h": 7, "w": 10, "y": 0, "x": 0},
                    },
                },
                {
                    "type": "terms",
                    "show_input": True,
                    "scale": "linear",
                    "quantity": f"entry_type",
                    "title": "Entry Type",
                    "layout": {
                        "sm": {"minH": 3, "minW": 3, "h": 5, "w": 4, "y": 0, "x": 8},
                        "md": {"minH": 3, "minW": 3, "h": 7, "w": 6, "y": 0, "x": 12},
                        "lg": {"minH": 3, "minW": 3, "h": 5, "w": 5, "y": 0, "x": 14},
                        "xl": {"minH": 3, "minW": 3, "h": 7, "w": 4, "y": 0, "x": 10},
                        "xxl": {"minH": 3, "minW": 3, "h": 7, "w": 4, "y": 0, "x": 10},
                    },
                },
                {
                    "type": "terms",
                    "show_input": True,
                    "scale": "linear",
                    "quantity": f"data.ENTRY.definition__field#{schema}",
                    "title": "NeXus Class",
                    "layout": {
                        "sm": {"minH": 3, "minW": 3, "h": 5, "w": 4, "y": 5, "x": 0},
                        "md": {"minH": 3, "minW": 3, "h": 7, "w": 6, "y": 7, "x": 0},
                        "lg": {"minH": 3, "minW": 3, "h": 5, "w": 5, "y": 0, "x": 19},
                        "xl": {"minH": 3, "minW": 3, "h": 7, "w": 4, "y": 0, "x": 14},
                        "xxl": {"minH": 3, "minW": 3, "h": 7, "w": 4, "y": 0, "x": 14},
                    },
                },
                {
                    "type": "terms",
                    "show_input": True,
                    "scale": "linear",
                    "quantity": f"data.ENTRY.USER.name__field#{schema}",
                    "title": "Author",
                    "layout": {
                        "sm": {"minH": 3, "minW": 3, "h": 5, "w": 4, "y": 5, "x": 4},
                        "md": {"minH": 3, "minW": 3, "h": 7, "w": 6, "y": 7, "x": 6},
                        "lg": {"minH": 3, "minW": 3, "h": 5, "w": 5, "y": 5, "x": 14},
                        "xl": {"minH": 3, "minW": 3, "h": 7, "w": 4, "y": 0, "x": 18},
                        "xxl": {"minH": 3, "minW": 3, "h": 7, "w": 4, "y": 0, "x": 18},
                    },
                },
                {
                    "type": "terms",
                    "show_input": True,
                    "scale": "linear",
                    "quantity": f"data.ENTRY.SAMPLE.name__field#{schema}",
                    "title": "Sample",
                    "layout": {
                        "sm": {"minH": 3, "minW": 3, "h": 5, "w": 4, "y": 5, "x": 8},
                        "md": {"minH": 3, "minW": 3, "h": 7, "w": 6, "y": 7, "x": 12},
                        "lg": {"minH": 3, "minW": 3, "h": 5, "w": 5, "y": 5, "x": 19},
                        "xl": {"minH": 3, "minW": 3, "h": 7, "w": 4, "y": 0, "x": 22},
                        "xxl": {"minH": 3, "minW": 3, "h": 7, "w": 4, "y": 0, "x": 22},
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
    resources=["nomad/examples/*"],
)
