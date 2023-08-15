# em reader

## Purpose
Tool for parsing electron microscopy research data from different representations
of technology partners on an instance of a NeXus/HDF5 file which is formatted
according to the NXem application definition.

In the process this data artifact is verified for the existence of certain
pieces of information and the formatting of these pieces of information.

Internally the tool uses different file format readers and mapping tables
whereby pieces of information in respective are mapped on corresponding
concepts represented by the nexus-fairmat-proposal.

The resulting data artifact is an HDF5 file which can be imported for
instance into the NOMAD OASIS research data management system to enable
functionalities and data exploration in NOMAD.

The parser documents how several non-trivial examples from electron microscopy
research can be read technically, mapped on semantic concepts using NeXus, and
the resulting data artifact verified using an application definition.

The parser does not convert and map every piece of information which the supported
file formats can technically store. This is to keep a balance between avoid a
duplication of data and metadata but adding additional value in that pieces of
information from different sources are combined and represented in an interpreted
form already to inject research content readily consumable by humans in a
research data management system. Default plots - presented in a harmonized form,
irrespective from which technology partner format they were originally stored in,
is one such benefit.

In effect, this is an example how pynxtools is an effective library for
developers and users of research data management systems whereby they can
offload mapping and harmonization code surplus have the possibility for
a verification of the content via application definitions.

For the example of the NOMAD OASIS research data management system
pynxtools is such a library to enable users an injection of domain-specific
content using existent community file format readers and generic information
mapping capabilities. 

## Support
The following table shows which use cases and associated technology partner file formats the em dataconverter handles.
| Use case | Community | Supported file formats | Previous parser |
| -------- | -------- | ------- | ------- |
| 1 | Electron backscatter diffraction | MTex/Matlab \*.nxs.mtex, Oxford Instruments \*.h5oina, DREAM3D \*.dream3d, EDAX APEX HDF5, Bruker Nanoscience HDF5, zip-compressed set of Kikuchi pattern | em_om |
| 2 | Nion Co. TEM and nionswift users | zip-compressed nionswift project directory | em_nion |
| 3 | SEM/TEM generic imaging | ThermoFisher TIFF | n/a |
| 4 | Energy-dispersive X-ray spectroscopy (EDS) via SEM/TEM | Bruker \*.bcf, ThermoFisher Velox \*.emd, Gatan Digital Micrograph \*.dm3, EDAX APEX \*.edaxh5 | em_spctrscpy |
| 5 | Electron energy loss spectroscopy (EELS) | DM3, zip-compressed nionswift project directory | em_spctrscpy |
| 6 | In-situ microscopy with Protochips AXONStudio | zip-compressed AXON Studio project | n/a |

## Manual
Please inspect the 

## Contact person for this reader
Markus Kühbach