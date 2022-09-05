# em_spctrscpy reader

## Purpose
Translate diverse vendor and community file formats from atom probe microscopy into
a standardized representation using the NeXus application definition NXem.
This parser does not copy over all of the data and metadata in the vendor file(s)
but the particular subset which is understood and useful inside a NOMAD OASIS instance.

## What this em reader supports
The main idea behind the parser is to offer users of the OASIS a diverse example of how
a parser for specific file formats can be written and designed. We would like to encourage
the EM community to share example files with us. These can be small and come from diverse use cases.
Ideally, these should represent data in vendor file formats other than the already supported ones,
so that we can broaden the applicability of this parser.

Specifically, the implementation shows how I/O functionalities of hyperspy can be used 
to load data of spectroscopy experiments from three exemplar file formats:
Bruker BCF, Velox EMD, and DigitalMicrograph DM3. The implementation shows how instances
of NeXus base classes like NXspectrum_set_em_xray, NXspectrum_set_em_eels, and NXimage_set_em_adf
can be created and registered inside instances of NXevent_data_em; and then how all these
can be composed and stored inside a NeXus/HDF5 file that matches the NXem application definition.

This makes the example relevant for researchers who work within the fields of
scanning electron microscopy (SEM) EDS/EDX, transmission electron microscopy
(EDS/STEM), and electron energy loss spectroscopy (EELS).

## Getting started - usage related to NOMAD OASIS
This parser can be used to map numerical data and metadata inside frequently
used vendor file formats of electron microscopy software tools into a NeXus
HDF5 file which complies with a specific version of the NXem application
definition.

If you are using a NOMAD OASIS you can use this tool as follows.
1. Log-in to a NOMAD OASIS and navigate to the *Create Upload* tab.
2. Select EM example from the list of available options.
3. Drag-and-drop your files in vendor-specific formats, i.e. bcf, emd, dm3.
3. Edit the electronic lab notebook (ELN) schema inside the NOMAD OASIS and click the
   save button in the NOMAD OASIS GUI to save the data that you have entered into
   the ELN template. Clicking *save* will trigger the automatic generation
   of an eln_data.yaml file. Second, the clicking will trigger a run of the
   dataconverter/em_spctrscpy parser which generates a NXem NeXus file based on the data
   in the vendor file and the eln_data.yaml file. Afterwards, the file will be
   displayed in the GUI and upload section of your OASIS.
   By default the converter performs a strong loss-less compression on the input
   as many of the stack data store integers with a low entropy.
   The compression may take some time. Arrays with floating point values are
   also compressed by default but with a lower compression strength.
   You can inspect the progress of the conversion in the console from which
   you started the NOMAD OASIS appworker.
4. If successful, a NeXus (nxs) file will appear in your upload. You can explore
   its content with the H5Web tools inside the NOMAD OASIS GUI and click interactively
   through the data including default plots. For electron microscopy these are the 
   EDS/EDX spectra stack, eventually an sum spectrum, annular dark field) overview images
   of the material region-of-interest (ROI) characterized, and if present in the vendor
   file composition maps.
   If unsuccessful, the data logger can help you to identify if problems occurred.

Clearly as microscopy software tools differ, users should not expect that every
required field in the application definition can be served by the data and metadata
from an arbitrary such microscopy tool and its often vendor-specific output (file
formats). Therefore, the em_spctrscpy reader takes the additional metadata from the
eln_data.yaml file. Specifically, this file can be created with the ELN schema creation
and customization functionalities offered through NOMAD OASIS or via any other ELN
or solution which can edit yaml files.

## Getting started - standalone usage
If you use this dataconverter/em_spctrscpy parser as a standalone tool,
1. You should follow the interactive jupyter notebook that is stored in 
   *nomad-parser-nexus\tests\data\tools\dataconverter\readers\em_spctrscpy*.
2. As the standalone usage of this parser does not require a NOMAD OASIS instance,
   you have to edit the ELN manually or via another ELN. For this you can edit the
   example eln_data_em.yaml which comes shipped with this example. Alternatively,
   you can at this point copy or place your own datasets into the working directory
   of the jupyter lab instance.
3. Once the eln_data_yaml has been edited to your satisfaction,
   you can continue executing the jupyter tutorial.
4. If successful, your edits of the eln_data.yaml will be considered and processed
   into an instance of a NeXus HDF5 file that is formatted according to the
   NXem application definition.

## Background
This em_spctrscpy reader was implemented as a response to an issue during sprint 9 by
Markus Kühbach and members of area B of the FAIRmat project while working on
application definitions and parsers for injecting data into and creating examples
for electron microscopy data inside NOMAD OASIS.

## Technical background details for developers and data scientists
The em_spctrscpy reader serves as a parser with multiple parts/readers/and sub-parser components
because data and metadata in electron microscopy come from such a diverse number of file
formats and use cases, from results of interactions with different GUIs, vendor scripts
running inside GUIs, or user-customized/-written scripts using open-source microscopy
software tools that it is essentially to keep things organized.
These subtilities make the development of a general enough parser challenging.

Our approach with dataconverter/em_spctrscpy is to offer users of a NOMAD OASIS instance
first at all an implemented step-by-step example how they can combine different software
tools and make these operational in a NOMAD OASIS. Therefore, we follow an approach that
is breadth- rather than depth-first. Our approach is driven by examples.
Breadth first means we would like to offer the user first an overview of the rather large
number of NeXus base classes within the design of the NXem application definition.

Practically, the process needs to be driven by examples as many I/O routines of especially
vendor file formats in open-source software was designed by reverse engineering. In fact,
there is currently no joint knowledge base how all possible vendor files can be safely and
robustly parsed so that each field and entry is not only binarily readable but can also
confidently be mapped on specific terms using a controlled vocabulary.

Currently the example implements for:
* NXspectrum_set_em_xray
* NXspectrum_set_em_eels
* NXimage_set_adf

These three already cover how also the simpler NXimage_set_se and NXimage_set_bse
could be covered, although they are not explicitly implemented in the current example.

## NXem and the status quo of data schemes in electron microscopy
NXem is a general application definition which embraces multiple EM sub-communities.
Specifically, condensed-matter physicists, materials scientists, and materials engineers,
i.e. electron microscopy users which have all their own software solutions or at least
different, best practices and protocols currently, to interact and work with electron
microscopy data.

Our starting point in FAIRmat for EM was thus different compared to the situation
in e.g. the field of atom probe microscopy. In the field of atom probe, only a few file
formats exists and have been in use when the FAIRmat project started.
This is why dataconverter/apm has its own subroutines for loading intricate
details of vendor and open-source-documented file formats, which we have implemented
and offer as a reference implementation.

By contrast, for electron microscopy developing these many file format readers
on our own is not a feasible approach for the FAIRmat project for two reasons:

First, there is a very limited use of writing again readers for a specific EM file formats
because the EM community has developed already many of such a number of these by now.
Many of them are mature in that they offer internal readers for several file formats.
The strength of the existent readers is that many users already work with such software.
Thus, supporting the development and working together on I/O functions for vendor files
and discussing open issues is in our opinion the preferred approach.

Specific examples of such community tools are:
**hyperspy** for analyses of spectra such as EDX/EDS and EELS, used in SEM/TEM communities
**mtex** for analyses of texture, and EBSD data, heavily used in the SEM community
**dream3d** for 3D EBSD post-processing into synthetic volume elements
**EMsoft** for indexing EBSD, **kikuchipy** and **pyxem** leaning towards the TEM community

Instead of reimplementing the wheel, we are convinced the I/O functionalities of these tools
should be used by even more people to support the respective open-source projects involved.

The other reason why we are not convinced that it is a sustainable approach for a National
Research Data Infrastructure that each project implements own formats is that there are already
two important challenges with the current status quo in electron microscopy:
Format constraints and limited documentation of the content and details behind 
some of the vendor file formats. We should make clear that we acknowledge the
significant momentum and effort which is ongoing at microscopy manufacturing companies
on implementing strategies for their software tools to store and document metadata.
We would like to see though that more of these efforts become documented in the literature
and the public domain.

## A request to take action by the vendors
While vendor software is used by numerous of microscopists every day it is interesting to note
that the detailed knowledge about the I/O routines has always been on a few developers shoulders.
We have realized that many of the file format readers in open-source software were 
reverse-engineered. This is challenging because the amount of documentation that is available
especially for some vendor file formats is neither exhaustive nor detailed enough.

This limits developers when they have to decide and design how to best implement the mapping
of specific binary numerical data and metadata into specifically named fields.
Here we hope that intensified exchange between vendors and the community can help to
improve the situation. You are very welcome to leave us comments in the issue list to
exchange specifically about this topic. Even better would be if commercial software tools
evolve into a state that they offer complementary options for exporting detailed metadata
and numerical data through publicly documented formats.

In fact, limited technical documentation of some vendor file formats stands in strong
contrast to the powerful GUI-based tools and the in fact continuous efforts of the vendors
to make the barriers for working with microscopy data simpler and become more aligned with the
FAIR principles.

## A starting point to harmonize metadata and numerical data from scripting based solutions
It is noteworthy that internally many of tools, whether it be commercial or open source tools,
implement their data analysis pipelines and functionalities via object-oriented programming.

Therefore, even though users of tools like mtex or hyperspy may in practice create very
different scripts, they still interact with a restricted set of class instances and methods.
In effect, having these classes offers a possibility for developing more generic parsers
like what is here exemplified with the dataconverter/em_spctrscpy parser.
