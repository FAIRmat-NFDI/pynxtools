# File/Metadata and Data Format Reader Plug-ins aka ``reader``

The purpose of the dataconverter is to create HDF5 files with content that matches a specific NeXus application definition. 
Such application definitions are useful for collecting a set of pieces of information about a specific experiment in a given
scientific field. The pieces of information are metadata and numerical data. The application definition is used to provide
these data in a format that the duties of a data delivery contract can be fulfilled: The HDF5 file, or so-called NeXus file,
delivers all those pieces of information which the application definition specifies.

The here developed and so-called readers, are effectively software tools (plug-ins) which the converter calls to 
accomplish this task for a specific set of application definition (NXDL file) plus a set of experiment/method-specific file(s).
These files can be files in a proprietary format, or of a certain format used in the respective scientific community, or
text files. Only in combination these files hold at least all the required pieces of information which the 
application definition demands.

## Project structure

- `tbd` - Maybe further explanations are useful here.

## Getting started

The readers get cloned as plug-in dependencies while cloning the dataconverter.
Therefore, please follow the instructions for cloning the reader as a complete package.

## Download the example data for testing and development purposes

Before using your own data we strongly encourage you to download a set of open-source
test data for testing the plug-ins. There are specific jupyter-notebook examples (where??) which
detail how these tests can be executed for each of the specific readers which are listed below. 

Once you have practised with these tools how to convert these examples, feel free to
use the tools for converting your own data. You should feel invited to contact the respective
corresponding author(s) of each plug-in if you run into issues with the plug-in or feel there
is a necessity to include additional data into the NeXus file for the respective application.

We are looking forward for learning from your experience and see the interesting use cases.

## Current readers/plug-ins

Details to the individual readers follow. Each reader is documented with a description 
of its primary target audience, its scientific field and corresponding author. In addition,
individual support is given on how each reader can be executed.

## apm

`targets:` atom probe microscopy
`accepts:` NXapm.nxdl.xml
`offers:` generic reader for atom probe tomography and some related field-ion microscopy experiments.
`supports:` pos, epos, apt (the one introduced with AP Suite), rng, rrng, json
`statusquo:` single experiment + single range file + single file with additional metadata as a json document.
`contact:` Markus Kühbach (Humboldt-Universität zu Berlin)

```sh
python converter.py --reader apm --nxdl ../../definitions/applications/NXapm.nxdl.xml --input-file 70_50_50.apt --input-file SeHoKim_R5076_44076_v02.rng --input-file ManuallyCollectedMetadata.json --output apm.test.nxs
```

## arpes

`targets:` photo-emission spectroscopy
`accepts:` ??
`offers:` ??
`supports:` ??
`statusquo:` ??
`contact:` Tommaso Pincelli, Laurenz Rettig, Abeer Arora (Fritz-Haber-Institute of the Max-Planck Society)

## em_nion

`targets:` electron microscopy
`accepts:` NXem_nion.nxdl.xml
`offers:` initial reader for results from Nion microscopes and results achieved with nionswift software.
`supports:` npy, json
`statusquo:` single experiment and two json file(s) with additional metadata
`contact:` Markus Kühbach, Benedikt Haas, Sherjeel Shabih (Humboldt-Universität zu Berlin)

```sh
python converter.py --reader em_nion --nxdl ../../definitions/applications/NXem_nion.nxdl.xml --input-file HAADF_01.npy --input-file HAADF_01.json --input-file HAADF_01.ELabFTW.dat --output em.test.nxs
```

## ellipsometry

`targets:` ellipsometry
`accepts:` ??
`offers:` ??
`supports:` ??
`statusquo:` ??
`contact:` Carola Emminger, Tamas Haraszti, Chris Sturm (add affiliations)


