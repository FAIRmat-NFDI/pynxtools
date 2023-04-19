This utility outputs a debug log for a given NeXus file by annotating the data and
metadata entries with the schema definitions from the respective NeXus base classes
and application definitions to which the file refers to.

```
Options:
    -f, --nexus-file : Name of nexus output file (.nxs) to enquiry.
    -d, --documentation : Definition path in nexus output (.nxs) file. Returns debug
                          log relavent with that definition path.
                          Example: /entry/data/delays
    -c, --concept : Concept path from application definition file (.nxdl,xml). Finds out
                    all the available concept definition (IS-A realation) for rendered
                    concept path.
                    Example: /NXarpes/ENTRY/INSTRUMENT/analyser
    --help : To get the documentaion above
    NOTE: Only one option from (-d and -c) is acceptable.

In console:

read_nexus [Options] <path_to_nexus_file>



```

_The environmental variable called "NEXUS_DEF_PATH" can be set to
a directory, which contains the NeXus definitions as XML files. If this environmental
variable is not defined, the module will use the definitions in its bundle._

An environmental variable can be set as follows:

```
export 'NEXUS_DEF_PATH'=<folder_path_that_contains_nexus_defs>
```

Following example dataset can be used to test `read_nexus` module `tests/data/nexus/201805_WSe2_arpes.nxs`.
This is an angular-resolved photoelectron spectroscopy (ARPES) dataset and it is formatted according to
the [NXarpes application definition of NEXUS](https://manual.nexusformat.org/classes/applications/NXarpes.html#nxarpes).