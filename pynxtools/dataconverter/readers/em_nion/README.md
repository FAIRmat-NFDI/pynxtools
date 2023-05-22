# em_nion reader

## Purpose
Parse convertable content from data and metadata inside an nionswift project to NXem.

## Input required
* eln_data.yaml file, contextualizing information entered via ELN (user, sample)
* *.nszip, rename *.zip file with the nionswift *.nsproj project file and its data objects
  renamed from zip to nszip to avoid that it gets unpacked during the upload

## Configuration files
For nionswift most data objects are not necessarily linked to concepts available in NeXus.
Internally, nionswift organizes data and metadata as so-called display_items. These can be
thought of as smart objects which have their data and metadata surplus a uuid, a creation
time and a (last) modification time whereby the place in the object hierarchy documented by
the nsproj tree is defined.
These display_items can be images captured during a microscope session, they can be processed
data within nionswift, images, spectra, or even higher-dimensional objects which wrap
n-dimensional numpy arrays.
There is no direct conceptualization in nionswift what an object bests represents as a
concept, is the object representing an image with metadata or an EELS spectrum, or an
omega-q mapping.
Therefore, we use configuration files whereby the rules are implemented how the
em_nion parsers decides which metadata have to be offered in a particular formatted way
by the object so that it qualifies to represent an instance of a respective NeXus concept
offered via NXem, e.g. NXimage_set, NXspectrum_set, NXhyperstack_set.
The configuration files are used to reduce the amount of hard-coded information transfer
to a minimum. But given that different concepts demand different types of e.g. dimension
scale axes to resolve to useful/sensible instance of such concept some concept-specific
parts of the reader are hardcoded.

## Output
The em_nion reader returns an instance of an NXem NeXus HDF5 file where data for
recognized concepts are mapped with the data and some of their metadata.

## TODO
* Add example and describe
* Remove the focus of the README.md on the NOMAD OASIS product

## Contact person for this reader
Markus Kühbach