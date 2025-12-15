# ELN generator

This is a helper tool for generating ELN files that can be used to add metadata to the dataconverter routine.

Two types of ELN are supported (by passing the flag `eln-type`):

- **`reader`**: The simple ELN generator that can be used in a console or jupyter-notebook, e.g. by the `pynxtools` dataconverter.
- **`schema`**: Scheme based ELN generator that can be used in NOMAD and the ELN can be used as a custom scheme in NOMAD.

 Here you can find more information about the tool:

 - [API documentation](https://fairmat-nfdi.github.io/pynxtools/reference/cli-api.html#generate_eln)