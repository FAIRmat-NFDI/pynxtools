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
    orcid: 0009-0008-6635-4465
    affiliation: 1
    equal-contrib: true
  - given-names: Lukas
    surname: Pielsticker
    orcid: 0000-0001-9361-8333
    affiliation: "1,2"
    equal-contrib: true
  - given-names: Florian
    surname: Dobener
    orcid: 0000-0003-1987-6224
    affiliation: "1,3"
  - given-names: Andrea
    surname: Albino
    orcid: 0000-0001-9280-7431
    affiliation: 1
  - given-names: Theodore
    surname: Chang
    orcid: 0000-0002-4911-0230
    affiliation: 1
  - given-names: Carola
    surname: Emminger
    orcid: 0000-0003-4793-1809
    affiliation: "1, 4"
  - given-names: Lev
    surname: Ginzburg
    orcid: 0000-0001-8929-1040
    affiliation: 1
  - given-names: Ron
    surname: Hildebrandt
    orcid: 0000-0001-6932-604X
    affiliation: "1, 4"
  - given-names: Markus
    surname: Kühbach
    orcid: 0000-0002-7117-5196
    affiliation: 1
  - given-names: Rubel
    surname: Mozumder
    orcid: 0009-0007-5926-6646
    affiliation: 1
  - given-names: Tommaso
    surname: Pincelli
    orcid: 0000-0003-2692-2540
    affiliation: 5
  - given-names: Martin
    surname: Aeschlimann
    orcid: 0000-0003-3413-5029
    affiliation: 3
  - given-names: Marius
    surname: Grundmann
    orcid: 0000-0001-7554-182X
    affiliation: 4
  - given-names: Walid
    surname: Hetaba
    orcid: 0000-0003-4728-0786
    affiliation: 2
  - given-names: Carlos-Andres
    surname: Palma
    orcid: 0000-0001-5576-8496
    affiliation: "1, 6"
  - given-names: Laurenz
    surname: Rettig
    orcid: 0000-0002-0725-6696
    affiliation: 5
  - given-names: Markus
    surname: Scheidgen
    orcid: 0000-0002-8038-2277
    affiliation: 1
  - given-names: José Antonio
    surname: Márquez Prieto
    orcid: 0000-0002-8173-2566
    affiliation: 1
  - given-names: Claudia
    surname: Draxl
    orcid: 0000-0003-3523-6657
    affiliation: 1
  - given-names: Sandor
    surname: Brockhauser
    orcid: 0000-0002-9700-4803
    affiliation: 1
  - given-names: Christoph
    surname: Koch
    orcid: 0000-0002-3984-1523
    affiliation: 1
  - given-names: Heiko B.
    surname: Weber
    orcid: 0000-0002-6403-9022
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

Scientific data across physics, materials science, and materials engineering often lacks adherence to FAIR principles [@Wilkinson:2016; @Jacobsen:2020; @Barker:2022; @Wilkinson:2025] due to incompatible instrument-specific formats and diverse standardization practices. `pynxtools` is a Python software development framework with a command line interface (CLI) that standardizes data conversion for scientific experiments to the NeXus format [@Koennecke:2015; @Koennecke:2006; @Klosowski:1997] across diverse scientific domains including atom probe tomography, electron microscopy, optical spectroscopy, photoemission spectroscopy, scanning probe microscopy, and X-ray diffraction. Through its modular plugin architecture, `pynxtools` converts data and metadata from instruments and electronic lab notebooks to unified NeXus application definitions while performing automated validation to ensure compliance. The framework is deployed in production as part of the `NOMAD` [@Scheidgen:2023; @Draxl:2019] research data management platform and is used across multiple `NOMAD` Oasis installations in experimental laboratories, by external Python packages, and in dataset publications on Zenodo.

# Statement of Need

Achieving FAIR (Findable, Accessible, Interoperable, and Reproducible) data principles in experimental physics and materials science requires consistent implementation of standardized data formats. NeXus provides comprehensive specifications for structured storage of scientific data through technique-specific application definitions. However, leveraging its full breadth and detailed NXDL documentation can require careful implementation. `pynxtools` addresses this by transforming NeXus from a complex specification into a practical solution through guided workflows, automated validation with detailed error reporting for missing required data points, and clear implementation pathways via configuration files and extensible plugins. This approach enables researchers to achieve true data interoperability without deep technical expertise in the underlying standards.

# State of the Field

Existing tools in the NeXus ecosystem typically address isolated aspects of adoption. For example, nxconvert supports backend conversion between NeXus representations (e.g., HDF5 to XML), nxbrowse enables inspection of file contents, and cnxvalidate [@Koennecke:2024] together with punx [@Jemian:2025] provide validation of NeXus files. In addition, some domain-specific software packages implement technique-specific routines for writing NeXus files.

`pynxtools` fills this gap by dynamically integrating any version of NXDL application definitions directly from their source repositories and validating conversions against the complete inheritance structure of the chosen definition. Rather than just offering an additional reader/writer, it operationalizes NeXus as an executable specification with automated, exhaustive validation and structured error reporting. The validation layer is paired with a plugin ecosystem that enables format-to-NeXus conversion for diverse instruments. Contributing comparable functionality to existing tools would require substantial architectural modifications, whereas `pynxtools` was, from the outset, designed as a dedicated framework that provides a cohesive, extensible solution to transform NeXus adoption from a manual, documentation-heavy task into a guided, programmatic workflow.

# Software Design

The core design decision in `pynxtools` is to treat NeXus application definitions not as static documentation but as machine-actionable schemas that drive the entire conversion workflow. We chose a plugin-based architecture to decouple instrument-specific parsing logic from specification-aware validation. Each plugin declares the file formats it supports and the NXDL application definitions it can target, enabling modular growth without central code modification. This design supports an evolving ecosystem where new techniques and file formats can be added independently.

A key architectural choice is the internal `Template` object: a subclass of Python's native dictionary that serves as a form for reader plugins to fill. By preserving the standard Python dict API, developers interact with a familiar data structure while benefiting from deep validation features. The `Template` embeds structural awareness of required, recommended, and optional NeXus fields, pre-populating and organizing them according to the selected application definition. Because the structure maps naturally to JSON, it can be serialized, inspected, and edited outside the runtime environment, supporting tools such as JSON/YAML mappers and electronic lab notebook integration.

`dataconverter`, the core module of pynxtools that provides the transformation workflow, validates reader output against the selected NeXus application definition, checking for instances of required concepts, complex dependencies (like inheritance and nested group rules), and data integrity (type, shape, constraints). All reader plugins are tested using the `pynxtools.testing` suite, which runs automatically via GitHub CI to ensure compatibility with the dataconverter, the NeXus specification, and integration across plugins.

# Implementation

The `dataconverter` combines instrument output files and data from electronic lab notebooks into NeXus-compliant HDF5 files. It provides a command-line interface (CLI) supporting both built-in readers for general-purpose functionality and technique-specific reader plugins distributed as separate Python packages. For developers, the `dataconverter` provides an abstract `reader` class for building plugins that process experiment-specific formats and populate the NeXus specification through the `Template` interface.

The dataconverter includes a tool called `eln_mapper` that creates either a fillable `YAML` file or a `NOMAD` ELN schema based on a selected NeXus application definition.

The `read_nexus` module enables semantic access to NeXus files by linking data items to NeXus concepts, allowing applications to locate relevant data without hardcoding file paths. It supports concept-based queries that return all data items associated with a specific NeXus vocabulary term. Each data item is annotated by traversing its group path and resolving its corresponding NeXus concept, including inherited definitions. Items not part of the NeXus schema are explicitly marked as such, aiding in validation and debugging. The tool also identifies and summarizes the file's default plottable data based on the `NXdata` definition.

# Research Impact

`pynxtools` is integrated into production systems, demonstrating real-world impact across multiple deployment contexts. It is designed as a plugin for `NOMAD` to support NeXus and the features that come with our framework. Within the `NOMAD` platform, it underpins NeXus-based ingestion, validation, and search of experimental datasets, enabling automatic unit handling, metadata linking, and advanced search over NeXus-defined quantities. The framework is also distributed with `NOMAD` Oasis installations operated in experimental laboratories, demonstrating its suitability for decentralized, on-premise data management.

The `NOMAD` integration consists of several key components: `pynxtools` extends `NOMAD`'s data schema (`Metainfo` [@Ghiringhelli:2017]) by integrating NeXus definitions as a `Schema Package`, introducing NeXus-specific quantities and enabling interoperability with other standardized data representations. The `NexusParser` module extracts structured data from NeXus HDF5 files to populate `NOMAD` with `Metainfo` object instances. Parsed data is post-processed using `NOMAD`'s `Normalization` pipeline, including automatic handling of units, linking references (sample and instrument identifiers), and populating derived quantities needed for advanced search and visualization. An integrated `Search Application` powered by `Elasticsearch` [@elasticsearch:2025] provides a dashboard for filtering uploaded data based on experiment type, upload timestamp, and domain-specific quantities. The entire workflow is exemplified in a representative `Example Upload` shipped with the package.

Beyond `NOMAD`, `pynxtools` supports external Python packages that rely on its validation and conversion capabilities and has been used in preparing datasets for publication on repositories such as Zenodo [@Maklar:2023; @Pincelli:2022; @Dendzik:2022; @Maklar:2022; @Beaulieu:2021; @Beaulieu:2021trARPES; @Maklar:2020; @Xian:2020]. Its continuous integration testing across plugins ensures robustness against updates in both NXDL definitions and dependent packages, signaling community readiness and maintainability. By lowering the technical barrier to rigorous NeXus compliance, pynxtools enables reproducible, interoperable experimental data workflows that are already operational across multiple scientific domains.

# Funding
The work is funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) - project 460197019 (FAIRmat).

# Acknowledgements

We acknowledge the following software packages our package depends on: `h5py` [@H5py:2008], `numpy` [@Harris:2020], `click` [@Click:2014] , `CFF` [@Druskat:2021], `xarray` [@Hoyer:2017], [@Hoyer:2025], `pandas` [@Pandas:2020], `scipy` [@McKinney:2010], `lxml` [@Behnel:2005], `mergedeep` [@Clarke:2019], `Atomic Simulation Environment` [@Hjorth:2017], `pint` [@Pint:2012].

# AI Usage Disclosure

No generative AI tools were used in the development of this software. We acknowledge the use of ChatGPT (https://chat.openai.com/) for language refinement and proofreading of this manuscript.

# References
