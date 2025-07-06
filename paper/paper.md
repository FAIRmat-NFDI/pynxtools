---
title: 'pynxtools: A framework for generating NeXus files from formats across disciplines.'
tags:
  - Python
  - NeXus
  - data modeling
  - file format
  - data parsing
  - data normalization
  - serialization
  - HDF5
authors:
  - given-names: Sherjeel
    surname: Shabih
    orcid: https://orcid.org/0009-0008-6635-4465
    affiliation: 1
    equal-contrib: true
  - given-names: Lukas
    surname: Pielsticker
    orcid: https://orcid.org/0000-0001-9361-8333
    affiliation: "1,3"
    equal-contrib: true
  - given-names: Florian
    surname: Dobener
    orcid: https://orcid.org/0000-0003-1987-6224
    affiliation: 1
  - given-names: Andrea
    surname: Albino
    orcid: https://orcid.org/0000-0001-9280-7431
    affiliation: 1
  - given-names: Theodore
    surname: Chang
    orcid: https://orcid.org/0000-0002-4911-0230
    affiliation: 1
  - given-names: Carola
    surname: Emminger
    orcid: https://orcid.org/0000-0003-4793-1809
    affiliation: "1, 5"
  - given-names: Lev
    surname: Ginzburg
    orcid: https://orcid.org/0000-0001-8929-1040
    affiliation: 1
  - given-names: Ron
    surname: Hildebrandt
    orcid: https://orcid.org/0000-0001-6932-604X
    affiliation: "1, 5"
  - given-names: Markus
    surname: Kühbach
    orcid: https://orcid.org/0000-0002-7117-5196
    affiliation: 1
  - given-names: José Antonio
    surname: Márquez Prieto
    orcid: https://orcid.org/0000-0002-8173-2566
    affiliation: 1
  - given-names: Rubel
    surname: Mozumder
    orcid: https://orcid.org/0009-0007-5926-6646
    affiliation: 1
  - given-names: Tommaso
    surname: Pincelli
    orcid: https://orcid.org/0000-0003-2692-2540
    affiliation: 4
  - given-names: Walid
    surname: Hetaba
    orcid: https://orcid.org/0000-0003-4728-0786
    affiliation: 3
  - given-names: Carlos-Andres
    surname: Palma
    orcid: https://orcid.org/0000-0001-5576-8496
    affiliation: "1, 6"
  - given-names: Marius
    surname: Grundmann
    orcid: https://orcid.org/0000-0001-7554-182X
  - given-names: Laurenz
    surname: Rettig
    orcid: https://orcid.org/0000-0002-0725-6696
    affiliation: 4
  - given-names: Christoph
    surname: Koch
    orcid: https://orcid.org/0000-0002-3984-1523
    affiliation: 1
  - given-names: Heiko B.
    surname: Weber
    orcid: https://orcid.org/0000-0002-6403-9022
    affiliation: 2
  - given-names: Markus
    surname: Scheidgen
    orcid: https://orcid.org/0000-0002-8038-2277
    affiliation: 1
  - given-names: Claudia
    surname: Draxl
    orcid: https://orcid.org/0000-0003-3523-6657
    affiliation: 1
  - given-names: Sandor
    surname: Brockhauser
    orcid: https://orcid.org/0000-0002-9700-4803
    affiliation: 1

affiliations:
  - name: Physics Department and CSMB, Humboldt-Universität zu Berlin, Berlin, Germany
    index: 1
    ror: 01hcx6992
  - name: Lehrstuhl für Angewandte Physik, Friedrich-Alexander-Universität Erlangen-Nürnberg, Erlangen, Germany
    index: 2
    ror: 00f7hpc57
  - name: Department Heterogeneous Reactions, Max Planck Institute for Chemical Energy Conversion, Mülheim an der Ruhr, Germany
    index: 3
    ror: 01y9arx16
  - name: Department of Physical Chemistry, Fritz Haber Institute of the Max Planck Society, Berlin, DE
    index: 4
    ror: 03k9qs827
  - name: Felix-Bloch-Institut für Festkörperphysik, Universität Leipzig, Leipzig, Germany
    index: 5
<<<<<<< HEAD
  - name: Institute of Physics, Chinese Academy of Sciences, Beijing, China
    index: 6
=======
    ror: 03s7gtk40
>>>>>>> f2c975e7 (Fixes)
date: 06 June 2025
bibliography: paper.bib

---

# Summary

Scientific data across experimental physics and materials science often lacks adherence to FAIR principles [@Wilkinson:2016; @Jacobsen:2020; @Barker:2022; @Wilkinson:2025] due to incompatible instrument-specific formats and diverse standardization practices. pynxtools is a Python software development framework with a command line interface (CLI) that standardizes data conversion for scientific experiments in materials characterization to the NeXus format [@Koennecke:2015; @Koennecke:2006; @Klosowski:1997] across diverse scientific domains. NeXus uses NeXus application definitions as their data storage specifications. pynxtools provides a fixed, versioned set of NeXus application definitions that ensures convergence and alignment in data specifications across atom probe tomography, electron microscopy, optical spectroscopy, photoemission spectroscopy, scanning probe microscopy, X-ray diffraction. Through its modular plugin architecture, pynxtools provides maps for instrument-specific raw data, and electronic lab notebook metadata, to these unified definitions, while performing validation to ensure data correctness and NeXus compliance. By simplifying the adoption of standardized application definitions, the framework enables true data interoperability and FAIR data management across multiple experimental techniques.

# Statement of need

Achieving FAIR (Findable, Accessible, Interoperable, and Reproducible) data principles in experimental physics and materials science requires consistent implementation of standardized data formats. NeXus provides comprehensive data specifications for structured storage of scientific data. pynxtools simplifies the use of NeXus for developers and researchers by providing guided workflows and automated validation to ensure complete compliance. Existing tools [@Koennecke:2024; @Jemian:2025] provide solutions with individual capabilities, but none offers a comprehensive end-to-end workflow for proper NeXus adoption. pynxtools addresses this critical gap by providing a framework that enforces complete NeXus application definition compliance through automated validation, detailed error reporting for missing required data points, and clear implementation pathways via configuration files and extensible plugins. This approach transforms NeXus from a complex specification into a practical solution, enabling researchers to achieve true data interoperability without deep technical expertise in the underlying standards.

# Dataconverter and validation

The __dataconverter__, core module of pynxtools, combines instrument output files and data from electronic lab notebooks into NeXus-compliant HDF5 files. The converter performs three key operations: reading experimental data through specialized readers, validating against NeXus application definitions to ensure compliance with existence, shape, and format constraints, and writing valid NeXus/HDF5 output files.

The __dataconverter__ provides a CLI to produce NeXus files where users can use one of the built-in readers for generic functionality or technique-specific reader plugins, distributed as separate Python packages.

For developers, the __dataconverter__ provides an abstract __reader__ class for building plugins that process experiment-specific formats and populate the NeXus specification. It passes a __Template__, a subclass of Python’s dict, to the __reader__ as a form to fill. The __Template__ ensures structural compliance with the chosen NeXus application definition and organizes data by NeXus's required, recommended, and optional levels.

The __dataconverter__ validates __reader__ output against the selected NeXus application definition, checking required fields, complex dependencies (like inheritance and nested group rules), and data integrity (type, shape, constraints). It reports errors for invalid required fields and emits CLI warnings for unmatched or invalid data, aiding practical NeXus file creation.

All reader plugins are tested using the pynxtools.testing suite, which runs automatically via GitHub CI to ensure compatibility with the dataconverter, the NeXus specification, and integration across plugins.

The dataconverter includes an ELN generator that creates either a fillable YAML file or a NOMAD [@Scheidgen:2023] ELN schema based on a selected NeXus application definition.

# NeXus reader and annotator

__read_nexus__ enables semantic access to NeXus files by linking data items to NeXus concepts, allowing applications to locate relevant data without hardcoding file paths. It supports concept-based queries that return all data items associated with a specific NeXus vocabulary term. Each data item is annotated by traversing its group path and connecting it to its corresponding NeXus concept, including inherited definitions.

Items not part of the NeXus schema are explicitly marked as such, aiding in validation and debugging. Targeted documentation of individual data items is supported through path-specific annotation. The tool also identifies and summarizes the file’s default plottable data based on the NXdata definition.

# NOMAD integration

While pynxtools works as a standalone tool, it can also be integrated directly into Research Data Management Systems (RDMS). Out of the box, the package functions as a plugin within the NOMAD platform. This enables data in the NeXus format to be integrated into NOMAD's metadata model, making it searchable and interoperable with other data from theory and experiment. The plugin consists of several key components (so called entry points):

- Schema Package: pynxtools extends NOMAD's Metainfo data schema by integrating NeXus definitions, adding NeXus-specific quantities and enabling interoperability with NOMAD through links to other standardized data representations.

- Dataconverter: The __dataconverter__ is integrated into NOMAD, making NeXus conversion accessible via their GUI. The __dataconverter__ also processes manually entered NOMAD ELN data in the conversion.

- Parser: The NOMAD parser module in pynxtools (__NexusParser__) extracts structured data from NeXus HDF5 files to populate NOMAD with __Metainfo__ object instances as defined by the pynxtools schema package. This enables ingestion of NeXus data directly into NOMAD.

- Normalization: Parsed data is post-processed using NOMAD's normalization pipeline. This includes automatic handling of units, linking references (including sample and instrument identifiers defined elsewhere in NOMAD), and populating derived quantities needed for advanced search and visualization.

- App: pynxtools contains an integrated search application for NeXus data within NOMAD, powered by Elasticsearch [@elasticsearch:2025]. This provides a search dashboard for users, enabling them to efficiently filter uploaded data based on parameters like experiment type, upload timestamp, and other relevant quantities.

- Example Upload: The entire pynxtools workflow (conversion, parsing, and normalization) is exemplified in a representative NOMAD upload shipped with the package. This example helps new users understand the workflow and serves as a template to adapt the plugin to new NeXus applications.

# Funding
The work is funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) - 460197019 (FAIRmat).

# Acknowledgements

We acknowledge the following software packages our package depends on: [@H5py:2008], [@Harris:2020], [@Click:2014], [@Druskat:2021], [@Hoyer:2017], [@Hoyer:2025], [@Pandas:2020], [@McKinney:2010], [@Behnel:2005], [@Clarke:2019], [@Hjorth:2017], [@Pint:2012].

# References
