# Using Python to create NeXus files

In general, we recommend using [`pynxtools`](https://github.com/FAIRmat-NFDI/pynxtools) to create NeXus files, which has the inherent advantage that the resulting NeXus file gets automatically validated against the NeXus application definition during conversion.

However, in some cases, it might be simpler to create the NeXus NeXus file (.nxs) directly using Python. For static data structures (i.e., always the same type of standard measurement) or one-time examples (small data publications), this may provide a feasible solution. For large scaled automated file processing, storage, and validation, we strongly recommend using `pynxtools` and its measurement method specific [plugins](../../reference/plugins.md).

This How-To is intended as easy access to FAIR data structures _via_ NeXus. It will demonstrate how NeXus file can be created in Python using `h5py`.

**You can find all of the data on Zenodo:**

[Download from Zenodo](https://zenodo.org/records/13373909){:target="_blank" .md-button }

Specifically, the Python script for creating a NeXus file can be downloaded here:

[Download h5py_nexus_file_creation.py](https://zenodo.org/records/13373909/files/h5py_nexus_file_creation.py?download=1){:target="_blank" .md-button }

We will discuss its content below and guide you through step-by-step in creating your NeXus file by hand.

## Create a NeXus file through Python and h5py

You start by installing `h5py` via `pip`:

```bash
pip install h5py
```

Next, we create the Python file and fill it with a minimal structure.

``` python
# Import h5py, to write an hdf5 file
import h5py

# create a h5py file in writing mode with given name "NXopt_minimal_example", file extension "nxs"
f = h5py.File("NXopt_minimal_example.nxs", "w")

# there are only 3 fundamental objects: >group<, >attribute< and >field<.


# create a >group< called "entry"
f.create_group('/entry')

# assign the >group< called "entry" an >attribute<
# The attribute is "NX_class"(a NeXus class) with the value of this class is "NXentry"
f['/entry'].attrs['NX_class'] = 'NXentry'

# create >field< called "definition" inside the entry, and assign it the value "NXoptical_spectroscopy"
# This field is important, as it is used in validation process to identify the NeXus definition.
f['/entry/definition'] = 'NXoptical_spectroscopy'
```

This structure is the starting point for our NeXus file. We will go through these functions in the following.

## Add NeXus concepts

We will create a file according to the NeXus application definition [`NXoptical_spectroscopy`](<https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_spectroscopy.html>), which provides a generic description for experiments in optical spectroscopy.

On the linked documentation NeXus definitions documentation page, you see a tree-like structure of `NXoptical_spectroscopy` with several tree nodes: Status, Description, Symbols, Groups_cited, Structure. For now, only the part in Structure is of interest. This contains the information which has to be written in the Python code to add fields/groups/attributes to the NeXus file.

Use your browser search (CTRL+F) and search for "required" to highlight all NeXus concepts which are required. You have to add those to the Python script to extend your created .nxs file. (Which fields/groups/attributes are "required" was defined by the respective scientific community, to ensure that the data serves the FAIR principles.)

In the following, it will be shown how to add three types of fundamental NeXus objects through the Python script:

1. Attribute

2. Field

3. Group

### Adding an attribute

In the tree structure, the first concept which is not created yet, is the `@version` attribute:

**@version**: (required) [NX\_CHAR](<https://fairmat-nfdi.github.io/nexus_definitions/nxdl-types.html#nx-char>) [⤆](<https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-definition-version-attribute>)

1. It is located in the tree at `ENTRY/definition/`

2. The "@" indicates that this is an attribute of the concept "definition".

3. The name of the attribute is "version".

4. Since it is "required", that means this attribute has to be added so that the resulting NeXus file is compliant with the NeXus definition `NXoptical\_spectroscopy`.

5. `NX\_CHAR` indicates the datatype. This should be a string: "The preferred string representation is UTF-8" (more information see [here](<https://manual.nexusformat.org/nxdl-types.html>))

![image.png](<../media/51dc82f9f0f5ec2f-image.png>)

We add an instance of this concept by adding an HDF5 attribute:

``` python
f['/entry/definition'].attrs['version'] = 'v2024.02'
```

This h5py command adds the attribute named "version" with the value "v2024.02" to the HDF5 dataset called "/entry/definition". The same is done for the URL attribute:

``` python
f['/entry/definition'].attrs['URL'] = 'https://github.com/FAIRmat-NFDI/nexus_definitions/blob/f75a29836431f35d68df6174e3868a0418523397/contributed_definitions/NXoptical_spectroscopy.nxdl.xml'
```

For your use case, you may want to use a different version of the NeXus definitions, since these are changed over time. In the following, it is shown where to obtain the correct version and URL.

__Get the values: *version* and *URL*__

At the time you create the NeXus file, can do the following to find the version and associated URL:

- Go to the page of the respectively used NeXus concept, i.e. [NXoptical_spectroscopy](<https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_spectroscopy.html>)

- Scroll down until you find "**NXDL Source**:" and follow this link, i.e. [NXoptical_spectroscopy.nxdl.xml](<https://github.com/FAIRmat-NFDI/nexus_definitions/blob/fairmat/contributed_definitions/NXoptical_spectroscopy.nxdl.xml>)

This is the GitHub website, in which the latest (FAIRmat) NeXus definition of NXoptical\_spectroscopy is stored in the NeXus definition language file (.nxdl). The information is structured in the xml format.

- Now you have to copy the permalink of this file. Go to the top right side of the website. Find the Menu made by 3 dots:

![image.png](<../media/c6ab2f4b925aed27-image.png>)

Copy the permalink and insert it as value for the "URL" attribute (Step 1, Red box in the image)

- Go to "nexus\_definitions" (Step 2, Red box in the image)

![image.png](<../media/d8e727b3b32dcbb9-image.png>)

On the right side, you should see below "Releases" the "tags" (Red box in the image). Follow this link.

- Copy the latest tag, which should look similar to "v2024.02". Insert it as value for the "version" attribute.

__Disclaimer__
When specifying this version tag, it would be better to include the GitHub commit ID as well. In pynxtools, these are [appended automatically](https://github.com/FAIRmat-NFDI/pynxtools/blob/c13716915bf8f69068c3b94d1423681b580fd437/src/pynxtools/_build_wrapper.py#L17). Such a version tag might look like this:
`v2022.07.post1.dev1278+g1d7000f4`.

If you have pynxtools installed, you can get the tag by:

```python
from pynxtools import get_nexus_version
get_nexus_version()
>>> 'v2022.07.post1.dev1284+gf75a2983'
```

### Adding a field

The next required concept of [NXoptical_spectroscopy](https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_spectroscopy.html) is "**experiment\_type"**.

**experiment\_type**: (required) [NX\_CHAR](<https://fairmat-nfdi.github.io/nexus_definitions/nxdl-types.html#nx-char>)

1. It is located in the tree at position `ENTRY/`

2. There is no "@" in front of "**experiment\_type"**. So, this may be a group or a field.

3. The name of this group/field is "**experiment\_type**".

4. The "required" indicates that this group/field has to be added to be in line with the NeXus definition "NXoptical\_spectroscopy".

5. `NX\_CHAR` indicates the datatype. This should NXoptical_spectrs be a string (see above).

6. The presence of the datatype `NX\_CHAR` indicates that this is a field. It is NOT a group.

Read the documentation at "▶ Specify the type of the optical experiment. ..." by extending it via click on the triangle symbol. You should see something like this:

![image.png](<../media/5cbd8c6a1ca227df-image.png>)

There, the value of the field has to be one of the shown list, since it is an enumeration (e.g. "transmission spectroscopy"). Note that this is requires an exact match to one of the enumerated items (case and whitespace sensitive).

Therefore, the Python script has to be extended by:

``` python
f['/entry/experiment_type'] = 'transmission spectroscopy'
```

### Adding a group

The first required group in NXoptical\_spectroscopy on the `ENTRY/` level is "**INSTRUMENT**: (required) [NXinstrument](<https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinstrument.html#nxinstrument>) [⤆"](<https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXentry.html#nxentry-instrument-group>)

1. It is located in the tree at position: NXentry/

2. There is no "@" in front of "**INSTRUMENT"** and because the `NXinstrument` is a NeXus group, this has to be implemented as an HDF5 group in the Python script.

3. The "required" indicates that this group has to be added to be in line with the NeXus definition "NXoptical\_spectroscopy".

4. As this is a group, other groups, fields, or attributes may be assigned to it.

5. The uppercase notation of "**INSTRUMENT**" means:

    1. You can give INSTRUMENT [almost](https://manual.nexusformat.org/datarules.html) any name, such as "abc" or "Raman\_setup" (see "regex" or regular expression).

    2. You can create as many groups with the class `NXinstrument` as you want. Their names have to be different.

    3. For more information, see the [NeXus rules](../../learn/nexus/nexus-rules.md)

The Python code to implement the `NXinstrument` group as an HDF5 group named with the name "experiment\_setup\_1"  is:

``` python
f.create_group('/entry/experiment_setup_1')
f['/entry/experiment_setup_1'].attrs['NX_class'] = 'NXinstrument'
```

The first line creates the group with the name "experiment\_setup\_1".

The second line assigns this group the attribute with the name "NX\_class" and its value "NXinstrument".

### Finishing the NeXus file

Afterwards, we repeat the process for all required NeXus groups/fields/attributes defined in
[NXoptical_spectroscopy](<https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXoptical_spectroscopy.html>).

The next required entries are located inside the NXinstrument class:

1. **beam\_TYPE**: (required) [NXbeam](<https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXbeam.html#nxbeam>) [⤆](<https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinstrument.html#nxinstrument-beam-group>)

2. **detector\_TYPE**: (required) [NXdetector](<https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXdetector.html#nxdetector>) [⤆](<https://fairmat-nfdi.github.io/nexus_definitions/classes/base_classes/NXinstrument.html#nxinstrument-detector-group>)

Both are groups. "**beam\_TYPE"** could be named: "beam\_abc" or "beam\_Raman\_setup". Use the knowledge above to extend the Python script to create those NeXus file entries.

Note that you can also add instances for recommended or optional concepts to the file by using the same Python functionality as above. The difference to the required concept is that they _have_ to be present in order for the file to comply with the application definitions, whereas recommended/optional files _can_, but don't need to be present.

## What's next?

- Once you have a finished NeXus file, you may continue [by validating the NeXus file](../pynxtools/validate-nexus-files.md).
- If you find yourself in the situation that you need to run such Python code routinely to convert your data, we strongly recommend creating your own reader or plugin in the `pynxtools` ecosystem. You can find a how-to guide to get you started [here](build-a-plugin.md).
