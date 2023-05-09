# File/Metadata and Data Format Reader Plug-ins aka `reader`

The purpose of the dataconverter is to create NeXus/HDF5 files with content that
matches a specific NeXus application definition.
Such application definitions are useful for collecting a set of pieces of information
about a specific experiment in a given scientific field. The pieces of information
are metadata and numerical data. The application definition is used to provide
these data in a format that serves a data delivery contract: The HDF5 file,
or so-called NeXus file, delivers all those pieces of information which the
application definition specifies. Required and optional pieces of information are
distinguished. NeXus classes can recommend the inclusion of certain pieces of information.
Recommended data are essentially optional. The idea is that flagging these data as
recommended motivates users to collect them but does not require to write dummy
or nonsense data if the user is unable to collect recommended data.

The here developed and so-called readers, are effectively software tools (plug-ins)
which the converter calls to accomplish this task for a specific set of application
definition (NXDL XML file) plus a set of experiment/method-specific file(s).
These files can be files in a proprietary format, or of a certain format used in the
respective scientific community, or text files. Only in combination, these files hold
all the required pieces of information which the application definition demands and which
are thus required to make a NeXus/HDF5 file compliant. Users can store additional
pieces of information in an NeXus/HDF5 file. In this case readers will issue a warning
that these data are not properly documented from the perspective of NeXus.

## Getting started

The readers get cloned as plug-in dependencies while cloning the dataconverter.
Therefore, please follow the instructions for cloning the reader as a complete package.

## Download the example data for testing and development purposes

Before using your own data we strongly encourage you to download a set of open-source
test data for testing the plug-ins. For this purpose pynxtools comes with
a tests directory with a data/dataconverter sub-directory including reader-specific jupyter-notebook
examples. These examples can be used for downloading test data and use specific readers
as a standalone converter to translate given data into a NeXus/HDF5 file.

Once you have practised with these tools how to convert these examples, feel free to
use the tools for converting your own data. You should feel invited to contact the respective
corresponding author(s) of each reader if you run into issues with the reader or feel there
is a necessity to include additional data into the NeXus file for the respective application.

We are looking forward for learning from your experience and see the interesting use cases.
You can find the contact persons in the respective README.md of each reader.
