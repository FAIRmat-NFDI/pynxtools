# XRD Reader
With the XRD reader, data from X-ray diffraction experiment can be read and written into a NeXus file (h5 type file with extension .nxs) according to NXxrd_pan application definition in [NeXus](https://github.com/FAIRmat-NFDI/nexus_definitions). There are a few different methods of measuring XRD: 1. θ:2θ instruments (e.g. Rigaku H3R), and 2. θ:θ instrument (e.g. PANalytical X’Pert Pro). The goal with this reader is to support both of these methods.

**NOTE: This reader is still under development. As of now, the reader can only handle files with the extension `.xrdml` , obtained with PANalytical X’Pert Pro version 1.5 (method 2 described above). Currently we are wtoking to include more file types and file versions.**

## Contact Person in FAIRmat
In principle, you can reach out to any member of Area B of the FAIRmat consortium, but Rubel Mozumder could be more reasonable for the early response.

## Parsers
Though, in computer science, parser is a process that reads code into smaller parts (called tocken) with relations among tockens in a tree diagram. The process helps compiler to understand the tocken relationship of the source code.

The XRD reader calls a program or class (called parser) that reads the experimenal input file and re-organises the different physical/experiment concepts or properties in a certain structure which is defined by developer.

### class pynxtools.dataconverter.readers.xrd.xrd_parser.XRDMLParser

    **inputs:**
        file_path: Full path of the input file.

    **Important method:**
        get_slash_separated_xrd_dict() -> dict

        This method can be used to check if all the data from the input file have been read or not, it returns the slash separated dict as described.


### Other Parsers
    **Coming Soon!!**

### How To
The reader can be run from Jupyter-notebook or Jupyter-lab with the following command:

```sh
 ! dataconverter \
--reader xrd \
--nxdl NXxrd_pan \
$<xps-file location> \
$<eln-file location> \
--output <output-file location>.nxs
```

An example file can be found here in GitLab in [nomad-remote-tools-hub](https://gitlab.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/-/tree/develop/docker/xrd) feel free to vist and try out the reader.
