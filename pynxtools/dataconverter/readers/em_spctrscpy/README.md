# em_spctrscpy reader

## Purpose
Translate diverse files from the scientific community and technology partners within
the electron microscopy community into a standardized representation using the NeXus
application definition NXem.
This parser does not copy over all of the data and metadata in files from especially
commercial software but that particular subset which is understood and useful
inside a NOMAD OASIS instance.

## What this em reader supports
The main idea behind the parser is to offer users of the OASIS a diverse example of how
a parser for specific file formats can be written and designed. We would like to encourage
the EM community to share example files with us. These can be small and come from diverse use cases.
Ideally, these should represent data in file formats from technology partners other than the 
already here supported and implemented ones. This would support us to broaden the applicability
of this parser.

Specifically, the implementation shows how I/O functionalities of hyperspy can be used
to load data of spectroscopy experiments from three exemplar file formats:
Bruker BCF, Velox EMD, and DigitalMicrograph DM3. The implementation shows how generic
and specialized instances of the NeXus base classes NXspectrum_set and NXimage_set
can be created and registered inside instances of NXevent_data_em; and then how all these
can be composed and stored inside a NeXus/HDF5 file that matches the NXem application definition.

This makes the example relevant for researchers who work within the fields of
scanning electron microscopy (SEM) EDS/EDX, transmission electron microscopy
(EDS/STEM), and electron energy loss spectroscopy (EELS).

## Getting started - standalone usage
If you use this dataconverter/em_spctrscpy parser as a standalone tool,
1. You should follow the interactive jupyter notebook that is stored in 
   *pynxtools/examples/em_spctrscpy*.
2. As the standalone usage of this parser does not require a NOMAD OASIS instance,
   you have to edit the ELN manually or via another ELN. For this you can edit the
   example eln_data_em_spctrscpy.yaml which comes shipped with this example.
   Alternatively, you can at this point copy or place your own datasets into the
   working directory of the jupyter lab instance.
3. Once the YAML file has been edited, to your satisfaction you can continue
   executing the jupyter tutorial. This should create an instance of a NeXus/HDF5 file
   which is formatted according to the NXem application definition.

## Getting started - usage related to NOMAD OASIS
This parser can be used to map numerical data and metadata inside frequently used
file formats from technology partners of electron microscopy software tools into a
NeXus/HDF5 file which complies with a specific version of the NXem application
definition.

If you are using a NOMAD OASIS you can use this tool as follows.
1. Log-in to a NOMAD OASIS instance and navigate to the *Create Uploads* tab.
2. Select em_spctrscpy example from the list of available options.
3. Drag-and-drop your files in specific file formats. Currently,
   support for Bruker BCF, Velox EMD, and DigitalMicrograph DM3 is implemented.
3. Edit the electronic lab notebook (ELN) schema inside the NOMAD OASIS and click the
   save button in the NOMAD OASIS GUI to save the data that you have entered into
   the ELN template. Clicking *save* will trigger the automatic generation
   of an eln_data.yaml file. Second, the clicking will trigger a run of the
   dataconverter/em_spctrscpy parser which generates a NXem NeXus file based on
   your uploaded BCF, EMD or DM3 file. You can explore these files in the file
   browsing tab of NOMAD OASIS.
   By default the converter performs a strong loss-less compression on the input
   as many of the stack data store integers with a low entropy. The compression may
   take some time. Arrays with floating point values are also compressed by
   default but with a lower compression strength.
   You can inspect the progress of the conversion in the console from which
   you started the NOMAD OASIS appworker.
4. If successful, a NeXus (nxs) file will appear in your upload. You can explore
   its content with the H5Web tools inside the NOMAD OASIS GUI and click interactively
   through the data including default plots. For electron microscopy these are the 
   EDS/EDX spectra stack, eventually a sum spectrum, and (annular dark field)
   overview images of the material region-of-interest (ROI) characterized if present.
   If unsuccessful, the console from which you started the NOMAD OASIS appworker
   can help you with identifying problems.

Given that microscopy software tools differ, users should not expect that every
required field in the application definition can be served by data and metadata
from an arbitrary such microscopy tool, often some metadata are not stored in
the files from technology partners in a way that they are openly accessible.

Therefore, the em_spctrscpy reader takes additional metadata from the eln_data.yaml file.
Here the feature of custom schema for the NOMAD ELN serve two tasks. Firstly, they
define the elements of the graphical user interface which this domain-specific ELN
template should offer. Secondly, they enable collecting metadata.

## Background
This em_spctrscpy reader was implemented as an example to show how tools like
the pynxtools, YAML-based schemas and files from technology partners can be customized
to enable automated parsing and mapping of data in different representations
on NXem.

## Technical background details for developers and data scientists
The em_spctrscpy reader serves as a parser with multiple parts/readers/and sub-parser/
components because data and metadata in electron microscopy come from such a diverse
number of file formats and use cases, from results of interactions with different GUIs,
scripts running inside GUIs, or user-customized/-written scripts using open-source microscopy
software tools that it is essential to keep things well modularized.
These subtilities make the development of a general enough parser challenging.

Our approach with dataconverter/em_spctrscpy is to offer users of a NOMAD OASIS instance
first at all an implemented step-by-step example how they can combine different software
tools and make these operational in a NOMAD OASIS. Therefore, we follow an approach that
is breadth- rather than depth-first. Our approach is driven by examples.
Breadth first means, we would like to offer the user first an overview of the rather large
number of NeXus base classes within the design of the NXem application definition.

Practically, the process needs to be driven by examples because many I/O routines for
file formats from technology partners in open-source software have been implemented based
on reverse engineering. Hyperspy is a good example of these developments and efforts.
In fact, there is currently no joint knowledge base how all possible file formats can be safely
and robustly parsed so that each field and entry is not only binarily readable but can also
confidently be mapped on specific terms using a controlled vocabulary.
Interestingly, this challenge is independent of the ontology used.

Currently the example implements for:
* NXspectrum_set
* NXimage_set

These already cover how also the simpler cases of plain calibrated images could be covered.

## NXem and the status quo of data schemes in electron microscopy
NXem is a general application definition which embraces multiple EM sub-communities.
Specifically, condensed-matter physicists, materials scientists, and materials engineers,
i.e. electron microscopy users which have all their own software solutions or at least
different, best practices and protocols currently, to interact and work with electron
microscopy data.

Our starting point in FAIRmat for EM was thus different compared to the situation
in e.g. the field of atom probe microscopy. In the field of atom probe, only a few file
formats exist and have been in use when the FAIRmat project started.
This is why dataconverter/em_spctrscpy has its own subroutines for loading intricate
details of files from the open-source community or technology partners.

By contrast, for electron microscopy developing that many file format readers
on our own is not a feasible approach for two reasons:

First, there is very limited use of writing again readers for specific EM file formats
because the EM community has developed already many of such parses. Many of them are mature
in that they offer internal readers for several file formats.
The strength of the existent readers is that many users already work with such software.
Thus, supporting the development and working together on I/O functions for files from
technology partners and discussing open issues is in our opinion the preferred approach.

Specific examples of such community tools are:
**hyperspy** for analyses of spectra such as EDX/EDS and EELS, used in SEM/TEM communities
**mtex** for analyses of texture, and EBSD data, heavily used in the SEM community
**dream3d** for 3D EBSD post-processing into synthetic volume elements
**EMsoft** for indexing EBSD, **kikuchipy** and **pyxem** leaning towards the TEM community

Processing of results from the latter three tools is partially covered by the em_om example.

Instead of reimplementing the wheel, we are convinced the I/O functionalities of these tools
should be used by even more people to support the respective open-source projects.

The other reason why we are not convinced that it is a sustainable approach for a National
Research Data Infrastructure that each project implements own formats is that there are already
two important challenges with the status quo in electron microscopy:
Format constraints and limited documentation of the content and details behind some of the file
formats from technology partners. We should make clear that we acknowledge the significant momentum
and effort which microscopy manufacturers as technology partners invest into the storing of metadata
in their (commercial) software solutions. We would like to see though that more of these efforts
become documented in the literature in technical design specifications and ideally as living
documents via public repositories which are lead by the technology partners but
open to contributions from the scientific community.

## A request to take action by technology partners and the scientific community
While commercial software is used by numerous microscopists every day, it is interesting to note
that the detailed knowledge about the I/O routines has always been on a few developers shoulders.
We have realized that many of the file format readers in open-source software were reverse-engineered.
This is challenging because the amount of documentation that is available especially for some file formats
is neither exhaustive nor documented enough in detail.

This limits developers when they have to decide and design how to best implement the mapping
of specific binary numerical data and metadata into specifically named fields.
Here we hope that intensified exchange between technology partners and the scientific community
can help to improve the situation.

You are very welcome to leave us comments in the issue list (or drop us an email) to exchange
specifically about this topic. Even better would be if commercial software tools evolve
into a state that they offer complementary options for exporting detailed metadata
and numerical data through publicly documented formats.

## A starting point to harmonize metadata and numerical data from scripting based solutions
It is noteworthy that internally many of tools, whether it be commercial or open source tools,
implement their data analysis pipelines and functionalities via object-oriented programming.

Therefore, even though users of tools like mtex or hyperspy may in practice create very
different scripts, they still interact with a restricted set of class instances and methods.
In effect, having these classes offers a possibility for developing more generic parsers
like what is here exemplified with the dataconverter/em_spctrscpy parser. As an example
we explore along this idea the parsing of data from EBSD class object instances
with MTex, which is offered via the em_om example.

## Contact person in FAIRmat for this reader
Markus Kühbach