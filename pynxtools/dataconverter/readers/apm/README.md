# APM reader

## Purpose
Translate diverse file formats from the scientific community and technology partners
within the field of atom probe microscopy into a standardized representation using the
NeXus application definition NXapm.

## What this apm reader supports
The main idea behind the parser is to offer users a diverse example of how a parser for
specific file formats from atom probe can be written and designed. We would like to encourage
the APM community to share example files with us. These can be small and come from diverse
use cases. Ideally, these should represent data in files other than the already supported
ones, so that we can broaden the applicability of this parser.
For this we work together with the International Field Emission Society's (IFES)
Atom Probe Technical Committee (APT TC).

Specifically, the here implemented apm reader shows how to load and interpret
data and metadata in different file formats; specifically POS, ePOS, and the APT files
from APSuite6, including RNG, and RRNG.

The example also shows how metadata which are not contained in the above-mentioned file formats
can also be added to the NeXus file via a generic text file, specifically a YAML-based solution.
In this example implementation metadata are read from a YAML file and placed in the
respective places inside an HDF5. This HDF5 file is formatted according to the NXapm
application definition. NXapm is based on the data and metadata which are not only contained
in classical atom probe file formats but also include the ideas of the APT HDF file format
which was drafted by the IFES APT TC.

Using a YAML file to parse in metadata which would otherwise not be available with classical
file formats makes this example generic enough to work with many other electronic lab notebook
(ELN) solutions provided that these also export their metadata using a YAML file with the same
formatting and mapping of concepts on the here shown NeXus vocabulary.

## Getting started - standalone usage
If you use this dataconverter/apm parser as a standalone tool,
1. You should follow the interactive jupyter notebook that is stored in
   *pynxtools/examples/apm*.
2. As the standalone usage of this parser does not require a NOMAD OASIS instance,
   you have to edit the ELN manually or via another ELN. For this you can edit the
   example eln_data_apm.yaml which comes shipped with this example. Alternatively,
   you can at this point copy or place your own datasets into the working directory
   of the jupyter lab instance.
3. Once the YAML file has been edited, to your satisfaction you can continue
   executing the jupyter tutorial. This should create an instance of a NeXus/HDF5 file
   which is formatted according to the NXem application definition.

## Getting started - usage related to NOMAD OASIS
This parser can be used to map numerical data and metadata inside frequently
used file formats of atom probe tomography and related field-ion microscopy
software tools into a NeXus HDF5 file which complies with a specific version
of the NXapm application definition.

If you are using a NOMAD OASIS, you can use this tool as follows.
1. Log-in to a NOMAD OASIS and navigate to the *Create Uploads* tab.
2. Select apm example from the list of available options.
3. Drag-and-drop the file with your reconstructed dataset via pos, epos, or apt,
   and add your ranging definitions file via rrng, or rng, or the fig files from
   Peter Felfer's Erlangen atom-probe-toolbox.
3. Edit the electronic lab notebook (ELN) schema inside the NOMAD OASIS and click the
   save button in the NOMAD OASIS GUI to save the data that you have entered into
   the ELN template. Clicking *save* will trigger the automatic generation
   of an eln_data.yaml file. Second, the clicking will trigger a run of the
   dataconverter/apm parser which generates a NXapm NeXus file based on the data
   in the reconstruction and ranging file and the eln_data.yaml file. Afterwards,
   the file will be displayed in the GUI and show up in the upload section of your OASIS.
   By default the converter performs a strong loss-less compression on the input
   as many of the stack data store integers with a low entropy. The compression may
   take some time. You can inspect the progress of the conversion in the console from
   which you started the NOMAD OASIS appworker.
4. If successful, a NeXus (nxs) file will appear in your upload. You can explore
   its content with the H5Web tools inside the NOMAD OASIS GUI and click interactively
   through the data including default plots. For atom probe these are a 3D discretized
   view of your reconstruction using 1nm rectangular binning and the mass spectrum
   with a default 0.01 Da binning an no additional corrections.
   If unsuccessful, the console from where you started the NOMAD appworker can help
   you with identifying if problems occurred.


## A request to take action by the technology partners
In fact, while the above-mentioned file formats and corresponding commercial software is routinely
used by numerous atom probers every day, the actual knowledge about the I/O routines has always
been on a few developers shoulders. In fact many of the open-source readers for file formats were
reverse-engineered. This is challenging because the amount of documentation that is available
for some file formats is neither exhaustive nor documented enough in detail.

This limits developers to decide and design how to best implement possible mappings of
specific binary numerical data and metadata into specifically named fields. We wish that
intensified exchange between technology partners like AMETEK/Cameca and the atom probe
community can help to improve the situation. Everybody is very welcomed to leave us
comments in the issue list (or drop us an email) to exchange specifically about this topic.

## Known limitations of this reader
Currently the apm parser reads the following quantities: reconstructed ion positions,
and mass-to-charge-state ratio values. The readers are technically capable to read
also all other fields in ePOS and APT files to the extent as these have been
documented by AMETEK/Cameca and the atom probe literature.

## Known performance issues of this reader
When the ranging definitions have molecular ions which are composed from many atoms
and using elements with many isotopes it is possible that the interpretation
of the ranging definitions can take long. The situation is highly case dependent.
The reason for this is that the apm reader internally uses a combinatorial
algorithm via the ifes_apt_tc_data_modeling library. Using this library has the 
benefit that it is automatically capable to identify charge states but for
complex molecular ions it may take a while evaluate all possible isotopic
combinations.

Currently, a more severe performance issue, relevant for some cases and input, is
that the verification of the instantiated schema is slow. This verification step
happens before the data are written to HDF5. The reason for this issue is that
components of the dataconverter traverse the dependency graph of the instantiated
NeXus application definition to assure that the template is valid, i.e. that
all required quantities are defined and mapping their individual concepts as defined
in NXapm. Depending on the complexity of the data model and which branches will be
instantiated by the input, though, this evaluation may be slower
as more pathes have to be visited. Noteworthy users should understand that this
issue is independent of size of the input (i.e. how many ions a dataset has).

## Contact person in FAIRmat for this reader
Markus Kühbach
