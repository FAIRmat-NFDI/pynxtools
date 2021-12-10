# Yaml to nxdl converter

This tool is composed of several steps:

1) read the user-specific experimental information as a yml file 

2) create an instantiated NXDL schema XML tree. 
   a) header add XML schema/namespaces
   b) user-defined attributes for the root group
   c) docstring

3) walk the dictionary nested in yml to create an instantiated NXDL schema XML tree rt

4) write the tree to a properly formatted NXDL XML file to disk

```console
user@box:~$ python yaml2nxdl.py

Usage: ./yaml2nxdl.py [OPTIONS]

Options:
   --input-file TEXT    The path to the input data file to read. (Repeat for
                        more than one file.)
   --help               Show this message and exit.

```
