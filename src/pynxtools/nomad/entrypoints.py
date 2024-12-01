try:
    from nomad.config.models.plugins import (
        AppEntryPoint,
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
    mainfile_mime_re="application/x-hdf5",
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

schema = "*#pynxtools.nomad.schema.NeXus"

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
            include=[schema],
        ),
        # Controls which columns are shown in the results table
        columns=[
            # Column(quantity='entry_id', selected=True),
            # Column(
            #     quantity=f'data.section.myquantity#{schema}',
            #     selected=True
            # ),
            # Column(
            #     quantity=f'data.my_repeated_section[*].myquantity#{schema}',
            #     selected=True
            # ),
            Column(quantity="upload_create_time")
        ],
        # Dictionary of search filters that are always enabled for queries made
        # within this app. This is especially important to narrow down the
        # results to the wanted subset. Any available search filter can be
        # targeted here. This example makes sure that only entries that use
        # MySchema are included.
        # filters_locked={
        #     "section_defs.definition_qualified_name": ['#pynxtools.nomad.schema'] #schema]
        # },
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
        # dashboard={
        #     'widgets': [
        #         {
        #             'type': 'histogram',
        #             'show_input': False,
        #             'autorange': True,
        #             'nbins': 30,
        #             'scale': 'linear',
        #             'quantity': f'data.mysection.myquantity#{schema}',
        #             'layout': {
        #                 'lg': {
        #                     'minH': 3,
        #                     'minW': 3,
        #                     'h': 4,
        #                     'w': 12,
        #                     'y': 0,
        #                     'x': 0
        #                 }
        #             }
        #         }
        #     ]
        # }
    ),
)
