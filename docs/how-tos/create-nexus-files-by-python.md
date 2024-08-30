# Create NeXus files by python

# The goal

Use python to create a NeXus file (.nxs) by hardcoding via the python package h5py. NeXus files can as well be created by our software [pynxtools](https://github.com/FAIRmat-NFDI/pynxtools) automatically, IF a recipe for the specific device/instrument/data-structure is written. This How-To is intended as easy access to FAIRdata structures via NeXus. For static-datastructures (i.e. always the same type of standard measurement) or one-time examples (small data publications), this may provide a feasable solution. For large scaled automated file processing, storage and validatation use [pynxtools](https://github.com/FAIRmat-NFDI/pynxtools) and it's measurement method specific plugins.

You can find the necessary file downloads [here](https://zenodo.org/records/13373909).



# Create NeXus by hardcoding with python

Install h5py via pip by `pip install h5py`

Then you can create a nexus file by the python script called [h5py_nexus_file_creation.py](https://zenodo.org/records/13373909/files/h5py_nexus_file_creation.py?download=1).

```
# Import h5py, to write an hdf5 file
import h5py

# create a h5py file in writing mode with given name "NXopt_minimal_example", file extension "nxs"
f = h5py.File("NXopt_minimal_example.nxs", "w")

# there are only 3 fundamental objects: >group<, >attribute< and >datafield<.


# create a >group< called "entry"
f.create_group('/entry')

# assign the >group< called "entry" an >attribute<
# The attribute is "NX_class"(a NeXus class) with the value of this class is "NXentry"
f['/entry'].attrs['NX_class'] = 'NXentry'

# create >datafield< called "definition" inside the entry, and assign it the value "NXoptical_spectroscopy"
# This field is important, as it is used in validation process to identify the NeXus definition.
f['/entry/definition'] = 'NXoptical_spectroscopy'
```

This proves a starting point of the NeXus file. We will go through these functions in the following.



# 2. Fill the content of the .nxs file

Go to [FAIRmat NeXus definitions](<https://fairmat-nfdi.github.io/nexus_definitions/index.html#>)

Scroll down until you see the search box named "Quick search".

Type "NXoptical" and press start the search.

You see several search results, select the one with is named "NXoptical\_spectroscopy".

Then you are (ideally) on this page: [NXoptical_spectroscopy NeXus definition](<https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_spectroscopy.html>)

You see a tree like structure of the NeXus definition NXoptical\_spectrosocopy with several tree nodes: Status, Description, Symbols, Groups\_cited, Structure. For now, only the part in Structure is of interest. This contains the information, which has to be written in the python code to add fields/groups/attributes to the NeXus file.

Use your browser search (CRTL+F) and search for "required". Ideally your browser highlights all entries which are required. You have to add those to the python script, to extend your created .nxs file. (Which fields/groups/attributes are "required" was defined by the respective scientific community, to ensure that the data serves the FAIR principles.)

In the following, it will be shown, how the python script has to be extended for the three fundamental objects:

1. Attribute

2. Datafield

3. Group





# 3. Adding a NeXus attribute

Search for the first concept/object in the NeXus file, which is not created yet. It is:

**@version**: (required) [NX\_CHAR](<https://fairmat-nfdi.github.io/nexus_definitions/nxdl-types.html#nx-char>) [⤆](<https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-definition-version-attribute>)

1. It is located in the tree at position: ENTRY/definition/

2. The "@" indicates that this is an attribute of the concept "definition".

3. The name of the attribute is "version".

4. Since it is "required", thas this attribute has to be added so that the resulting NeXus file is compliant with the NeXus definition "NXoptical\_spectroscopy".

5. The "NX\_CHAR" indicates the datatype. This should be a string: "The preferred string representation is UTF-8" (more information see [here](<https://manual.nexusformat.org/nxdl-types.html>))

![image.png](<./attachments/51dc82f9f0f5ec2f-image.png>)

Now the python script has to be extended in the following:

```
f['/entry/definition'].attrs['version'] = 'v2024.02'
```

This h5py command adds the attribute named "version" with the value "v2024.02" to the HDF5 dataset called  "/entry/definition". The same is done for the URL attribute:

```
f['/entry/definition'].attrs['URL'] = 'https://github.com/FAIRmat-NFDI/nexus_definitions/blob/f75a29836431f35d68df6174e3868a0418523397/contributed_definitions/NXoptical_spectroscopy.nxdl.xml'
```

For your use case, you may want to use a different version of the NeXus definitions, since these are changed over time. In the following, it is shown where to obtain the correct version and URL.

### How to get the "version" and "URL" values

At the time, you create the NeXus definition. Go to the page of the respectively used NeXus concept, i.e. [NXoptical_spectroscopy](<https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_spectroscopy.html>)

Scroll down until you find "**NXDL Source**:" and follow this link, i.e. [NXoptical_spectroscopy.nxdl.xml](<https://github.com/FAIRmat-NFDI/nexus_definitions/blob/fairmat/contributed_definitions/NXoptical_spectroscopy.nxdl.xml>)

This is the GitHub website, in which the latest (FAIRmat) NeXus definition of NXoptical\_spectroscopy is stored in the NeXus definition language file (.nxdl). The information is structured in the xml format.

Now you have to copy the permalink of this file. Go to the top right side of the website. Find the Menu made by 3 dots:

![image.png](<./attachments/c6ab2f4b925aed27-image.png>)

Copy the permalink and insert it as value for the "URL" attribute (Step 1, Red box in the image)

Go to "nexus\_definitions" (Step 2, Red box in the image)

![image.png](<./attachments/d8e727b3b32dcbb9-image.png>)

On the right side, you should see below "Releases" the "tags" (Red box in the image). Follow this link.

Copy the latest tag, which should look similar to "v2024.02". Insert it as value for the "version" attribute.

### Disclaimer:
It would be better, to specify this version tag to include as well the "GitHub commit id". In this way, a [pynxtools generated version tag](https://github.com/FAIRmat-NFDI/pynxtools/blob/c13716915bf8f69068c3b94d1423681b580fd437/src/pynxtools/_build_wrapper.py#L17) might look like this:
`v2022.07.post1.dev1278+g1d7000f4`. For simplicity, this is omitted here.





# 4. Adding a datafield

Two attributes were added two "ENTRY/definition", both of which were required. By now, this part of the NeXus file fulfills the requirements of the application definition NXoptical\_spectroscopy.

The next required concept of [NXoptical_spectrsocopy](https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_spectroscopy.html) is "**experiment\_type"**.

**experiment\_type**: (required) [NX\_CHAR](<https://fairmat-nfdi.github.io/nexus_definitions/nxdl-types.html#nx-char>)

1. It is located in the tree at position: ENTRY/

2. There is no "@" in front of "**experiment\_type"**. So, this may be a group or a datafield.

3. The name of this group/datafield is "**experiment\_type**".

4. The "required" indicates, that this group/datafield has to be added to be in line with the NeXus definition "NXoptical\_spectroscopy".

5. The "NX\_CHAR" indicates the datatype. This should be a string: "The preferred string representation is UTF-8" (more information see [here](<https://manual.nexusformat.org/nxdl-types.html>)).

6. The "NX\_CHAR" indicates that this is a datafield. It is NOT a group.  
    A group is a NeXus class. "NXentry" is for example is a NeXus class, while "NX_CHAR" indicates the datatype of the field.
    Wheter or not the underscore "_" is present after NX, indicates therefore if it is a NeXus class or datafield.

Read the documentation at "▶ Specify the type of the optical experiment. ..." by extending it via click on the triangle symbol. You should see something like this:

![image.png](<./attachments/5cbd8c6a1ca227df-image.png>)

There, the value of the datafield, has to be one of the shwon list. e.g "transmission spectroscopy", since it is an enumeration. Note that this is case sensitive.

Therefore, the python script has to be extended by:

```
f['/entry/experiment_type'] = 'transmission spectroscopy'
```





# 5. Adding a group

The first required group in NXoptical\_spectroscopy on the "ENTRY/" level is "**INSTRUMENT**: (required) [NXinstrument](<https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinstrument.html#nxinstrument>) [⤆"](<https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-instrument-group>)

1. It is located in the tree at position: NXentry/experiment_type

2. There is no "@" in front of "**INSTRUMENT"** and because the "NXinstrument" is a NeXus class, this has to be implemented as group in the python script.

3. The "required" indicates that this group has to be added to be in line with the NeXus definition "NXoptical\_spectroscopy".

4. The "NXinstrument" indicates that it is a NeXus class (or group in python), as it starts with "NX".

5. As this is a group, attributes or valuees may be assigned to it.

6. As this is a group, it can contain many datafields or groups.

7. The uppercase notation of "**INSTRUMENT**" means:

    1. You can give INSTRUMENT [almost](https://manual.nexusformat.org/datarules.html) any name, such as "abc" or "Raman\_setup" (see "regex" or regular expression).

    2. You can create as many groups with the class NXinstrument as you want. Their names have to be different.

    3. For more information see the [NeXus rules](../learn/nexus-rules.md)

The respective python code to implement a NXinstrument class (or equivalently in python group) with the name "experiment\_setup\_1" is:

```
f.create_group('/entry/experiment_setup_1')
f['/entry/experiment_setup_1'].attrs['NX_class'] = 'NXinstrument'
```

The first line creates the group with the name "experiment\_setup\_1".

The second line assigns this group the attribute with the name "NX\_class" and it's value "NXinstrument".





# 6. Finishing the .nxs file

This has to be done by using the respective NeXus definiton website:

[NXoptical_spectroscopy](<https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_spectroscopy.html>)

And by searching for all "required" entries. The next required entries are located inside the NXinstrument class:

1. **beam\_TYPE**: (required) [NXbeam](<https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam>) [⤆](<https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinstrument.html#nxinstrument-beam-group>)

2. **detector\_TYPE**: (required) [NXdetector](<https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector>) [⤆](<https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinstrument.html#nxinstrument-detector-group>)

Both are groups. "**beam\_TYPE"** could be named: "beam\_abc" or "beam\_Raman\_setup". Use the knowledge above to extend the python script to create those NeXus file entries.

### Note for required concepts in optional fields/groups:

Above in the definition of NXoptical\_spectroscopy, you as well may found a required entry "**depends\_on**: (required) [NX\_CHAR](<https://fairmat-nfdi.github.io/nexus_definitions/nxdl-types.html#nx-char>) [⤆"](<https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXcoordinate_system.html#nxcoordinate-system-depends-on-field>). This is at the level of "ENTRY/reference\_frames/beam\_ref\_frame". If you dont have the group "**beam\_ref\_frame"** because this is "optional", then you don't need to have this field.




### Feedback and contact:

1. Best way is to contact the software development directly via a [Github Issue](https://github.com/FAIRmat-NFDI/nexus_definitions/issues/new).

2. ron.hildebrandt(at)physik.hu-berlin.de



