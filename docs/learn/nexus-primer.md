# A primer on NeXus

!!! danger "Work in progress"

    This part of the documentation is still being written and it might be confusing or incomplete.

NeXus is is a description of a common data exchange format initially developed for neutron, X-ray, and muon experiments. Within FAIRmat we extensively extended the format to cover a range of experiments with major support for APM, ARPES, XPS, and optical spectroscpy but we also give advice and guidance for developing standards for other formats as well.

!!! info "NeXus as a tool for FAIR data"

    NeXus is supported be the research data management platform NOMAD.
    Experimental data following an NeXus application definition can easily be uploaded and is recognized by NOMAD's search system.
    If you want to learn more about uploading NeXus data to NOMAD, please refer to the [NeXus to nomad](../tutorial/nexus-to-nomad.md) tutorial
    of this documentation.
    Accordingly, if you want to build data according to the FAIR principles, you can think of NeXus fulfilling the interoperability and
    reproducibility part and a research data management platform like NOMAD the findable and accessible part.

## What is NeXus?

Sometimes, NeXus is seen as writing data to some form of file in hdf5 format.
While this is partly true, NeXus is independent of the actual storage format but is typically written into an hdf5 file.

But what is NeXus then? It is the conceptual layer above the file structure.
It is a contract on which data has to be present and how to name them in a given dataset.
Hence, using NeXus participates in making data FAIR.
It especially covers the interoperability and reproducibility part of research data.

!!! info "NeXus path notations"

    There are several methods for referencing concepts or data paths within NeXus:

    - **Concept Path Notation:** This notation describes the hierarchical structure of NeXus concepts using class names. For example, `NXexperiment:/NXentry/NXinstrument/NXdetector` indicates the creation of a new NXdetector class within the NXexperiment concept. This path typically forms automatically when an application definition extends a base class's fields.

    - **Instance Path Notation:** It represents the actual location of a field or group in a NeXus data instance (e.g., an HDF5 file). An example is `my_file.nxs:/entry/instrument/detector`.

    - **Combined Notation:** This combines concept and instance paths. For example, `NXexperiment:/NXentry[my_file.nxs:entry]/NXinstrument[instrument]/NXdetector[detector]`. Here, concept paths are outside and instance paths within square brackets. The leftmost entries may include the NeXus class or file reference.

    - **Appdef Notation:** This format is used in application definitions, where uppercase indicates a selectable name and lowercase a fixed name. Examples include `NXexperiment:ENTRY[my_experiment.nxs:entry]/INSTRUMENT[instrument]/DETECTOR[detector]` and `NXexperiment:ENTRY[my_experiment.nxs:entry]/my_INSTRUMENT[my_instrument]/DETECTOR[detector]`.
