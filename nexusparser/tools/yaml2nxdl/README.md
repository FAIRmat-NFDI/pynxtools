# YAML to NXDL converter and NXDL to YAML converter

**Tools purpose**: Offer a simple YAML-based schema to describe NeXus instances. These can be NeXus application definitions, or classes such as base or contributed classes. Users create NeXus instances by writing a YAML file which details a hierarchy of data/metadata elements.
The reverse conversion is also implemented.

**How the tool works**:
- yaml2nxdl.py
1. Reads the user-specified NeXus instance that the YML input file represents as a nested dictionary.
2. Creates an instantiated NXDL schema XML tree by walking the dictionary nest.
3. Write the tree into a properly formatted NXDL XML schema file to disk.

- nxdl2yaml.py
1. Reads the user-specified NeXus instance that the NXDL input file represents as a nested dictionary.
2. Creates a YML file walking the dictionary nest.
3. Optionally, if --append-to-base flag is switched on, the NXDL input file is read as an extension of a base class and the entries contained are appended below a standard Nexus base class. The NXDL file name must be the same of a Nexus base class for this feature.

```console
user@box:~$ python yaml2nxdl.py

Usage: ./yaml2nxdl.py [OPTIONS]

Options:
   --input-file TEXT    The path to the input data file to read. (Repeat for
                        more than one file.)
   --verbose            Addictional std output info is printed to help debugging.
   --help               Show this message and exit.


user@box:~$ python nxdl2yaml.py

Usage: ./nxdl2yaml.py [OPTIONS]

Options:
   --input-file TEXT    The path to the input data file to read. (Repeat for
                        more than one file.)
   --append-to-base     Parse xml file and append to base class, given that the xml file has same name of an existing base class.
   --help               Show this message and exit.

```

**Rule set**: From transcoding YAML files we need to follow several rules.
* Named NeXus groups, which are instances of NeXus classes especially base or contributed classes. Creating (NXbeam) is a simple example of a request to define a group named according to NeXus default rules. mybeam1(NXbeam) or mybeam2(NXbeam) are examples how to create multiple named instances at the same hierarchy level.
* Members of groups so-called fields. A simple example of a member is voltage. Here the datatype is implied automatically as the default NeXus NX_CHAR type.  By contrast, voltage(NX_FLOAT) can be used to instantiate a member of class which should be of NeXus type NX_FLOAT.
* And attributes or either groups or fields. Names of attributes have to be preceeded by \@ to mark them as attributes.

**Special keywords**: Several keywords can be used as childs of groups, fields, and attributes to specify the members of these. Groups, fields and attributes are nodes of the XML tree.
* *doc*: A human-readable description/docstring
* *exists* A statement if an entry is more than optional. Options are recommended, required, [min, 1, max, infty] numbers like here 1 can be replaced by uint or infty to indicate no restriction on how frequently the entry can occur inside the NXDL schema at the same hierarchy level.
* *link* Define links between nodes.
* *units* A statement introducing NeXus-compliant NXDL units arguments, like NX_VOLTAGE
* *dimensions* Details which dimensional arrays to expect
* *enumeration* Python list of strings which are considered as recommended entries to choose from.
