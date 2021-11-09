import numpy as np            # pylint: disable=unused-import
import typing                 # pylint: disable=unused-import
from nomad.metainfo import (  # pylint: disable=unused-import
    MSection, MCategory, Category, Package, Quantity, Section, SubSection, SectionProxy,
    Reference, MEnum)
from nomad.metainfo.legacy import LegacyDefinition


m_package = Package(
    name='NEXUS',
    description='None')


class NXarpes(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                This is an application definition for angular resolved photo electron
        spectroscopy.          It has been drawn up with hemispherical electron analysers
        in mind.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    ENTRY = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXcanSAS(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                Implementation of the canSAS standard to store reduced small-angle scattering data
        of any dimension.                  .. index:: canSAS                  For more
        details, see:                  * http://www.cansas.org/         *
        http://www.cansas.org/formats/canSAS1d/1.1/doc/         * http://cansas-
        org.github.io/canSAS2012/         * https://github.com/canSAS-
        org/NXcanSAS_examples                  The minimum requirements for *reduced*
        small-angle scattering data          as described by canSAS are summarized in the
        following figure:                  .. _canSAS_2012_minimum:                  ..
        figure:: canSAS/2012-minimum.png            :width: 60%                        The
        minimum requirements for *reduced* small-angle scattering data.
        (:download:`full image <canSAS/2012-minimum.png>`)            See :ref:`below
        <NXcanSAS_minimum>` for the minimum required             information for a NeXus
        data file            written to the NXcanSAS specification.                  ..
        rubric::  Implementation of canSAS standard in NeXus                  This
        application definition is an implementation of the canSAS         standard for
        storing both one-dimensional and multi-dimensional          *reduced* small-angle
        scattering data.

        * NXcanSAS is for reduced SAS data and metadata to be stored together in one file.
        * *Reduced* SAS data consists of :math:`I(\\vec{Q})` or :math:`I(|\\vec{Q}|)`
        * External file links are not to be used for the reduced data.          * A good
        practice/practise is, at least, to include a reference to how the data was
        acquired and processed.  Yet this is not a requirement.         * There is no need
        for NXcanSAS to refer to any raw data.

        The canSAS data format has a structure similar to NeXus, not identical.         To
        allow canSAS data to be expressed in NeXus, yet identifiable         by the canSAS
        standard, an additional group attribute ``canSAS_class``         was introduced.
        Here is the mapping of some common groups.                  ===============
        ============  ==========================         group (*)        NX_class
        canSAS_class         ===============  ============  ==========================
        sasentry         NXentry       SASentry         sasdata          NXdata
        SASdata         sasdetector      NXdetector    SASdetector         sasinstrument
        NXinstrument  SASinstrument         sasnote          NXnote        SASnote
        sasprocess       NXprocess     SASprocess         sasprocessnote   NXcollection
        SASprocessnote         sastransmission  NXdata        SAStransmission_spectrum
        sassample        NXsample      SASsample         sassource        NXsource
        SASsource         ===============  ============  ==========================
        (*) The name of each group is a suggestion,         not a fixed requirement and is
        chosen as fits each data file.           See the section on defining
        :ref:`NXDL group and field names <RegExpName>`.                  Refer to the
        NeXus Coordinate System drawing (:ref:`Design-CoordinateSystem`)         for
        choice and direction of :math:`x`, :math:`y`, and :math:`z` axes.
        .. _NXcanSAS_minimum:                  .. rubric:: The minimum required
        information for a NeXus data file            written to the NXcanSAS
        specification.                  .. literalinclude:: canSAS/minimum-required.txt
        :tab-width: 4            :linenos:            :language: text
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    ENTRY = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXtomo(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                This is the application definition for x-ray or neutron tomography raw data.
        In tomography            a number of dark field images are measured, some bright
        field images and, of course the sample.            In order to distinguish between
        them images carry a image_key.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    entry = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXsas(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                raw, monochromatic 2-D SAS data with an area detector

        This is an application definition for raw data (not processed or reduced data)
        from a 2-D small angle scattering instrument collected with a monochromatic
        beam and an area detector. It is meant to be suitable both for neutron SANS
        and X-ray SAXS data.           It covers all raw data from any monochromatic SAS
        techniques that     use an area detector: SAS, WSAS, grazing incidence, GISAS

        It covers all raw data from any SAS techniques     that use an area detector
        and a monochromatic beam.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    ENTRY = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXxkappa(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                raw data from a kappa geometry (CAD4) single crystal diffractometer, extends
        :ref:`NXxbase`          This is the application definition for raw data from a
        kappa geometry      (CAD4) single crystal     diffractometer. It extends
        :ref:`NXxbase`, so the full definition is      the content of :ref:`NXxbase` plus
        the     data defined here.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    entry = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXxbase(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                This definition covers the common parts of all monochromatic single crystal raw
        data application definitions.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    entry = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXmx(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                functional application definition for macromolecular crystallography
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    ENTRY = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXtofraw(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        This is an application definition for raw data from a generic TOF instrument
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    entry = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXsqom(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                This is the application definition for S(Q,OM) processed data.           As this
        kind of data is in     general not on a rectangular grid after data reduction, it
        is stored as Q,E positions plus their     intensity, table like. It is the task of
        a possible visualisation program to regrid this data in     a sensible way.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    ENTRY = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXxlaueplate(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                raw data from a single crystal Laue camera, extends :ref:`NXxlaue`          This
        is the application definition for raw data from a single crystal Laue      camera
        with an image plate as a detector. It extends :ref:`NXxlaue`.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    entry = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXtomophase(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                This is the application definition for x-ray or neutron tomography raw data with
        phase contrast variation at each point.               In tomography first
        some dark field images are measured, some bright field images and, of course the
        sample. In order        to properly sort the order of the images taken, a sequence
        number is stored with each image.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    entry = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXiqproc(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        Application definition for any :math:`I(Q)` data.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    ENTRY = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXspe(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        NXSPE Inelastic Format.  Application definition for NXSPE file format.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    ENTRY = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXxas(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                This is an application definition for raw data from an X-ray absorption
        spectroscopy experiment.               This is essentially a scan on energy versus
        incoming/        absorbed beam.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    ENTRY = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXxasproc(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                Processed data from XAS. This is energy versus I(incoming)/I(absorbed).
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    ENTRY = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXxeuler(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                raw data from a :index:`four-circle diffractometer` with an :index:`eulerian
        cradle`, extends :ref:`NXxbase`              It extends :ref:`NXxbase`, so the
        full definition is the content        of :ref:`NXxbase` plus the data defined
        here. All four angles are        logged in order to support arbitrary scans in
        reciprocal space.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    entry = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXlauetof(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                This is the application definition for a TOF laue diffractometer
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    entry = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXxnb(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                raw data from a single crystal diffractometer, extends :ref:`NXxbase`
        This is the application definition for raw data from      a single crystal
        diffractometer     measuring in normal beam mode. It extends :ref:`NXxbase`,
        so the full definition is the content of     :ref:`NXxbase` plus the data defined
        here. All angles are      logged in order to support arbitrary scans in
        reciprocal space.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    entry = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXtas(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                This is an application definition for a triple axis spectrometer.           It is
        for the trademark scan of the TAS, the Q-E scan.      For your alignment scans use
        the rules in :ref:`NXscan`.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    entry = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXarchive(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                This is a definition for data to be archived by ICAT
        (http://www.icatproject.org/).                  .. text from the icatproject.org
        site                          the database (with supporting software) that
        provides an                  interface to all ISIS experimental data and will
        provide                  a mechanism to link all aspects of ISIS research from
        proposal through to publication.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    entry = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXmonopd(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                Monochromatic Neutron and X-Ray Powder diffractometer                   Instrument
        definition for a powder diffractometer at a monochromatic neutron          or
        X-ray beam. This is both suited for a powder diffractometer          with a single
        detector or a powder diffractometer with a position          sensitive detector.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    entry = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXrefscan(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                This is an application definition for a monochromatic scanning reflectometer.

        It does not have the information to calculate the resolution     since it does not
        have any apertures.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    entry = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXtomoproc(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        This is an application definition for the final result of a tomography experiment:
        a 3D construction of some volume of physical properties.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    entry = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXdirecttof(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        This is a application definition for raw data from a direct geometry TOF
        spectrometer
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    entry = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXtofnpd(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        This is a application definition for raw data from a TOF neutron powder
        diffractometer
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    entry = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXfluo(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                This is an application definition for raw data from an X-ray fluorescence
        experiment
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    entry = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXxrot(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                raw data from a rotation camera, extends :ref:`NXxbase`           This is the
        application definition for raw data from a rotation camera.     It extends
        :ref:`NXxbase`, so the full definition is the content of :ref:`NXxbase`     plus
        the data defined here.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    entry = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXsastof(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                raw, 2-D SAS data with an area detector with a time-of-flight source          It
        covers all raw data from any SAS techniques     that use an area detector     at a
        time-of-flight source.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    ENTRY = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXscan(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                Application definition for a generic scan instrument.           This definition is
        more an      example then a stringent definition as the content of a given NeXus
        scan file needs to      differ for different types of scans. This example
        definition shows a scan like done      on a rotation camera: the sample is rotated
        and a detector image, the rotation angle     and a monitor value is stored at each
        step in the scan. In the following, the symbol      ``NP`` is used to represent
        the number of scan points. These are the rules for      storing scan data in NeXus
        files which are implemented in this example:          * Each value varied
        throughout a scan is stored as an array of        length ``NP`` at its respective
        location within the NeXus hierarchy.     * For area detectors, ``NP`` is the first
        dimension,        example for a detector of 256x256:  ``data[NP,256,256]``     *
        The NXdata group contains links to all variables varied in the scan and the data.
        This to give an equivalent to the more familiar classical tabular representation
        of scans.           These rules exist for a reason: HDF allows the first dimension
        of a data set to be      unlimited. This means the data can be appended too. Thus
        a NeXus file built according      to the rules given above can be used in the
        following way:          * At the start of a scan, write all the static
        information.     * At each scan point, append new data from varied variables
        and the detector to the file.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    ENTRY = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXreftof(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        This is an application definition for raw data from a TOF reflectometer.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    entry = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXxlaue(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                raw data from a single crystal laue camera, extends :ref:`NXxrot`          This is
        the application definition for raw data from a single crystal laue      camera. It
        extends :ref:`NXxrot`.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    entry = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXindirecttof(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        This is a application definition for raw data from a direct geometry TOF
        spectrometer
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    entry = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXstxm(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                Application definition for a STXM instrument.                       The
        interferometer           position measurements, monochromator photon energy values
        and           detector measurements are all treated as NXdetectors and stored
        within the NXinstrument group as lists of values stored in
        chronological order. The NXdata group then holds another version           of the
        data in a regular 3D array (NumE by NumY by NumX, for a           total of nP
        points in a sample image stack type scan). The former           data values should
        be stored with a minimum loss of precision, while           the latter values can
        be simplified and/or approximated in order to           fit the constraints of a
        regular 3D array. 'Line scans' and 'point spectra'           are just sample_image
        scan types with reduced dimensions in the same way            as single images
        have reduced E dimensions compared to image 'stacks'.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    ENTRY = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXtofsingle(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        This is a application definition for raw data from a generic TOF instrument
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    entry = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXtranslation(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                legacy class - (used by :ref:`NXgeometry`) - general spatial location of a
        component.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    geometry = SubSection(
        sub_section=SectionProxy('NXgeometry'),
        repeats=True,
        )

    distances = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXdisk_chopper(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                A device blocking the beam in a temporal periodic pattern.

        A disk which blocks the beam but has one or more slits to periodically
        let neutrons through as the disk rotates. Often used in pairs, one
        NXdisk_chopper should be defined for each disk.

        The rotation of the disk is commonly monitored by recording a timestamp for
        each full rotation of disk, by having a sensor in the stationary disk housing
        sensing when it is aligned with a feature (such as a magnet) on the disk.
        We refer to this below as the "top-dead-center signal".

        Angles and positive rotation speeds are measured in an anticlockwise
        direction when facing away from the source.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    GEOMETRY = SubSection(
        sub_section=SectionProxy('NXgeometry'),
        repeats=True,
        )

    type = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    rotation_speed = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    slits = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    slit_angle = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    pair_separation = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    slit_edges = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    top_dead_center = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    beam_position = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    radius = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    slit_height = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    phase = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    delay = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    ratio = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    distance = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    wavelength_range = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXoff_geometry(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                Geometry (shape) description.     The format closely matches the Object File
        Format (OFF) which can be output     by most CAD software.     It can be used to
        describe the shape of any beamline component, including detectors.     In the case
        of detectors it can be used to define the shape of a single pixel, or,     if the
        pixel shapes are non-uniform, to describe the shape of the whole detector.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    vertices = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    winding_order = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    faces = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    detector_faces = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXfermi_chopper(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        A Fermi chopper, possibly with curved slits.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    GEOMETRY = SubSection(
        sub_section=SectionProxy('NXgeometry'),
        repeats=True,
        )

    type = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    rotation_speed = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    radius = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    slit = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    r_slit = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    number = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    height = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    width = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    distance = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    wavelength = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    energy = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    absorbing_material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    transmitting_material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXprocess(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        Document an event of data processing, reconstruction, or analysis for this data.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    NOTE = SubSection(
        sub_section=SectionProxy('NXnote'),
        repeats=True,
        )

    program = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    sequence_index = SubSection(
        sub_section=SectionProxy('NX_POSINT'),
        repeats=True,
        )

    version = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    date = SubSection(
        sub_section=SectionProxy('NX_DATE_TIME'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXcapillary(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                A capillary lens to focus the X-ray beam.              Based on information
        provided by Gerd Wellenreuther (DESY).
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    gain = SubSection(
        sub_section=SectionProxy('NXdata'),
        repeats=True,
        )

    transmission = SubSection(
        sub_section=SectionProxy('NXdata'),
        repeats=True,
        )

    type = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    manufacturer = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    maximum_incident_angle = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    accepting_aperture = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    working_distance = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    focal_size = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXgeometry(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_deprecated = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                legacy class - recommend to use :ref:`NXtransformations` now                  It
        is recommended that instances of :ref:`NXgeometry` be converted to          use
        :ref:`NXtransformations`.                  This is the description for a general
        position of a component.          It is recommended to name an instance of
        :ref:`NXgeometry` as "geometry"         to aid in the use of the definition in
        simulation codes such as McStas.         Also, in HDF, linked items must share the
        same name.         However, it might not be possible or practical in all
        situations.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    SHAPE = SubSection(
        sub_section=SectionProxy('NXshape'),
        repeats=True,
        )

    TRANSLATION = SubSection(
        sub_section=SectionProxy('NXtranslation'),
        repeats=True,
        )

    ORIENTATION = SubSection(
        sub_section=SectionProxy('NXorientation'),
        repeats=True,
        )

    description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    component_index = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXfilter(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                For band pass beam filters.                                  If uncertain whether
        to use :ref:`NXfilter` (band-pass filter)                 or :ref:`NXattenuator`
        (reduces beam intensity), then use                  :ref:`NXattenuator`.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    GEOMETRY = SubSection(
        sub_section=SectionProxy('NXgeometry'),
        repeats=True,
        )

    transmission = SubSection(
        sub_section=SectionProxy('NXdata'),
        repeats=True,
        )

    temperature_log = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    sensor_type = SubSection(
        sub_section=SectionProxy('NXsensor'),
        repeats=True,
        )

    description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    status = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    temperature = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    thickness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    density = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    chemical_formula = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    unit_cell_a = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    unit_cell_b = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    unit_cell_c = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    unit_cell_alpha = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    unit_cell_beta = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    unit_cell_gamma = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    unit_cell_volume = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    orientation_matrix = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    m_value = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    substrate_material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    substrate_thickness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    coating_material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    substrate_roughness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    coating_roughness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXsubentry(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                Group of multiple application definitions for "multi-modal" (e.g. SAXS/WAXS)
        measurements.                                  ``NXsubentry`` is a base class
        virtually identical to :ref:`NXentry`                 and is used as the (overlay)
        location for application definitions.                 Use a separate
        ``NXsubentry`` for each application definition.
        To use ``NXsubentry`` with a hypothetical application definition
        called ``NXmyappdef``:

        * Create a group with attribute ``NX_class="NXsubentry"``                 * Within
        that group, create a field called ``definition="NXmyappdef"``.                 *
        There are two optional attributes of definition: ``version`` and ``URL``

        The intended use is to define application definitions for a
        multi-modal (a.k.a. multi-technique) :ref:`NXentry`.                  Previously,
        an application definition                  replaced :ref:`NXentry` with its own
        definition.                  With the increasing popularity of instruments
        combining                  multiple techniques for data collection (such as
        SAXS/WAXS instruments),                  it was recognized the application
        definitions must be entered in the NeXus                 data file tree as
        children of :ref:`NXentry`.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    experiment_documentation = SubSection(
        sub_section=SectionProxy('NXnote'),
        repeats=True,
        )

    notes = SubSection(
        sub_section=SectionProxy('NXnote'),
        repeats=True,
        )

    thumbnail = SubSection(
        sub_section=SectionProxy('NXnote'),
        repeats=True,
        )

    USER = SubSection(
        sub_section=SectionProxy('NXuser'),
        repeats=True,
        )

    SAMPLE = SubSection(
        sub_section=SectionProxy('NXsample'),
        repeats=True,
        )

    INSTRUMENT = SubSection(
        sub_section=SectionProxy('NXinstrument'),
        repeats=True,
        )

    COLLECTION = SubSection(
        sub_section=SectionProxy('NXcollection'),
        repeats=True,
        )

    MONITOR = SubSection(
        sub_section=SectionProxy('NXmonitor'),
        repeats=True,
        )

    DATA = SubSection(
        sub_section=SectionProxy('NXdata'),
        repeats=True,
        )

    PARAMETERS = SubSection(
        sub_section=SectionProxy('NXparameters'),
        repeats=True,
        )

    PROCESS = SubSection(
        sub_section=SectionProxy('NXprocess'),
        repeats=True,
        )

    title = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    experiment_identifier = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    experiment_description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    collection_identifier = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    collection_description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    entry_identifier = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    definition = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    definition_local = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    start_time = SubSection(
        sub_section=SectionProxy('NX_DATE_TIME'),
        repeats=True,
        )

    end_time = SubSection(
        sub_section=SectionProxy('NX_DATE_TIME'),
        repeats=True,
        )

    duration = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    collection_time = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    run_cycle = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    program_name = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    revision = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    pre_sample_flightpath = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    IDF_Version = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXpolarizer(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                A spin polarizer.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    type = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    composition = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    reflection = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    efficiency = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXdetector_module(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                Geometry and logical description of a detector module. When used, child group to
        NXdetector.                                  Many detectors consist of multiple
        smaller modules. Sometimes it is important to know the exact position of such
        modules.                 This is the purpose of this group. It is a child group to
        NXdetector.

        Note, the pixel size is given as values in the array fast_pixel_direction and
        slow_pixel_direction.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    data_origin = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    data_size = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    module_offset = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    fast_pixel_direction = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    slow_pixel_direction = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXattenuator(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                A device that reduces the intensity of a beam by attenuation.

        If uncertain whether to use :ref:`NXfilter` (band-pass filter)         or
        :ref:`NXattenuator` (reduces beam intensity), then choose
        :ref:`NXattenuator`.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    distance = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    type = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    thickness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    scattering_cross_section = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    absorption_cross_section = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    attenuator_transmission = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    status = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXenvironment(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        Parameters for controlling external conditions
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    position = SubSection(
        sub_section=SectionProxy('NXgeometry'),
        repeats=True,
        )

    NOTE = SubSection(
        sub_section=SectionProxy('NXnote'),
        repeats=True,
        )

    SENSOR = SubSection(
        sub_section=SectionProxy('NXsensor'),
        repeats=True,
        )

    name = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    short_name = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    type = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    program = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXparameters(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        Container for parameters, usually used in processing or analysis.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    term = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXcollimator(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        A beamline collimator.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    GEOMETRY = SubSection(
        sub_section=SectionProxy('NXgeometry'),
        repeats=True,
        )

    frequency_log = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    type = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    soller_angle = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    divergence_x = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    divergence_y = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    frequency = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    blade_thickness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    blade_spacing = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    absorbing_material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    transmitting_material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXslit(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                A simple slit.                                  For more complex geometries,
        :ref:`NXaperture` should be used.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    depends_on = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    x_gap = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    y_gap = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXbeam(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                Properties of the neutron or X-ray beam at a given location.                   It
        will be referenced         by beamline component groups within the
        :ref:`NXinstrument` group or by the :ref:`NXsample` group. Note         that
        variables such as the incident energy could be scalar values or arrays. This group
        is         especially valuable in storing the results of instrument simulations in
        which it is useful         to specify the beam profile, time distribution etc. at
        each beamline component. Otherwise,         its most likely use is in the
        :ref:`NXsample` group in which it defines the results of the neutron
        scattering by the sample, e.g., energy transfer, polarizations.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    DATA = SubSection(
        sub_section=SectionProxy('NXdata'),
        repeats=True,
        )

    distance = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    incident_energy = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    final_energy = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    energy_transfer = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    incident_wavelength = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    incident_wavelength_spread = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    incident_beam_divergence = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    extent = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    final_wavelength = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    incident_polarization = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    final_polarization = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    final_wavelength_spread = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    final_beam_divergence = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    flux = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXsample_component(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                One group like this per component can be recorded For a sample consisting of
        multiple components.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    transmission = SubSection(
        sub_section=SectionProxy('NXdata'),
        repeats=True,
        )

    name = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    chemical_formula = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    unit_cell_abc = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    unit_cell_alphabetagamma = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    unit_cell_volume = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    sample_orientation = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    orientation_matrix = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    mass = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    density = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    relative_molecular_mass = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    volume_fraction = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    scattering_length_density = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    unit_cell_class = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    space_group = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    point_group = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXflipper(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        A spin flipper.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    type = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    flip_turns = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    comp_turns = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    guide_turns = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    flip_current = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    comp_current = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    guide_current = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    thickness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXsample(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                Any information on the sample.                                   This could
        include scanned variables that                 are associated with one of the data
        dimensions, e.g. the magnetic field, or                 logged data, e.g.
        monitored temperature vs elapsed time.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    geometry = SubSection(
        sub_section=SectionProxy('NXgeometry'),
        repeats=True,
        )

    BEAM = SubSection(
        sub_section=SectionProxy('NXbeam'),
        repeats=True,
        )

    SAMPLE_COMPONENT = SubSection(
        sub_section=SectionProxy('NXsample_component'),
        repeats=True,
        )

    transmission = SubSection(
        sub_section=SectionProxy('NXdata'),
        repeats=True,
        )

    temperature = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    temperature_log = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    temperature_env = SubSection(
        sub_section=SectionProxy('NXenvironment'),
        repeats=True,
        )

    magnetic_field = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    magnetic_field_log = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    magnetic_field_env = SubSection(
        sub_section=SectionProxy('NXenvironment'),
        repeats=True,
        )

    external_ADC = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    POSITIONER = SubSection(
        sub_section=SectionProxy('NXpositioner'),
        repeats=True,
        )

    name = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    chemical_formula = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    temperature = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    electric_field = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    magnetic_field = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    stress_field = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    pressure = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    changer_position = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    unit_cell_abc = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    unit_cell_alphabetagamma = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    unit_cell = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    unit_cell_volume = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    sample_orientation = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    orientation_matrix = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    ub_matrix = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    mass = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    density = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    relative_molecular_mass = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    type = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    situation = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    preparation_date = SubSection(
        sub_section=SectionProxy('NX_DATE_TIME'),
        repeats=True,
        )

    component = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    sample_component = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    concentration = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    volume_fraction = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    scattering_length_density = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    unit_cell_class = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    space_group = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    point_group = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    path_length = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    path_length_window = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    thickness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    external_DAC = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    short_title = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    rotation_angle = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    x_translation = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    distance = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXcollection(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_ignoreExtraGroups = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_ignoreExtraFields = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_ignoreExtraAttributes = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

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
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)


class NXentry(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                (**required**) :ref:`NXentry` describes the measurement.
        The top-level NeXus group which contains all the data and associated
        information that comprise a single measurement.                  It is mandatory
        that there is at least one                 group of this type in the NeXus file.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    DATA = SubSection(
        sub_section=SectionProxy('NXdata'),
        repeats=True,
        )

    experiment_documentation = SubSection(
        sub_section=SectionProxy('NXnote'),
        repeats=True,
        )

    notes = SubSection(
        sub_section=SectionProxy('NXnote'),
        repeats=True,
        )

    thumbnail = SubSection(
        sub_section=SectionProxy('NXnote'),
        repeats=True,
        )

    USER = SubSection(
        sub_section=SectionProxy('NXuser'),
        repeats=True,
        )

    SAMPLE = SubSection(
        sub_section=SectionProxy('NXsample'),
        repeats=True,
        )

    INSTRUMENT = SubSection(
        sub_section=SectionProxy('NXinstrument'),
        repeats=True,
        )

    COLLECTION = SubSection(
        sub_section=SectionProxy('NXcollection'),
        repeats=True,
        )

    MONITOR = SubSection(
        sub_section=SectionProxy('NXmonitor'),
        repeats=True,
        )

    PARAMETERS = SubSection(
        sub_section=SectionProxy('NXparameters'),
        repeats=True,
        )

    PROCESS = SubSection(
        sub_section=SectionProxy('NXprocess'),
        repeats=True,
        )

    SUBENTRY = SubSection(
        sub_section=SectionProxy('NXsubentry'),
        repeats=True,
        )

    title = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    experiment_identifier = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    experiment_description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    collection_identifier = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    collection_description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    entry_identifier = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    entry_identifier_uuid = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    features = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    definition = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    definition_local = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    start_time = SubSection(
        sub_section=SectionProxy('NX_DATE_TIME'),
        repeats=True,
        )

    end_time = SubSection(
        sub_section=SectionProxy('NX_DATE_TIME'),
        repeats=True,
        )

    duration = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    collection_time = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    run_cycle = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    program_name = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    revision = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    pre_sample_flightpath = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    IDF_Version = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXshape(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                legacy class - (used by :ref:`NXgeometry`) - the shape and size of a component.
        This is the description of the general shape and size of a
        component, which may be made up of ``numobj`` separate                  elements -
        it is used by the :ref:`NXgeometry` class
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    shape = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    size = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    direction = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXlog(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                Information recorded as a function of time.

        Description of information that is recorded against                 time. There
        are two common use cases for this:

        - When logging data such as temperature during a run                 - When data
        is taken in streaming mode data acquisition,                   i.e. just
        timestamp, value pairs are stored and                   correlated later in data
        reduction with other data,

        In both cases, NXlog contains                 the logged or streamed  values and
        the times at which they were measured as elapsed time since a starting
        time recorded in ISO8601 format. The time units are                 specified in
        the units attribute. An optional scaling attribute                 can be used to
        accomodate non standard clocks.

        This method of storing logged data helps to distinguish                 instances
        in which a variable is a dimension scale of the data, in which case it is stored
        in an :ref:`NXdata` group, and instances in which it is logged during the
        run, when it should be stored in an :ref:`NXlog` group.

        In order to make random access to timestamped data faster there is an optional
        array pair of                 ``cue_timestamp_zero`` and ``cue_index``. The
        ``cue_timestamp_zero`` will                 contain coarser timestamps than in the
        time array, say                 every five minutes. The ``cue_index`` will then
        contain the                 index into the time,value pair of arrays for that
        coarser ``cue_timestamp_zero``.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    time = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    value = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    raw_value = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    average_value = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    average_value_error = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    average_value_errors = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    minimum_value = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    maximum_value = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    duration = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    cue_timestamp_zero = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    cue_index = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXreflections(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        Reflection data from diffraction experiments
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    experiments = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    h = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    k = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    l = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    id = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    reflection_id = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    entering = SubSection(
        sub_section=SectionProxy('NX_BOOLEAN'),
        repeats=True,
        )

    det_module = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    flags = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    d = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    partiality = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    predicted_frame = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    predicted_x = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    predicted_y = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    predicted_phi = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    predicted_px_x = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    predicted_px_y = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    observed_frame = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    observed_frame_var = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    observed_frame_errors = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    observed_px_x = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    observed_px_x_var = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    observed_px_x_errors = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    observed_px_y = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    observed_px_y_var = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    observed_px_y_errors = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    observed_phi = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    observed_phi_var = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    observed_phi_errors = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    observed_x = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    observed_x_var = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    observed_x_errors = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    observed_y = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    observed_y_var = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    observed_y_errors = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    bounding_box = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    background_mean = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    int_prf = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    int_prf_var = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    int_prf_errors = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    int_sum = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    int_sum_var = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    int_sum_errors = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    lp = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    prf_cc = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    overlaps = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    polar_angle = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    azimuthal_angle = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXpositioner(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                A generic positioner such as a motor or piezo-electric transducer.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    name = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    value = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    raw_value = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    target_value = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    tolerance = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    soft_limit_min = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    soft_limit_max = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    velocity = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    acceleration_time = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    controller_record = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXcrystal(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                A crystal monochromator or analyzer.           Permits double bent
        monochromator comprised of multiple segments with anisotropic      Gaussian
        mosaic.          If curvatures are set to zero or are absent, array      is
        considered to be flat.          Scattering vector is perpendicular to surface.
        Crystal is oriented     parallel to beam incident on crystal before rotation, and
        lies in     vertical plane.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    GEOMETRY = SubSection(
        sub_section=SectionProxy('NXgeometry'),
        repeats=True,
        )

    temperature_log = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    reflectivity = SubSection(
        sub_section=SectionProxy('NXdata'),
        repeats=True,
        )

    transmission = SubSection(
        sub_section=SectionProxy('NXdata'),
        repeats=True,
        )

    shape = SubSection(
        sub_section=SectionProxy('NXshape'),
        repeats=True,
        )

    usage = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    type = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    chemical_formula = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    order_no = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    cut_angle = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    space_group = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    unit_cell = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    unit_cell_a = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    unit_cell_b = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    unit_cell_c = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    unit_cell_alpha = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    unit_cell_beta = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    unit_cell_gamma = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    unit_cell_volume = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    orientation_matrix = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    wavelength = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    d_spacing = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    scattering_vector = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    reflection = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    thickness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    density = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    segment_width = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    segment_height = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    segment_thickness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    segment_gap = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    segment_columns = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    segment_rows = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    mosaic_horizontal = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    mosaic_vertical = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    curvature_horizontal = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    curvature_vertical = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    is_cylindrical = SubSection(
        sub_section=SectionProxy('NX_BOOLEAN'),
        repeats=True,
        )

    cylindrical_orientation_angle = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    polar_angle = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    azimuthal_angle = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    bragg_angle = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    temperature = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    temperature_coefficient = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXdata(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_ignoreExtraFields = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_ignoreExtraAttributes = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                :ref:`NXdata` describes the plottable data and related dimension scales.
        .. index:: plotting                                  It is mandatory  that there
        is at least one :ref:`NXdata` group                  in each :ref:`NXentry` group.
        Note that the ``variable`` and ``data``                  can be defined with
        different names.                   The ``signal`` and ``axes`` attributes of the
        ``data`` group define which items                  are plottable data and which
        are *dimension scales*, respectively.
        :ref:`NXdata` is used to implement one of the basic motivations in NeXus,
        to provide a default plot for the data of this :ref:`NXentry`.  The actual data
        might be stored in another group and (hard) linked to the :ref:`NXdata` group.

        * Each :ref:`NXdata` group will define only one data set
        containing plottable data, dimension scales, and                    possibly
        associated standard deviations.                   Other data sets may be present
        in the group.                 * The plottable data may be of arbitrary rank up to
        a maximum                   of ``NX_MAXRANK=32``.                 * The plottable
        data will be named as the value of                    the group ``signal``
        attribute, such as::                                        data:NXdata
        @signal = "counts"                       @axes = "mr"
        @mr_indices = 0                       counts: float[100]  --> the default
        dependent data                       mr: float[100]  --> the default independent
        data                                      The field named in the ``signal``
        attribute **must** exist, either                   directly as a dataset or
        defined through a link.                                  * The group ``axes``
        attribute will name the                   *dimension scale* associated with the
        plottable data.

        If available, the standard deviations of the data are to be                 stored
        in a data set of the same rank and dimensions, with the name ``errors``.

        * For each data dimension, there should be a one-dimensional array
        of the same length.                 * These one-dimensional arrays are the
        *dimension scales* of the                   data,  *i.e*. the values of the
        independent variables at which the data                   is measured, such as
        scattering angle or energy transfer.                                  .. index::
        link                 .. index:: axes (attribute)
        The preferred method to associate each data dimension with                 its
        respective dimension scale is to specify the field name                 of each
        dimension scale in the group ``axes`` attribute as a string list.
        Here is an example for a 2-D data set *data* plotted                  against
        *time*, and *pressure*.  (An additional *temperature* data set                  is
        provided and could be selected as an alternate for the *pressure* axis.)::

        data_2d:NXdata                     @signal="data"
        @axes=["time", "pressure"]                     @pressure_indices=1
        @temperature_indices=1                     @time_indices=0
        data: float[1000,20]                     pressure: float[20]
        temperature: float[20]                     time: float[1000]

        .. rubric:: Old methods to identify the plottable data
        There are two older methods of associating                  each data dimension to
        its respective dimension scale.                 Both are now out of date and
        should not be used when writing new data files.                 However, client
        software should expect to see data files                 written with any of these
        methods.                                    * One method uses the ``axes``
        attribute to specify the names of each *dimension scale*.
        * The oldest method uses the ``axis`` attribute on each
        *dimension scale* to identify                     with an integer the axis whose
        value is the number of the dimension.

        .. index: !plot; axis label                    plot, axis units
        units                    dimension scale

        Each axis of the plot may be labeled with information from the
        dimension scale for that axis.  The optional ``@long_name`` attribute
        is provided as the axis label default.  If ``@long_name`` is not
        defined, then use the name of the dimension scale.  A ``@units`` attribute,
        if available, may be added to the axis label for further description.
        See the section :ref:`Design-Units` for more information.

        .. index: !plot; axis title

        The optional ``title`` field, if available, provides a suggested
        title for the plot.  If no ``title`` field is found in the :ref:`NXdata`
        group, look for a ``title`` field in the parent :ref:`NXentry` group,
        with a fallback to displaying the path to the :ref:`NXdata` group.

        NeXus is about how to find and annotate the data to be plotted
        but not to describe how the data is to be plotted.
        (https://www.nexusformat.org/NIAC2018Minutes.html#nxdata-plottype--attribute)
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    VARIABLE = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    VARIABLE_errors = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    DATA = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    errors = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    scaling_factor = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    offset = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    title = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    x = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    y = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    z = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    auxiliary_signals = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    signal = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    axes = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    AXISNAME_indices = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXinsertion_device(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        An insertion device, as used in a synchrotron light source.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    spectrum = SubSection(
        sub_section=SectionProxy('NXdata'),
        repeats=True,
        )

    GEOMETRY = SubSection(
        sub_section=SectionProxy('NXgeometry'),
        repeats=True,
        )

    type = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    gap = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    taper = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    phase = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    poles = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    magnetic_wavelength = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    k = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    length = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    power = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    energy = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    bandwidth = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    harmonic = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXpdb(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_ignoreExtraGroups = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_ignoreExtraFields = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_ignoreExtraAttributes = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                A NeXus transliteration of a PDB file, to be validated only as a PDB
        rather than in NeXus.

        Use :ref:`NXpdb` to incorporate the information in an arbitrary
        PDB into a NeXus file.

        The main suggestion is to use this as a container                 class for a PDB
        entry to describe a sample in NXsample,                 but it may be more
        appropriate to place this higher in the                 hierarchy, say in NXentry.

        The structure has to follow the structure of a PDB                 with each PDB
        data block mapped to a NeXus group of class NXpdb,                 using a
        lowercase version of the data block name as the name                 of the NeXus
        group, each PDB category in that data block                 mapped to a NeXus
        group of class NXpdb and with each PDB column                 mapped to a NeXus
        field.  Each column in a looped PDB category                 should always be
        presented as a 1-dimensional array.  The columns                  in an unlooped
        PDB category should be presented as scalar values.                   If a PDB
        category specifies particular units for columns, the same                  units
        should beused for the corresponding fields.

        A PDB entry is unambigous when all information is carried as text.
        All text data should be presented as quoted strings, with the quote
        marks except for the null values "." or "?"

        For clarity in NXpdb form, numeric data may be presented using the
        numeric types specified in the mmCIF dictionary.  In that case,                 if
        a PDB null value, "." or "?", is contained in a numeric column, the
        IEEE nan should be used for "?" and the IEEE inf should be used for ".".

        An arbitrary DDL2 CIF file can be represented in NeXus using NXpdb.
        However, if save frames are required, an NXpdb_class  attribute with the
        value "CBF_cbfsf" is required for each NeXus group representing a save
        frame.  NXpdb attributes are not required for other CIF components,
        but may be used to provide internal documentation.

        The nesting of NXpdb groups and datasets that correspond to a CIF with
        two categories and one saveframe, including the NXpdb_class attribues is::

        (datablock1):NXpdb                            @NXpdb_class:CBF_cbfdb
        (category1):NXpdb                              @NXpdb_class:CBF_cbfcat
        (column_name1):[...]                               (column_name2):[...]
        (column_name3):[...]                               ...
        (category2):NXpdb                               @NXpdb_class:CBF_cbfcat
        (column_name4):[...]                               (column_name5):[...]
        (column_name6):[...]                               ...
        (saveframe1):NXpdb                               @NXpdb_class:CBF_cbfsf
        (category3):NXpdb                                 @NXpdb_class:CBF_cbfcat
        (column_name7):[...]                                 (column_name8):[...]
        (column_name9):[...]                                  ...
        ...                            ...

        For example, a PDB entry that begins::

        data_1YVA                         #                          _entry.id   1YVA
        #                         _audit_conform.dict_name       mmcif_pdbx.dic
        _audit_conform.dict_version    5.279
        _audit_conform.dict_location
        http://mmcif.pdb.org/dictionaries/ascii/mmcif_pdbx.dic                         #
        loop_                         _database_2.database_id
        _database_2.database_code                         PDB   1YVA
        RCSB  RCSB031959                         WWPDB D_1000031959
        #

        would produce::                                  sample:NXsample
        1yva:NXpdb                              entry:NXpdb
        id:"1YVA"                              audit_conform:NXpdb
        dict_name:"mmcif_pdbx.dic"                                  dict_version:"5.279"
        dict_location:"http://mmcif.pdb.org/dictionaries/ascii/mmcif_pdbx.dic"
        database_2:NXpdb
        database_id:["PDB","RCSB","WWPDB"]
        database_code:["1YVA","RCSB031959","D_1000031959"]

        another example is the following excerpt from pdb entry 9ins, giving the sequences
        of the two chains::

        loop_                         _entity_poly.entity_id
        _entity_poly.nstd_linkage                         _entity_poly.nstd_monomer
        _entity_poly.pdbx_seq_one_letter_code
        _entity_poly.pdbx_seq_one_letter_code_can
        _entity_poly.type                         1 no no GIVEQCCTSICSLYQLENYCN
        GIVEQCCTSICSLYQLENYCN polypeptide(L)                         2 no no
        FVNQHLCGSHLVEALYLVCGERGFFYTPKA FVNQHLCGSHLVEALYLVCGERGFFYTPKA
        polypeptide(L)

        which converts to::

        entity_poly:NXpdb                           @NXpdb_class:CBF_cbfcat
        entity_id:["1", "2"]                           nstd_linkage:["no", "no"]
        nstd_monomer:["no", "no"]                           pdbx_seq_one_letter_code:["GIV
        EQCCTSICSLYQLENYCN","FVNQHLCGSHLVEALYLVCGERGFFYTPKA"]                           pd
        bx_seq_one_letter_code_can:["GIVEQCCTSICSLYQLENYCN","FVNQHLCGSHLVEALYLVCGERGFFYTPK
        A"]                           type:["polypeptide(L)", "polypeptide(L)"]
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)


class NXsensor(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                A sensor used to monitor an external condition
        The condition itself is described in :ref:`NXenvironment`.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    geometry = SubSection(
        sub_section=SectionProxy('NXgeometry'),
        repeats=True,
        )

    value_log = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    value_deriv1_log = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    value_deriv2_log = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    external_field_full = SubSection(
        sub_section=SectionProxy('NXorientation'),
        repeats=True,
        )

    model = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    name = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    short_name = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    attached_to = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    measurement = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    type = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    run_control = SubSection(
        sub_section=SectionProxy('NX_BOOLEAN'),
        repeats=True,
        )

    high_trip_value = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    low_trip_value = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    value = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    value_deriv1 = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    value_deriv2 = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    external_field_brief = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXaperture(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        A beamline aperture.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    GEOMETRY = SubSection(
        sub_section=SectionProxy('NXgeometry'),
        repeats=True,
        )

    BLADE_GEOMETRY = SubSection(
        sub_section=SectionProxy('NXgeometry'),
        repeats=True,
        )

    NOTE = SubSection(
        sub_section=SectionProxy('NXnote'),
        repeats=True,
        )

    material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXroot(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        Definition of the root NeXus group.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    ENTRY = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )

    NX_class = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    file_time = SubSection(
        sub_section=SectionProxy('NX_DATE_TIME'),
        repeats=True,
        )

    file_name = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    file_update_time = SubSection(
        sub_section=SectionProxy('NX_DATE_TIME'),
        repeats=True,
        )

    NeXus_version = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    HDF_version = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    HDF5_Version = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    XML_version = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    h5py_version = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    creator = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    creator_version = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXmonochromator(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                A  wavelength defining device.                  This is a base class for
        everything which         selects a wavelength or energy, be it a
        monochromator crystal, a velocity selector,         an undulator or whatever.
        The expected units are:                  * wavelength: angstrom         * energy:
        eV
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    distribution = SubSection(
        sub_section=SectionProxy('NXdata'),
        repeats=True,
        )

    geometry = SubSection(
        sub_section=SectionProxy('NXgeometry'),
        repeats=True,
        )

    CRYSTAL = SubSection(
        sub_section=SectionProxy('NXcrystal'),
        repeats=True,
        )

    VELOCITY_SELECTOR = SubSection(
        sub_section=SectionProxy('NXvelocity_selector'),
        repeats=True,
        )

    GRATING = SubSection(
        sub_section=SectionProxy('NXgrating'),
        repeats=True,
        )

    wavelength = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    wavelength_error = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    wavelength_errors = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    energy = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    energy_error = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    energy_errors = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXbending_magnet(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        A bending magnet
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    spectrum = SubSection(
        sub_section=SectionProxy('NXdata'),
        repeats=True,
        )

    GEOMETRY = SubSection(
        sub_section=SectionProxy('NXgeometry'),
        repeats=True,
        )

    critical_energy = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    bending_radius = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    magnetic_field = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    accepted_photon_beam_divergence = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    source_distance_x = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    source_distance_y = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    divergence_x_plus = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    divergence_x_minus = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    divergence_y_plus = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    divergence_y_minus = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXmonitor(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                A monitor of incident beam data.                   It is similar to the
        :ref:`NXdata` groups containing         monitor data and its associated dimension
        scale, e.g. time_of_flight or         wavelength in pulsed neutron instruments.
        However, it may also include         integrals, or scalar monitor counts, which
        are often used in both in both         pulsed and steady-state instrumentation.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    integral_log = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    GEOMETRY = SubSection(
        sub_section=SectionProxy('NXgeometry'),
        repeats=True,
        )

    mode = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    start_time = SubSection(
        sub_section=SectionProxy('NX_DATE_TIME'),
        repeats=True,
        )

    end_time = SubSection(
        sub_section=SectionProxy('NX_DATE_TIME'),
        repeats=True,
        )

    preset = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    distance = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    range = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    nominal = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    integral = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    type = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    time_of_flight = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    efficiency = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    data = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    sampled_fraction = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    count_time = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXtransformations(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_ignoreExtraGroups = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_ignoreExtraFields = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_ignoreExtraAttributes = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                Collection of axis-based translations and rotations to describe a geometry.
        May also contain axes that do not move and therefore do not have a transformation
        type specified, but are useful in understanding coordinate frames within which
        transformations are done, or in documenting important directions, such as the
        direction of gravity.

        A nested sequence of transformations lists the translation and rotation steps
        needed to describe the position and orientation of any movable or fixed device.

        There will be one or more transformations (axes) defined by one or more fields
        for each transformation.  The all-caps name ``AXISNAME`` designates the
        particular axis generating a transformation (e.g. a rotation axis or a translation
        axis or a general axis).   The attribute ``units="NX_TRANSFORMATION"`` designates
        the                 units will be appropriate to the ``transformation_type``
        attribute:

        * ``NX_LENGTH`` for ``translation``                 * ``NX_ANGLE`` for
        ``rotation``                 * ``NX_UNITLESS`` for axes for which no
        transformation type is specified

        This class will usually contain all axes of a sample stage or goniometer or
        a detector.  The NeXus default McSTAS coordinate frame is assumed, but additional
        useful coordinate axes may be defined by using axes for which no transformation
        type has been specified.

        The entry point (``depends_on``) will be outside of this class and point to a
        field in here. Following the chain may also require following ``depends_on``
        links to transformations outside, for example to a common base table.  If
        a relative path is given, it is relative to the group enclosing the ``depends_on``
        specification.

        For a chain of three transformations, where :math:`T_1` depends on :math:`T_2`
        and that in turn depends on :math:`T_3`, the final transformation :math:`T_f` is

        .. math:: T_f = T_3 T_2 T_1

        In explicit terms, the transformations are a subset of affine transformations
        expressed as 4x4 matrices that act on homogeneous coordinates,
        :math:`w=(x,y,z,1)^T`.

        For rotation and translation,

        .. math:: T_r &= \\begin{pmatrix} R & o \\\\ 0_3 & 1 \\end{pmatrix} \\\\ T_t &=
        \\begin{pmatrix} I_3  & t + o \\\\ 0_3 & 1 \\end{pmatrix}

        where :math:`R` is the usual 3x3 rotation matrix, :math:`o` is an offset vector,
        :math:`0_3` is a row of 3 zeros, :math:`I_3` is the 3x3 identity matrix and
        :math:`t` is the translation vector.

        :math:`o` is given by the ``offset`` attribute, :math:`t` is given by the
        ``vector``                 attribute multiplied by the field value, and :math:`R`
        is defined as a rotation                 about an axis in the direction of
        ``vector``, of angle of the field value.

        NOTE                                  One possible use of ``NXtransformations`` is
        to define the motors and                 transformations for a diffractometer
        (goniometer).  Such use is mentioned                 in the ``NXinstrument`` base
        class.  Use one ``NXtransformations`` group                  for each
        diffractometer and name the group appropriate to the device.
        Collecting the motors of a sample table or xyz-stage in an NXtransformation
        group is equally possible.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    AXISNAME = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    AXISNAME_end = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    AXISNAME_increment_set = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXguide(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                A neutron optical element to direct the path of the beam.
        :ref:`NXguide` is used by neutron instruments to describe         a guide consists
        of several mirrors building a shape through which          neutrons can be guided
        or directed. The simplest such form is box shaped         although elliptical
        guides are gaining in popularity.          The individual parts of a guide usually
        have common characteristics          but there are cases where they are different.
        For example,  a neutron guide might consist of 2 or 4 coated walls or         a
        supermirror bender with multiple, coated vanes.

        To describe polarizing supermirrors such as used in neutron reflection,         it
        may be necessary to revise this definition of :ref:`NXguide`         to include
        :ref:`NXpolarizer` and/or :ref:`NXmirror`.

        When even greater complexity exists in the definition of what         constitutes
        a *guide*,  it has been suggested that :ref:`NXguide`          be redefined as a
        :ref:`NXcollection` of :ref:`NXmirror` each          having their own
        :ref:`NXgeometry` describing their location(s).

        For the more general case when describing mirrors, consider using
        :ref:`NXmirror`.

        NOTE: The NeXus International Advisory Committee welcomes          comments for
        revision and improvement of          this definition of :ref:`NXguide`.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    GEOMETRY = SubSection(
        sub_section=SectionProxy('NXgeometry'),
        repeats=True,
        )

    reflectivity = SubSection(
        sub_section=SectionProxy('NXdata'),
        repeats=True,
        )

    description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    incident_angle = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    bend_angle_x = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    bend_angle_y = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    interior_atmosphere = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    external_material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    m_value = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    substrate_material = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    substrate_thickness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    coating_material = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    substrate_roughness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    coating_roughness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    number_sections = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXuser(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                Contact information for a user.                                    The format
        allows more                  than one user with the same affiliation and contact
        information,                  but a second :ref:`NXuser` group should be used if
        they have different                  affiliations, etc.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    name = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    role = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    affiliation = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    address = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    telephone_number = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    fax_number = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    email = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    facility_user_id = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    ORCID = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXmoderator(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        A neutron moderator
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    GEOMETRY = SubSection(
        sub_section=SectionProxy('NXgeometry'),
        repeats=True,
        )

    temperature_log = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    pulse_shape = SubSection(
        sub_section=SectionProxy('NXdata'),
        repeats=True,
        )

    distance = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    type = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    poison_depth = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    coupled = SubSection(
        sub_section=SectionProxy('NX_BOOLEAN'),
        repeats=True,
        )

    coupling_material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    poison_material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    temperature = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXbeam_stop(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                A device that blocks the beam completely, usually to protect a detector.
        Beamstops and their positions are important for SANS         and SAXS experiments.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    GEOMETRY = SubSection(
        sub_section=SectionProxy('NXgeometry'),
        repeats=True,
        )

    description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    size = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    x = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    y = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    distance_to_detector = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    status = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXmirror(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        A beamline mirror or supermirror.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    GEOMETRY = SubSection(
        sub_section=SectionProxy('NXgeometry'),
        repeats=True,
        )

    reflectivity = SubSection(
        sub_section=SectionProxy('NXdata'),
        repeats=True,
        )

    shape = SubSection(
        sub_section=SectionProxy('NXshape'),
        repeats=True,
        )

    figure_data = SubSection(
        sub_section=SectionProxy('NXdata'),
        repeats=True,
        )

    type = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    incident_angle = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    bend_angle_x = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    bend_angle_y = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    interior_atmosphere = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    external_material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    m_value = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    substrate_material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    substrate_density = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    substrate_thickness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    coating_material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    substrate_roughness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    coating_roughness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    even_layer_material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    even_layer_density = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    odd_layer_material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    odd_layer_density = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    layer_thickness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXnote(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                Any additional freeform information not covered by the other base classes.
        This class can be used to store additional information in a                  NeXus
        file e.g. pictures, movies, audio, additional text logs
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    author = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    date = SubSection(
        sub_section=SectionProxy('NX_DATE_TIME'),
        repeats=True,
        )

    type = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    file_name = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    sequence_index = SubSection(
        sub_section=SectionProxy('NX_POSINT'),
        repeats=True,
        )

    data = SubSection(
        sub_section=SectionProxy('NX_BINARY'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXpinhole(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                A simple pinhole.                                  For more complex geometries,
        :ref:`NXaperture` should be used.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    depends_on = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    diameter = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXvelocity_selector(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        A neutron velocity selector
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    geometry = SubSection(
        sub_section=SectionProxy('NXgeometry'),
        repeats=True,
        )

    type = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    rotation_speed = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    radius = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    spwidth = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    length = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    num = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    twist = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    table = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    height = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    width = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    wavelength = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    wavelength_spread = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXinstrument(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                Collection of the components of the instrument or beamline.
        Template of instrument descriptions comprising various beamline components.
        Each component will also be a NeXus group defined by its distance from the
        sample. Negative distances represent beamline components that are before the
        sample while positive distances represent components that are after the sample.
        This device allows the unique identification of beamline components in a way
        that is valid for both reactor and pulsed instrumentation.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    APERTURE = SubSection(
        sub_section=SectionProxy('NXaperture'),
        repeats=True,
        )

    ATTENUATOR = SubSection(
        sub_section=SectionProxy('NXattenuator'),
        repeats=True,
        )

    BEAM = SubSection(
        sub_section=SectionProxy('NXbeam'),
        repeats=True,
        )

    BEAM_STOP = SubSection(
        sub_section=SectionProxy('NXbeam_stop'),
        repeats=True,
        )

    BENDING_MAGNET = SubSection(
        sub_section=SectionProxy('NXbending_magnet'),
        repeats=True,
        )

    COLLIMATOR = SubSection(
        sub_section=SectionProxy('NXcollimator'),
        repeats=True,
        )

    COLLECTION = SubSection(
        sub_section=SectionProxy('NXcollection'),
        repeats=True,
        )

    CAPILLARY = SubSection(
        sub_section=SectionProxy('NXcapillary'),
        repeats=True,
        )

    CRYSTAL = SubSection(
        sub_section=SectionProxy('NXcrystal'),
        repeats=True,
        )

    DETECTOR = SubSection(
        sub_section=SectionProxy('NXdetector'),
        repeats=True,
        )

    DETECTOR_GROUP = SubSection(
        sub_section=SectionProxy('NXdetector_group'),
        repeats=True,
        )

    DISK_CHOPPER = SubSection(
        sub_section=SectionProxy('NXdisk_chopper'),
        repeats=True,
        )

    EVENT_DATA = SubSection(
        sub_section=SectionProxy('NXevent_data'),
        repeats=True,
        )

    FERMI_CHOPPER = SubSection(
        sub_section=SectionProxy('NXfermi_chopper'),
        repeats=True,
        )

    FILTER = SubSection(
        sub_section=SectionProxy('NXfilter'),
        repeats=True,
        )

    FLIPPER = SubSection(
        sub_section=SectionProxy('NXflipper'),
        repeats=True,
        )

    GUIDE = SubSection(
        sub_section=SectionProxy('NXguide'),
        repeats=True,
        )

    INSERTION_DEVICE = SubSection(
        sub_section=SectionProxy('NXinsertion_device'),
        repeats=True,
        )

    MIRROR = SubSection(
        sub_section=SectionProxy('NXmirror'),
        repeats=True,
        )

    MODERATOR = SubSection(
        sub_section=SectionProxy('NXmoderator'),
        repeats=True,
        )

    MONOCHROMATOR = SubSection(
        sub_section=SectionProxy('NXmonochromator'),
        repeats=True,
        )

    POLARIZER = SubSection(
        sub_section=SectionProxy('NXpolarizer'),
        repeats=True,
        )

    POSITIONER = SubSection(
        sub_section=SectionProxy('NXpositioner'),
        repeats=True,
        )

    SOURCE = SubSection(
        sub_section=SectionProxy('NXsource'),
        repeats=True,
        )

    DIFFRACTOMETER = SubSection(
        sub_section=SectionProxy('NXtransformations'),
        repeats=True,
        )

    VELOCITY_SELECTOR = SubSection(
        sub_section=SectionProxy('NXvelocity_selector'),
        repeats=True,
        )

    XRAYLENS = SubSection(
        sub_section=SectionProxy('NXxraylens'),
        repeats=True,
        )

    name = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXdetector_group(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                Logical grouping of detectors. When used, describes a group of detectors.

        Each detector is represented as an NXdetector                  with its own
        detector data array.  Each detector data array                 may be further
        decomposed into array sections by use of                 NXdetector_module groups.
        Detectors can be grouped logically                 together using
        NXdetector_group. Groups can be further grouped                 hierarchically in
        a single NXdetector_group (for example, if                 there are multiple
        detectors at an endstation or multiple                  endstations at a
        facility).  Alternatively, multiple                  NXdetector_groups can be
        provided.

        The groups are defined hierarchically, with names given                 in the
        group_names field, unique identifying indices given                 in the field
        group_index, and the level in the hierarchy                 given in the
        group_parent field.  For example if an x-ray                 detector group, DET,
        consists of four detectors in a                 rectangular array::
        DTL    DTR                                  DLL    DLR
        We could have::
        group_names: ["DET", "DTL", "DTR", "DLL", "DLR"]
        group_index: [1, 2, 3, 4, 5]                         group_parent:  [-1, 1, 1, 1,
        1]
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    group_names = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    group_index = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    group_parent = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    group_type = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXobject(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                This is the base object of NeXus
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)


class NXcite(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                A literature reference                                  Definition to include
        references for example for detectors,                 manuals, instruments,
        acquisition or analysis software used.                                  The idea
        would be to include this in the relevant NeXus object:
        :ref:`NXdetector` for detectors, :ref:`NXinstrument` for instruments, etc.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    url = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    doi = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    endnote = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    bibtex = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXcylindrical_geometry(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                Geometry description for cylindrical shapes.     This class can be used in place
        of ``NXoff_geometry`` when an exact     representation for cylinders is preferred.
        For example, for Helium-tube, neutron detectors.     It can be used to describe
        the shape of any beamline component, including detectors.     In the case of
        detectors it can be used to define the shape of a single pixel, or,     if the
        pixel shapes are non-uniform, to describe the shape of the whole detector.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    vertices = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    cylinders = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    detector_number = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXsource(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        The neutron or x-ray storage ring/facility.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    notes = SubSection(
        sub_section=SectionProxy('NXnote'),
        repeats=True,
        )

    bunch_pattern = SubSection(
        sub_section=SectionProxy('NXdata'),
        repeats=True,
        )

    pulse_shape = SubSection(
        sub_section=SectionProxy('NXdata'),
        repeats=True,
        )

    geometry = SubSection(
        sub_section=SectionProxy('NXgeometry'),
        repeats=True,
        )

    distribution = SubSection(
        sub_section=SectionProxy('NXdata'),
        repeats=True,
        )

    distance = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    name = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    type = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    probe = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    power = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    emittance_x = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    emittance_y = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    sigma_x = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    sigma_y = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    flux = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    energy = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    current = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    voltage = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    frequency = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    period = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    target_material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    number_of_bunches = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    bunch_length = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    bunch_distance = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    pulse_width = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    mode = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    top_up = SubSection(
        sub_section=SectionProxy('NX_BOOLEAN'),
        repeats=True,
        )

    last_fill = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXgrating(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        A diffraction grating, as could be used in a soft X-ray monochromator
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    shape = SubSection(
        sub_section=SectionProxy('NXshape'),
        repeats=True,
        )

    figure_data = SubSection(
        sub_section=SectionProxy('NXdata'),
        repeats=True,
        )

    TRANSFORMATIONS = SubSection(
        sub_section=SectionProxy('NXtransformations'),
        repeats=True,
        )

    angles = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    period = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    duty_cycle = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    depth = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    diffraction_order = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    deflection_angle = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    interior_atmosphere = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    substrate_material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    substrate_density = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    substrate_thickness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    coating_material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    substrate_roughness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    coating_roughness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    layer_thickness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXdetector(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                A detector, detector bank, or multidetector.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    GEOMETRY = SubSection(
        sub_section=SectionProxy('NXgeometry'),
        repeats=True,
        )

    efficiency = SubSection(
        sub_section=SectionProxy('NXdata'),
        repeats=True,
        )

    calibration_method = SubSection(
        sub_section=SectionProxy('NXnote'),
        repeats=True,
        )

    data_file = SubSection(
        sub_section=SectionProxy('NXnote'),
        repeats=True,
        )

    COLLECTION = SubSection(
        sub_section=SectionProxy('NXcollection'),
        repeats=True,
        )

    DETECTOR_MODULE = SubSection(
        sub_section=SectionProxy('NXdetector_module'),
        repeats=True,
        )

    time_of_flight = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    raw_time_of_flight = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    detector_number = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    data = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    data_errors = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    x_pixel_offset = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    y_pixel_offset = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    z_pixel_offset = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    distance = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    polar_angle = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    azimuthal_angle = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    serial_number = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    local_name = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    solid_angle = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    x_pixel_size = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    y_pixel_size = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    dead_time = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    gas_pressure = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    detection_gas_path = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    crate = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    slot = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    input = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    type = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    real_time = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    start_time = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    stop_time = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    calibration_date = SubSection(
        sub_section=SectionProxy('NX_DATE_TIME'),
        repeats=True,
        )

    layout = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    count_time = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    sequence_number = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    beam_center_x = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    beam_center_y = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    frame_start_number = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    diameter = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    acquisition_mode = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    angular_calibration_applied = SubSection(
        sub_section=SectionProxy('NX_BOOLEAN'),
        repeats=True,
        )

    angular_calibration = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    flatfield_applied = SubSection(
        sub_section=SectionProxy('NX_BOOLEAN'),
        repeats=True,
        )

    flatfield = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    flatfield_errors = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    pixel_mask_applied = SubSection(
        sub_section=SectionProxy('NX_BOOLEAN'),
        repeats=True,
        )

    pixel_mask = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    countrate_correction_applied = SubSection(
        sub_section=SectionProxy('NX_BOOLEAN'),
        repeats=True,
        )

    bit_depth_readout = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    detector_readout_time = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    trigger_delay_time = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    trigger_delay_time_set = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    trigger_internal_delay_time = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    trigger_dead_time = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    frame_time = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    gain_setting = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    saturation_value = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    underload_value = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    number_of_cycles = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    sensor_material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    sensor_thickness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    threshold_energy = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXxraylens(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                An X-ray lens, typically at a synchrotron X-ray beam line.              Based on
        information provided by Gerd Wellenreuther (DESY).
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    cylinder_orientation = SubSection(
        sub_section=SectionProxy('NXnote'),
        repeats=True,
        )

    lens_geometry = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    symmetric = SubSection(
        sub_section=SectionProxy('NX_BOOLEAN'),
        repeats=True,
        )

    cylindrical = SubSection(
        sub_section=SectionProxy('NX_BOOLEAN'),
        repeats=True,
        )

    focus_type = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    lens_thickness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    lens_length = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    curvature = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    aperture = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    number_of_lenses = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    lens_material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    gas = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    gas_pressure = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXfresnel_zone_plate(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        A fresnel zone plate
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    TRANSFORMATIONS = SubSection(
        sub_section=SectionProxy('NXtransformations'),
        repeats=True,
        )

    focus_parameters = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    outer_diameter = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    outermost_zone_width = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    central_stop_diameter = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    fabrication = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    zone_height = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    zone_material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    zone_support_material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    central_stop_material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    central_stop_thickness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    mask_thickness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    mask_material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    support_membrane_material = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    support_membrane_thickness = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXorientation(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                legacy class - recommend to use :ref:`NXtransformations` now
        Description for a general orientation of a component - used by :ref:`NXgeometry`
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    GEOMETRY = SubSection(
        sub_section=SectionProxy('NXgeometry'),
        repeats=True,
        )

    value = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXevent_data(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                NXevent_data is a special group for storing data from neutron     detectors in
        event mode.  In this mode, the detector electronics     emits a stream of
        detectorID, timestamp pairs. With detectorID     describing the detector element
        in which the neutron was detected     and timestamp the timestamp at which the
        neutron event was     detected. In NeXus detectorID maps to event_id,
        event_time_offset     to the timestamp.

        As this kind of data is common at pulsed neutron     sources, the timestamp is
        almost always relative to the start of a     neutron pulse. Thus the pulse
        timestamp is recorded too together     with an index in the event_id,
        event_time_offset pair at which data for     that pulse starts. At reactor source
        the same pulsed data effect     may be achieved through the use of choppers or in
        stroboscopic     measurement setups.

        In order to make random access to timestamped data     faster there is an optional
        array pair of     cue_timestamp_zero and cue_index. The cue_timestamp_zero will
        contain courser timestamps then in the time array, say     every five minutes. The
        cue_index will then contain the     index into the event_id,event_time_offset pair
        of arrays for that     courser cue_timestamp_zero.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    event_time_offset = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    event_id = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    event_time_zero = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    event_index = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    pulse_height = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    cue_timestamp_zero = SubSection(
        sub_section=SectionProxy('NX_DATE_TIME'),
        repeats=True,
        )

    cue_index = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXspin_rotator(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        definition for a spin rotator.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    read_Bfield_current = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    read_Bfield_voltage = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    read_Efield_current = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    read_Efield_voltage = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    beamline_distance = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    set_Bfield_current = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    set_Efield_voltage = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )


class NXsolenoid_magnet(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        definition for a solenoid magnet.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    read_current = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    read_voltage = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    beamline_distance = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    set_current = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )


class NXsolid_geometry(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                the head node for constructively defined geometry
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    QUADRIC = SubSection(
        sub_section=SectionProxy('NXquadric'),
        repeats=True,
        )

    OFF_GEOMETRY = SubSection(
        sub_section=SectionProxy('NXoff_geometry'),
        repeats=True,
        )

    CSG = SubSection(
        sub_section=SectionProxy('NXcsg'),
        repeats=True,
        )


class NXcxi_ptycho(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                Application definition for a ptychography experiment, compatible with CXI from
        version 1.6.

        This is compatible with CXI from version 1.6 if this application definition
        is put at the top "entry" level. Above this a "cxi_version" field should be
        defined. The CXI format is name based, rather than class based, and so it is
        important                 to pay attention to the naming convention to be CXI
        compatible. There are duplications due to the format merger. These should be
        achieved by linking,                  with hdf5 Virtual Dataset being used to
        restructure any data that needs to be remapped. To be fully CXI compatible, all
        units (including energy) must be in SI units.

        An example here is that CXI expects the data to always to have shape
        (npts_x*npts_y, frame_size_x, frame_size_y). For nexus this is only true for
        arbitrary scan paths                 with raster format scans taking shape
        (npts_x, npts_y, frame_size_x, frame_size_y).
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    entry_1 = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )

    DATA = SubSection(
        sub_section=SectionProxy('NXdata'),
        repeats=True,
        )

    data_1 = SubSection(
        sub_section=SectionProxy('NXcollection'),
        repeats=True,
        )

    sample_1 = SubSection(
        sub_section=SectionProxy('NXsample'),
        repeats=True,
        )


class NXcsg(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                constructive solid geometry NeXus class, using :ref:`NXquadric`     and
        :ref:`NXoff_geometry`.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    a = SubSection(
        sub_section=SectionProxy('NXcsg'),
        repeats=True,
        )

    b = SubSection(
        sub_section=SectionProxy('NXcsg'),
        repeats=True,
        )

    operation = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    geometry = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXquadric(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        definition of a quadric surface.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    parameters = SubSection(
        sub_section=SectionProxy('NX_NUMBER'),
        repeats=True,
        )

    surface_type = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    depends_on = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )


class NXsnshisto(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        This is a definition for histogram data from Spallation Neutron Source (SNS) at
        ORNL.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    ENTRY = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXsnsevent(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        This is a definition for event data from Spallation Neutron Source (SNS) at ORNL.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    ENTRY = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )


class NXseparator(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        definition for an electrostatic separator.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    read_Bfield_current = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    read_Bfield_voltage = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    read_Efield_current = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    read_Efield_voltage = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    beamline_distance = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    set_Bfield_current = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    set_Efield_voltage = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )


class NXquadrupole_magnet(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        definition for a quadrupole magnet.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    read_current = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    read_voltage = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    beamline_distance = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    set_current = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )


class NXelectrostatic_kicker(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        definition for a electrostatic kicker.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    read_current = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    read_voltage = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    beamline_distance = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    timing = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    set_current = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    set_voltage = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )


class NXmagnetic_kicker(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
        definition for a magnetic kicker.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    read_current = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    read_voltage = SubSection(
        sub_section=SectionProxy('NXlog'),
        repeats=True,
        )

    description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    beamline_distance = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    timing = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    set_current = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    set_voltage = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )


class NXcontainer(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                State of a container holding the sample under investigation.
        A container is any object in the beam path which absorbs the beam and
        whose contribution to the overall attenuation/scattering needs to be
        determined to process the experimental data. Examples of containers
        include glass capillary tubes, vanadium cans, windows in furnaces or
        diamonds in a Diamond Anvil Cell. The following figures show a complex
        example of a container:                                  .. figure::
        container/ComplexExampleContainer.png                                        A
        hypothetical capillary furnace. The beam passes from left to right
        (blue dashes), passing through window 1, then window 2, before
        passing through the downstream wall of the capillary. It is then
        scattered by the sample with scattered beams passing through the
        upstream wall of the capillary, then windows 4 and 5. As part of the
        corrections for a PDF experiment it is necessary to subtract the PDF
        of the empty container (i.e. each of the windows and the capillary).
        To calculate the PDF of the empty container it is necessary to have
        the measured scattering data and to know the nature (e.g. density,
        elemental composition, etc.) of the portion of the container which
        the beam passed through.                                     .. figure::
        container/ComplexContainerBeampath.png                                        A
        complete description of the shapes of the container elements with
        their orientation relative to the beam and also information on
        whether they are upstream or downstream of the sample is also
        therefore important. For example, although the windows 2 and 4 have
        the same shape, the path taken through them by the beam is very
        different and this needs to be modelled. Furthermore, it is not
        inconceivable that windows might move during an experiment and thus
        the changes to the beampath would need to be accounted for.
        This class encodes the position of the container with respect to the
        sample and allows the calculation of the beampath through the container.
        It also includes sufficient data to model beam absorption of the
        container and a link to a dataset containing a measurement of the
        container with nothing inside, to allow data corrections (at a specific
        beam energy/measurement time) to be made.
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    beam = SubSection(
        sub_section=SectionProxy('NXbeam'),
        repeats=True,
        )

    shape = SubSection(
        sub_section=SectionProxy('NXshape'),
        repeats=True,
        )

    orientation = SubSection(
        sub_section=SectionProxy('NXtransformations'),
        repeats=True,
        )

    name = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    description = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    chemical_formula = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    density = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    packing_fraction = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )

    relative_molecular_mass = SubSection(
        sub_section=SectionProxy('NX_FLOAT'),
        repeats=True,
        )


class NXspecdata(MSection):

    m_def = Section(
        validate=False,
        )

    nxp_name = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_extends = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_type = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_category = Quantity(
        type=str,
        shape=[],
        description='''

        ''',)

    nxp_documentation = Quantity(
        type=str,
        shape=[],
        description='''
                DEPRECATED: This definition will be removed by 2022.  Not for new use.

        Data collected by SPEC control and data acquisition software

        SPEC [#]_ is software for instrument control       and data acquisition in X-ray
        diffraction experiments.              .. [#] SPEC: https://certif.com
        ''',)

    nxd_required = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_recommended = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    nxd_deprecated = Quantity(
        type=bool,
        shape=[],
        description='''

        ''',)

    ENTRY = SubSection(
        sub_section=SectionProxy('NXentry'),
        repeats=True,
        )

    default = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    HDF5_Version = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    h5py_version = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    SPEC_file = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    SPEC_date = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    SPEC_epoch = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )

    SPEC_comments = SubSection(
        sub_section=SectionProxy('NX_CHAR'),
        repeats=True,
        )

    SPEC_num_headers = SubSection(
        sub_section=SectionProxy('NX_INT'),
        repeats=True,
        )


m_package.__init_metainfo__()None