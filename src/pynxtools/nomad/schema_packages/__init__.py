# SPDX-FileCopyrightText: The pynxtools Authors
#
# This file is part of pynxtools.
#
# SPDX-License-Identifier: Apache-2.0

try:
    from nomad.config.models.plugins import SchemaPackageEntryPoint
except ImportError as exc:
    raise ImportError(
        "Could not import nomad package. Please install the package 'nomad-lab'."
    ) from exc


class NexusDataConverterEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from pynxtools.nomad.schema_packages.dataconverter import m_package

        return m_package


class NexusSchemaEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from pynxtools.nomad.schema_packages.schema import nexus_metainfo_package

        return nexus_metainfo_package


nexus_data_converter = NexusDataConverterEntryPoint(
    name="NeXus Dataconverter",
    description="The NeXus dataconverter to convert data into the NeXus format.",
)

nexus_schema = NexusSchemaEntryPoint(
    name="NeXus",
    description="The NeXus metainfo package.",
)
