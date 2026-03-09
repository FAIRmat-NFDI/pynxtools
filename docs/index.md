---
hide: toc
---

# Welcome to the FAIRmat NeXus documentation

Within [FAIRmat](https://www.fairmat-nfdi.eu/fairmat/), we are extending the [NeXus data format standard](https://www.nexusformat.org/) to support the FAIR principles for experimental data in materials science.

This documentation covers our contributions to the NeXus standard and our supporting software tool, **`pynxtools`**. `pynxtools` maps data and metadata from diverse instruments and electronic lab notebooks (ELNs) into NeXus-compliant HDF5 files, and provides tools for validation, annotation, and schema-aware processing.

`pynxtools` can also be used as a plugin in the research data management system [**NOMAD**](https://nomad-lab.eu/nomad-lab/), an open-source platform for FAIR materials data management. Learn more in the [NOMAD documentation](https://nomad-lab.eu/prod/v1/staging/docs/).

- [**Getting started**](getting-started.md)

<div markdown="block" class="home-grid">
<div markdown="block">

### Tutorials

- [Installation guide](tutorial/installation.md)
- [Converting your research data to NeXus](tutorial/converting-data-to-nexus.md)
- [Uploading NeXus data to NOMAD](tutorial/nexus-to-nomad.md)
- [Development guide](tutorial/contributing.md)

</div>
<div markdown="block">

### How-to guides

#### NeXus data modelling

- [Writing an application definition](how-tos/nexus/writing-an-appdef.md)

#### pynxtools

- [Build your own `pynxtools` plugin](how-tos/pynxtools/build-a-plugin.md)
- [How to use the built-in `MultiFormatReader`](how-tos/pynxtools/use-multi-format-reader.md)
- [Implement a custom `NexusVisitor`](how-tos/pynxtools/implement-a-visitor.md)
- [Validate and inspect NeXus files](how-tos/pynxtools/validate-nexus-files.md)
- [Test functionality for `pynxtools` plugins](how-tos/pynxtools/using-pynxtools-test-framework.md)
- [Running `pynxtools` tests in parallel](how-tos/pynxtools/run-tests-in-parallel.md)
- [Using Python to create NeXus files](how-tos/pynxtools/create-nexus-files-by-python.md)

</div>

<div markdown="block">

### Learn

#### An introduction to NeXus and its design principles

- [A primer on NeXus](learn/nexus/nexus-primer.md)
- [Rules for storing data in NeXus](learn/nexus/nexus-rules.md)

#### pynxtools

- [pynxtools architecture](learn/pynxtools/architecture.md)
- [NeXus definitions in `pynxtools`](learn/pynxtools/nexus-definitions.md)
- [Data conversion in `pynxtools`](learn/pynxtools/dataconverter-and-readers.md)
- [Validation of NeXus files](learn/pynxtools/nexus-validation.md)
- [The `MultiFormatReader`](learn/pynxtools/multi-format-reader.md)

</div>
<div markdown="block">

### Reference

#### NeXus definitions

[Here](reference/definitions.md), you find the detailed list of application definitions and base classes and their respective fields.

#### pynxtools

- [CLI tools — `dataconverter`, `validate_nexus`, `read_nexus`](reference/cli-api.md)
- [Built-in `pynxtools` readers](reference/built-in-readers.md)
- [FAIRmat-supported `pynxtools` plugins](reference/plugins.md)

</div>
</div>

<h2> Contact </h2>

For questions or suggestions:

- Open an issue on the [`pynxtools` GitHub](https://github.com/FAIRmat-NFDI/pynxtools/issues)
- Join our [Discord channel](https://discord.gg/Gyzx3ukUw8)
- Get in contact with our [lead developers](contact.md)

<h2>Project and community</h2>

The work is funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) — [460197019 (FAIRmat)](https://gepris.dfg.de/gepris/projekt/460197019?language=en).
