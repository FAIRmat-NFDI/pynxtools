# XPS reader

## Purpose
Translate diverse file formats from the scientific community and technology partners
within the field of X-ray photoelectron spectroscopy into a standardized representation using the
[NeXus](https://www.nexusformat.org/) application definition [NXmpes](https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmpes.html#nxmpes).

## Supported file formats
The reader decides which parser to use based on the file extension of the files provided. For the main XPS files, the following file extensions are supported:
- .sle: [SpecsLabProdigy](https://www.specs-group.com/nc/specs/products/detail/prodigy/) files, propietary format of SPECS GmbH (v1.6)
- .xml: SpecsLab 2files, XML format from SPECS GmbH (v1.6)
- .vms: VAMAS files, ISO standard data transfer format ([ISO 14976](https://www.iso.org/standard/24269.html)), both in regular and irregular format
- .xy: SpecsLabProdigy export format in XY format (including all export settings)
- .txt:
  - exported by [Scienta Omicron](https://scientaomicron.com/en) instruments
  - exported by [CasaXPS](https://www.casaxps.com/) analysis software

We are continously working on adding parsers for other data formats and technology partners. If you would like to implement a parser for your data, feel free to get in contact.

## Getting started
An example script to run the XPS reader:
```sh
 ! dataconverter \
--reader xps \
--nxdl NXmpes \
$<xps-file path> \
$<eln-file path> \
--output <output-file path>.test.nxs
```
Note that none of the supported file format have data/values for all required and recommended fields and attributes in NXmpes. In order for the validation step of the **XPS** reader to pass,
you need to provide an ELN file that contains the missing values. An example can be found in  [*pynxtools/examples/xps*]().

## Development Notes
The development process is modular so that new parsers can be added. The read logic is the following.
1. First, [*XpsDataFileParser*]([https://github.com/FAIRmat-NFDI/pynxtools/blob/master/pynxtools/dataconverter/readers/xps/file_parser.py#L39]) selects the proper parser based on the file extensions
of the provided files. It then calls a sub-parser that can read files with such extensions and calls the *parse_file* function of that reader. In addition, it selects a proper config file from
the *config* subfolder.
2. Afterwards, the NXmpes nxdl template is filled with the data in *XpsDataFileParser* using the *config* file. Data that is not in the given main files can be added through the ELN file (and must
be added for required fields in NXmpes).

## Contact person in FAIRmat for this reader
Lukas Pielsticker
