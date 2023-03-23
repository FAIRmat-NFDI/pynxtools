# A short guideline for writting stm reader

## eln.yaml
This is an example of NXmpes definition ELN for XPS reader
NXmpes definition:
      yaml link: https://github.com/FAIRmat-Experimental/nexus_definitions/blob/fairmat/contributed_definitions/nyaml/NXmpes.yaml
      nxdl.xml link: https://github.com/FAIRmat-Experimental/nexus_definitions/blob/fairmat/contributed_definitions/NXmpes.nxdl.xml
 
Here values for Nexus fields, attributes and groups are given, because they not available in raw data files. 
But the fields, attributes and groups are needed to filled up.

## Confing_file.json
This file mainly works as mapper. 
**key**: Intended for xml path or nexus definition path
**value**: Data path to raw data file or structured data file (which comes from raw data)

## reader.py
Which fill the NXmpes template(this is a python dictionary) for generating nexus output file.
