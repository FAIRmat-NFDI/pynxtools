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
"""
NeXus App v2 — backed by the Phase 2 generated Python metainfo (NexusParserV2).

Column paths use new archive structure (no __field suffix, lowercase
group names).
"""

try:
    from nomad.config.models.plugins import AppEntryPoint
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
except ImportError as exc:
    raise ImportError(
        "Could not import nomad package. Please install the package 'nomad-lab'."
    ) from exc

schema = "pynxtools.nomad.metainfo.base_classes.Entry"

nexus_app_v2 = AppEntryPoint(
    name="NeXus App",
    description="NeXus app backed by generated Python metainfo.",
    app=App(
        label="NeXus v2",
        path="nexusappv2",
        category="Experiment",
        description="Search app for NeXus data parsed by the annotation-based parser.",
        readme=(
            "Searches NeXus entries parsed using the generated Python metainfo classes "
            "(nexus_parser_v2)."
        ),
        search_quantities=SearchQuantities(
            include=[f"*#{schema}"],
        ),
        columns=[
            Column(title="Entry ID", search_quantity="entry_id", selected=True),
            Column(title="Entry Name", search_quantity="entry_name", selected=True),
            Column(title="File Name", search_quantity="mainfile", selected=True),
            Column(
                title="Start Time",
                search_quantity=f"data.start_time#{schema}",
                selected=True,
            ),
            Column(
                title="Author",
                search_quantity=f"data.user[*].name_quantity#{schema}",
                selected=True,
            ),
            Column(
                title="Sample",
                search_quantity=f"data.sample[*].name_quantity#{schema}",
                selected=True,
            ),
            Column(
                title="Sample ID",
                search_quantity=f"data.sample[*].identifierNAME#{schema}",
                selected=False,
            ),
            Column(
                title="Definition",
                search_quantity=f"data.definition#{schema}",
                selected=True,
            ),
        ],
        filters_locked={"section_defs.definition_qualified_name": [schema]},
        menu=Menu(
            size=MenuSizeEnum.MD,
            title="Menu",
            items=[
                Menu(
                    title="Elements",
                    size=MenuSizeEnum.XXL,
                    items=[
                        MenuItemPeriodicTable(
                            search_quantity="results.material.elements"
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
                        MenuItemHistogram(x="results.material.n_elements"),
                    ],
                ),
                Menu(
                    title="Experiment type",
                    size=MenuSizeEnum.LG,
                    items=[
                        MenuItemTerms(
                            title="Entry Type",
                            search_quantity="entry_type",
                            width=12,
                            options=12,
                        ),
                        MenuItemTerms(
                            title="NeXus Class",
                            search_quantity=f"data.definition#{schema}",
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
                            search_quantity=f"data.instrument.name_quantity#{schema}",
                            width=12,
                            options=12,
                        ),
                        MenuItemTerms(
                            title="Short Name",
                            search_quantity=f"data.instrument.name_quantity__short_name#{schema}",
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
                            search_quantity=f"data.sample.name_quantity#{schema}",
                            width=12,
                            options=12,
                        ),
                        MenuItemTerms(
                            title="Sample ID",
                            search_quantity=f"data.sample.identifierNAME#{schema}",
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
                            search_quantity=f"data.user.name_quantity#{schema}",
                            width=12,
                            options=5,
                        ),
                        MenuItemTerms(
                            title="Upload Author",
                            search_quantity="authors.name",
                            width=12,
                            options=5,
                        ),
                        MenuItemTerms(
                            title="Affiliation",
                            search_quantity=f"data.user.affiliation#{schema}",
                            width=12,
                            options=5,
                        ),
                    ],
                ),
                MenuItemHistogram(
                    title="Start Time",
                    x=f"data.start_time#{schema}",
                    autorange=True,
                ),
                MenuItemHistogram(
                    title="Upload Creation Time",
                    x="upload_create_time",
                    autorange=True,
                ),
            ],
        ),
        dashboard={
            "widgets": [
                {
                    "type": "periodic_table",
                    "scale": "linear",
                    "quantity": "results.material.elements",
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
                    "quantity": "entry_type",
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
                    "quantity": f"data.definition#{schema}",
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
                    "quantity": f"data.user.name_quantity#{schema}",
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
                    "quantity": f"data.sample.name_quantity#{schema}",
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
