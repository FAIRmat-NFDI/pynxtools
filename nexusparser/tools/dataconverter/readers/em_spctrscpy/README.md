# em_spctrscpy reader

## Purpose
Translate diverse numerical data and metadata in vendor file from electron microscopy
into a standardized representation using the NeXus application definition NXem.
The parser does not copy over all the data and metadata in the vendor files
but the particular subset that is understood and useful inside a NOMAD OASIS instance.

## What this em reader supports
The main idea behind the parser is to offer users of the OASIS a diverse example
of how a parser for specific file formats can be written and designed. We would like
to encourage the EM community to share with us example files (these can be small and
from diverse use cases), ideally represent in other vendor file formats like those
implemented here already. With these examples we can improve the parser mainly
by broaden its applicability.

Specifically, the implementation shows how I/O functionalities of hyperspy can be used 
to load data from three exemplar file formats: Bruker BCF, Velox EMD, DigitalMicrograph DM3.
The implementation shows how instances of NXspectrum_set_em_xray, NXspectrum_set_em_eels,
and NXimage_set_em_adf can be created and registered inside instances of NXevent_data_em;
and then how all these instances can be arranged and stored in a NeXus NXem file.

This makes the example relevant for researcher working within the fields of
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
3. Drag-and-drop your files in vendor-specific formats.
   Currently bcf, emd, and dm3 are supported.
3. Edit the electronic lab notebook (ELN) schema inside the NOMAD OASIS and
   click the save button in the NOMAD OASIS GUI to save the data that you have
   entered in this ELN template. Clicking *save* will trigger the automatic generation
   of an eln_data.yaml utility file. Second, the clicking will trigger a run of the
   dataconverter/em parser which generates an NXem NeXus file based on the data
   in the vendor files and the eln_data.yaml file. The file will be returned in the OASIS.
   By default the converter performs a strong loss-less compression on the input
   as many of the stack data store integers with a low entropy.
   The compression may take some time. You can inspect the progress of the conversion
   in the console from which you started the NOMAD OASIS appworker.
4. If successful, a NeXus (nxs) file will now in your upload. You can explore
   its content with the H5Web tools inside the NOMAD OASIS GUI.
   If unsuccessful, the data logger can help you to identify if problems occurred.

Clearly as microscopy software tools differ, users should not expect that every
required field in the application definition can be served by the data and metadata
from an arbitrary such microscopy tool and its often vendor-specific output (file
formats). Therefore, the em reader takes additional input from a text file.
Specifically, this text file can be created with the ELN schema creation and 
customization functionalities offered through NOMAD OASIS.

## Getting started - standalone usage
If you use this dataconverter/em parser as a standalone tool,
1. You should follow the interactive jupyter notebook that is stored in *nomad-parser-nexus\tests\data\tools\dataconverter\readers\em*.
2. As the standalone usage of this parser does not require a NOMAD OASIS instance,
   you have to edit the ELN manually. For this you can edit the example that
   comes shipped with the example. Alternatively, you can at this point copy or
   place your own datasets into the working directory of the jupyter instance.
   Specifically, after you have executed the download of the em-sprint9-example.zip
   dataset there is an eln_data.yaml file through which you can edit the ELN content.
3. Ones this file has been edited you can continue executing the jupyter tutorial.
4. If successful, your edits of the eln_data.yaml will be considered and processed
   together with the data files into an instance of a NeXus HDF5 file, formatted
   according to the NXem application definition.

## Background
This em reader was implemented as a response to an issue during sprint 9 within
Area B of the FAIRmat project while working on application definitions and parsers
for them to inject data into and create an example for electron microscopy with
NOMAD OASIS.

## Technical background details for developers and data scientists
The em reader serves as a parser with multiple parts/readers/and sub-parser components
because data and metadata in electron microscopy come from such a diverse number of file
formats and use cases, from results of interactions with different GUIs, vendor scripts
running inside GUIs, or user-customized/-written scripts using open-source microscopy
software tools. These subtilities make the development of a general enough parser challenging.

Therefore, the approach that we pursue here with the example of the dataconverter/em
parser is to offer users of a NOMAD OASIS instance first at all an implemented step-by-step
worked out example how they can combine different software tools and make these
operational in the OASIS. Therefore, we follow an approach that is breadth-first and
driven by examples. Breadth first to offer users first an overview of the rather large
number of NeXus base classes within the design of the NXem application definition.
Practically the process needs to be driven by examples as many I/O routines of 
open-source software was designed by reverse engineering and thus there is currently
no joint knowledge base how specific vendor files can be safely and robustly
parsed so that each field and entry is readily interpretable and mappable on
specific terms of a controlled vocabulary. 

Currently the example implements for:
* NXspectrum_set_em_xray
* NXspectrum_set_em_eels
* NXimage_set_adf

These three already cover how also the simpler NXimage_set_se and NXimage_set_bse
could be covered, although they are not implemented in the current example.

## NXem and the status quo of data schemes in electron microscopy
NXem is a general application definition which embraces multiple EM sub-communities.
Specifically, condensed-matter physicists, materials scientists, and materials engineers,
i.e. electron microscopy users which have all their own software solutions or at least
different, best practices and protocols currently, to interact and work with electron
microscopy data.

Our starting point in FAIRmat for EM was thus different compared to the situation
in e.g. the field of atom probe microscopy. In the field of atom probe, only a
few file formats exists and have been in use when the FAIRmat project started.
Back then there was not a very strong community activity for working towards a
joint file format parser for atom probe. Therefore, the apm reader of this dataconverter
has its own subroutines for loading intricate details of vendor and open-source-documented
file formats, which we implemented and offer as a reference implementation.

By contrast, for electron microscopy developing these many file format readers on our own
in FAIRmat would not have been a feasible approach for two reasons:

One reason is that there is a very limited use of writing again readers for a specific EM file
formats because the EM community has developed a number of these by now. Many of them are mature
or at least promising enough I/O functions which internally have readers for several file formats
implemented. Their strength is that many users already work with such software and thus
support the development with running I/O functions on vendor files and discussing issues openly.

Specific examples are:
**hyperspy** for analyses of spectra such as EDX/EDS and EELS, used in SEM/TEM communities
**mtex** for analyses of texture, and EBSD data, heavily used in the SEM community
**dream3d** for 3D EBSD post-processing into synthetic volume elements
**EMsoft** for indexing EBSD, **kikuchipy** and **pyxem** leaning towards the TEM community

Instead of reimplementing the wheel, we are convinced the I/O functionalities of these tools
should be used by even more people to support the respective open-source projects involved.

The other reason why we are not convinced that it is a sustainable approach for
a National Research Data Infrastructure when each project implements own formats is that there
are two important challenges with the current status quo in electron microscopy:
Format constraints and limited documentation of the content and details behind 
file formats design especially by vendors. We should make clear that we acknowledge the
significant moment and work that we have learned is currently ongoing at microscopy companies
to implement strategies for their software tools to store and document metadata. We
would like to see though that more of this is documented in the literature.

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

On the open-source end of the spectrum of such tools we find e.g.
**nionswift**
**fiji/imagej**

and of course the very sophisticated and useful proprietary software tools
from the manufacturers which offer different levels of internal scripting
capabilities.

## A starting point to harmonize metadata and numerical data from scripting based solutions
It is noteworthy that internally all these tools, like also many of those not explicitly
mentioned here, implement their data analysis pipelines and functionalities in a similar
conceptual manner. Namely, the design for most of the these tools and their scripting interfaces
follows and makes heavy use of object-oriented programming.

Therefore, even though users of mtex or hyperspy may in practice create very different
scripts, they all interact with a restricted set of class instances and call methods of
these instances to trigger certain processing tasks in their script.

In summary, having these classes offers a possibility to develop more generic parsers
like what is here exemplified with the dataconverter/em_spctrscpy parser.

We can essentially understand this reader as a translator and mapping tool which
takes members of class instances defined in some of the above-mentioned software tools
and maps these data onto specific groups, fields, and attributes defined by the
NXem application definition.
