## em_om reader

This is an example how the em_om parser/reader/data extractor can be used as a
standalone tool to convert data and metadata from different sources into an
NXem_ebsd-formatted NeXus/HDF5 file. Further details to the functionalities of the
parser are documented in the parsers sub-directory:

```
pynxtools/pynxtools/dataconverter/readers/em_om
```

**Write.NXem_ebsd.Example.1.ipynb** is the Jupyter notebook which exemplies
how the parser can be used as a standalone version, i.e. without NOMAD.

**eln_data_em_om.yaml** is a YAML/text file which contains relevant data which are not
contained typically in files from technology partners. These data have been collected
either by editing the file manually or by using an electronic lab notebook (ELN),
such as the NOMAD ELN.
A few example files from real electron backscatter diffraction measurements are
offered as downloads to run the example with the above-mentioned Juypter notebook.

Every other ELN can be used with this parser provided that this ELN writes its data
into a YAML file with the same keywords and structure as is exemplified in the
above-mentioned YAML file.

### Map data from Matlab/MTex to NXem_ebsd
The download material includes several \*.mtex files. These reflect that the
em_om parser can handle data which have been generated with the Matlab/MTex
texture tool box. These \*.mtex files are currently an exchange file format
to map data from the MTex internal representation to something which the em_om
parser understands and can map to NXem_ebsd. You are very much invited to test this
feature. The feature requires, though, a specific extension of the MTex toolbox,
which is an MTex/Matlab script surplus a wrapper for the HDF5 library to enable
writing HDF5 files with more flexible data structures and attributes.
We tested this extension with Matlab>=2021 and MTex>=5.8.2.
Please contact Markus Kühbach directly if you are interested in testing this feature
and contribute thereby to make EBSD data more interoperable.