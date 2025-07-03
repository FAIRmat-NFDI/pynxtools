# A primer on NeXus

NeXus is a common data exchange format initially developed for neutron, X-ray, and muon experiments. Within FAIRmat we extensively extended the format to cover a range of experiments with major support for APM, ARPES, XPS, and optical spectroscopy, but we also give advice and guidance for developing standards for other formats as well.

## What is NeXus?

Sometimes, NeXus is seen as writing data to some form of file in HDF5 format. While this is partly true, NeXus is independent of the actual storage format, but is typically written into an HDF5 file.

But what is NeXus then? It is the conceptual layer above the file structure. It is a contract on which data has to be present and how to name them in a given dataset. Hence, the use of NeXus helps to make data FAIR. It especially covers the interoperability and reproducibility part of research data.

!!! info "NeXus path notations"

    There are several methods for referencing concepts or data paths within NeXus:

    - **Concept Path Notation:** This notation describes the hierarchical structure of NeXus concepts using class names. For example, `NXexperiment:/NXentry/NXinstrument/NXdetector` indicates the creation of a new NXdetector class within the NXexperiment concept. This path typically forms automatically when an application definition extends a base class's fields.

    - **Instance Path Notation:** It represents the actual location of a field or group in a NeXus data instance (e.g., an HDF5 file). An example is `my_file.nxs:/entry/instrument/detector`.

    - **Combined Notation:** In pynxtools, we sometimes use templates and configuration files to match data instances from other sources to the terms defined in NeXus application definitions and base classes. We represent these NeXus concepts using a mixed notation, where uppercase indicates a selectable (part of the) name and lowercase a fixed name. Examples include `NXexperiment:ENTRY[my_experiment.nxs:entry]/INSTRUMENT[instrument]/DETECTOR[detector]` and `NXexperiment:ENTRY[my_experiment.nxs:entry]/my_INSTRUMENT[my_instrument]/DETECTOR[detector]`. In this notation, we combine concept (outside the square brackets) and instance paths (inside the square brackets). The leftmost entries may include the NeXus class or file reference.

## NeXus as a tool for FAIR data

If you want to build data according to the FAIR principles, you can think of NeXus fulfilling the interoperability and reproducibility part. As NeXus defines commonly used standards for describing experiments in materials science, any data that is written according to the NeXus standard can be compared to any other such data. NeXus application definitions, which exactly define which data is required to describe a given experiments, help to reproduce experiments.

If integrated into a research data management (RDM) platform, the findable and accessible part of FAIR can also be fulfilled. We integrate NeXus into the RDM we are developing in FAIRmat: **NOMAD**. Experimental data following an NeXus application definition can easily be uploaded and is recognized by NOMAD's search system. If you want to learn more about uploading NeXus data to NOMAD, please refer to the [NeXus to NOMAD](../../tutorial/nexus-to-nomad.md) tutorial of this documentation. Since NeXus follows a rigorously defined structure, NOMAD can enabling semantic searches, making it easy to find and access NeXus data.