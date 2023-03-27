#!/usr/bin/env python3
"""This file collects the function used in the reverse tool nxdl2yaml.

"""
# -*- coding: utf-8 -*-
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
import sys
from typing import List

from nexusutils.nyaml2nxdl.nyaml2nxdl_helper import (get_node_parent_info,
                                                     get_yaml_escape_char_dict,
                                                     cleaning_empty_lines)
from nexusutils.dataconverter.helpers import remove_namespace_from_tag


DEPTH_SIZE = "  "


def handle_mapping_char(text):
    """Check for ":" char and replace it by "':'". """

    # This escape chars and sepeerator ':' is not allowed in yaml library
    escape_char = get_yaml_escape_char_dict()
    for esc_key, val in escape_char.items():
        if esc_key in text:
            text = text.replace(esc_key, val)
    return text


class Nxdl2yaml():
    """
        Parse XML file and print a YML file
    """

    def __init__(
            self,
            symbol_list: List[str],
            root_level_definition: List[str],
            root_level_doc='',
            root_level_symbols=''):

        # updated part of yaml_dict
        self.append_flag = True
        self.found_definition = False
        self.root_level_doc = root_level_doc
        self.root_level_symbols = root_level_symbols
        self.root_level_definition = root_level_definition
        self.symbol_list = symbol_list

    def handle_symbols(self, depth, node):
        """Handle symbols field and its childs symbol"""

        # pylint: disable=consider-using-f-string
        self.root_level_symbols = (
            f"{remove_namespace_from_tag(node.tag)}: "
            f"{node.text.strip() if node.text else ''}"
        )
        depth += 1
        for child in list(node):
            tag = remove_namespace_from_tag(child.tag)
            if tag == 'doc':
                self.symbol_list.append(self.handle_not_root_level_doc(depth,
                                                                       text=child.text))
            elif tag == 'symbol':
                if 'doc' in child.attrib:
                    self.symbol_list.append(
                        self.handle_not_root_level_doc(depth,
                                                       tag=child.attrib['name'],
                                                       text=child.attrib['doc']))
                else:
                    for symbol_doc in list(child):
                        tag = remove_namespace_from_tag(symbol_doc.tag)
                        if tag == 'doc':
                            self.symbol_list.append(
                                self.handle_not_root_level_doc(depth,
                                                               tag=child.attrib['name'],
                                                               text=symbol_doc.text))

    def handle_definition(self, node):
        """
            Handle definition group and its attributes
            NOTE: Here we tried to store the order of the xml element attributes. So that we get
            exactly the same file in nxdl from yaml.
        """
        # pylint: disable=consider-using-f-string
        # self.root_level_definition[0] = ''
        keyword = ''
        # tmp_word for reseving the location
        tmp_word = "#xx#"
        attribs = node.attrib
        # for tracking the order of name and type
        keyword_order = -1
        for item in attribs:
            if "name" in item:
                keyword = keyword + attribs[item]
                if keyword_order == -1:
                    self.root_level_definition.append(tmp_word)
                    keyword_order = self.root_level_definition.index(tmp_word)
            elif "extends" in item:
                keyword = f"{keyword}({attribs[item]})"
                if keyword_order == -1:
                    self.root_level_definition.append(tmp_word)
                    keyword_order = self.root_level_definition.index(tmp_word)
            elif 'schemaLocation' not in item \
                    and 'extends' != item:
                text = f"{item}: {attribs[item]}"
                self.root_level_definition.append(text)
        self.root_level_definition[keyword_order] = f"{keyword}:"

    def handle_root_level_doc(self, node):
        """
            Handle the documentation field found at root level.
        """
        # tag = remove_namespace_from_tag(node.tag)
        text = node.text
        text = self.handle_not_root_level_doc(depth=0, text=text)
        self.root_level_doc = text

    # pylint: disable=too-many-branches
    def handle_not_root_level_doc(self, depth, text, tag='doc', file_out=None):
        """
        Handle docs field along the yaml file. In this function we also tried to keep
        the track of intended indentation. E.g. the bollow doc block.
            * Topic name
              DEscription of topic
        """

        # Handling empty doc
        if not text:
            text = ""
        else:
            text = handle_mapping_char(text)
        # pylintxxxxx: disable=consider-using-f-string
        if "\n" in text:
            # To remove '\n' character as it will be added before text.
            text = text.split('\n')
            text = cleaning_empty_lines(text)
            text_tmp = []
            yaml_indent_n = len((depth + 1) * DEPTH_SIZE)
            # Find indentaion in the first valid line with alphabet
            tmp_i = 0
            while tmp_i != -1:
                first_line_indent_n = 0
                for ch_ in text[tmp_i]:
                    if ch_ == ' ':
                        first_line_indent_n = first_line_indent_n + 1
                    elif ch_ != '':
                        tmp_i = -2
                        break
                tmp_i = tmp_i + 1
            # Taking care of doc like bellow:
            # <doc>Text liness
            # text continues</doc>
            # So no indentaion at the staring or doc. So doc group will come along general
            # alignment
            if first_line_indent_n == 0:
                first_line_indent_n = yaml_indent_n

            # for indent_diff -ve all lines will move left by the same ammout
            # for indect_diff +ve all lines will move right the same amount
            indent_diff = yaml_indent_n - first_line_indent_n
            # CHeck for first line empty if not keep first line empty

            for _, line in enumerate(text):
                line_indent_n = 0
                # Collect first empty space without alphabate
                for ch_ in line:
                    if ch_ == ' ':
                        line_indent_n = line_indent_n + 1
                    else:
                        break
                line_indent_n = line_indent_n + indent_diff
                if line_indent_n < yaml_indent_n:
                    # if line still under yaml identation
                    text_tmp.append(yaml_indent_n * ' ' + line.strip())
                else:
                    text_tmp.append(line_indent_n * ' ' + line.strip())

            text = '\n' + '\n'.join(text_tmp)
            if "}" in tag:
                tag = remove_namespace_from_tag(tag)
            indent = depth * DEPTH_SIZE
        elif text:
            text = '\n' + (depth + 1) * DEPTH_SIZE + text.strip()
            if "}" in tag:
                tag = remove_namespace_from_tag(tag)
            indent = depth * DEPTH_SIZE
        else:
            text = ""
            if "}" in tag:
                tag = remove_namespace_from_tag(tag)
            indent = depth * DEPTH_SIZE

        doc_str = f"{indent}{tag}: | {text}\n"
        if file_out:
            file_out.write(doc_str)
            return None
        return doc_str

    def print_root_level_doc(self, file_out):
        """
        Print at the root level of YML file \
        the general documentation field found in XML file
        """
        # pylint: disable=consider-using-f-string
        file_out.write(
            '{indent}{root_level_doc}\n'.format(
                indent=0 * DEPTH_SIZE,
                root_level_doc=self.root_level_doc))
        self.root_level_doc = ''

    def print_root_level_info(self, depth, file_out):
        """
        Print at the root level of YML file \
        the information stored as definition attributes in the XML file
        """
        # pylint: disable=consider-using-f-string
        if depth < 0:
            raise ValueError("Somthing wrong with indentaion in root level.")

        has_categoty = False
        for def_line in self.root_level_definition:
            if def_line in ("category: application", "category: base"):
                file_out.write(f"{def_line}\n")
                has_categoty = True

        if not has_categoty:
            raise ValueError("Definition dose not get any category from 'base or application'.")
        self.print_root_level_doc(file_out)
        if self.root_level_symbols:
            file_out.write(
                '{indent}{root_level_symbols}\n'.format(
                    indent=0 * DEPTH_SIZE,
                    root_level_symbols=self.root_level_symbols))
            for symbol in self.symbol_list:
                file_out.write(
                    '{indent}{symbol}\n'.format(
                        indent=0 * DEPTH_SIZE,
                        symbol=symbol))
        if self.root_level_definition:
            # Soring NXname for writting end of the definition attributes
            nx_name = ''
            for defs in self.root_level_definition:
                if 'NX' in defs and defs[-1] == ':':
                    nx_name = defs
                    continue
                if defs in ("category: application", "category: base"):
                    continue
                file_out.write(
                    '{indent}{defs}\n'.format(
                        indent=0 * DEPTH_SIZE,
                        defs=defs))
            file_out.write(
                '{indent}{defs}\n'.format(
                    indent=0 * DEPTH_SIZE,
                    defs=nx_name))
        self.found_definition = False

    def handle_exists(self, exists_dict, key, val):
        """
            Create exist component as folows:

            {'min' : value for min,
             'max' : value for max,
             'optional' : value for optional}

            This is created separately so that the keys stays in order.
        """
        if not val:
            val = ''
        else:
            val = str(val)
        if 'minOccurs' == key:
            exists_dict['minOccurs'] = ['min', val]
        if 'maxOccurs' == key:
            exists_dict['maxOccurs'] = ['max', val]
        if 'optional' == key:
            exists_dict['optional'] = ['optional', val]
        if 'recommended' == key:
            exists_dict['recommended'] = ['recommended', val]
        if 'required' == key:
            exists_dict['required'] = ['required', val]

    # pylint: disable=consider-using-f-string
    # pylint: disable=too-many-branches
    def handle_group_or_field(self, depth, node, file_out):
        """Handle all the possible attributes that come along a field or group"""

        allowed_attr = ['optional', 'recommended', 'name', 'type', 'axes', 'axis', 'data_offset',
                        'interpretation', 'long_name', 'maxOccurs', 'minOccurs', 'nameType',
                        'optional', 'primary', 'signal', 'stride', 'units', 'required',
                        'deprecated', 'exists']

        name_type = ""
        node_attr = node.attrib
        rm_key_list = []
        # Maintain order: name and type in form name(type) or (type)name that come first
        for key, val in node_attr.items():
            if key == 'name':
                name_type = name_type + val
                rm_key_list.append(key)
            if key == 'type':
                name_type = name_type + "(%s)" % val
                rm_key_list.append(key)
        if not name_type:
            raise ValueError(f"No 'name' or 'type' hase been found. But, 'group' or 'field' "
                             f"must have at list a nme.We got attributes:  {node_attr}")
        file_out.write('{indent}{name_type}:\n'.format(
            indent=depth * DEPTH_SIZE,
            name_type=name_type))

        for key in rm_key_list:
            del node_attr[key]

        # tmp_dict intended to persevere order of attribnutes
        tmp_dict = {}
        exists_dict = {}
        for key, val in node_attr.items():
            # As both 'minOccurs', 'maxOccurs' and optionality move to the 'exists'
            if key in ['minOccurs', 'maxOccurs', 'optional', 'recommended', 'required']:
                if 'exists' not in tmp_dict:
                    tmp_dict['exists'] = []
                self.handle_exists(exists_dict, key, val)
            elif key == 'units':
                tmp_dict['unit'] = str(val)
            else:
                tmp_dict[key] = str(val)
            if key not in allowed_attr:
                raise ValueError(f"An attribute ({key}) in 'field' or 'group' has been found "
                                 f"that is not allowed. The allowed attr is {allowed_attr}.")

        if exists_dict:
            for key, val in exists_dict.items():
                if key in ['minOccurs', 'maxOccurs']:
                    tmp_dict['exists'] = tmp_dict['exists'] + val
                elif key in ['optional', 'recommended', 'required']:
                    tmp_dict['exists'] = key

        depth_ = depth + 1
        for key, val in tmp_dict.items():
            file_out.write(f'{depth_ * DEPTH_SIZE}{key}: {handle_mapping_char(val)}\n')

    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    def handle_dimension(self, depth, node, file_out):
        """
        Handle the dimension field.
            NOTE: Usually we take care of any xml element in xmlparse(...) and
        recursion_in_xml_tree(...) functions. But Here it is a bit different. The doc dimension
          and attributes of dim has been handled inside this function here.
        """
        # pylint: disable=consider-using-f-string
        possible_dim_attrs = ['ref', 'optional', 'recommended',
                              'required', 'incr', 'refindex']
        possible_dimemsion_attrs = ['rank']

        # taking care of Dimension tag
        file_out.write(
            '{indent}{tag}:\n'.format(
                indent=depth * DEPTH_SIZE,
                tag=node.tag.split("}", 1)[1]))
        node_attrs = node.attrib

        node_attrs = node.attrib
        # Taking care of dimension attributes
        for attr, value in node_attrs.items():
            if attr in possible_dimemsion_attrs and not isinstance(value, dict):
                indent = (depth + 1) * DEPTH_SIZE
                file_out.write(f'{indent}{attr}: {value}\n')
            else:
                raise ValueError(f"Dimension has got an attribute {attr} that is not valid."
                                 f"Current the allowd atributes are {possible_dimemsion_attrs}."
                                 f" Please have a look")
        # taking carew of dimension doc
        for child in list(node):
            tag = remove_namespace_from_tag(child.tag)
            if tag == 'doc':
                text = self.handle_not_root_level_doc(depth + 1, child.text)
                file_out.write(text)
                node.remove(child)

        dim_index_value = ''
        dim_other_parts = {}
        # taking care of dim and doc childs of dimension
        for child in list(node):
            tag = child.tag.split("}", 1)[1]
            child_attrs = child.attrib
            # taking care of index and value attributes
            if tag == ('dim'):
                # taking care of index and value in format [[index, value]]
                dim_index_value = dim_index_value + '[{index}, {value}], '.format(
                    index=child_attrs['index'] if "index" in child_attrs else '',
                    value=child_attrs['value'] if "value" in child_attrs else '')
                if "index" in child_attrs:
                    del child_attrs["index"]
                if "value" in child_attrs:
                    del child_attrs["value"]

                # Taking care of doc comes as child of dim
                for cchild in list(child):
                    ttag = cchild.tag.split("}", 1)[1]
                    if ttag == ('doc'):
                        if ttag not in dim_other_parts:
                            dim_other_parts[ttag] = []
                        text = cchild.text
                        dim_other_parts[ttag].append(text.strip())
                        child.remove(cchild)
                        continue
                # taking care of other attributes except index and value
                for attr, value in child_attrs.items():
                    if attr in possible_dim_attrs:
                        if attr not in dim_other_parts:
                            dim_other_parts[attr] = []
                        dim_other_parts[attr].append(value)

        # index and value attributes of dim elements
        file_out.write(
            '{indent}dim: [{value}]\n'.format(
                indent=(depth + 1) * DEPTH_SIZE,
                value=dim_index_value[:-2] or ''))
        # Write the attributes, except index and value, and doc of dim as child of dim_parameter.
        # But tthe doc or attributes for each dim come inside list according to the order of dim.
        if dim_other_parts:
            file_out.write(
                '{indent}dim_parameters:\n'.format(
                    indent=(depth + 1) * DEPTH_SIZE))
            # depth = depth + 2 dim_paramerter has child such as doc of dim
            indent = (depth + 2) * DEPTH_SIZE
            for key, value in dim_other_parts.items():
                if key == 'doc':
                    value = self.handle_not_root_level_doc(depth + 2, str(value), key, file_out)
                else:
                    file_out.write(f"{indent}{key}: {handle_mapping_char(value)}\n")

    def handle_enumeration(self, depth, node, file_out):
        """
            Handle the enumeration field parsed from the xml file.

        If the enumeration items contain a doc field, the yaml file will contain items as child
        fields of the enumeration field.

        If no doc are inherited in the enumeration items, a list of the items is given for the
        enumeration list.

    """
        # pylint: disable=consider-using-f-string

        check_doc = []
        for child in list(node):
            if list(child):
                check_doc.append(list(child))
        if check_doc:
            file_out.write(
                '{indent}{tag}: \n'.format(
                    indent=depth * DEPTH_SIZE,
                    tag=node.tag.split("}", 1)[1]))
            for child in list(node):
                tag = child.tag.split("}", 1)[1]
                if tag == ('item'):
                    file_out.write(
                        '{indent}{value}: \n'.format(
                            indent=(depth + 1) * DEPTH_SIZE,
                            value=child.attrib['value']))
                    if list(child):
                        for item_doc in list(child):
                            item_doc_depth = depth + 2
                            self.handle_not_root_level_doc(item_doc_depth, item_doc.text,
                                                           item_doc.tag, file_out)
        else:
            file_out.write(
                '{indent}{tag}:'.format(
                    indent=depth * DEPTH_SIZE,
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

    def handle_attributes(self, depth, node, file_out):
        """Handle the attributes parsed from the xml file"""

        allowed_attr = ['name', 'type', 'units', 'nameType', 'recommended', 'optional',
                        'minOccurs', 'maxOccurs', 'deprecated']

        name = ""
        node_attr = node.attrib
        if 'name' in node_attr:
            pass
        else:
            raise ValueError("Attribute must have an name key.")
        rm_key_list = []
        # Maintain order: name and type in form name(type) or (type)name that come first
        for key, val in node_attr.items():
            if key == 'name':
                name = val
                rm_key_list.append(key)

        for key in rm_key_list:
            del node_attr[key]

        file_out.write('{indent}{escapesymbol}{name}:\n'.format(
            indent=depth * DEPTH_SIZE,
            escapesymbol=r'\@',
            name=name))

        tmp_dict = {}
        exists_dict = {}
        for key, val in node_attr.items():
            # As both 'minOccurs', 'maxOccurs' and optionality move to the 'exists'
            if key in ['minOccurs', 'maxOccurs', 'optional', 'recommended', 'required']:
                if 'exists' not in tmp_dict:
                    tmp_dict['exists'] = []
                self.handle_exists(exists_dict, key, val)
            elif key == 'units':
                tmp_dict['unit'] = val
            else:
                tmp_dict[key] = val
            if key not in allowed_attr:
                raise ValueError(f"An attribute ({key}) has been found that is not allowed."
                                 f"The allowed attr is {allowed_attr}.")

        has_min_max = False
        has_opt_reco_requ = False
        if exists_dict:
            for key, val in exists_dict.items():
                if key in ['minOccurs', 'maxOccurs']:
                    tmp_dict['exists'] = tmp_dict['exists'] + val
                    has_min_max = True
                elif key in ['optional', 'recommended', 'required']:
                    tmp_dict['exists'] = key
                    has_opt_reco_requ = True
        if has_min_max and has_opt_reco_requ:
            raise ValueError("Optionality 'exists' can take only either from ['minOccurs',"
                             " 'maxOccurs'] or from ['optional', 'recommended', 'required']"
                             ". But not from both of the groups together. Please check in"
                             " attributes")

        depth_ = depth + 1
        for key, val in tmp_dict.items():
            file_out.write(f'{depth_ * DEPTH_SIZE}{key}: {handle_mapping_char(val)}\n')

    def handel_link(self, depth, node, file_out):
        """
            Handle link elements of nxdl
        """

        possible_link_attrs = ['name', 'target', 'napimount']
        node_attr = node.attrib
        # Handle special cases
        if 'name' in node_attr:
            file_out.write('{indent}{name}(link):\n'.format(
                indent=depth * DEPTH_SIZE,
                name=node_attr['name'] or ''))
            del node_attr['name']

        depth_ = depth + 1
        # Handle general cases
        for attr_key, val in node_attr.items():
            if attr_key in possible_link_attrs:
                file_out.write('{indent}{attr}: {value}\n'.format(
                    indent=depth_ * DEPTH_SIZE,
                    attr=attr_key,
                    value=val))
            else:
                raise ValueError(f"An anexpected attribute '{attr_key}' of link has found."
                                 f"At this moment the alloed keys are {possible_link_attrs}")

    def handel_choice(self, depth, node, file_out):
        """
            Handle choice element which is a parent node of group.
        """

        possible_attr = []

        node_attr = node.attrib
        # Handle special casees
        if 'name' in node_attr:
            file_out.write('{indent}{attr}(choice): \n'.format(
                indent=depth * DEPTH_SIZE,
                attr=node_attr['name']))
            del node_attr['name']

        depth_ = depth + 1
        # Taking care of general attrinutes. Though, still no attrinutes have found,
        # but could be used for future
        for attr in node_attr.items():
            if attr in possible_attr:
                file_out.write('{indent}{attr}: {value}\n'.format(
                    indent=depth_ * DEPTH_SIZE,
                    attr=attr,
                    value=node_attr[attr]))
            else:
                raise ValueError(f"An unexpected attribute '{attr}' of 'choice' has been found."
                                 f"At this moment attributes for choice {possible_attr}")

    def recursion_in_xml_tree(self, depth, xml_tree, output_yml, verbose):
        """
            Descend lower level in xml tree. If we are in the symbols branch, the recursive
        behaviour is not triggered as we already handled the symbols' childs.
        """

        tree = xml_tree['tree']
        node = xml_tree['node']
        for child in list(node):
            xml_tree_children = {'tree': tree, 'node': child}
            self.xmlparse(output_yml, xml_tree_children, depth, verbose)

    # pylint: disable=too-many-branches
    def xmlparse(self, output_yml, xml_tree, depth, verbose):
        """
        Main of the nxdl2yaml converter.
        It parses XML tree, then prints recursively each level of the tree
        """
        tree = xml_tree['tree']
        node = xml_tree['node']

        if verbose:
            sys.stdout.write(f'Node tag: {remove_namespace_from_tag(node.tag)}\n')
            sys.stdout.write(f'Attributes: {node.attrib}\n')
        with open(output_yml, "a", encoding="utf-8") as file_out:
            tag = remove_namespace_from_tag(node.tag)
            if tag == ('definition'):
                self.found_definition = True
                self.handle_definition(node)
                for child in list(node):
                    tag_tmp = remove_namespace_from_tag(child.tag)
                    if tag_tmp == 'doc':
                        self.handle_root_level_doc(child)
                        node.remove(child)
                    if tag_tmp == 'symbols':
                        self.handle_symbols(depth, child)
                        node.remove(child)

            if tag == ('doc') and depth != 1:
                parent = get_node_parent_info(tree, node)[0]
                doc_parent = remove_namespace_from_tag(parent.tag)
                if doc_parent != 'item':
                    self.handle_not_root_level_doc(depth, text=node.text,
                                                   tag=node.tag,
                                                   file_out=file_out)

            if self.found_definition is True and self.root_level_doc:
                self.print_root_level_info(depth, file_out)
            # End of print root-level definitions in file
            if tag in ('field', 'group') and depth != 0:
                self.handle_group_or_field(depth, node, file_out)
            if tag == ('enumeration'):
                self.handle_enumeration(depth, node, file_out)
            if tag == ('attribute'):
                self.handle_attributes(depth, node, file_out)
            if tag == ('dimensions'):
                self.handle_dimension(depth, node, file_out)
            if tag == ('link'):
                self.handel_link(depth, node, file_out)
            if tag == ('choice'):
                self.handel_choice(depth, node, file_out)
        depth += 1
        # Write nested nodes
        self.recursion_in_xml_tree(depth, xml_tree, output_yml, verbose)


def compare_niac_and_my(tree, tree2, verbose, node, root_no_duplicates):
    """This function creates two trees with Niac XML file and My XML file.
The main aim is to compare the two trees and create a new one that is the
union of the two initial trees.

"""
    root = tree.getroot()
    root2 = tree2.getroot()
    attrs_list_niac = []
    for nodo in root.iter(node):
        attrs_list_niac.append(nodo.attrib)
    if verbose:
        sys.stdout.write('Attributes found in Niac file: \n')
        sys.stdout.write(str(attrs_list_niac) + '\n')
        sys.stdout.write('  \n')
        sys.stdout.write('Started merging of Niac and My file... \n')
    for elem in root.iter(node):
        if verbose:
            sys.stdout.write('- Niac element inserted: \n')
            sys.stdout.write(str(elem.attrib) + '\n')
        index = get_node_parent_info(tree, elem)[1]
        root_no_duplicates.insert(index, elem)

    for elem2 in root2.iter(node):
        index = get_node_parent_info(tree2, elem2)[1]
        if elem2.attrib not in attrs_list_niac:
            if verbose:
                sys.stdout.write('- My element inserted: \n')
                sys.stdout.write(str(elem2.attrib) + '\n')
            root_no_duplicates.insert(index, elem2)

    if verbose:
        sys.stdout.write('     \n')
    return root_no_duplicates
