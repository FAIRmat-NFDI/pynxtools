## em_nion reader

This is an example how the em_nion parser/reader/data extractor can be used as a standalone
tool to convert data and metadata from a compressed nionswift project into an NXem-formatted
NeXus/HDF5 file. Further details to the functionalities of the parser are documented
in the parsers sub-directory:

```
pynxtools/pynxtools/dataconverter/readers/em_nion
```

**Write.NXem_nion.Example.1.ipynb** is the Jupyter notebook which exemplies
how the parser can be used as a standalone version, i.e. without NOMAD.

**eln_data_em_nion.yaml** is a YAML/text file which contains relevant data which are not
contained typically in files from technology partners. These data have been collected
either by editing the file manually or by using an electronic lab notebook (ELN),
such as the NOMAD ELN.
A few example files from real atom probe reconstructions and ranging definitions are
offered as downloads to run the example with the above-mentioned Juypter notebook.

Every other ELN can be used with this parser provided that this ELN writes its data
into a YAML file with the same keywords and structure as is exemplified in the
above-mentioned YAML file.