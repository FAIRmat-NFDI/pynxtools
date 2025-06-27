# Getting started

This is the entry point for anybody that is new to the NeXus data format and to FAIRmat/NOMAD. It serves as a guide to getting started with the `pynxtools` software.

## What should you should know before reading this guide?

Nothing!

However, to get started, it does not hurt to read the following explanations:

- [A primer on NeXus](learn/nexus-primer.md)
- [What is FAIR data](https://www.nature.com/articles/sdata201618)

## What you will know at the end of this guide?

You will have

- a basic understanding of what this software is about and which capabilities it contains
- how the different software tools are connected which each other.

## What is NeXus?

NeXus is a





For a more detailed description on the general principles of NeXus we recommend reading our [learning page for NeXus](../learn/nexus-primer.md) or the [official NeXus user manual](https://manual.nexusformat.org/user_manual.html).

## What is FAIRmat?

## What is NOMAD?

NOMAD is a research data management system for making materials science data searchable and publishable.

NOMAD is developed by the FAIRmat consortium which is a consortium of the German National Research Data Infrastructure (NFDI).

## What is pynxtools?

It allows to develop ontologies and to create ontological instances based on the [NeXus format](https://www.nexusformat.org/).

`pynxtools` is a parser for combining various instrument output formats and electronic lab notebook (ELN) formats into an [HDF5](https://support.hdfgroup.org/HDF5/) file according to NeXus application definitions.

 who want to standardize their research data by converting their research data into a NeXus standardized format.

## How can I install pynxtools? How can I contribute?

- [Installation tutorial](./tutorial/installation.md)
- [Development tutorial](./tutorial/contributing.md)

## Does this software require NOMAD or NOMAD OASIS?

No. The data files produced here can be uploaded to NOMAD. Therefore, this tool acts as the framework to design schemas and instances of data within the NeXus universe. It can, however, be used as a NOMAD plugin to parse nexus files, please see the section below for details.

## How to use pynxtools with NOMAD

To use pynxtools with NOMAD, simply install it in the same environment as the `nomad-lab` package. NOMAD will recognize pynxtools as a plugin automatically and offer automatic parsing of `.nxs` files. In addition, NOMAD will install a schema for NeXus application definitions. By default, `pynxtools` is already included in the NOMAD [production]https://nomad-lab.eu/prod/v1/gui/ and [staging](https://nomad-lab.eu/prod/v1/staging/gui/) deployments.

NeXus is supported be the research data management platform NOMAD. Experimental data following an NeXus application definition can easily be uploaded and is recognized by NOMAD's search system. If you want to learn more about uploading NeXus data to NOMAD, please refer to the NeXus to NOMAD tutorial of this documentation. Accordingly, if you want to build data according to the FAIR principles, you can think of NeXus fulfilling the interoperability and reproducibility part and a research data management platform like NOMAD the findable and accessible part.

!!! info "A note on FAIR data"

    FAIRmat's contribution to the existing NeXus standard, together with the tools provided through `pynxtools`, enable scientists and research groups working with data, as well as helping communities implement standardized FAIR research data.

    We consider this package useful for meeting the following FAIR principle as defined in [FAIR Principles: Interpretations and Implementation Considerations](https://direct.mit.edu/dint/article/2/1-2/10/10017/FAIR-Principles-Interpretations-and-Implementation): F2-4, I2-I3, and R1.

## Where to go next?

We suggest you have a look at one of our tutorials for [installing `pynxtools`](tutorial/installation.md) and [how go convert data to NeXus](tutorial/converting-data-to-nexus.md).