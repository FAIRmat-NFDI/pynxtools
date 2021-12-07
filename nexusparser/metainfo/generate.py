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

'''
This module contains functionality to generate metainfo source-code from metainfo
definitions.
'''

from re import sub
import numpy as np

from nomad import utils
from nomad.metainfo import Definition, Package, Reference, MEnum

logger = utils.get_logger(__name__)


def generate_metainfo_code(metainfo_pkg: Package, python_package_path: str):
    '''
    Generates python code with metainfo definitions from the given :class:`Package`.

    Arguments:
        metainfo_pkg: The metainfo package.
        python_package_path:
            The file path for the python module file that should be generated.
    '''
    from jinja2 import Environment as JinjaEnvironment, PackageLoader, select_autoescape
    import textwrap

    def format_description(description, indent=0, width=90):
        paragraphs = [paragraph.strip() for paragraph in description.split('\n\n')]

        def format_paragraph(paragraph, first):
            lines = textwrap.wrap(text=paragraph, width=width - indent * 4, break_on_hyphens=False, break_long_words=False)
            lines = [line.replace('\\', '\\\\') for line in lines]
            return textwrap.indent(
                '\n'.join(lines), ' ' * 4 * indent, lambda x: not (first and x.startswith(lines[0])))

        return '\n\n'.join([
            format_paragraph(p, i == 0)
            for i, p in enumerate(paragraphs) if p != ''])

    def format_type(pkg, mi_type):
        if isinstance(mi_type, np.dtype):
            if mi_type == np.dtype('U'):
                return 'np.dtype(\'U\')'

            return 'np.dtype(np.%s)' % mi_type

        if mi_type in [int, float, str, bool]:
            return mi_type.__name__

        if isinstance(mi_type, Reference):
            if pkg == mi_type.target_section_def.m_parent:
                return "Reference(SectionProxy('%s'))" % mi_type.target_section_def.name

            else:
                python_module = mi_type.target_section_def.m_parent.a_legacy.python_module
                return '%s.%s' % (python_module.split('.')[-1], mi_type.target_section_def.name)

        if isinstance(mi_type, MEnum):
            return 'MEnum(%s)' % ', '.join(["'%s'" % item for item in mi_type])

        return str(mi_type)

    def format_unit(unit):
        return "'%s'" % unit

    def format_default(default):
        if isinstance(default,bool):
            return "%s" % str(default)
        return "'%s'" % str(default)

    def format_definition_refs(pkg, definitions):
        def format_definition_ref(definition: Definition):
            return definition.name
            if pkg == definition.m_parent:
                return definition.name
            else:
                python_module = definition.m_parent.a_legacy.python_module
                return '%s.%s' % (python_module.split('.')[-1], definition.name)

        return ', '.join([format_definition_ref(definition) for definition in definitions])

    def format_package_import(pkg):
        #python_module = pkg.a_legacy.python_module
        #modules = python_module.split('.')
        #return 'from %s import %s' % ('.'.join(modules[:-1]), modules[-1])
        return ''

    def format_aliases(pkg):
        result = ''
        for definition in pkg.category_definitions + pkg.section_definitions:
            for alias in definition.aliases:
                result += '%s = %s\n' % (alias, definition.name)

        if result != '':
            return '\n\n\n%s' % result

    def sub_section_path(sub_section, level):
        if level == 0:
            return sub_section.name
        return sub_section_path(sub_section.m_parent.nexus_parent, level -1) + '.' + sub_section.name


    def format_quantity(pkg, quantity, indent=0, level=0):
        result = ''
        indent_str = indent * 4 * ' '
        inner_indent_str = (indent + 1) * 4 * ' '
        inner2_indent_str = (indent + 2) * 4 * ' '
        result += inner_indent_str + quantity.name + '= Quantity(\n'
        result += inner2_indent_str + 'type=' + format_type(pkg, quantity.type) + ',\n'
        result += inner2_indent_str + 'shape=' + str(quantity.shape) + ',\n'
        if quantity.unit is not None:
            result += inner2_indent_str + 'unit=' + format_unit(quantity.unit) + ',\n'
        if quantity.description is not None:
            result += inner2_indent_str + 'description=' + "'''" + '\n' + format_description(quantity.description, indent=indent+3) + "\n"+ inner2_indent_str +"''',\n"
        if quantity.default is not None:
            result += inner2_indent_str + 'default=' + format_default(quantity.default) + ',\n'
        if len(quantity.categories) > 0:
            result += inner2_indent_str +'categories=[' + format_definition_refs(pkg, quantity.categories) + '],\n'
        # if quantity.a_search == 'defined':
        #     result += 'a_search=Search()+\n'
        result += inner_indent_str + ')\n'
        return result


    def format_section(pkg, section, indent=0, level=0):
        result = ''
        indent_str = indent * 4 * ' '
        inner_indent_str = (indent + 1) * 4 * ' '
        inner2_indent_str = (indent + 2) * 4 * ' '
        result += indent_str + "class "+section.name+"("+(format_definition_refs(pkg, section.base_sections) if section.extends_base_section else "MSection")+"):\n"
        if section.description is not None:
            result += inner_indent_str + "'''\n"
            result += format_description(section.description, indent=1)+"\n"
            result += inner_indent_str + "'''\n"
        else: 
            doc=section.all_quantities["nxp_documentation"]
            if doc is not None and doc.description is not None:
                result += inner_indent_str + "'''\n"
                result += format_description(doc.description, indent=2)+"\n"
                result += inner_indent_str + "'''\n"
        result += inner_indent_str + "m_def = Section(\n"
        #if section.aliases | length > 0 %}
        #    aliases=['{{ section.aliases[0] }}'],
        result += inner2_indent_str + "validate=False"
        if section.extends_base_section:
            result+=",\n"
            result += inner2_indent_str + "extends_base_section=True,\n"
        #add own nexus properties
        for quantity in section.quantities:
            if quantity.name.startswith("nxp_"):
                if quantity.name=="nxp_deprecated":
                    result += inner2_indent_str + "deprecated=''' DEPRECATED:\n"
                    result += inner2_indent_str + quantity.default +"\n"
                    result += inner2_indent_str + "''',\n"
                else:
                    if quantity.default is not None:
                        result += inner2_indent_str + quantity.name + "='" + str(quantity.default) + "',\n"
        result+=inner2_indent_str +")\n"
        #inherited case:
        #result += inner_indent_str + "nxp_base = SubSection(sub_section="+sub_section.sub_section.name+".m_def,repeats=True)\n"

        #real Quantities (not nexus properties)
        for quantity in section.quantities:
            if not quantity.name.startswith("nxp_"):
                result += format_quantity(pkg, quantity, indent, level)

        #SubSections (groups/fields/attributes)
        for sub_section in section.sub_sections:
            result += format_sub_section(pkg, sub_section, indent+1, level+1)

        return result


    def format_sub_section(pkg, sub_section, indent=0, level=0):
        result = ''
        indent_str = indent * 4 * ' '
        inner_indent_str = (indent + 1) * 4 * ' '
        inner2_indent_str = (indent + 2) * 4 * ' '
        #class
        result += indent_str + "class "+sub_section.name+"(NXobject):\n"  #"+sub_section.sub_section.name+"):\n"    #NXobject):\n"
        doc=sub_section.sub_section.all_quantities["nxp_documentation"] if "nxp_documentation" in sub_section.sub_section.all_quantities.keys() else None
        if doc is not None and doc.description is not None:
            result += inner_indent_str + "'''\n"
            result += format_description(doc.description, indent=indent+2)+"\n"
            result += inner_indent_str + "'''\n"
        #section definition
        result += inner_indent_str + "m_def = Section(validate=False,\n"
        result += inner2_indent_str +")\n"   #extends_base_section=True)\n"
        #inherited section
        result += inner_indent_str + "nxp_base = SubSection(sub_section="+sub_section.sub_section.name+".m_def,repeats=True)\n"
        #real (non nexus property /nxp_/) quantities
        for quantity in sub_section.sub_section.quantities:
            if not quantity.name.startswith("nxp_"):
                result += format_quantity(pkg, quantity, indent, level)
        #additional sub_sections (nexus groups/fields/attributes)
        for sub_sec in sub_section.sub_section.sub_sections:
            result += format_sub_section(pkg, sub_sec, indent=indent+1, level=level+1)
            pass
            #  if sub_section.sub_sections is not None:
            #     sub_section = sub_section.sub_sections
            #     format_sub_section(pkg, sub_section, indent=1)
        #the actual sub_section (either a group/field/attribute)
        result += indent_str + sub_section.name+' = '+'SubSection(sub_section='+sub_section.name+'.m_def,repeats=True,\n'
        #also add its own nexus properties
        for quantity in sub_section.sub_section.quantities:
            if quantity.name.startswith("nxp_"):
                if quantity.name=="nxp_enumeration":
                    if quantity.default is not None:
                        result += inner_indent_str + "enumeration="+quantity.default+",\n"
                elif quantity.name=="nxp_deprecated":
                    result += inner_indent_str + "deprecated=''' DEPRECATED:\n"
                    result += inner_indent_str + quantity.default +"\n"
                    result += inner_indent_str + "''',\n"
                else:
                    if quantity.default is not None:
                        result += inner_indent_str + quantity.name + "='" + str(quantity.default) + "',\n"
        result += inner_indent_str +")\n"   #extends_base_section=True)\n"

        return result

    def order_categories(categories):
        return sorted(categories, key=lambda c: len(c.categories))

    import sys
    sys.path.insert(0, '..')
    sys.path.insert(0, '../..')
    sys.path.insert(0, '.')
    env = JinjaEnvironment(
        loader=PackageLoader('metainfo', 'templates'),
        autoescape=select_autoescape(['python']))
    env.globals.update(
        order_categories=order_categories,
        format_description=format_description,
        format_type=format_type,
        format_unit=format_unit,
        format_definition_refs=format_definition_refs,
        format_package_import=format_package_import,
        format_aliases=format_aliases,
        format_default=format_default,
        format_section=format_section)
    with open(python_package_path, 'wt') as f:
        code = env.get_template('package.j2').render(pkg=metainfo_pkg)
        code = '\n'.join([
            line.rstrip() if line.strip() != '' else ''
            for line in code.split('\n')])
        f.write(code)


if __name__ == '__main__':
    # Simple use case that re-generates the common_dft package
    from nomad.datamodel.metainfo.common_dft import m_package

    generate_metainfo_code(m_package, 'nomad/datamodel/metainfo/common_dft.py')
