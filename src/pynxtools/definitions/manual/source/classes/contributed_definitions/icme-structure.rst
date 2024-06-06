.. _Icme-Structure:

==============================================
Integrated Computational Materials Engineering
==============================================

.. index::
   IcmeMsModels

.. _IcmeMsModels:

Application definitions for ICME models
#######################################

It is important to embrace the large research community of materials engineers
as they are frequent users of electron microscopy and atom probe microscopy.
ICME is an abbreviation for Integrated Computational Materials Engineering, which is
a design strategy and workflow whereby physics-based modelling of microstructure
evolution is used to understand the relations between the microstructure and
its technologically relevant descriptors to understand and tailor properties of materials.

The following application definitions are proposed to support the discussion on how
materials-engineering-specific data schemas can connect to or be mapped on
concepts which are equally modellable with NeXus:

    :ref:`NXms`:
        An application definition for arbitrary spatiotemporally resolved simulations.

    :ref:`NXms_recon`:
        A base class for documenting results of reconstructed microstructures.

    :ref:`NXms_score_config`, :ref:`NXms_score_results`:
        A specific example of an application definition for documenting the
        configuration and results respectively of a computer simulation with
        the static recrystallization cellular automata model SCORE.
