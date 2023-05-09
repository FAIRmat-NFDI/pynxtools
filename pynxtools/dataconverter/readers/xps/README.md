# xps reader

## Contact person in FAIRmat for this reader

Rubel Mozumder

## Some Notes

1. The reader only compatible with xps data file (xml) of version 1.6.
2. The reader builds on [NXmpes](https://fairmat-experimental.github.io/nexus-fairmat-proposal/1c3806dba40111f36a16d0205cc39a5b7d52ca2e/classes/contributed_definitions/NXmpes.html#nxmpes) definition language.
3. The development process is intended in two steps.
   i. [reader_utils](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/pynxtools/dataconverter/readers/xps/reader_utils.py) parse the xps data from raw input files.
   ii. Later the NXmpes nxdl template will be filled the parsed data comming from **reader_utils.py**.
4. XPS data file (1.6v) does not have data/values for all requied fields and attributes. So, to launch **xps** reader user must provide a [xps eln](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/tests/data/dataconverter/readers/xps/xps_eln.yaml) with [raw data](https://github.com/FAIRmat-NFDI/pynxtools/blob/master/tests/data/dataconverter/readers/xps/In-situ_PBTTT_XPS_SPECS.xml) file.
5. Example script to run xps reader use code snipet below-

```sh
 ! dataconverter \
--reader xps \
--nxdl NXmpes \
--input-file $<xps-file location> \
--input-file $<eln-file location> \
--output <output-file location>.test.nxs
```
