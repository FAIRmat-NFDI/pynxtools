"""This script runs the conversion routine using a selected reader and write out a Nexus file."""

import glob
import importlib.machinery
import importlib.util
import json
import logging
import os
import sys
from typing import List, Tuple, Dict
import xml.etree.ElementTree as ET

import click

from nexusparser.tools.dataconverter.writer import Writer

logger = logging.getLogger(__name__)  # pylint: disable=C0103
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


# Nexus related functions to be exported in a common place for all tools
def convert_nexus_to_caps(nexus):
    """Helper function to convert a Nexus class from <NxClass> to <CLASS>."""
    return nexus[2:].upper()


def convert_nexus_to_suggested_name(nexus):
    """Helper function to suggest a name for a group from its Nexus class."""
    return nexus[2:]


# Common XML function
def remove_namespace_from_tag(tag):
    """Helper function to remove the namespace from an XML tag."""
    return tag.split("}")[-1]


# Helper functions for the convert script
def get_first_group(root):
    """Helper function to get the actual first group element from the NXDL"""
    for child in root:
        if remove_namespace_from_tag(child.tag) == "group":
            return child
    return root


def generate_template_from_nxdl(root, path, template):
    """Helper function to generate a template dictionary for given NXDL"""
    tag = remove_namespace_from_tag(root.tag)

    if tag == "doc":
        return

    suffix = ""
    if "name" in root.attrib:
        suffix = root.attrib['name']
    elif "type" in root.attrib:
        nexus_class = convert_nexus_to_caps(root.attrib['type'])
        hdf5name = f"[{convert_nexus_to_suggested_name(root.attrib['type'])}]"
        suffix = f"{nexus_class}{hdf5name}"

    if tag == "attribute":
        suffix = f"@{suffix}"

    path = path + "/" + suffix

    # Only add fields or attributes to the dictionary
    if tag in ("field", "attribute"):
        template[path] = None

    # Only add units if it is a field and the the units are not set to NX_UNITLESS
    if tag == "field" and "units" in root.attrib.keys() and root.attrib["units"] != "NX_UNITLESS":
        template[f"{path}/@units"] = None

    for child in root:
        generate_template_from_nxdl(child, path, template)


def get_reader(reader_name):
    """Helper function to get the reader object from it's given name"""
    path_prefix = f"{os.path.dirname(__file__)}/" if os.path.dirname(__file__) else ""
    path = f"{path_prefix}readers/{reader_name}_reader.py"
    spec = importlib.util.spec_from_file_location(f"{reader_name}_reader.py", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.READER


def get_names_of_all_readers() -> List[str]:
    """Helper function to populate a list of all available readers"""
    path_prefix = f"{os.path.dirname(__file__)}/" if os.path.dirname(__file__) else ""
    files = glob.glob(f"{path_prefix}/readers/*.py")
    return [file.split('_reader.py')[0][file.rindex("/") + 1:] for file in files]


@click.command()
@click.option(
    '--input-file',
    default=['example.data'],
    multiple=True,
    help='The path to the input data file to read. (Repeat for more than one file.)'
)
@click.option(
    '--reader',
    default='example',
    type=click.Choice(get_names_of_all_readers(), case_sensitive=False),
    help='The reader to use. default="example"'
)
@click.option(
    '--nxdl',
    default=None,
    required=True,
    help='The path to the corresponding NXDL file.'
)
@click.option(
    '--output',
    default='output.nxs',
    help='The path to the output Nexus file to be generated.'
)
@click.option(
    '--generate-template',
    is_flag=True,
    default=False,
    help='Just print out the template generated from given NXDL file.'
)
def convert(input_file: Tuple[str], reader: str, nxdl: str, output: str, generate_template: bool):
    """The conversion routine that takes the input parameters and calls the necessary functions."""
    # Reading in the NXDL and generating a template
    tree = ET.parse(nxdl)

    template: Dict[str, str] = {}
    root = get_first_group(tree.getroot())
    generate_template_from_nxdl(root, '', template)
    if generate_template:
        template.update((key, 'None') for key in template)
        logger.info(json.dumps(template, indent=4, sort_keys=True))
        return

    # Setting up all the input data
    bulletpoint = "\n\u2022 "
    print_input_files = bulletpoint.join((' ', *input_file))
    logger.info("Using %s reader to convert the given files: %s ", reader, print_input_files)

    reader = get_reader(reader)
    data = reader().read(template=template, file_paths=input_file)  # type: ignore[operator]

    logger.debug("The following data was read: %s", json.dumps(template, indent=4, sort_keys=True))

    # Writing the data to output file
    Writer(data, nxdl, output).write()

    logger.info("The output file generated: %s", output)


if __name__ == '__main__':
    convert()  # pylint: disable=no-value-for-parameter
