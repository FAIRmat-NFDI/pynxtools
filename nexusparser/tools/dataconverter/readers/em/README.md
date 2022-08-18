# EM reader

## Purpose
Translate diverse numerical data and metadata into a standardized representation
using NeXus. Such a representation is understood by a NOMAD OASIS.

## Getting started - usage related to NOMAD OASIS
This parser can be used to map numerical data and metadata inside specific
class instances from frequently used microscopy software tools into a
NeXus file which complies with a specific version of the NXem application
definition.

Clearly as microscopy software tools differ, users should not expected that every
required field in the application definition can be served by the data and metadata
from an arbitrary such microscopy tool. Therefore, the em reader takes optionally
additional data input from a text file. This text file can be created with the
ELN schema creation and customization functionalities offered by your NOMAD OASIS.

## Getting started - standalone usage
If you use this dataconverter as a standalone tool, the above-mentioned text file
has to be formatted in a particular way which the example shows.


## Technical background for developers and data scientists
The em reader is designed as a parser with multiple parts/components because data
in electronmicroscopy come from such a diverse number of file formats and use cases,
GUI interactions, scripts running inside GUIs, or scripts written with the help
of open-source microscopy software tools.

NXem is a general application definition which embraces multiple EM sub-communities.
Specifically, condensed-matter physicists, materials scientists, and materials engineers,
i.e. electron microscopy users which have all their own software solutions or at least
different currently habits and protocols to interact and work with electron
microscopy data.

Our starting point in FAIRmat for EM was thus different compared to the situation
in e.g. the field of atom probe microscopy. Here, only a few file formats exists and
at the same time, i.e. while the National Research Data Infrastructure in Germany
started working, there has since been not a very strong community activity for
working towards a joint file format parser for atom probe. Therefore, the apm
reader of this dataconverter has its own subroutines for loading intricate
details of vendor and open-source-documented file formats, which we implemented
and offer as a reference implementation.

By contrast, for electron microscopy developing this on our own would not be a
feasible approach. There is only very limited use of writing again a reader for
a specific EM file format because the EM community has developed a number of by now
mature or at least promising enough software solutions which internally
have readers for these file formats implemented.

Specifically examples are e.g.:
**hyperspy** for analyses of spectra such as EDX/EDS and EELS, used in SEM/TEM communities
**mtex** for analyses of texture, and EBSD data, heavily used in the SEM community
**dream3d** for 3D EBSD post-processing into synthetic volume elements
**EMsoft** for indexing EBSD as well as **pyxem** leaning towards the TEM community

Instead of reimplementing the wheel, the I/O functionalities of these tools should
be used (and the respective open-source projects) be supported.

There are two important grains of salt to this though: Format constraints and 
limited documentation. In fact, while the above-mentioned tools are nowadays used by
thousands of users every day, the actual knowledge about the I/O routines
has always been on a few developers shoulders. We have to realize that many of these
readers were reverse-engineered because the amount of documentation especially for
some vendor file formats is not exhaustive and detailed enough that developers should
implement the mapping of specific binary data into specifically named fields.
Here we hope that intensified exchange between vendors and the community can help
to improve the situation. You are very welcome to leave us comments in the issue
list to specifically this topic also.

The oftentimes flabbergastingly limited technical documentation of some vendor
file formats is a strong contrast to the powerful often GUI-based tools which
vendors offer. These tools have different levels of data accessibility.

On the open-source end of the spectrum of such tools we find e.g.
**nionswift**
**fiji/imagej**

and of course the very sophisticated and useful proprietary software tools
from the manufacturers which offer different levels of internal scripting
capabilities.

## A starting point to harmonize metadata and numerical data from scripting based solutions
It is noteworthy that internally all these tools, like also many of those not explicitly
mentioned here, internally implement their data analysis pipelines and functionalities
in a similar manner. Namely, the design for most of the these tools and their scripting interfaces
follows and makes heavy use of object-oriented programming.

Therefore, even though users of mtex or hyperspy may in practice create very different
scripts, they all interact with a restricted set of class instances and call methods of
these instances to trigger certain processing tasks in their script. 

In summary, having these classes offers a possibility to develop more generic parsers
like what is here our attempt with the em parser.

We can essentially understand this reader as a translator and mapping tool which
takes members of class instances defined in some of the above-mentioned tools
and maps these data onto specific groups, fields, and attributes defined by the
NXem application definition.
