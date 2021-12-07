import numpy as np            # pylint: disable=unused-import
import typing                 # pylint: disable=unused-import
from nomad.metainfo import (  # pylint: disable=unused-import
    MSection, MCategory, Category, Package, Quantity, Section, SubSection, SectionProxy,
    Reference, MEnum)
#from nomad.metainfo.legacy import LegacyDefinition
#from nomad.datamodel.metainfo.nxobject import NXobject




m_package = Package(
    name='NEXUS',
    description='None')

class NXobject(MSection):
    pass

class NXtranslation(NXobject):
    pass

class NXorientation(NXobject):
    pass

class NXcsg(NXobject):
    pass

class NX_FLOAT(NXobject):
    pass

class NX_BINARY(NXobject):
    pass

class NX_BOOLEAN(NXobject):
    pass

class NX_CHAR(NXobject):
    pass

class NX_DATE_TIME(NXobject):
    pass

class NX_INT(NXobject):
    pass

class NX_NUMBER(NXobject):
    pass

class NX_POSINT(NXobject):
    pass

class NX_UINT(NXobject):
    pass



class NXcollection(NXobject):

    m_def = Section(
        validate=False,
        extends_base_section=True)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',
        default='base',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',
        default='NXcollection',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',
        default='group',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',
        default='NXobject',)

    nxp_ignoreExtraGroups = Quantity(
        type=str,
        shape=[],
        description='''

        ''',
        default='true',)

    nxp_ignoreExtraFields = Quantity(
        type=str,
        shape=[],
        description='''

        ''',
        default='true',)

    nxp_ignoreExtraAttributes = Quantity(
        type=str,
        shape=[],
        description='''

        ''',
        default='true',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                An unvalidated set of terms, such as the description of a beam line.
        Use :ref:`NXcollection` to gather together any set of terms.                 The
        original suggestion is to use this as a container                  class for the
        description of a beamline.                                  For NeXus validation,
        :ref:`NXcollection` will always generate                  a warning since it is
        always an optional group.                   Anything (groups, fields, or
        attributes) placed in                 an :ref:`NXcollection` group will not be
        validated.
        https://manual.nexusformat.org/classes/base_classes/NXcollection.html#nxcollection
        .
        ''',
        default='https://manual.nexusformat.org/classes/base_classes/NXcollection.html#nxcollection',)

    nxp_optional = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',
        default=True,)


class NXslit(NXobject):

    m_def = Section(
        validate=False,
        extends_base_section=True)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',
        default='base',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',
        default='NXslit',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',
        default='group',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',
        default='NXobject',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                A simple slit.                                  For more complex geometries,
        :ref:`NXaperture` should be used.
        https://manual.nexusformat.org/classes/base_classes/NXslit.html#nxslit .
        ''',
        default='https://manual.nexusformat.org/classes/base_classes/NXslit.html#nxslit',)

    nxp_optional = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',
        default=True,)

    class nxp_depends_on(NXobject):
        m_def = Section(validate=False,extends_base_section=True)
        nxp_base = SubSection(sub_section=NX_CHAR.m_def,repeats=True)
        nxp_name= Quantity(
            type=str,
            shape=[],
            description='''
        ''',
            default='depends_on',
        )
        nxp_type= Quantity(
            type=str,
            shape=[],
            description='''
        ''',
            default='NX_CHAR',
        )
        nxp_documentation= Quantity(
            type=str,
            shape=[],
            description='''
                        Points to the path of the last element in the geometry chain that places
                this object in space.                          When followed through that
                chain is supposed to end at an element depending
                on "." i.e. the origin of the coordinate system.
                If desired the location of the slit can also be described relative to
                an NXbeam, which will allow a simple description of a non-centred slit.
                https://manual.nexusformat.org/classes/base_classes/NXslit.html#nxslit-depends-on-field
                .''',
            default='https://manual.nexusformat.org/classes/base_classes/NXslit.html#nxslit-depends-on-field',
        )
        nxp_optional= Quantity(
            type=bool,
            shape=[],
            description='''
        ''',
            default=True,
        )
    nxp_depends_on = SubSection(sub_section=nxp_depends_on.m_def,repeats=True)


    class nxp_x_gap(NXobject):
        m_def = Section(validate=False,extends_base_section=True)
        nxp_base = SubSection(sub_section=NX_NUMBER.m_def,repeats=True)
        nxp_name= Quantity(
            type=str,
            shape=[],
            description='''
        ''',
            default='x_gap',
        )
        nxp_type= Quantity(
            type=str,
            shape=[],
            description='''
        ''',
            default='NX_NUMBER',
        )
        nxp_units= Quantity(
            type=str,
            shape=[],
            description='''
        ''',
            default='NX_LENGTH',
        )
        nxp_documentation= Quantity(
            type=str,
            shape=[],
            description='''
                        Size of the gap opening in the first dimension of the local
                coordinate system.
                https://manual.nexusformat.org/classes/base_classes/NXslit.html#nxslit-x-gap-field
                .''',
            default='https://manual.nexusformat.org/classes/base_classes/NXslit.html#nxslit-x-gap-field',
        )
        nxp_optional= Quantity(
            type=bool,
            shape=[],
            description='''
        ''',
            default=True,
        )
    nxp_x_gap = SubSection(sub_section=nxp_x_gap.m_def,repeats=True)


    class nxp_y_gap(NXobject):
        m_def = Section(validate=False,extends_base_section=True)
        nxp_base = SubSection(sub_section=NX_NUMBER.m_def,repeats=True)
        nxp_name= Quantity(
            type=str,
            shape=[],
            description='''
        ''',
            default='y_gap',
        )
        nxp_type= Quantity(
            type=str,
            shape=[],
            description='''
        ''',
            default='NX_NUMBER',
        )
        nxp_units= Quantity(
            type=str,
            shape=[],
            description='''
        ''',
            default='NX_LENGTH',
        )
        nxp_documentation= Quantity(
            type=str,
            shape=[],
            description='''
                        Size of the gap opening in the second dimension of the local
                coordinate system.
                https://manual.nexusformat.org/classes/base_classes/NXslit.html#nxslit-y-gap-field
                .''',
            default='https://manual.nexusformat.org/classes/base_classes/NXslit.html#nxslit-y-gap-field',
        )
        nxp_optional= Quantity(
            type=bool,
            shape=[],
            description='''
        ''',
            default=True,
        )
    nxp_y_gap = SubSection(sub_section=nxp_y_gap.m_def,repeats=True)


    class nxp_default(NXobject):
        m_def = Section(validate=False,extends_base_section=True)
        nxp_base = SubSection(sub_section=NX_CHAR.m_def,repeats=True)
        nxp_name= Quantity(
            type=str,
            shape=[],
            description='''
        ''',
            default='default',
        )
        nxp_documentation= Quantity(
            type=str,
            shape=[],
            description='''
                        .. index:: plotting                          Declares which child group
                contains a path leading              to a :ref:`NXdata` group.
                It is recommended (as of NIAC2014) to use this attribute             to
                help define the path to the default dataset to be plotted.             See
                https://www.nexusformat.org/2014_How_to_find_default_data.html
                for a summary of the discussion.
                https://manual.nexusformat.org/classes/base_classes/NXslit.html#nxslit-default-attribute
                .''',
            default='https://manual.nexusformat.org/classes/base_classes/NXslit.html#nxslit-default-attribute',
        )
        nxp_optional= Quantity(
            type=bool,
            shape=[],
            description='''
        ''',
            default=True,
        )
    nxp_default = SubSection(sub_section=nxp_default.m_def,repeats=True)


m_package.__init_metainfo__()
#None