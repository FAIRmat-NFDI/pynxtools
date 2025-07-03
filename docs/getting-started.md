# Getting started

This is the entry point for anybody that is new to the NeXus data format and to FAIRmat/NOMAD. It serves as a guide to getting started with the `pynxtools` software.

## What should you should know before reading this guide?

Nothing!

However, to get started, it does not hurt to read the following explanations:

- [A primer on NeXus](learn/nexus/nexus-primer.md)
- [What is FAIR data](https://www.nature.com/articles/sdata201618)

## What you will know at the end of this guide?

You will have

- a basic understanding of what this software is about and which capabilities it contains
- how the different software tools are connected which each other.

## What is NeXus?

NeXus is a framework for describing and standardizing experimental data. NeXus provides domain-specific rules for organizing data within files in addition to a dictionary of well-defined domain-specific field concepts. It helps communities to agree on terms to describe their data, acting as a contract on which data has to be present and how to name them in a given dataset.

For a more detailed description on the general principles of NeXus we recommend:

- [our learning page for NeXus](learn/nexus/nexus-primer.md)
- [the official NeXus manual](https://manual.nexusformat.org/)

## What is FAIRmat?

FAIRmat is one of the consortia of the German National Research Data Infrastructure (NFDI). It is tasked with building a FAIR data infrastructure for condensed-matter physics and the chemical physics of solids.

## What is NOMAD?

Within FAIRmat, we develop **NOMAD**: an open source research data management system for making materials science data searchable and publishable. NOMAD can host all kinds of data from materials science - including, but not limited to, NeXus data.

- [NOMAD Homepage](https://nomad-lab.eu/)
- [NOMAD documentation](https://nomad-lab.eu/prod/v1/staging/docs/)

## What is pynxtools?

`pynxtools` is our main software tool for end-to-end handling of data from experiments using NeXus. It contains a parser for combining various instrument output formats and electronic lab notebook (ELN) formats into an [HDF5](https://support.hdfgroup.org/HDF5/) file according to NeXus application definitions. It provides validation against these NeXus definitions and can be used to annotate existing NeXus files with semantic meaning.

`pynxtools` can be used for standalone NeXus conversion, but it can also be used as a _plugin_ to NOMAD, extending NOMAD schemas and parsing capabilities with NeXus-specific capabilities.

## How can I install pynxtools? How can I contribute?

- [Installation tutorial](./tutorial/installation.md)
- [Development tutorial](./tutorial/contributing.md)

## Does `pynxtools` require NOMAD or NOMAD OASIS?

No. You can use `pynxtools` perfectly fine as a standalone tool for converting data from experiments to NeXus-compliant files. Therefore, this tool acts as the framework to design instances of data within the NeXus universe. The software _can_, however, be used as a **NOMAD plugin** to parse NeXus files, please see the section below for details.

## How to use `pynxtools` with NOMAD

NeXus is supported be the research data management platform NOMAD. Experimental data following an NeXus application definition can easily be uploaded to NOMAD and is recognized by NOMAD's search system. If you want to learn more about uploading NeXus data to NOMAD, please refer to the [NeXus to NOMAD tutorial](./tutorial/nexus-to-nomad.md) of this documentation.

To use the `pynxtools` Python package with NOMAD, simply install it in the same environment as the `nomad-lab` package. NOMAD will recognize pynxtools as a plugin automatically and offer automatic parsing of `.nxs` files. In addition, NOMAD will install a schema for NeXus application definitions. By default, `pynxtools` is already included in the NOMAD [production]https://nomad-lab.eu/prod/v1/gui/ and [staging](https://nomad-lab.eu/prod/v1/staging/gui/) deployments.

!!! info "A note on FAIR data"

    FAIRmat's contribution to the existing NeXus standard, together with the tools provided through `pynxtools`, enable scientists and research groups working with data, as well as helping communities implement standardized FAIR research data.

    You can think of NeXus fulfilling the interoperability and reproducibility part and a research data management platform like NOMAD the findable and accessible part.

    We consider `pynxtools` particularly useful for meeting the following FAIR principle as defined in [FAIR Principles: Interpretations and Implementation Considerations](https://direct.mit.edu/dint/article/2/1-2/10/10017/FAIR-Principles-Interpretations-and-Implementation): F2-4, I2-I3, and R1.

## Where to go next?

We suggest you have a look at one of our tutorials:

- [installing `pynxtools`](tutorial/installation.md)
- [how go convert data to NeXus](tutorial/converting-data-to-nexus.md)