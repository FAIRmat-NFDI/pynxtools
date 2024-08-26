---
hide: toc
---

# FAIRmat NeXus documentation

<!-- A single sentence that says what the product is, succinctly and memorably -->
Within [FAIRMat](https://www.fairmat-nfdi.eu/fairmat/), we are extending the [NeXus data format standard](https://www.nexusformat.org/) to support the FAIR data principles for experimental data in materials science and and phyics. This is the documentation for both our contribution to the NeXus standard as well as for our tools for data conversion and verification.

<!-- A paragraph of one to three short sentences, that describe what the product does. -->
`pynxtools`, which is the main tool under development, provides a dataconverter that maps from experimental data to the NeXus format as well as tools to verify NeXus files. It is intended as a parser for combining various instrument output formats and electronic lab notebook (ELN) formats to an HDF5 file according to NeXus application definitions.

<!-- A third paragraph of similar length, this time explaining what need the product meets -->
`pynxtools` offers scientists a convenient way to use the NeXus format and solves the challenge of unstructured and non-standardized data in experimental materials science.

<!-- Finally, a paragraph that describes whom the product is useful for. -->
The new contribution to the standard, together with the tools provided through `pynxtools`, enable scientists and research groups working with data, as well as helping communities implement standardized FAIR research data.

Additionally, the software is used as a plugin in the research data management system [NOMAD](https://nomad-lab.eu/nomad-lab/) for making experimental data searchable and publishable. NOMAD is developed by the FAIRMAT consortium, as a part of the German National Research Data Infrastructure (NFDI).

<div markdown="block" class="home-grid">
<div markdown="block">

### Tutorial

A series of tutorials giving you an overview on how to store or convert your data to NeXus compliant files.

- [Converting your data to NeXus](tutorial/converting-data-to-nexus.md)
- [Uploading NeXus data to NOMAD](tutorial/nexus-to-nomad.md)
- [Troubleshooting guide](tutorial/troubleshooting.md)

</div>
<div markdown="block">

### How-to guides

How-to guides provide step-by-step instructions for a wide range of tasks.

- [Writing an application definition](how-tos/writing-an-appdef.md)
- [Storing data in multiple application definitions](how-tos/using-multiple-appdefs.md)
- [Build your own pynxtools plugin](how-tos/build-a-plugin.md)
- [Implement a reader based on the MultiFormatReader](how-tos/use-multi-format-reader.md)
- [Representing experimental geometries](how-tos/transformations.md)
- [Using pynxtools test framework](how-tos/using-pynxtools-test-framework.md)

</div>

<div markdown="block">

### Learn

#### An introduction to NeXus and its design principles

- [An introduction to NeXus](learn/nexus-primer.md)
- [Rules for storing data in NeXus](learn/nexus-rules.md)
- [The concept of multiple application definitions](learn/multiple-appdefs.md)

#### pynxtools

- [Data conversion in `pynxtools`](learn/dataconverter-and-readers.md)
- [NeXus verification in `pynxtools`](learn/nexus-verification.md)
- [The MultiFormatReader as a reader superclass](learn/multi-format-reader.md)

</div>
<div markdown="block">

### Reference

#### NeXus definitions
[Here](reference/definitions.md), you find the detailed list of application definitions and base classes and their respective fields.

Or go directly to the [official NIAC](https://manual.nexusformat.org/classes/index.html)
 or [latest FAIRmat](https://fairmat-nfdi.github.io/nexus_definitions/) definitions.

#### pynxtools

`pynxtools` has a number of command line tools that can be used to convert data and verify NeXus files. You can more information about the
API [here](reference/cli-api.md).

Within FAIRmat, we maintain a number of pynxtools readers as well as reader plugins for different experimental techniques. Here you can find more information:

- [Built-in pynxtools readers](reference/built-in-readers.md)
- [FAIRMat-suppored pynxtools plugins](reference/plugins.md)


</div>
</div>

<h2>Project and community</h2>

[The work is funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) - 460197019 (FAIRmat).](https://gepris.dfg.de/gepris/projekt/460197019?language=en)