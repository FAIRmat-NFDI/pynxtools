## Getting started
We offer examples of how you can convert your data (raw data, numerical data, metadata), 
from your acquisition software or electronic lab notebook (ELN), into a NeXus/HDF5 file
using the [dataconverter](../pynxtools/dataconverter) tool.
This tool offers parsers/readers/data extractors for various experimental techniques, including
electron microscopy, photo-emission spectroscopy, optical spectroscopy, atom probe, and other
techniques. Please refer to the individual README's in each sub-directory for details.

The examples contain code snippets for creating a NeXus/HDF5 file for the experimental technique
according to a standardized application definition (e.g. NXem, NXmpes, NXellipsometry, NXapm).
Respective [Jupyter Notebooks](https://jupyter.org/) are used for running these examples.

There is also a documentation of the [dataconverter](../pynxtools/dataconverter) available.
You can also write a [reader](../pynxtools/dataconverter/readers) for your experimental technique
if it is not supported yet. Feel also free to [contact](../README.md#questions-suggestions)
us if you need help.

For giving specific feedback to specific parsers/readers/data extractors please contact the
respective developers directly:

### em_om, em_spctrscpy
Markus Kühbach

### mpes, xps
Florian Dobner, Rubel Mozumder, Lukas Pielsticker

### ellipsometry
Carola Emminger, Florian Dobner

### apm
Markus Kühbach

