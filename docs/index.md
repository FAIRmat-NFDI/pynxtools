---
hide: toc
---

# FAIRmat NeXus documentation

<!-- A single sentence that says what the product is, succinctly and memorably -->
Within [FAIRmat](https://www.fairmat-nfdi.eu/fairmat/), we are extending the [NeXus data format standard](https://www.nexusformat.org/) to support the FAIR data principles for experimental data in materials science (covering solid-state physics and the chemical physics of solids, as well as materials engineering). This is the documentation for both our contribution to the NeXus standard and for our tools for data conversion and verification.

<!-- A paragraph of one to three short sentences, that describe what the product does. -->
`pynxtools`, the main tool under development, provides a data converter that maps experimental data and metadata to the NeXus format, performing parsing, normalization, visualization, and ontology matching. It combines various instrument output formats and electronic lab notebook (ELN) formats to an HDF5 file according to NeXus application definitions. In addition, `pynxtools` can be used to validate and verify NeXus files.

<!-- A third paragraph of similar length, this time explaining what need the product meets -->
`pynxtools` offers scientists a convenient way to use the NeXus format and solves the challenge of unstructured and non-standardized data in experimental materials science. We consider this package useful for meeting the following FAIR principle as defined in [FAIR Principles: Interpretations and Implementation Considerations](https://direct.mit.edu/dint/article/2/1-2/10/10017/FAIR-Principles-Interpretations-and-Implementation): F2-4, I2-I3, and R1.

<!-- Finally, a paragraph that describes whom the product is useful for. -->
FAIRmat's contribution to the existing NeXus standard, together with the tools provided through `pynxtools`, enable scientists and research groups working with data, as well as helping communities implement standardized FAIR research data.

Additionally, the software is used as a plugin in the research data management system [NOMAD](https://nomad-lab.eu/nomad-lab/) for making experimental data searchable and publishable. NOMAD is developed by the FAIRMAT consortium, as a part of the German National Research Data Infrastructure (NFDI).

<div markdown="block" class="home-grid">
<div markdown="block">

### Tutorial

A series of tutorials giving you an overview on how to store or convert your data to NeXus compliant files.

- [Converting your data to NeXus](tutorial/converting-data-to-nexus.md)
- [Uploading NeXus data to NOMAD](tutorial/nexus-to-nomad.md)

</div>
<div markdown="block">

### How-to guides

How-to guides provide step-by-step instructions for a wide range of tasks.


- [Build your own pynxtools plugin](how-tos/build-a-plugin.md)
- [Implement a reader based on the MultiFormatReader](how-tos/use-multi-format-reader.md)
- [Validation of NeXus files](how-tos/validate-nexus-file.md)
- [Creation of NeXus files in python via hard-coding ](how-tos/create-nexus-files-by-python.md)
- [Using pynxtools test framework for plugins](how-tos/using-pynxtools-test-framework.md)

__The following How-To guides are still under development:__

- [Writing an application definition](how-tos/writing-an-appdef.md)
- [Storing data in multiple application definitions](how-tos/using-multiple-appdefs.md)
- [Representing experimental geometries](how-tos/transformations.md)

</div>

<div markdown="block">

### Learn

#### An introduction to NeXus and its design principles

- [An introduction to NeXus](learn/nexus-primer.md)
- [Rules for storing data in NeXus](learn/nexus-rules.md)
- [The concept of multiple application definitions](learn/multiple-appdefs.md)
- [The MultiFormatReader as a reader superclass](learn/multi-format-reader.md)

#### pynxtools

- [Data conversion in `pynxtools`](learn/dataconverter-and-readers.md)
- [Validation of NeXus files](learn/nexus-validation.md)
- [The MultiFormatReader as a reader superclass](learn/multi-format-reader.md)

</div>
<div markdown="block">

### Reference

#### NeXus definitions
[Here](reference/definitions.md), you find the detailed list of application definitions and base classes and their respective fields.

Or go directly to the [official NIAC](https://manual.nexusformat.org/classes/index.html)
 or [latest FAIRmat](https://fairmat-nfdi.github.io/nexus_definitions/) definitions.

Note: To connect NeXus concepts with semantic web tools, efforts are underway to represent them using the [W3C Web Ontology Language (OWL)](https://www.w3.org/OWL/). See the [NeXusOntology](https://github.com/FAIRmat-NFDI/NeXusOntology) for more details.

#### pynxtools

`pynxtools` has a number of command line tools that can be used to convert data and verify NeXus files. You can find more information about the API [here](reference/cli-api.md).

Within FAIRmat, we maintain a number of generic built-in pynxtools readers, together with reader plugins for different experimental techniques. Here you can find more information:

- [Built-in pynxtools readers](reference/built-in-readers.md)
- [FAIRMat-supported pynxtools plugins](reference/plugins.md)


</div>
</div>

<h2>Project and community</h2>

[The work is funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) - 460197019 (FAIRmat).](https://gepris.dfg.de/gepris/projekt/460197019?language=en)