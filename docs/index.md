---
hide: toc
---

# Welcome to the FAIRmat NeXus documentation

<!-- A single sentence that says what the product is, succinctly and memorably -->
Within [FAIRmat](https://www.fairmat-nfdi.eu/fairmat/), we are extending the [NeXus data format standard](https://www.nexusformat.org/) to support the FAIR principles for experimental data in materials science.

<!-- A paragraph of one to three short sentences, that describe what the product does. -->
This documentation covers our contributions to the NeXus standard, and our supporting software tool, **`pynxtools`**. `pynxtools` maps data and metadata from diverse instruments and electronic lab notebooks (ELNs) into NeXus-compliant HDF5 files. It supports parsing, normalization, visualization, and ontology matching.

<!-- A third paragraph of similar length, this time explaining what need the product meets -->
`pynxtools` offers scientists a convenient way to use the NeXus format and solves the challenge of unstructured and non-standardized data in experimental materials science. 

<!-- Finally, a paragraph that describes whom the product is useful for. -->
The software can also be used as a plugin in the research data management system [**NOMAD**](https://nomad-lab.eu/nomad-lab/), an open-source platform for FAIR materials data management. Learn more in the [NOMAD documentation](https://nomad-lab.eu/prod/v1/staging/docs/).

We are offering a small guide to getting started with NeXus and pynxtools:

- [**Getting started**](getting-started.md)

<div markdown="block" class="home-grid">
<div markdown="block">


### Tutorial

A series of tutorials giving you an overview on how to store or convert your data to NeXus-compliant files.

- [Installation](tutorial/installation.md)
- [Converting your data to NeXus](tutorial/converting-data-to-nexus.md)
- [Uploading NeXus data to NOMAD](tutorial/nexus-to-nomad.md)
- [Development guide](tutorial/nexus-to-nomad.md)

</div>
<div markdown="block">

### How-to guides

How-to guides provide step-by-step instructions for a wide range of tasks.

#### NeXus data modelling

- [Writing an application definition](how-tos/nexus/writing-an-appdef.md)
<!-- - [Storing data in multiple application definitions](how-tos/nexus/using-multiple-appdefs.md) -->
<!-- - [Representing experimental geometries](how-tos/nexus/transformations.md) -->

#### pynxtools

- [Build your own pynxtools plugin](how-tos/pynxtools/build-a-plugin.md)
- [Implement a reader based on the MultiFormatReader](how-tos/pynxtools/use-multi-format-reader.md)
- [Using pynxtools test framework for plugins](how-tos/pynxtools/using-pynxtools-test-framework.md)
- [Using pynxtools tests in parallel](how-tos/pynxtools/run-tests-in-parallel.md)
- [Creation of NeXus files in python via hard-coding](how-tos/pynxtools/create-nexus-files-by-python.md)
- [Validation of NeXus files](how-tos/pynxtools/validate-nexus-file.md)

</div>

<div markdown="block">

### Learn

#### An introduction to NeXus and its design principles

- [An introduction to NeXus](learn/nexus/nexus-primer.md)
- [Rules for storing data in NeXus](learn/nexus/nexus-rules.md)
<!-- - [The concept of multiple application definitions](learn/multiple-appdefs.md) -->

#### pynxtools

- [Data conversion in `pynxtools`](learn/pynxtools/dataconverter-and-readers.md)
- [Validation of NeXus files](learn/pynxtools/nexus-validation.md)
- [The MultiFormatReader as a reader superclass](learn/pynxtools/multi-format-reader.md)

</div>
<div markdown="block">

### Reference

#### NeXus definitions

[Here](reference/definitions.md), you find the detailed list of application definitions and base classes and their respective fields.

#### pynxtools

`pynxtools` has a number of command line tools that can be used to convert data and verify NeXus files. You can find more information about the API [here](reference/cli-api.md).

Within FAIRmat, we maintain a number of generic built-in pynxtools readers, together with reader plugins for different experimental techniques. Here you can find more information:

- [Built-in pynxtools readers](reference/built-in-readers.md)
- [FAIRmat-supported pynxtools plugins](reference/plugins.md)


</div>
</div>

<h2> Contact </h2>

For questions or suggestions:

- Open an issue on the [pynxtools GitHub](https://github.com/FAIRmat-NFDI/pynxtools/issues)
- Join our [Discord channel ](https://discord.gg/Gyzx3ukUw8)
- Get in contact with our [lead developers](contact.md).

<h2>Project and community</h2>

The work is funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) - [460197019 (FAIRmat)](https://gepris.dfg.de/gepris/projekt/460197019?language=en).