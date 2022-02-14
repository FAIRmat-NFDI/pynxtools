# YAML to NXDL converter and NXDL to YAML converter

**Tools purpose**: Offer a simple YAML-based schema and a XML-based schema to describe NeXus instances. These can be NeXus application definitions, or classes such as base or contributed classes. Users either create NeXus instances by writing a YAML file or a XML file which details a hierarchy of data/metadata elements.
The forward (YAML -> XML) and backward (XML -> YAML) conversions are implemented.

**How the tool works**:
- yaml2nxdl.py
1. Reads the user-specified NeXus instance, either in YML or XML format.
2. If input is in YAML, creates an instantiated NXDL schema XML tree by walking the dictionary nest.
   If input is in XML, creates a YML file walking the dictionary nest.
3. Write the tree into a YAML file or a properly formatted NXDL XML schema file to disk.
4. Optionally, if --append argument is given,
   the XML or YAML input file is interpreted as an extension of a base class and the entries contained in it
   are appended below a standard Nexus base class.
   You need to specify both your input file (with YAML or XML extension) and Nexus class (with no extension).
   Both .yml and .nxdl.xml file of the extended class are printed.

```console
user@box:~$ python yaml2nxdl.py

Usage: python yaml2nxdl.py [OPTIONS]

Options:
   --input-file TEXT     The path to the input data file to read.
   --append TEXT         Parse xml NeXus file and append to specified base class,
                         write the base class name with no extension.
   --verbose             Addictional std output info is printed to help debugging.
   --help                Show this message and exit.

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
