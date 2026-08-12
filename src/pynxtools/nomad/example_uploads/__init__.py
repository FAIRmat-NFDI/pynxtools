# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

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
