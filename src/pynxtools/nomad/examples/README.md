

# Introduction

This is an example of a PID controlled sensor sweep scan. The temperature is set using a PID controller. Then, for the set temperature, a voltage sweep is performed. For each of the voltages, the current is measured. This is repeated for a given list of temperatures.

This specific data was captured using a Bluesky controlled system. This was then saved into a binary file using Pickle. This example illustrates how such a dataset could be converted using the [`JSONMapReader`](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/src/pynxtools/dataconverter/readers/json_map) of the NOMAD plugin [`pynxtools`](https://github.com/FAIRmat-NFDI/pynxtools).
The data is mapped on to a Nexus application definition for temperature-dependent IV curve measurements, [NXiv_temp](https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXiv_temp.html).

# Viewing uploaded data

Below, you find an overview of your uploaded data.
Click on the `> /` button to get a list of your data or select **FILES** from the top menu of this upload.
You may add your own files to the upload or experiment with the pre-existing electronic lab book example.
The ELN follows the general structure of NOMAD ELN templates and you may refer to the [documentation](https://nomad-lab.eu/prod/v1/staging/docs/archive.html) or a [YouTube tutorial](https://youtu.be/o5ETHmGmnaI) (~1h)
for further information.
When the ELN is saved a NeXus file will be generated from the provided example data.
You may also view your supplied or generated NeXus files here with the H5Web viewer.
To do so open the **FILES** tab and just select a `.nxs` file.

# Using a Jupyter Notebook

This example comes with a very simple Jupyter Notebook that shows how one could easily get access to a Python environment with access to all your data in one place.
To give this a go, click the **FILES** tab and select `IV_temp.ipynb`. Feel free to modify this or just create a new one to try!

# Where to go from here?

If you're interested in using this pipeline and NOMAD in general you'll find support at [FAIRmat](https://www.fairmat-nfdi.eu/fairmat/consortium).

If you have any questions about this example you may contact [Sherjeel Shabih](https://www.fairmat-nfdi.eu/fairmat/fairmat_/fairmatteam) from the FAIRmat consortium.
