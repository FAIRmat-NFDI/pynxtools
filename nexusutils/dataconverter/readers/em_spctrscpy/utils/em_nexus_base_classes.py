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
"""General metadata object connecting units and values for a quantity."""

# pylint: disable=E1101

from typing import Dict

from nexusutils.dataconverter.readers.em_spctrscpy.utils.em_versioning \
    import NX_EM_ADEF_NAME, NX_EM_ADEF_VERSION, \
    NX_EM_EXEC_NAME, NX_EM_EXEC_VERSION


class NxObject:  # pylint: disable=R0903
    """An object in a graph e.g. a field or group in NeXus."""

    def __init__(self,
                 name: str = None,
                 unit: str = None,
                 dtype=str,
                 value=None,
                 **kwargs):
        if name is not None:
            assert name != "", "Argument name needs to be a non-empty string !"
        if unit is not None:
            assert unit != "", "Argument unit needs to be a non-empty string !"
        assert dtype is not None, "Argument dtype must not be None !"
        if dtype is not None:
            assert isinstance(dtype, type), \
                "Argument dtype needs a valid, ideally numpy, datatype !"
        # ##MK::if value is not None:
        self.is_a = "NXobject"
        self.is_attr = False  # if True indicates object is attribute
        self.doc = ""  # docstring
        self.name = name  # name of the field
        self.unit = unit  # not unit category but actual unit
        # use special values "unitless" for NX_UNITLESS (e.g. 1) and
        # "dimensionless" for NX_DIMENSIONLESS (e.g. 1m / 1m)
        self.dtype = dtype  # use np.dtype if possible
        if value is None or dtype is str:
            self.unit = "unitless"
        if value is not None:
            self.value = value
        else:
            self.value = None
        # value should be a numpy scalar, tensor, or string if possible
        if "is_attr" in kwargs:
            assert isinstance(kwargs["is_attr"], bool), \
                "Kwarg is_attr needs to be a boolean !"
            self.is_attr = kwargs["is_attr"]

    def __repr__(self):
        """Report values."""
        return f'''Name: {self.name}, unit: {self.unit}, dtype: {self.dtype}'''


class NxEmUser:  # pylint: disable=R0903
    """An object representing a user, typically a human."""

    def __init__(self):
        self.meta: Dict[str, NxObject] = {}
        self.meta["name"] = NxObject()
        self.meta["affiliation"] = NxObject()
        self.meta["address"] = NxObject()
        self.meta["email"] = NxObject()
        self.meta["orcid"] = NxObject()
        self.meta["telephone_number"] = NxObject()
        self.meta["role"] = NxObject()
        self.meta["social_media_name"] = NxObject()
        self.meta["social_media_platform"] = NxObject()

    def report(self, prefix: str, template: dict) -> dict:
        """Copy data from self into template the appdef instance.

        Paths in template are prefixed by prefix and have to be compliant
        with the application definition.
        """
        template[prefix + "/address"] = self.meta["address"].value
        template[prefix + "/affiliation"] = self.meta["affiliation"].value
        template[prefix + "/email"] = self.meta["email"].value
        template[prefix + "/name"] = self.meta["name"].value
        template[prefix + "/orcid"] = self.meta["orcid"].value
        template[prefix + "/role"] = self.meta["role"].value
        template[prefix + "/social_media_name"] \
            = self.meta["social_media_name"].value
        template[prefix + "/social_media_platform"] \
            = self.meta["social_media_platform"].value
        template[prefix + "/telephone_number"] \
            = self.meta["telephone_number"].value
        return template


class NxEmSample:  # pylint: disable=R0903
    """An object representing a sample."""

    def __init__(self):
        self.meta: Dict[str, NxObject] = {}
        self.meta["method"] = NxObject(value="experimental")
        self.meta["name"] = NxObject()
        self.meta["sample_history"] = NxObject()
        self.meta["preparation_date"] = NxObject()
        self.meta["short_title"] = NxObject()
        self.meta["atom_types"] = NxObject(value=[])
        self.meta["thickness"] = NxObject()
        self.meta["description"] = NxObject()

    def report(self, prefix: str, template: dict) -> dict:
        """Copy data from self into template the appdef instance.

        Paths in template are prefixed by prefix and have to be compliant
        with the application definition.
        """
        template[prefix + "/method"] = self.meta["method"].value
        template[prefix + "/name"] = self.meta["name"].value
        template[prefix + "/sample_history"] = self.meta["sample_history"].value
        template[prefix + "/preparation_date"] = self.meta["preparation_date"].value
        template[prefix + "/short_title"] = self.meta["short_title"].value
        template[prefix + "/atom_types"] = self.meta["atom_types"].value
        template[prefix + "/thickness"] = self.meta["thickness"].value
        template[prefix + "/thickness/@units"] = self.meta["thickness"].unit
        template[prefix + "/description"] = self.meta["description"].value
        return template


class NxEmAppDefHeader:  # pylint: disable=R0903
    """An object representing the typical header of nexus-fairmat appdefs."""

    def __init__(self):
        self.meta: Dict[str, NxObject] = {}
        self.meta["version"] \
            = NxObject(value=NX_EM_ADEF_VERSION, is_attr=True)
        self.meta["definition"] \
            = NxObject(value=NX_EM_ADEF_NAME)
        self.meta["experiment_identifier"] = NxObject()
        self.meta["experiment_description"] = NxObject()
        self.meta["start_time"] = NxObject()
        self.meta["end_time"] = NxObject()
        self.meta["program"] = NxObject(value=NX_EM_EXEC_NAME)
        self.meta["program_version"] \
            = NxObject(value=NX_EM_EXEC_VERSION, is_attr=True)
        self.meta["experiment_documentation"] = NxObject()
        self.meta["thumbnail"] = NxObject()
        self.meta["thumbnail_type"] = NxObject()

    def report(self, prefix: str, template: dict) -> dict:
        """Copy data from self into template the appdef instance.

        Paths in template are prefixed by prefix and have to be compliant
        with the application definition.
        """
        template[prefix + "/@version"] = self.meta["version"].value
        template[prefix + "/definition"] = self.meta["definition"].value
        template[prefix + "/experiment_identifier"] \
            = self.meta["experiment_identifier"].value
        template[prefix + "/experiment_description"] \
            = self.meta["experiment_description"].value
        template[prefix + "/start_time"] = self.meta["start_time"].value
        template[prefix + "/end_time"] = self.meta["end_time"].value
        template[prefix + "/program"] = self.meta["program"].value
        template[prefix + "/program/@version"] \
            = self.meta["program_version"].value
        template[prefix + "/experiment_documentation"] \
            = self.meta["experiment_documentation"].value
        template[prefix + "/thumbnail"] \
            = self.meta["thumbnail"].value
        template[prefix + "/thumbnail/@type"] \
            = self.meta["thumbnail_type"].value
        return template
