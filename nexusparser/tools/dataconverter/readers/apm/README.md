# APM reader

## Purpose
Translate diverse vendor and community file formats from atom probe microscopy into
a standardized representation using the NeXus application definition NXapm.
This parser does not copy over all of the data and metadata in the vendor file(s)
but the particular subset which is understood and useful inside a NOMAD OASIS instance.

## What this apm reader supports
The main idea behind the parser is to offer users of the OASIS a diverse example of how
a parser for specific file formats can be written and designed. We would like to encourage
the APM community to share example files with us. These can be small and come from diverse use cases.
Ideally, these should represent data in vendor file formats other than the already supported
ones, so that we can broaden the applicability of this parser.

Specifically, the implementation shows how data and metadata in different file formats can
be loaded and interpreted; specifically POS, ePOS, and the APT files from APSuite6, RNG, and RRNG.

The example also shows how metadata which are not contained in the above-mentioned file formats
can also be added to the NeXus file via a generic text file, specifically a YAML based solution.
In our example implementation we read these metadata from a YAML file and place the values in the
respective places inside the HDF5 according to their place as defined in the NXapm
application definition.

This makes this example generic to work with many other electronic lab notebook (ELN) solutions
provided also these export a YAML file using the same formatting.

## Getting started - usage related to NOMAD OASIS
This parser can be used to map numerical data and metadata inside frequently
used vendor file formats of electron microscopy software tools into a NeXus
HDF5 file which complies with a specific version of the NXapm application
definition.

If you are using a NOMAD OASIS, you can use this tool as follows.
1. Log-in to a NOMAD OASIS and navigate to the *Create Upload* tab.
2. Select APM example from the list of available options.
3. Drag-and-drop your files in vendor-specific formats, i.e. pos, epos, apt
   (for reconstructed datasets) and rrng or rng (for ranging definitions/range files).
3. Edit the electronic lab notebook (ELN) schema inside the NOMAD OASIS and click the
   save button in the NOMAD OASIS GUI to save the data that you have entered into
   the ELN template. Clicking *save* will trigger the automatic generation
   of an eln_data.yaml file. Second, the clicking will trigger a run of the
   dataconverter/apm parser which generates a NXapm NeXus file based on the data
   in the vendor file and the eln_data.yaml file. Afterwards, the file will be
   displayed in the GUI and upload section of your OASIS.
   By default the converter performs a strong loss-less compression on the input
   as many of the stack data store integers with a low entropy.
   The compression may take some time. You can inspect the progress of the conversion
   in the console from which you started the NOMAD OASIS appworker.
4. If successful, a NeXus (nxs) file will appear in your upload. You can explore
   its content with the H5Web tools inside the NOMAD OASIS GUI and click interactively
   through the data including default plots. For atom probe these are a 3D discretized
   view of your reconstruction using 1nm rectangular binning and the mass spectrum.
   If unsuccessful, the data logger can help you to identify if problems occurred.

## Getting started - standalone usage
If you use this dataconverter/apm parser as a standalone tool,
1. You should follow the interactive jupyter notebook that is stored in
   *nomad-parser-nexus\tests\data\tools\dataconverter\readers\apm*.
2. As the standalone usage of this parser does not require a NOMAD OASIS instance,
   you have to edit the ELN manually or via another ELN. For this you can edit the
   example eln_data_apm.yaml which comes shipped with this example. Alternatively,
   you can at this point copy or place your own datasets into the working directory
   of the jupyter lab instance.
3. Once the eln_data.yaml file has been edited to your satisfaction,
   you can continue executing the jupyter tutorial.
4. If successful, your edits of the eln_data.yaml will be considered and processed
   into an instance of a NeXus HDF5 file that is formatted according to the
   NXapm application definition.

## A request to take action by the vendors
In fact, while the above-mentioned vendor file formats and corresponding vendor software is routinely
used by numerous atom probers every day, the actual knowledge about the I/O routines has always
been on a few developers shoulders. In fact many of the open-source readers for vendor file formats were
reverse-engineered. This is challenging because the amount of documentation that is especially
for some vendor file formats available is neither exhaustive nor detailed enough. This limits developers
to decide and design how to best implement possible mappings of specific binary numerical data and metadata
into specifically named fields. We wish that intensified exchange between vendors and the community
can help to improve the situation. Everybody is very welcomed to leave us comments in the issue
list to exchange specifically about this topic.

Limited technical documentation of some vendor file formats stands in strong contrast
to the powerful GUI-based tools and the in fact continuous efforts of the vendors
to make the barriers for working with microscopy data simpler and becoming more
aligned with the FAIR principles.

## Known limitations of this parser

Currently the apm parser reads the following quantities: reconstructed ion positions,
and mass-to-charge-state ratio values. The readers are technically capable to read
also all other fields in ePOS and APT files to the extent as these have been
documented.
