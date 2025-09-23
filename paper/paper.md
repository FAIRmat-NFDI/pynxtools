---
title: 'pynxtools: A Python framework for generating and validating NeXus files in experimental data workflows'
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
    affiliation: "1,2"
    equal-contrib: true
  - given-names: Florian
    surname: Dobener
    orcid: https://orcid.org/0000-0003-1987-6224
    affiliation: "1,3"
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
    affiliation: "1, 4"
  - given-names: Lev
    surname: Ginzburg
    orcid: https://orcid.org/0000-0001-8929-1040
    affiliation: 1
  - given-names: Ron
    surname: Hildebrandt
    orcid: https://orcid.org/0000-0001-6932-604X
    affiliation: "1, 4"
  - given-names: Markus
    surname: Kühbach
    orcid: https://orcid.org/0000-0002-7117-5196
    affiliation: 1
  - given-names: Rubel
    surname: Mozumder
    orcid: https://orcid.org/0009-0007-5926-6646
    affiliation: 1
  - given-names: Tommaso
    surname: Pincelli
    orcid: https://orcid.org/0000-0003-2692-2540
    affiliation: 5
  - given-names: Martin
    surname: Aeschlimann
    orcid: https://orcid.org/0000-0003-3413-5029
    affiliation: 3
  - given-names: Marius
    surname: Grundmann
    orcid: https://orcid.org/0000-0001-7554-182X
    affiliation: 4
  - given-names: Walid
    surname: Hetaba
    orcid: https://orcid.org/0000-0003-4728-0786
    affiliation: 2
  - given-names: Carlos-Andres
    surname: Palma
    orcid: https://orcid.org/0000-0001-5576-8496
    affiliation: "1, 6"
  - given-names: Laurenz
    surname: Rettig
    orcid: https://orcid.org/0000-0002-0725-6696
    affiliation: 5
  - given-names: Markus
    surname: Scheidgen
    orcid: https://orcid.org/0000-0002-8038-2277
    affiliation: 1
  - given-names: José Antonio
    surname: Márquez Prieto
    orcid: https://orcid.org/0000-0002-8173-2566
    affiliation: 1
  - given-names: Claudia
    surname: Draxl
    orcid: https://orcid.org/0000-0003-3523-6657
    affiliation: 1
  - given-names: Sandor
    surname: Brockhauser
    orcid: https://orcid.org/0000-0002-9700-4803
    affiliation: 1
  - given-names: Christoph
    surname: Koch
    orcid: https://orcid.org/0000-0002-3984-1523
    affiliation: 1
  - given-names: Heiko B.
    surname: Weber
    orcid: https://orcid.org/0000-0002-6403-9022
    affiliation: 7

affiliations:
  - name: Physics Department and CSMB, Humboldt-Universität zu Berlin, Zum Großen Windkanal 2, D-12489 Berlin, Germany
    index: 1
    ror: 01hcx6992
  - name: Department Heterogeneous Reactions, Max Planck Institute for Chemical Energy Conversion, Stiftstraße 34-36, D-45470 Mülheim an der Ruhr, Germany
    index: 2
    ror: 01y9arx16
  - name: Department of Physics, RPTU Kaiserslautern-Landau, Erwin-Schrödinger-Str. 46, D-67663 Kaiserslautern, Germany
    index: 3
    ror: 01qrts582
  - name: Felix Bloch Institute for Solid State Physics, Leipzig University, Linnestr. 5, D-04103 Leipzig, Germany
    index: 4
    ror: 03s7gtk40
  - name: Department of Physical Chemistry, Fritz Haber Institute of the Max Planck Society, Faradayweg 4-6, D-14195 Berlin, DE
    index: 5
    ror: 03k9qs827
  - name: Institute of Physics, Chinese Academy of Sciences, No.8, 3rd South Street, Zhongguancun, Haidian District, Beijing, China
    index: 6
    ror: 05cvf7v30
  - name: Lehrstuhl für Angewandte Physik, Friedrich-Alexander-Universität Erlangen-Nürnberg, Staudtstr. 7, D-91058 Erlangen, Germany
    index: 7
    ror: 00f7hpc57

date: 07 July 2025
bibliography: paper.bib

---

# Summary

Scientific data across physics, materials science, and materials engineering often lacks adherence to FAIR principles [@Wilkinson:2016; @Jacobsen:2020; @Barker:2022; @Wilkinson:2025] due to incompatible instrument-specific formats and diverse standardization practices. `pynxtools` is a Python software development framework with a command line interface (CLI) that standardizes data conversion for scientific experiments in materials science to the NeXus format [@Koennecke:2015; @Koennecke:2006; @Klosowski:1997] across diverse scientific domains. NeXus defines data storage specifications for different experimental techniques through application definitions.  `pynxtools` provides a fixed, versioned set of NeXus application definitions that ensures convergence and alignment in data specifications across, among others, atom probe tomography, electron microscopy, optical spectroscopy, photoemission spectroscopy, scanning probe microscopy, and X-ray diffraction. Through its modular plugin architecture `pynxtools` provides conversion of data and metadata from instruments and electronic lab notebooks to these unified definitions, while performing validation to ensure data correctness and NeXus compliance. `pynxtools` can be integrated directly into Research Data Management Systems (RDMS) to facilitate parsing and normalization. We detail one example for the RDM system NOMAD. By simplifying the adoption of NeXus, the framework enables true data interoperability and FAIR data management across multiple experimental techniques.

# Statement of need

Achieving FAIR (Findable, Accessible, Interoperable, and Reproducible) data principles in experimental physics and materials science requires consistent implementation of standardized data formats. NeXus provides comprehensive data specifications for structured storage of scientific data. `pynxtools` simplifies the use of NeXus for developers and researchers by providing guided workflows and automated validation to ensure complete compliance. Existing solutions [@Koennecke:2024; @Jemian:2025] provide individual capabilities, but none offers a comprehensive end-to-end workflow for proper NeXus adoption. `pynxtools` addresses this critical gap by providing a framework that enforces complete NeXus application definition compliance through automated validation, detailed error reporting for missing required data points, and clear implementation pathways via configuration files and extensible plugins. This approach transforms NeXus from a complex specification into a practical solution, enabling researchers to achieve true data interoperability without deep technical expertise in the underlying standards.

# Dataconverter and validation

The `dataconverter`, core module of pynxtools, combines instrument output files and data from electronic lab notebooks into NeXus-compliant HDF5 files. The converter performs three key operations: extracting experimental data through specialized readers, validating against NeXus application definitions to ensure compliance with existence and format constraints, and writing valid NeXus/HDF5 output files.

The `dataconverter` provides a command-line interface (CLI) for generating NeXus files, supporting both built-in readers for general-purpose functionality and technique-specific reader plugins, which are distributed as separate Python packages.

For developers, the `dataconverter` provides an abstract `reader` class for building plugins that process experiment-specific formats and populate the NeXus specification. It passes a `Template`, a subclass of Python’s dictionary, to the `reader` as a form to fill. The `Template` ensures structural compliance with the chosen NeXus application definition and organizes data by NeXus's required, recommended, and optional levels.

The `dataconverter` validates `reader` output against the selected NeXus application definition, checking for instances of required concepts, complex dependencies (like inheritance and nested group rules), and data integrity (type, shape, constraints). It validates required concepts, reporting errors for any violations, and issues warnings for invalid data, facilitating reliable and practical NeXus file generation.

All reader plugins are tested using the `pynxtools.testing` suite, which runs automatically via GitHub CI to ensure compatibility with the dataconverter, the NeXus specification, and integration across plugins.

The dataconverter includes `eln_mapper` that creates either a fillable `YAML` file or a `NOMAD` [@Scheidgen:2023] ELN schema based on a selected NeXus application definition.

# NeXus reader and annotator

`read_nexus` enables semantic access to NeXus files by linking data items to NeXus concepts, allowing applications to locate relevant data without hardcoding file paths. It supports concept-based queries that return all data items associated with a specific NeXus vocabulary term. Each data item is annotated by traversing its group path and resolving its corresponding NeXus concept, included inherited definitions.

Items not part of the NeXus schema are explicitly marked as such, aiding in validation and debugging. Targeted documentation of individual data items is supported through path-specific annotation. The tool also identifies and summarizes the file’s default plottable data based on the `NXdata` definition.

# `NOMAD` integration

While `pynxtools` works independently, it can also be integrated directly into any Research Data Management Systems (RDMS). The package works as a plugin within the `NOMAD` platform [@Scheidgen:2023; @Draxl:2019] out of the box. This enables data in the NeXus format to be integrated into `NOMAD`'s metadata model, making it searchable and interoperable with other data from theory and experiment. The plugin consists of several key components (so called entry points):

`pynxtools` extends `NOMAD`’s data schema, known as `Metainfo` [@Ghiringhelli:2017], by integrating NeXus definitions as a `NOMAD` `Schema Package`. This integration introduces NeXus-specific quantities and enables interoperability by linking to other standardized data representations within `NOMAD`. The `dataconverter` is integrated into `NOMAD`, making the conversion of data to NeXus accessible via the `NOMAD` GUI. The `dataconverter` also processes manually entered `NOMAD` ELN data in the conversion.

The `NOMAD` Parser module in `pynxtools` (`NexusParser`) extracts structured data from NeXus HDF5 files to populate `NOMAD` with `Metainfo` object instances as defined by the `pynxtools` schema package. This enables ingestion of NeXus data directly into `NOMAD`. Parsed data is post-processed using `NOMAD`'s `Normalization` pipeline. This includes automatic handling of units, linking references (including sample and instrument identifiers defined elsewhere in `NOMAD`), and populating derived quantities needed for advanced search and visualization.

`pynxtools` contains an integrated `Search Application` for NeXus data within `NOMAD`, powered by `Elasticsearch` [@elasticsearch:2025]. This provides a search dashboard whereby users can efficiently filter uploaded data based on parameters like experiment type, upload timestamp, and domain- and technique-specific quantities. The entire `pynxtools` workflow (conversion, parsing, and normalization) is exemplified in a representative `NOMAD` `Example Upload` that is shipped with the package. This example helps new users understand the workflow and serves as a template to adapt the plugin to new NeXus applications.

# Funding
The work is funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) - project 460197019 (FAIRmat).

# Acknowledgements

We acknowledge the following software packages our package depends on: `h5py` [@H5py:2008], `numpy` [@Harris:2020], `click` [@Click:2014] , `CFF` [@Druskat:2021], `xarray` [@Hoyer:2017], [@Hoyer:2025], `pandas` [@Pandas:2020], `scipy` [@McKinney:2010], `lxml` [@Behnel:2005], `mergedeep` [@Clarke:2019], `Atomic Simulation Environment` [@Hjorth:2017], `pint` [@Pint:2012].

# References
