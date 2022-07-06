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

from setuptools import setup, find_packages
import os
import re


def parse_requirements():
    '''
    Parses the requirements.txt file to extras install and extra requirements.
    Sections headed with # [extra] are assigned to the 'extra' extra.

    Returns:
        Tuple with install and extra requires passible to :func:`setuptools.setup`.
    '''
    with open('requirements.txt', 'rt') as f:
        lines = f.readlines()

    extras_require = {}
    requires = []
    all_requires = []
    current = None
    for line in lines:
        line = line.strip()

        if line == '':
            continue

        match = re.match(r'^#\s*\[([a-zA-Z0-9_]+)\]$', line)
        if match:
            extra = match.group(1)
            current = list()
            extras_require[extra] = current
        elif line.startswith('#'):
            continue
        else:
            line = line.split('#')[0].strip()
            if current is None:
                requires.append(line)
            else:
                current.append(line)
                all_requires.append(line)

    extras_require['all'] = all_requires

    return requires, extras_require

def main():
    try:
        for nexus_definition_dir in ("/./", "/base_classes/", "/applications/", "/contributed_definitions/"):
            f = open(os.path.abspath(os.path.dirname(__file__)) + "/nexusparser/definitions/" + nexus_definition_dir + "__init__.py", "a")
            f.close()
    except FileNotFoundError:
        pass

    with open("README.md", "r") as f:
        long_description = f.read()

    requires, extras_require = parse_requirements()

    setup(
        name='nexusparser',
        version='0.0.1',
        description='NOMAD parser implementation for Nexus.',
        long_description=long_description,
        long_description_content_type="text/markdown",
        author='The NOMAD Authors',
        license='APACHE 2.0',
        packages=find_packages(exclude=['tests']),
        package_data={
            'nexusparser.definitions.base_classes': ['*.xml'],
            'nexusparser.definitions.applications': ['*.xml'],
            'nexusparser.definitions.contributed_definitions': ['*.xml'],
            'nexusparser.definitions': ['*.xsd']
        },
        include_package_data=True,
        install_requires=requires,
        extras_require=extras_require,
        entry_points={
            'console_scripts': [
                'read_nexus = nexusparser.tools.nexus:main',
                'dataconverter = nexusparser.tools.dataconverter.convert:convert_cli',
                'yaml2nxdl = nexusparser.tools.yaml2nxdl.yaml2nxdl:launch_tool'
            ]
        })


if __name__ == '__main__':
    main()
