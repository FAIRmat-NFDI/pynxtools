# NeXus file reader and debugger

This utility outputs a debug log for a given NeXus file by annotating the data and
metadata entries with the schema definitions from the respective NeXus base classes
and application definitions to which the file refers to.

```console
user@box:~$ read_nexus --help
Usage: read_nexus [OPTIONS]

  The main function to call when used as a script.

Options:
  -f, --nexus-file TEXT     NeXus file with extension .nxs to learn NeXus
                            different concept documentation and concept.
  -d, --documentation TEXT  Definition path in nexus output (.nxs) file.
                            Returns debuglog relavent with that definition
                            path. Example: /entry/data/delays
  -c, --concept TEXT        Concept path from application definition file
                            (.nxdl,xml). Finds outall the available concept
                            definition (IS-A realation) for renderedconcept
                            path. Example: /NXarpes/ENTRY/INSTRUMENT/analyser
  --help                    Show this message and exit.

NOTE: Only one option from (-d and -c) is acceptable.
```

The following example dataset can be used to test the `read_nexus` module: `tests/data/nexus/201805_WSe2_arpes.nxs`.
This is an angular-resolved photoelectron spectroscopy (ARPES) dataset and it is formatted according to
the [NXarpes application definition of NeXus](https://manual.nexusformat.org/classes/applications/NXarpes.html#nxarpes).

## Using a different set of NeXus definitions
_The environmental variable called "NEXUS_DEF_PATH" can be set to
a directory, which contains the NeXus definitions as XML files. If this environmental
variable is not defined, the module will use the definitions in its bundle._

An environmental variable can be set as follows:

```
export 'NEXUS_DEF_PATH'=<folder_path_that_contains_nexus_defs>
```

## A note to Windows users
If you run `read_nexus` from `git bash`, you need to set the environmental variable
`MSYS_NO_PATHCONV` to avoid the [path translation in Windows Git MSys](https://stackoverflow.com/questions/7250130/how-to-stop-mingw-and-msys-from-mangling-path-names-given-at-the-command-line#34386471).
The easiest way is to prefix the `read_nexus` call with `MSYS_NO_PATHCONV=1`:

```
MSYS_NO_PATHCONV=1 read_nexus -c /NXarpes/ENTRY/INSTRUMENT/analyser
```