#Yaml to nxdl converter

This tool is composed of several steps:

a) read the user-specific experimental information as a yml file 

b) create an instantiated NXDL schema XML tree

c) write the NXDL XML file to file

```console
user@box:~$ python yaml2nxdl.py

Usage: ./yaml2nxdl.py [OPTIONS]

Options:
   --input_file TEXT    The path to the input data file to read. (Repeat for
                        more than one file.)
   --help               Show this message and exit.

```

The tool is reading a yml file manually defined in the 'fnm' variable in yaml2nxdl.py

