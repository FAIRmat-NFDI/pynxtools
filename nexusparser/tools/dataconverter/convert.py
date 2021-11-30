import importlib.machinery
import importlib.util
import json
import logging
import os
import pprint
import xml.etree.ElementTree as ET
from typing import Tuple

import click

from writer import Writer


# Nexus related functions to be exported in a common place for all tools
def convert_nexus_to_caps(nexus):
    return nexus[2:].upper()


def convert_nexus_to_suggested_name(nexus):
    return nexus[2:]


# Common XML function
def remove_namespace_from_tag(tag):
    return tag.split("}")[-1]


# Helper functions for the convert script
def get_first_group(root):
    for child in root:
        if remove_namespace_from_tag(child.tag) == "group":
            return child
    return root


def generate_template_from_nxdl(root, path, template):
    tag = remove_namespace_from_tag(root.tag)
    # print(' ' * indent + "tag: " + tag)
    if tag == "doc":
        return

    suffix = ""
    if "name" in root.attrib:
        suffix = root.attrib['name']
    elif "type" in root.attrib:
        nexus_class = convert_nexus_to_caps(root.attrib['type'])
        hdf5name = f"[{convert_nexus_to_suggested_name(root.attrib['type'])}]"
        suffix = f"{nexus_class}{hdf5name}"

    path = path + "/" + suffix

    # Only add fields or attributes to the dictionary
    if tag in ("field", "attribute"):
        template[path] = None

    # Only add units if it is a field and the the units are not set to NX_UNITLESS
    if tag == "field" and "units" in root.attrib.keys() and root.attrib["units"] != "NX_UNITLESS":
        template[f"{path}/units"] = None

    for child in root:
        generate_template_from_nxdl(child, path, template)


def get_reader(reader_name):
    path_prefix = f"{os.path.dirname(__file__)}/" if os.path.dirname(__file__) else ""
    path = f"{path_prefix}readers/{reader_name}_reader.py"
    spec = importlib.util.spec_from_file_location(f"{reader_name}_reader.py", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.READER


def get_names_of_all_readers():
    path_prefix = f"{os.path.dirname(__file__)}/" if os.path.dirname(__file__) else ""
    files = next(os.walk(f"{path_prefix}readers/"), (None, None, []))[2]
    return [file.split('_reader.py')[0] for file in files]



@click.command()
@click.option(
    '--input_file',
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
    # Reading in the NXDL and generating a template
    tree = ET.parse(nxdl)

    template = {}
    root = get_first_group(tree.getroot())
    generate_template_from_nxdl(root, '', template)

    if generate_template:
        template.update((key, 'None') for key in template)
        logging.info(json.dumps(template, indent=4, sort_keys=True))

    # Setting up all the input data
    bulletpoint = "\n\u2022 "
    print_input_files = bulletpoint.join((' ', *input_file))
    logging.info("Using %s reader to convert the given files: %s ", reader, print_input_files)

    reader = get_reader(reader)
    data = reader().read(template=template, file_paths=input_file)

    logging.debug("The following data was read: %s", pprint.pformat(data, depth=1))

    # Writing the data to output file
    Writer().write(data)

    logging.info("The output file generated: %s", output)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    convert() # pylint: disable=no-value-for-parameter
