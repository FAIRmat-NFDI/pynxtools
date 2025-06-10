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

(Add statement like sentence for the start like the Nomad JOSS). pynxtools is a Python framework that standardizes data conversion for scientific experiments (materials characterization, something like This standardized approach addresses the historical problem of incompatible formats across research communities.) to NeXus HDF5 format across diverse scientific domains. pynxtools provides a fixed set of NeXus application definitions (reference needed here) that ensures convergence and alignment in data specifications across photoemission spectroscopy, electron microscopy(Check if there is a review paper, or just cite rosettasciIO), atom probe tomography, optical spectroscopy, scanning probe microscopy, and X-ray diffraction (Ref: CIFF, IUPAC). Through its modular plugin architecture, pynxtools provides maps for instrument-specific raw data and electronic lab notebook metadata to these unified definitions, while performing validation to ensure data correctness and NeXus compliance. By simplifying the adoption of standardized application definitions, the framework enables true data interoperability and FAIR data management across multiple experimental techniques.
(Missing what NeXus is. Add a bit of context.)
(Add it's a CLI tool. And code framework)
(Nexus Reference, https://doi.org/10.1107/S1600576714027575)
(Compromise for Nomad: We have a standalone tool that is also integrated in Nomad as an example.)
(https://github.com/ess-dmsc/nexus-constructor)
(Cite some FAIR papers, one from Jacobson, FAIR4RS, FAIR4Workflows-thisnotsoimp)



# Statement of need

Scientific data across experimental physics and materials science remains largely non-FAIR (Findable, Accessible, Interoperable, and Reproducible) due to inconsistent implementation and documentation of standardized data formats. While NeXus provides comprehensive data specifications for structured scientific data storage, researchers typically struggle with its specification requirements, leading to incomplete implementations, non-compliant outputs, or abandonment of standardization efforts entirely. Existing tools (do some parts of what we offer, and then list what we provide) lack robust validation frameworks and provide insufficient guidance for proper NeXus adoption. pynxtools addresses this critical gap by providing an accessible framework that enforces complete NeXus application definition compliance through automated validation, detailed error reporting for missing required data points, and clear implementation pathways via configuration files and extensible plugins. This approach transforms NeXus from a complex specification into a practical solution, enabling researchers to achieve true data interoperability without deep technical expertise in the underlying standards.
(Can we tone down the first sentence to not offend readers/people who worked before. Don't dwell on stuff not working. How to make this sound less negative?)
(Second sentence: We base everything on NeXus. We don't wanna say it's too complicated. Make it nicer. We make it more easier to handle it.)
(Third: refer to cnxvalidate and such)

# Dataconverter and validation (Sherjeel)

      * Mechanism to write an own reader, i.e. pynxtools-plugin mechanism and test frameworks, not mentioned to much about pynxtools-plugins

# NeXus reader and annotator (read\_nexus) (Sandor)

# NOMAD integration (schema, parser) (Lukas, Sandor)

# ELN generator

# Funding
The work is funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) - 460197019 (FAIRmat).

# Author contributions

# Acknowledgements

We acknowledge contributions from Brigitta Sipocz, Syrtis Major, and Semyeong
Oh, and support from Kathryn Johnston during the genesis of this project.

# References
