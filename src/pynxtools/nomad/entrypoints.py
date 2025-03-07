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
    MenuItemOption,
    MenuItemPeriodicTable,
    MenuItemTerms,
    SearchQuantities,
)

schema = "pynxtools.nomad.schema.Root"

nxdefs_inheriting_from_sensorscan = [
    "NXsensor_scan",
    "NXiv_temp",
    "NXspm",
    "NXsts",
    "NXafm",
    "NXstm",
]

nxsensor_scan_app = AppEntryPoint(
    name="NXsensor_scan App",
    description="App for NXsensor_scan and inheriting from it classes.",
    app=App(
        # Label of the App
        label="Simple Scan",
        # Path used in the URL, must be unique
        path="nxsensor_scan",
        # Used to categorize apps in the explore menu
        category="Experiment",
        # Brief description used in the app menu
        description="Search simple scan experiments (NXsensor_scan and inheriting classes), including output of NOMAD CAMELS",
        # Longer description that can also use markdown
        readme="This page allows to search for generic experimental entries corresponding to NXsensor_scan and inheriting from it classes, including output of NOMAD CAMELS. It is similar to the entries search, but with reduced filter set, modified menu on the left and different shown columns. The dashboard directly shows useful interactive statistics about the data",
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
                search_quantity=f"data.name#{schema}",
                selected=True,
            ),
            Column(
                title="Start Time",
                search_quantity=f"data.ENTRY[*].start_time#{schema}",
                selected=True,
            ),
            Column(
                title="Description",
                search_quantity=f"data.ENTRY[*].experiment_description__field#{schema}",
                selected=True,
            ),
            Column(
                title="Author",
                search_quantity=f"[data.ENTRY[*].USER[*].name__field, data.ENTRY[*].userID[*].name__field]#{schema}",
                selected=True,
            ),
            Column(
                title="Sample",
                search_quantity=f"data.ENTRY[*].SAMPLE[*].name__field#{schema}",
                selected=True,
            ),
            Column(
                title="Sample ID",
                search_quantity=f"data.ENTRY[*].SAMPLE[*].sample_id__field#{schema}",
                selected=False,
            ),
            Column(
                title="Definition",
                search_quantity=f"data.ENTRY[*].definition__field#{schema}",
                selected=True,
            ),
            Column(
                title="Protocol",
                search_quantity=f"data.ENTRY[*].NOTE[?name=='protocol'].file_name__field#{schema}#str",
                selected=False,
            ),
        ],
        # Dictionary of search filters that are always enabled for queries made
        # within this app. This is especially important to narrow down the
        # results to the wanted subset.
        filters_locked={
            f"data.ENTRY.definition__field#{schema}": nxdefs_inheriting_from_sensorscan,
        },
        # Controls the menu shown on the left
        menu=Menu(
            title="Menu",
            items=[
                Menu(
                    title="Elements",
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
                        MenuItemHistogram(
                            x="results.material.n_elements",
                        ),
                    ],
                ),
                Menu(
                    title="Instruments",
                    items=[
                        MenuItemTerms(
                            title="Model",
                            search_quantity=f"data.ENTRY.INSTRUMENT.name__field#{schema}",
                            width=12,
                            options=12,
                        ),
                        MenuItemTerms(
                            name="Name",
                            search_quantity=f"data.ENTRY.INSTRUMENT.name#{schema}",
                            width=12,
                            options=12,
                        ),
                    ],
                ),
                Menu(
                    title="Samples",
                    items=[
                        MenuItemTerms(
                            title="Name",
                            search_quantity=f"data.ENTRY.SAMPLE.name__field#{schema}",
                            width=12,
                            options=12,
                        ),
                        MenuItemTerms(
                            title="Sample ID",
                            search_quantity=f"data.ENTRY.SAMPLE.sample_id__field#{schema}",
                            width=12,
                            options=12,
                        ),
                    ],
                ),
                Menu(
                    title="Authors",
                    items=[
                        MenuItemTerms(
                            title="Name",
                            search_quantity=f"data.ENTRY.USER.name__field#{schema}",
                            width=12,
                            options=12,
                        ),
                        MenuItemTerms(
                            title="Affiliation",
                            search_quantity=f"data.ENTRY.USER.affiliation__field#{schema}",
                            width=12,
                            options=12,
                        ),
                    ],
                ),
                Menu(
                    title="Protocols (NOMAD CAMELS)",
                    items=[
                        MenuItemTerms(
                            title="CAMELS files",
                            search_quantity=f"data.ENTRY.PROCESS.program__field#{schema}",
                            width=12,
                            options={
                                "NOMAD CAMELS": MenuItemOption(
                                    label="NOMAD CAMELS entries only",
                                ),
                            },
                            show_header=False,
                            show_input=False,
                        ),
                        MenuItemTerms(
                            title="Protocols (only for CAMELS files)",
                            search_quantity=f"data.ENTRY.NOTE.file_name__field#{schema}#str",
                            width=12,
                            options=12,
                        ),
                    ],
                ),
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
                    "quantity": f"data.ENTRY.start_time#{schema}",
                    "title": "Start Time",
                    "layout": {
                        "lg": {"minH": 3, "minW": 3, "h": 6, "w": 10, "y": 0, "x": 0}
                    },
                },
                {
                    "type": "terms",
                    "show_input": False,
                    "scale": "linear",
                    "quantity": f"entry_type",
                    "title": "Entry Type",
                    "layout": {
                        "lg": {"minH": 3, "minW": 3, "h": 6, "w": 5, "y": 6, "x": 0}
                    },
                },
                {
                    "type": "terms",
                    "show_input": False,
                    "scale": "linear",
                    "quantity": f"data.ENTRY.SAMPLE.sample_id__field#{schema}",
                    "title": "Sample ID",
                    "layout": {
                        "lg": {"minH": 3, "minW": 3, "h": 12, "w": 4, "y": 0, "x": 14}
                    },
                },
                {
                    "type": "terms",
                    "show_input": False,
                    "scale": "linear",
                    "quantity": f"data.ENTRY.USER.name__field#{schema}",
                    "title": "Author",
                    "layout": {
                        "lg": {"minH": 3, "minW": 3, "h": 6, "w": 5, "y": 6, "x": 5}
                    },
                },
                {
                    "type": "terms",
                    "show_input": False,
                    "scale": "linear",
                    "quantity": f"data.ENTRY.SAMPLE.name__field#{schema}",
                    "title": "Sample",
                    "layout": {
                        "lg": {"minH": 3, "minW": 3, "h": 12, "w": 4, "y": 0, "x": 10}
                    },
                },
            ]
        },
    ),
)

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
