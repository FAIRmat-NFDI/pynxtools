# XRD reader
By XRD reader data can read from X-ray diffraction experiment and write  in a nexus (h5 type file with extension .nxs) according to NXxrd_pan application definition in NeXus, github repository (https://github.com/FAIRmat-NFDI/nexus_definitions). There are a few methods e.g. 1. θ:2θ instrument (e.g. Rigaku H3R), 2. θ:θ instrument (e.g. PANalytical X’Pert Pro). The goal with this reader to support both of that methods.

**NOTE: At this moment the reader can handle file with extension `.xrdml` of version (1.5) for method-2. This reader still under development. Currently we are woking to include more file types and file versions.**

## Contact persion in FAIRmat
In principle any one from Area-B of FAIRmat consortium can be reached out, but Rubel Mozumder could be more reasonable for the early response.

## Parsers
Though, in computer science, parser is a process that reads code into smaller parts (called tocken) with relations among tockens in a tree diagram. The process helps compiler to understand the tocken relationship of the source code.

Here, usully we call a program or class that reads the experimenal input file and relate the different physical/experiment concepts or propertise in a certain structure which defined by developer. The relation is a slash separated string, for example (according to xrdml file) `{/XRDmeasurement/Datapoints/position_1/axis : 2theta}`, which reads the root element or coponent is `XRDmeasurement`  with sub-element `Datapoints` with sub-element `position_1` that has a attribute or an element `axis` refering `2theta values`. In this reader, a parser that parsers a specific file type from a specific xrd method. Some of the parser features with annotated below:

**NOTE: there are several parserS will be available in future.**

### class pynxtools.dataconverter.readers.xrd.xrd_parser.XRDMLParser

    **inputs:**
        file_path: Full path of the input file.

    **Important method:**
        get_slash_separated_xrd_dict() -> dict

        This method can be used to check if all the data from input file have been read or not, it returns the slash separated dict as described.

### Other parsers
    **Coming Soon!!**

### How To
Reader can be run from Jupyter-notebook or Jupyter-lab with the follwoing command:
```sh
 ! dataconverter \
--reader xrd \
--nxdl NXxrd_pan \
--input-file $<xps-file location> \
--input-file $<eln-file location> \
--output <output-file location>.nxs
```

An example file can be found here in GitLab, but to have access in that GitLab on must need an account in https://gitlab.mpcdf.mpg.de/.
