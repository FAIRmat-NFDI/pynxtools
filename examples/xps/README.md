# XPS Reader

## What is this reader?

This reader supports converting X-ray photoelectron spectroscopy into a NeXus formatted file. The application definiton it follows is [NXmpes](https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXmpes.html#nxmpes).

## Supported file formats
The reader decides which parser to use based on the file extension of the files provided. For the main XPS files, the following file extensions are supported:
- .sle: [SpecsLabProdigy](https://www.specs-group.com/nc/specs/products/detail/prodigy/) files, propietary format of SPECS GmbH (v1.6)
- .xml: SpecsLab 2files, XML format from SPECS GmbH (v1.6)
- .vms: VAMAS files, ISO standard data transfer format ([ISO 14976](https://www.iso.org/standard/24269.html)), both in regular and irregular format
- .xy: SpecsLabProdigy export format in XY format (including all export settings)
- .txt:
  - exported by [Scienta Omicron](https://scientaomicron.com/en) instruments
  - exported by [CasaXPS](https://www.casaxps.com/) analysis software

```console
user@box:~$ dataconverter --params-file params.yaml
```

## Contact person in FAIRmat for this reader
Lukas Pielsticker