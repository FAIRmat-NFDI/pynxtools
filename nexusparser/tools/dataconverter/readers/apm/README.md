# APM reader

## Purpose
Translate diverse vendor and community file formats from atom probe microscopy
into a standardized representation using the NeXus application definition NXapm.
The parser does not copy over all the data and metadata in the vendor files
but the particular subset that is understood and useful inside a NOMAD OASIS instance.

## What this apm reader supports
The main idea behind the parser is to offer users of the OASIS a diverse example
of how a parser for specific file formats can be written and designed. We would like
to encourage the APM community to share with us example files (these can be small and
from diverse use cases), ideally represent in other vendor file formats like those
implemented here already. With these examples we can improve the parser mainly
by broaden its applicability.

Specifically, the implementation shows how data different file formats can be
loaded and interpreted: POS, ePOS, and the APT files from APSuite6, RNG, and RRNG.

The example also shows how metadata which are not contained in the above-mentioned
file format can also be added to the NeXus file with a generic text file, specifically
YAML file format based solution. In our example implementation here we read these
metadata from a YAML file and place the values in the respective places in the HDF5
according to their place in the NXapm application definition.

This makes this example generic to work with many other electronic lab notebook
solutions provided that also these ELNs export a YAML file with the same formatting.

## Getting started - usage related to NOMAD OASIS
This parser can be used to map numerical data and metadata inside frequently
used vendor file formats of electron microscopy software tools into a NeXus
HDF5 file which complies with a specific version of the NXapm application
definition.

If you are using a NOMAD OASIS you can use this tool as follows.
1. Log-in to a NOMAD OASIS and navigate to the *Create Upload* tab.
2. Select APM example from the list of available options.
3. Drag-and-drop your files in vendor-specific formats.
   Currently pos, epos, apt (for reconstructed datasets) and rrng or rng 
   for ranging definitions/range files) are supported.
3. Edit the electronic lab notebook (ELN) schema inside the NOMAD OASIS and
   click the save button in the NOMAD OASIS GUI to save the data that you have
   entered in this ELN template. Clicking *save* will trigger the automatic generation
   of an eln_data.yaml utility file. Second, the clicking will trigger a run of the
   dataconverter/apm parser which generates an NXapm NeXus file based on the data
   in the vendor files and the eln_data.yaml file. The file will be returned in the OASIS.
   By default the converter performs a strong loss-less compression on the input
   as many of the stack data store integers with a low entropy.
   The compression may take some time. You can inspect the progress of the conversion
   in the console from which you started the NOMAD OASIS appworker.
4. If successful, a NeXus (nxs) file will now in your upload. You can explore
   its content with the H5Web tools inside the NOMAD OASIS GUI.
   If unsuccessful, the data logger can help you to identify if problems occurred.

## Getting started - standalone usage
If you use this dataconverter/apm parser as a standalone tool,
1. You should follow the interactive jupyter notebook that is stored in
   *nomad-parser-nexus\tests\data\tools\dataconverter\readers\apm*.
2. As the standalone usage of this parser does not require a NOMAD OASIS instance,
   you have to edit the ELN manually. For this you can edit the example that
   comes shipped with the example. Alternatively, you can at this point copy or
   place your own datasets into the working directory of the jupyter instance.
   Specifically, after you have placed the vendor files also edit the eln_data.yaml
   file.
3. Ones the eln_data.yaml file has been edited you can continue executing the jupyter tutorial.
4. If successful, your edits of the eln_data.yaml will be considered and processed
   together with the data files into an instance of a NeXus HDF5 file, formatted
   according to the NXapm application definition.

## A request to take action by the vendors
In fact, while the above-mentioned vendor software is nowadays used by numerous of users every day,
the actual knowledge about the I/O routines has always been on a few developers shoulders.
We have realized that many of the file format readers in open-source software were reverse-engineered
which is challenging because the amount of documentation that is especially for
some vendor file formats is neither exhaustive nor detailed enough. This limits developers
to decide and design how to best implement the mapping of specific binary numerical data and metadata
into specifically named fields. Here we hope that intensified exchange between vendors and the community
can help to improve the situation. You are very welcome to leave us comments in the issue
list to exchange specifically about this topic.

Limited technical documentation of some vendor file formats stands in strong contrast
to the powerful GUI-based tools and the in fact continuous efforts of the vendors
to make the barriers for working with microscopy data simpler.

## Known limitations of this parser

Currently the apm parser reads the following quantities: reconstructed ion positions, and mass-to-charge-state ratio values.
The readers are technically capable though to read also all other fields which are stored in ePOS and APT files.
