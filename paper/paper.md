---
title: 'Pynxtools: A framework for generating NeXus files from raw file formats.'
tags:
  - Python
  - nexus
  - data modeling
  - file format
  - data parsing
authors:
  - name: Adrian M. Price-Whelan
    orcid: 0000-0000-0000-0000
    equal-contrib: true
    affiliation: "1, 2" # (Multiple affiliations must be quoted)
  - name: Author Without ORCID
    equal-contrib: true # (This is how you can denote equal contributions between multiple authors)
    affiliation: 2
  - name: Author with no affiliation
    corresponding: true # (This is how to denote the corresponding author)
    affiliation: 3
  - given-names: Ludwig
    dropping-particle: van
    surname: Beethoven
    affiliation: 3
affiliations:
 - name: Lyman Spitzer, Jr. Fellow, Princeton University, United States
   index: 1
   ror: 00hx57361
 - name: Institution Name, Country
   index: 2
 - name: Independent Researcher, Country
   index: 3
date: 06 June 2025
bibliography: paper.bib

---

# Summary

Scientific data across experimental physics and materials science remains largely fragmented due to incompatible instrument-specific formats and diverse standardization practices. pynxtools is a Python software development framework with a CLI interface that standardizes data conversion for scientific experiments in materials characterization to NeXus HDF5 format [@konnecke2015nexus] across diverse scientific domains. pynxtools provides a fixed set of NeXus application definitions that ensures convergence and alignment in data specifications across photoemission spectroscopy, electron microscopy [@eric_prestat_2025_15548174], atom probe tomography, optical spectroscopy, scanning probe microscopy, and X-ray diffraction. Through its modular plugin architecture, pynxtools provides maps for instrument-specific raw data and electronic lab notebook metadata to these unified definitions, while performing validation to ensure data correctness and NeXus compliance. By simplifying the adoption of standardized application definitions, the framework enables true data interoperability and FAIR [@wilkinson2016fair; @jacobsen2020fair; @barker2022introducing] data management across multiple experimental techniques.

# Statement of need

Achieving FAIR (Findable, Accessible, Interoperable, and Reproducible) data principles in experimental physics and materials science requires consistent implementation of standardized data formats. While NeXus provides comprehensive data specifications for structured scientific data storage, pynxtools simplifies the implementation process for developers and researchers by providing guided workflows and automated validation to ensure complete compliance. Existing tools [@mkoennecke2024nexusformat; @Jemian2025prjemian] lack robust validation frameworks and provide insufficient guidance for proper NeXus adoption. pynxtools addresses this critical gap by providing an accessible framework that enforces complete NeXus application definition compliance through automated validation, detailed error reporting for missing required data points, and clear implementation pathways via configuration files and extensible plugins. This approach transforms NeXus from a complex specification into a practical solution, enabling researchers to achieve true data interoperability without deep technical expertise in the underlying standards.

# Dataconverter and validation (Sherjeel)

      * Mechanism to write an own reader, i.e. pynxtools-plugin mechanism and test frameworks, not mentioned to much about pynxtools-plugins
      * ELN Generator - one sentence or so

# NeXus reader and annotator (read\_nexus)

# NOMAD integration (schema, parser)

While pynxtools works as a standalone tool using the command line, it can also be integrated directly into Research Data Management Systems (RDMS). Out of the box, the package functions as a plugin within the NOMAD platform [@Scheidgen:2023], converting and parsing data from experiments. This enables experimental data in the NeXus format to be integrated into NOMAD's metadata model, making it searchable and interoperable with other data from theory and experiment. The plugin consists of several key components (so called entry points):

- Schema Package: The NeXus (meta)data definitions are expressed in XML using the NeXus Definition Language (NXDL), which in turn is defined using XSD. pynxtools converts this representation and extends NOMAD's internal data schema (called __Metainfo__) with these domain-specific quantities. pynxtools also connects the NeXus vocabulary to existing base sections in NOMAD — reusable, standardized building blocks used to represent common scientific concepts. This connection enables interoperability between NeXus-defined concepts and other standardized representations in NOMAD, such as those for sample synthesis or theoretical calculations.

- Data Converter: The __DataConverter__ as described above is also available in NOMAD. Thus, NOMAD users can directly convert their experimental data to NeXus using NOMAD's graphical interface. In addition to the capabilities already described, the internal __DataConverter__ class also handles NOMAD's electronic lab notebooks (ELNs) and converts these such that the manually inputted data can be converted to NeXus as well.

- Parser: The NOMAD parser module in pynxtools (__NexusParser__) reads NeXus HDF5 files and uses the structured data instances from these files to populate the NOMAD __Metainfo__ model with __Metainfo__ object instances as defined by the pynxtools schema package. This step enables ingestion of NeXus data directly into the NOMAD __Metainfo__ model.

- Normalization: Parsed data is post-processed using NOMAD's normalization pipeline. This includes automatic handling of units (via pint), linking references across sections (including sample and instrument identifiers defined elsewhere in NOMAD), and populating derived quantities needed for advanced search and visualization.

- App: pynxtools contains an integrated search application for NeXus data within NOMAD. This application, powered by Elasticsearch [@elasticsearch:2025], enables users to efficiently filter uploaded data based on various parameters, such as experiment type, upload timestamp, and other relevant quantities.

- Example Upload: The plugin includes a representative NOMAD upload (based on the NeXus application definition __NX_iv_temp__ describing temperature-dependent IV curve measurements), which exemplifies the entire workflow of pynxtools as a NOMAD package. This example upload details the conversion of data from experiments into NeXus files using the __DataConverter__, along with parsing them into the NOMAD archive. This example upload is designed for new users to understand the pynxtools workflow in NOMAD and serves as templates to adapt the plugin to new NeXus applications.


# Funding
The work is funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) - 460197019 (FAIRmat).

# Author contributions

# Acknowledgements

We acknowledge contributions from Brigitta Sipocz, Syrtis Major, and Semyeong
Oh, and support from Kathryn Johnston during the genesis of this project.

# References
