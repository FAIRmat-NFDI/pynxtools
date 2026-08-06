# SPDX-FileCopyrightText: NeXus International Advisory Committee (NIAC)
# SPDX-FileCopyrightText: The pynxtools Authors
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# This file is generated from the NeXus definition NXtest (see
# https://github.com/nexusformat/definitions). It preserves that
# definition's structure and content as NOMAD Metainfo
# (Quantity/SubSection) objects. Accordingly, it is distributed under
# LGPL-3.0-or-later, matching the license of the upstream NXDL
# definitions, unlike the rest of this package (Apache-2.0).
# During generation, pynxtools may add project-specific content (extra quantities,
# annotations, normalize() logic, ...). See
# docs/learn/pynxtools/licensing.md and
# LICENSES/LGPL-3.0-or-later.txt.
#
# This file is AUTO-GENERATED from the NeXus definitions (NXDL).
# Run `pynx nomad generate-metainfo --nxdl NXtest` to regenerate.
# Additive-only: the generator will not remove or rename existing class members
# (unless the `--force` flag is used).
# Add normalize() logic directly; it will be preserved on regeneration.
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from nomad.datamodel.metainfo.annotations import (
    ELNAnnotation,
    ELNComponentEnum,
    SchemaAnnotation,
)
from nomad.metainfo import MEnum, Quantity, Section, SubSection
from nomad.metainfo.data_type import Bytes, Datetime

from pynxtools.nomad.annotations import (
    NeXusAttribute,
    NeXusChoice,
    NeXusDefinition,
    NeXusField,
    NeXusGroup,
    NeXusLink,
)
from pynxtools.nomad.metainfo._category import ExperimentCategory
from pynxtools.nomad.metainfo.base_classes.calibration import Calibration
from pynxtools.nomad.metainfo.base_classes.data import Data
from pynxtools.nomad.metainfo.base_classes.entry import Entry
from pynxtools.nomad.metainfo.base_classes.note import Note
from pynxtools.nomad.metainfo.base_classes.user import User

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

__all__ = ["Test"]


class Test(Entry):
    """
    This is a dummy NXDL to test out the dataconverter.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest"
        ],
        categories=[ExperimentCategory],
        a_nexus_definition=NeXusDefinition(
            nx_class="NXtest",
            category="application",
            symbols={"n": "number of data points shared across symbol_group fields"},
        ),
    )

    OPTIONAL_group = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.test.TestOPTIONAL_group",
        repeats=True,
        variable=True,
    )
    specified_group_with_no_name_type = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.test.TestSpecifiedGroupWithNoNameType",
        repeats=False,
    )
    specified_group = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.test.TestSpecifiedGroup",
        repeats=False,
    )
    any_groupgroup = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.test.TestAnyGroupgroup",
        repeats=True,
        variable=True,
    )
    NXODD_name = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.test.TestNXODD_name",
        repeats=True,
        variable=True,
    )
    required_group = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=False,
        description=("This is a required yet empty group."),
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="required_group",
            name_type="specified",
            optionality="required",
        ),
    )
    required_group2 = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.note.Note",
        repeats=False,
        description=("This is a second required yet empty group."),
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="required_group2",
            name_type="specified",
            optionality="required",
        ),
    )
    optional_parent = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.test.TestOptionalParent",
        repeats=False,
    )
    user = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.test.TestUser",
        repeats=True,
        variable=True,
    )
    identified_calibration = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.test.TestIdentifiedCalibration",
        repeats=False,
    )
    named_collection = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.collection.Collection",
        repeats=False,
        a_nexus_group=NeXusGroup(
            nx_class="NXcollection",
            name="named_collection",
            name_type="specified",
            optionality="optional",
        ),
    )
    symbol_group = SubSection(
        section_def="pynxtools.nomad.metainfo.applications.test.TestSymbolGroup",
        repeats=False,
    )

    program_name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-program-name-field"
        ],
        a_nexus_field=NeXusField(
            name="program_name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    definition = Quantity(
        type=MEnum(["NXTEST", "NXtest"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-definition-field"
        ],
        description=("This is a dummy NXDL to test out the dataconverter."),
        a_nexus_field=NeXusField(
            name="definition",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["NXTEST", "NXtest"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    definition__version = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-definition-version-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="version",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="definition",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    my_link = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-my-link-link"
        ],
        a_nexus_link=NeXusLink(
            name="my_link",
            target="NXentry/NXdata/specified_group_with_no_name_type",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


# =============================================================================
# Named NeXus concept groups — only when the group element defines own
# quantities that differ from the generic class (changed optionality, extra
# fields, different type/units/enumeration). These inherit from the specific
# generic class so all # base quantities are available.
# Resolved lazily by NOMAD at __init_metainfo__() time via string FQNs.
# =============================================================================


class TestOPTIONAL_group(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-optional-group-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="OPTIONAL_group",
            name_type="partial",
            optionality="optional",
        ),
    )

    required_field = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-optional-group-required-field-field"
        ],
        description=(
            "A dummy entry to test optional parent check for a required child."
        ),
        a_nexus_field=NeXusField(
            name="required_field",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    required_field_set = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-optional-group-required-field-set-field"
        ],
        description=("A dummy entry to test reserved suffixes."),
        a_nexus_field=NeXusField(
            name="required_field_set",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    some_field_set = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-optional-group-some-field-set-field"
        ],
        description=(
            "A dummy entry to test reserved suffixes where the actual field is "
            "not given. Note that this is not allowed by NeXus, but we do this "
            "here to test the validation."
        ),
        a_nexus_field=NeXusField(
            name="some_field_set",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    optional_field = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-optional-group-optional-field-field"
        ],
        description=(
            "A dummy entry to test optional parent check for an optional child."
        ),
        a_nexus_field=NeXusField(
            name="optional_field",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TestSpecifiedGroupWithNoNameType(Data):
    """
    A group with a (specified) name, but nameType not given explicitly.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-specified-group-with-no-name-type-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="specified_group_with_no_name_type",
            name_type="specified",
            optionality="required",
        ),
    )

    specified_field_with_no_name_type = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-specified-group-with-no-name-type-specified-field-with-no-name-type-field"
        ],
        flexible_unit=True,
        a_nexus_field=NeXusField(
            name="specified_field_with_no_name_type",
            type="NX_FLOAT",
            name_type="specified",
            optionality="required",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    specified_field_with_no_name_type__specified_attr_in_field_with_no_name_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-specified-group-with-no-name-type-specified-field-with-no-name-type-specified-attr-in-field-with-no-name-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="specified_attr_in_field_with_no_name_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="specified_field_with_no_name_type",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    specified_attr_with_no_name_type = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-specified-group-with-no-name-type-specified-attr-with-no-name-type-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="specified_attr_with_no_name_type",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TestSpecifiedGroup(Data):
    """
    A group with a name and nameType="specified".
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-specified-group-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="specified_group",
            name_type="specified",
            optionality="required",
        ),
    )

    specified_field = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-specified-group-specified-field-field"
        ],
        flexible_unit=True,
        a_nexus_field=NeXusField(
            name="specified_field",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ANY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    specified_field__specified_attr_in_field = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-specified-group-specified-field-specified-attr-in-field-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="specified_attr_in_field",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            parent_field="specified_field",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    specified_attr = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-specified-group-specified-attr-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="specified_attr",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TestAnyGroupgroup(Data):
    """
    A group with a name and nameType="any".
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-any-groupgroup-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="any_groupGROUP",
            name_type="any",
            optionality="required",
        ),
    )

    any_fieldFIELD = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-any-groupgroup-any-fieldfield-field"
        ],
        variable=True,
        flexible_unit=True,
        a_nexus_field=NeXusField(
            name="any_fieldFIELD",
            type="NX_FLOAT",
            name_type="any",
            optionality="required",
            units="NX_ANY",
        ),
    )
    any_fieldFIELD__any_attrATTR_in_field = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-any-groupgroup-any-fieldfield-any-attrattr-in-field-attribute"
        ],
        variable=True,
        a_nexus_attribute=NeXusAttribute(
            name="any_attrATTR_in_field",
            type="NX_CHAR",
            name_type="any",
            optionality="required",
            parent_field="any_fieldFIELD",
        ),
    )
    any_attrATTR = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-any-groupgroup-any-attrattr-attribute"
        ],
        variable=True,
        a_nexus_attribute=NeXusAttribute(
            name="any_attrATTR",
            type="NX_CHAR",
            name_type="any",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TestNXODD_name(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-nxodd-name-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="NXODD_name",
            name_type="partial",
            optionality="required",
        ),
    )

    anamethatRENAMES = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-nxodd-name-anamethatrenames-field"
        ],
        variable=True,
        dimensionality="dimensionless",
        unit="dimensionless",
        a_nexus_field=NeXusField(
            name="anamethatRENAMES",
            type="NX_INT",
            name_type="partial",
            optionality="required",
            units="NX_UNITLESS",
        ),
    )
    float_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-nxodd-name-float-value-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="eV",
        description=("A dummy entry for a float value."),
        a_nexus_field=NeXusField(
            name="float_value",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "eV"},
    )
    number_value = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-nxodd-name-number-value-field"
        ],
        dimensionality="[mass] * [length] ** 2 / [time] ** 2",
        unit="eV",
        description=("A dummy entry for a number value."),
        a_nexus_field=NeXusField(
            name="number_value",
            type="NX_NUMBER",
            name_type="specified",
            optionality="optional",
            units="NX_ENERGY",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "eV"},
    )
    bool_value = Quantity(
        type=bool,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-nxodd-name-bool-value-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("A dummy entry for a bool value."),
        a_nexus_field=NeXusField(
            name="bool_value",
            type="NX_BOOLEAN",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    int_value = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-nxodd-name-int-value-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("A dummy entry for an int value."),
        a_nexus_field=NeXusField(
            name="int_value",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    posint_value = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-nxodd-name-posint-value-field"
        ],
        dimensionality="[length]",
        unit="m",
        description=("A dummy entry for a positive int value."),
        a_nexus_field=NeXusField(
            name="posint_value",
            type="NX_POSINT",
            name_type="specified",
            optionality="required",
            units="NX_LENGTH",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        a_display={"unit": "m"},
    )
    char_value = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-nxodd-name-char-value-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("A dummy entry for a char value."),
        a_nexus_field=NeXusField(
            name="char_value",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    date_value = Quantity(
        type=Datetime,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-nxodd-name-date-value-field"
        ],
        dimensionality="dimensionless",
        unit="dimensionless",
        description=("A dummy entry for a date value."),
        a_nexus_field=NeXusField(
            name="date_value",
            type="NX_DATE_TIME",
            name_type="specified",
            optionality="required",
            units="NX_UNITLESS",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateTimeEditQuantity,
        ),
    )
    type = Quantity(
        type=MEnum(["1st type", "2nd type", "3rd type", "4th type"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-nxodd-name-type-field"
        ],
        a_nexus_field=NeXusField(
            name="type",
            type="NX_CHAR_OR_NUMBER",
            name_type="specified",
            optionality="required",
            enumeration=["1st type", "2nd type", "3rd type", "4th type"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
    )
    type__array = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-nxodd-name-type-array-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="array",
            type="NX_INT",
            name_type="specified",
            optionality="required",
            parent_field="type",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    type2 = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-nxodd-name-type2-field"
        ],
        a_nexus_field=NeXusField(
            name="type2",
            type="NX_CHAR_OR_NUMBER",
            name_type="specified",
            optionality="optional",
            enumeration=["1st type open", "2nd type open"],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    type2__attribute_with_open_enum = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-nxodd-name-type2-attribute-with-open-enum-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="attribute_with_open_enum",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
            parent_field="type2",
            enumeration=["1st option", "2nd option"],
            open_enum=True,
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    group_attribute = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-nxodd-name-group-attribute-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="group_attribute",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    signal = Quantity(
        type=MEnum(["data"]),
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-nxodd-name-signal-attribute"
        ],
        a_nexus_attribute=NeXusAttribute(
            name="signal",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
            enumeration=["data"],
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            default="data",
        ),
    )
    AXISNAME_indices = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-nxodd-name-axisname-indices-attribute"
        ],
        variable=True,
        description=("A dummy entry to test required variadic attribute resolution."),
        a_nexus_attribute=NeXusAttribute(
            name="AXISNAME_indices",
            type="NX_UINT",
            name_type="partial",
            optionality="required",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TestOptionalParent(Data):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-optional-parent-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="optional_parent",
            name_type="specified",
            optionality="optional",
        ),
    )

    req_group_in_opt_group = SubSection(
        section_def="pynxtools.nomad.metainfo.base_classes.data.Data",
        repeats=False,
        description=("This is a required group in an optional group."),
        a_nexus_group=NeXusGroup(
            nx_class="NXdata",
            name="req_group_in_opt_group",
            name_type="specified",
            optionality="required",
        ),
    )

    required_child = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-optional-parent-required-child-field"
        ],
        description=("A dummy entry to test optional parent check for required child."),
        a_nexus_field=NeXusField(
            name="required_child",
            type="NX_INT",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )
    optional_child = Quantity(
        type=np.int64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-optional-parent-optional-child-field"
        ],
        description=("A dummy entry to test optional parent check for required child."),
        a_nexus_field=NeXusField(
            name="optional_child",
            type="NX_INT",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TestUser(User):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-user-group"
        ],
        variable=True,
        a_nexus_group=NeXusGroup(
            nx_class="NXuser",
            name=None,
            name_type="any",
            optionality="optional",
        ),
    )

    name = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-user-name-field"
        ],
        description=("A required NXuser entry."),
        a_nexus_field=NeXusField(
            name="name",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TestIdentifiedCalibration(Calibration):
    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-identified-calibration-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXcalibration",
            name="identified_calibration",
            name_type="specified",
            optionality="optional",
        ),
    )

    identifier_1 = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-identified-calibration-identifier-1-field"
        ],
        a_nexus_field=NeXusField(
            name="identifier_1",
            type="NX_CHAR",
            name_type="specified",
            optionality="required",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    identifier_2 = Quantity(
        type=str,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-identified-calibration-identifier-2-field"
        ],
        a_nexus_field=NeXusField(
            name="identifier_2",
            type="NX_CHAR",
            name_type="specified",
            optionality="optional",
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)


class TestSymbolGroup(Note):
    """
    Group used to test cross-field NXDL symbol-size consistency.
    """

    m_def = Section(
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-symbol-group-group"
        ],
        a_nexus_group=NeXusGroup(
            nx_class="NXnote",
            name="symbol_group",
            name_type="specified",
            optionality="optional",
        ),
    )

    field_a = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-symbol-group-field-a-field"
        ],
        shape=["*"],
        description=("First field sharing symbol n."),
        a_nexus_field=NeXusField(
            name="field_a",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )
    field_b = Quantity(
        type=np.float64,
        links=[
            "https://fairmat-nfdi.github.io/nexus_definitions/classes/src/pynxtools/data/NXtest.html#nxtest-entry-symbol-group-field-b-field"
        ],
        shape=["*"],
        description=("Second field sharing symbol n."),
        a_nexus_field=NeXusField(
            name="field_b",
            type="NX_FLOAT",
            name_type="specified",
            optionality="optional",
        ),
    )

    def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:
        super().normalize(archive, logger)
