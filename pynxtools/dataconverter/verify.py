"""Verifies a nxs file"""
import os
import click
import xml.etree.ElementTree as ET

from pynxtools.dataconverter import helpers
from pynxtools.dataconverter.template import Template
from pynxtools.nexus import nexus


@click.command()
@click.argument('file')
def verify(file: str):
    """Verifies a nexus file"""
    nxdl = 'NXellipsometry'  # TODO: Read from file
    definitions_path = nexus.get_nexus_definitions_path()
    nxdl_path = os.path.join(definitions_path, "contributed_definitions", f"{nxdl}.nxdl.xml")
    if not os.path.exists(nxdl_path):
        nxdl_path = os.path.join(definitions_path, "applications", f"{nxdl}.nxdl.xml")
    if not os.path.exists(nxdl_path):
        raise FileNotFoundError(f"The nxdl file, {nxdl}, was not found.")

    nxdl_root = ET.parse(nxdl_path).getroot()

    template = Template()
    helpers.generate_template_from_nxdl(nxdl_root, template)
