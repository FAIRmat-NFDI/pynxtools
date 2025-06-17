---
title: 'pynxtools: A framework for generating NeXus files from raw file formats.'
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

Scientific data across experimental physics and materials science often lacks adherence to FAIR principles [@Wilkinson:2016; @Jacobsen:2020; @Barker:2022] due to incompatible instrument-specific formats and diverse standardization practices. pynxtools is a Python software development framework with a CLI interface that standardizes data conversion for scientific experiments in materials characterization to the NeXus format [@Koennecke:2015] across diverse scientific domains. NeXus uses NeXus application definitions as their data storage specifications. pynxtools provides a fixed, versioned set of NeXus application definitions that ensures convergence and alignment in data specifications across photoemission spectroscopy, electron microscopy [@Prestat:2025], atom probe tomography, optical spectroscopy, scanning probe microscopy, and X-ray diffraction. Through its modular plugin architecture, pynxtools provides maps for instrument-specific raw data, and electronic lab notebook metadata, to these unified definitions, while performing validation to ensure data correctness and NeXus compliance. By simplifying the adoption of standardized application definitions, the framework enables true data interoperability and FAIR data management across multiple experimental techniques.

# Statement of need

Achieving FAIR (Findable, Accessible, Interoperable, and Reproducible) data principles in experimental physics and materials science requires consistent implementation of standardized data formats. While NeXus provides comprehensive data specifications for structured storeage of scientific data, pynxtools simplifies the implementation process for developers and researchers by providing guided workflows and automated validation to ensure complete compliance. Existing tools [@Koennecke:2024; @Jemian:2025] provide solutions with individual capabilities, but none offers a comprehensive end-to-end workflow for proper NeXus adoption. pynxtools addresses this critical gap by providing an accessible framework that enforces complete NeXus application definition compliance through automated validation, detailed error reporting for missing required data points, and clear implementation pathways via configuration files and extensible plugins. This approach transforms NeXus from a complex specification into a practical solution, enabling researchers to achieve true data interoperability without deep technical expertise in the underlying standards.

# Dataconverter and validation

The __dataconverter__ module forms the core of pynxtools, combining instrument output files and data from electronic lab notebooks into NeXus-compliant HDF5 files. The converter performs three key operations: reading experimental data through specialized readers, validating against NeXus application definitions to ensure compliance with existence, shape, and format constraints, and writing valid NeXus/HDF5 output files.

The __dataconverter__ provides a command line interface (CLI) to produce NeXus files where users can use one of the built-in readers for generic functionality or technique-specific reader plugins distributed as separate Python packages.

For developers, the __dataconverter__ provides an abstract __reader__ class to create plugins that process experiment-specific file formats and try to fill the NeXus specification. A __Template__ object is passed to the __reader__ by the __dataconverter__ that acts like a form that has to be filled by the __reader__. __Template__ is a subclass of a regular Python __dict__ class. It keeps a similar interface to a __dict__ to help developers write code they are familiar with. It transparently ensures structural compliance with the selected NeXus application definition. __Template__ categorizes all data elements according to three requirement levels: required, recommended, and optional.

This allows the __dataconverter__ to control what the reader plugins provide and validate this against the selected NeXus application definition. Once, the reader plugin returns a __Template__ object, the __dataconverter__'s validation routine checks if all required fields in the NeXus application definition exist. This includes complex dependency relationships such as inheritance chains or required children within optional parent groups. The validation then collects all data entities that have a specification and ensures data integrity by verifying the data type, shape, and constraints set by the specification. The __dataconverter__'s validation routine throws an error if there is a required data entity it found invalid. It also emits warnings to the CLI for the user and/or developer for any data it invalidates or doesn't find a specification for. This helps the users identify issues while practically building a NeXus file.

After validation the __dataconverter__ passes the __Template__ object to the __Writer__ class. This class has the job of writing an HDF5 file as provided in a __Template__ object. It also converts the __Template__ object's simple link syntax to an HDF5 link. This can be a softlink or hardlink. It can be within the same file or another file. We reduce this syntax to a __dict__ object with a __link__ key with a string formatted as "<filename.hdf5>:<\/path\/to\/data\/in\/template\/object>". The filename is optional and can be ommitted if the data being linked is in the same file: "<\/path\/to\/data\/in\/template\/object>". This drastically simplifies linking to data for new users and developers. The same syntax is available in our dynamic mapping built-in readers.

All reader implementations are validated through a test suite that ensures compatibility with the __dataconverter__ framework. These tests run automatically via the continuous integration pipeline provided by GitHub, maintaining code quality and functional integration across all reader plugins.

The __dataconverter__ module is also shipped with an ELN generator that, for a selected NeXus application definition, creates either a YAML file that can be manually filled in and used by __dataconverter__ readers or a NOMAD ELN schema that can be used to manually fill in data on the NOMAD platform.

# NeXus reader and annotator (read\_nexus)

__read_nexus__ is a command line tool to annotate and explore NeXus data files. Once pynxtools is installed, it is immediately available and offers options for selecting a NeXus file and either documenting all or part of its content. Note that with no specific NeXus file provided as an argument, the tool will use by default an example NeXus file shipped together with the package.

_annotations -_ As it is expained above[!!! Ref better when it is done], NeXus defines a rich set of concepts, the so called [NeXus Vocabulary](https://manual.nexusformat.org/classes/index.html#classes-vocabulary-downloads). These include _Attributes_ and _Fields_ which are organized in _Groups_ and their subgroups. [NeXus files](https://manual.nexusformat.org/design.html) store their [data items](see details in https://manual.nexusformat.org/datarules.html) following the hierarchy of these groups. _read\_nexus_ traverses the input NeXus file and interprets each data item by following its group path and connecting it to the concept of the specific vocabulary item. It reports the concept's definition. Since NeXus concepts follow inheritance, the all superclass concepts along the inheritance chain and their definitions are also reported. If a data item in a NeXus file does not belong to any concept (which is allowed by the NeXus standard), _read\_nexus_ reports the message 'NOT IN SCHEMA'.

_default plottable -_ NeXus allows to specify which [plottable data](https://manual.nexusformat.org/datarules.html#find-plottable-data) shall be presented by default for a given NeXus file. After traversing the whole file and visiting all data items, _read\_nexus_ additionally reports a summary of the default plottable by presenting its path and also its plotting details as specified by the [NXdata definition](https://manual.nexusformat.org/classes/base_classes/NXdata.html).

__semantic use__: _read\_nexus_ also supports the proper semantic use of data items in NeXus files by automating the annotation process of connecting them to the corresponding NeXus concepts. Hence, data processing applications can find data items in a NeXus file based on the semantic concepts, without the need of hardcoding any data path which could lead to incompatibilities. Note that _read\_nexus_ uses [NeXus Ontology's](https://github.com/nexusformat/NeXusOntology) [OWL](https://www.w3.org/OWL/) labels assigned to each NeXus' semantic concept. Hence, it can also be used to connect data items from any NeXus files to the semantic web. The following features facilitate such use:

_--concept_: This command line queries the NeXus file using a specific NeXus vocabulary item (or NeXus Ontology class), reporting all data item paths that correspond to this concept.

_--documentation_: Instead of traversing the whole file, this feature annotates only a single data item at a specific path in the NeXus file. This is practical when only a few specific data items need to be investigated, e.g. those selected by a _--concept_ query.

!!! Check the NeXus links! Use either nexusformat.org links, or reference the path in the actual(!) pynxtools repo noting that pynxtools/definitions is a github submodule and content (as well as content path) can change version to version.

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

We acknowledge the following software packages our package depends on: [@H5py:2008], [@Harris:2020], [@Click:2014], [@Druskat:2021], [@Hoyer:2017], [@Hoyer:2025], [@Pandas:2020], [@McKinney:2010], [@Behnel:2005], [@Clarke:2019], [@Hjorth:2017], [@Pint:2012].

# References
