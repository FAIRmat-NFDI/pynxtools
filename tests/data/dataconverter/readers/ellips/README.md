# Ellipsometry example

As an example, a test data set (SiO2 on Si measured with a commercial ellipsometer) is provided. The metadata relevant for this example experiment are structured according to the application definition **NXellipsometry** (the corresponding NXDL file can be found ![here](https://github.com/FAIRmat-Experimental/nexus_definitions/blob/fairmat-ellips/contributed_definitions/NXellipsometry.nxdl.xml)).

Files in this directory:
- Data file: test-data.dat
- Metadata file: test.yaml
- Notebook with instructions: ELLIPSOMETRY.NeXus.READER.EXAMPLE.02.ipynb
- NeXus file: ellips.test.nxs (will be created if running the notebook)

## Instructions and notebook
The notebook ELLIPSOMETRY.NeXus.READER.EXAMPLE.02.ipynb contains instructions on how to install Jupyter Lab and the required packages needed to run this example. Furthermore, it is explained how to run the ellipsometry reader and how to create a NeXus file, which then can be inspected within the notebook.

## Data analysis example
The above test data are analyzed in this ![example](https://gitlab.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/-/tree/develop/docker/ellips/example) using the analysis tool ![pyElli](https://pyelli.readthedocs.io). Please have a look at the notebook ![Ellipsometry workflow example.ipynb](https://gitlab.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/-/blob/develop/docker/ellips/example/Ellipsometry%20workflow%20example.ipynb) for detailed instructions on how to analyze the data, which are being loaded from the NeXus file.
