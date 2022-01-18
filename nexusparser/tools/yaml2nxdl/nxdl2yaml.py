#!/usr/bin/env python3
"""The xml2yml tool is going backward from xml to yaml file.
It also has the --append-to-base option that allows to append
the content of a user provided input file at the bottom of an existing Nexus base class,
to allow for generation of new extended base classes files

"""
import os
import xml.etree.ElementTree as ET
from typing import List
import click
from click.testing import CliRunner
import nexusparser.tools.yaml2nxdl.yaml2nxdl as yml2nxdl


def handle_group_or_field(depth, node, file_out):
    """Handle all the possible attributes that come along a field or group

"""
    if "name" in node.attrib and "type" in node.attrib:
        file_out.write(
            '{indent}{name}({value1}):\n'.format(
                indent=depth * '  ',
                name=node.attrib['name'] or '',
                value1=node.attrib['type'] or ''))
    if "name" in node.attrib and "type" not in node.attrib:
        file_out.write(
            '{indent}{name}:\n'.format(
                indent=depth * '  ',
                name=node.attrib['name'] or ''))
    if "name" not in node.attrib and "type" in node.attrib:
        file_out.write(
            '{indent}({type}):\n'.format(
                indent=depth * '  ',
                type=node.attrib['type'] or ''))
    if "minOccurs" in node.attrib and "maxOccurs" in node.attrib:
        file_out.write(
            '{indent}exists: [min, {value1}, max, {value2}]\n'.format(
                indent=(depth + 1) * '  ',
                value1=node.attrib['minOccurs'] or '',
                value2=node.attrib['maxOccurs'] or ''))
    if "minOccurs" in node.attrib \
            and "maxOccurs" not in node.attrib \
            and node.attrib['minOccurs'] == "1":
        file_out.write(
            '{indent}{name}: required \n'.format(
                indent=(depth + 1) * '  ',
                name='exists'))
    if "recommended" in node.attrib and node.attrib['recommended'] == "true":
        file_out.write(
            '{indent}exists: recommended\n'.format(
                indent=(depth + 1) * '  '))
    if "units" in node.attrib:
        file_out.write(
            '{indent}unit: {value}\n'.format(
                indent=(depth + 1) * '  ',
                value=node.attrib['units'] or ''))


def handle_dimension(depth, node, file_out):
    """Handle the dimension field

"""
    file_out.write(
        '{indent}{tag}:\n'.format(
            indent=depth * '  ',
            tag=node.tag.split("}", 1)[1]))
    file_out.write(
        '{indent}rank: {rank}\n'.format(
            indent=(depth + 1) * '  ',
            rank=node.attrib['rank']))
    dim_list = ''
    for child in list(node):
        tag = child.tag.split("}", 1)[1]
        if tag == ('dim'):
            dim_list = dim_list + '[{index}, {value}], '.format(
                index=child.attrib['index'],
                value=child.attrib['value'])
    file_out.write(
        '{indent}dim: [{value}]\n'.format(
            indent=(depth + 1) * '  ',
            value=dim_list[:-2] or ''))


def handle_attributes(depth, node, file_out):
    """Handle the attributes parsed from the xml file

"""
    file_out.write(
        '{indent}{escapesymbol}{key}:\n'.format(
            indent=depth * '  ',
            escapesymbol=r'\@',
            key=node.attrib['name']))


def handle_enumeration(depth, node, file_out):
    """Handle the enumeration field parsed from the xml file

"""
    file_out.write(
        '{indent}{tag}:'.format(
            indent=depth * '  ',
            tag=node.tag.split("}", 1)[1]))
    enum_list = ''
    for child in list(node):
        tag = child.tag.split("}", 1)[1]
        if tag == ('item'):
            enum_list = enum_list + '{value}, '.format(
                value=child.attrib['value'])
    file_out.write(
        ' [{enum_list}]\n'.format(
            enum_list=enum_list[:-2] or ''))


def handle_not_root_level_doc(depth, node, file_out):
    """Handle docs field along the yaml file

"""
    file_out.write(
        '{indent}{tag}: "{text}"\n'.format(
            indent=depth * '  ',
            tag=node.tag.split("}", 1)[1],
            text=node.text.strip().replace('\"', '\'') if node.text else ''))


class Nxdl2yaml():
    """Parse XML file and print a YML file

"""
    def __init__(
            self,
            symbol_list: List[str],
            root_level_definition: List[str],
            root_level_doc='',
            root_level_symbols=''):
        self.append_flag = True
        self.found_definition = False
        self.jump_symbol_child = False
        self.root_level_doc = root_level_doc
        self.root_level_symbols = root_level_symbols
        self.root_level_definition = root_level_definition
        self.symbol_list = symbol_list

    def handle_symbols(self, depth, node):
        """Handle symbols field and its childs

        """
        self.root_level_symbols = '{indent}{tag}: {text}'.format(
            indent=0 * '  ',
            tag=node.tag.split("}", 1)[1],
            text=node.text.strip() if node.text else '')
        depth += 1
        for child in list(node):
            tag = child.tag.split("}", 1)[1]
            if tag == ('doc'):
                self.symbol_list.append(
                    '{indent}{tag}: "{text}"'.format(
                        indent=1 * '  ',
                        tag=child.tag.split("}", 1)[1],
                        text=child.text.strip().replace('\"', '\'') if child.text else ''))
            elif tag == ('symbol'):
                self.symbol_list.append(
                    '{indent}{key}: "{value}"'.format(
                        indent=1 * '  ',
                        key=child.attrib['name'],
                        value=child.attrib['doc'] or ''))

    def handle_definition(self, node):
        """Handle definition group and its attributes

        """
        for item in node.attrib:
            if 'schemaLocation' not in item \
                    and 'name' not in item \
                    and 'extends' not in item \
                    and 'type' not in item:
                self.root_level_definition.append(
                    '{key}: {value}'.format(
                        key=item,
                        value=node.attrib[item] or ''))
        if 'name' in node.attrib.keys():
            self.root_level_definition.append(
                '({value}):'.format(
                    value=node.attrib['name'] or ''))

    def handle_root_level_doc(self, node):
        """Handle the documentation field found at root level

"""
        for child in list(node):
            tag = child.tag.split("}", 1)[1]
            if tag == ('doc'):
                self.root_level_doc = '{indent}{tag}: "{text}"'.format(
                    indent=0 * '  ',
                    tag=child.tag.split("}", 1)[1],
                    text=child.text.strip().replace('\"', '\'') if child.text else '')
                node.remove(child)

    def print_root_level_doc(self, file_out):
        """Print at the root level of YML file \
the general documentation field found in XML file

 """
        file_out.write(
            '{indent}{root_level_doc}\n'.format(
                indent=0 * '  ',
                root_level_doc=self.root_level_doc))
        self.root_level_doc = ''

    def print_root_level_info(self, depth, file_out):
        """Print at the root level of YML file \
the information stored as definition attributes in the XML file

"""
        if depth > 0 \
                and [s for s in self.root_level_definition if "category: application" in s]\
                or depth == 1 \
                and [s for s in self.root_level_definition if "category: base" in s]:
            if self.root_level_symbols:
                file_out.write(
                    '{indent}{root_level_symbols}\n'.format(
                        indent=0 * '  ',
                        root_level_symbols=self.root_level_symbols))
                for symbol in self.symbol_list:
                    file_out.write(
                        '{indent}{symbol}\n'.format(
                            indent=0 * '  ',
                            symbol=symbol))
            if self.root_level_definition:
                for defs in self.root_level_definition:
                    file_out.write(
                        '{indent}{defs}\n'.format(
                            indent=0 * '  ',
                            defs=defs))
            self.found_definition = False

    def recursion_in_xml_tree(self, depth, node, output_yml):
        """Descend lower level in xml tree. If we are in the symbols branch, \
the recursive behaviour is not triggered as we already handled the symbols' childs
"""
        if self.jump_symbol_child is True:
            self.jump_symbol_child = False
        else:
            for child in list(node):
                Nxdl2yaml.xmlparse(self, output_yml, child, depth)

    def xmlparse(self, output_yml, node, depth):
        """Main of the nxdl2yaml converter.
It parses XML tree,
then prints recursively each level of the tree

    """
        print(depth, node.attrib)
        with open(output_yml, "a") as file_out:
            tag = node.tag.split("}", 1)[1]
            if tag == ('definition'):
                self.found_definition = True
                Nxdl2yaml.handle_definition(self, node)
            if depth == 0 and not self.root_level_doc:
                Nxdl2yaml.handle_root_level_doc(self, node)
            if tag == ('doc') and depth != 1:
                handle_not_root_level_doc(depth, node, file_out)
            if tag == ('symbols'):
                Nxdl2yaml.handle_symbols(self, depth, node)
                self.jump_symbol_child = True
            # End of root level definition parsing. Print root-level definitions in file
            if self.root_level_doc \
                    and self.append_flag is True \
                    and (depth in (0, 1)):
                Nxdl2yaml.print_root_level_doc(self, file_out)
            if self.found_definition is True and self.append_flag is True:
                Nxdl2yaml.print_root_level_info(self, depth, file_out)
            # End of print root-level definitions in file
            if tag in ('field', 'group') and depth != 0:
                handle_group_or_field(depth, node, file_out)
            if tag == ('enumeration'):
                handle_enumeration(depth, node, file_out)
            if tag == ('attribute'):
                handle_attributes(depth, node, file_out)
            if tag == ('dimensions'):
                handle_dimension(depth, node, file_out)
        depth += 1
        # Write nested nodes
        Nxdl2yaml.recursion_in_xml_tree(self, depth, node, output_yml)


def print_yml(input_file):
    """Parse an XML file provided as input and print a YML file

"""
    output_yml = input_file[:-9] + '_parsed.yml'
    if os.path.isfile(output_yml):
        os.remove(output_yml)
    my_file = Nxdl2yaml([], [])
    depth = 0
    tree = ET.parse(input_file)
    my_file.xmlparse(output_yml, tree.getroot(), depth)


def append_yml(input_file, append_to_base):
    """Append to an existing Nexus base class new elements provided in YML input file \
and print both an XML and YML file of the extended base class.
Note: the input file name must match one existing Nexus base class to be appended

"""
    output_yml = input_file[:-9] + '_appended.yml'
    if os.path.isfile(output_yml):
        os.remove(output_yml)
    local_dir = os.path.abspath(os.path.dirname(__file__))
    nexus_def_path = os.path.join(local_dir, '../../definitions')
    base_classes_list_files = os.listdir(os.path.join(nexus_def_path, 'base_classes'))
    assert [s for s in base_classes_list_files if append_to_base.strip() == s.strip('.nxdl.xml')], \
        'Your base class extension does not match any existing Nexus base classes'
    base_class = os.path.join(nexus_def_path + '/base_classes', append_to_base + '.nxdl.xml')
    nexus_file = Nxdl2yaml([], [])
    depth = 0
    tree = ET.parse(base_class)
    nexus_file.xmlparse(output_yml, tree.getroot(), depth)
    my_file = Nxdl2yaml([], [], False)  # False print of definition: it's already on top of file
    depth = 0
    tree = ET.parse(input_file)
    my_file.xmlparse(output_yml, tree.getroot(), depth)
    back_to_xml = CliRunner().invoke(yml2nxdl.yaml2nxdl, ['--input-file', output_yml])
    assert back_to_xml.exit_code == 0


@click.command()
@click.option(
    '--input-file',
    help='The path to the xml-formatted input data file to read and create \
a YAML file from.'
)
@click.option(
    '--append-to-base',
    help='Parse xml file and append to base class, given that the xml file has same name \
of an existing base class'
)
def launch_nxdl2yml(input_file: str, append_to_base: str):
    """Helper function that triggers either the parsing or the appending routines

"""
    if not append_to_base:
        print_yml(input_file)
    else:
        append_yml(input_file, append_to_base)


if __name__ == '__main__':
    launch_nxdl2yml()   # pylint: disable=no-value-for-parameter
