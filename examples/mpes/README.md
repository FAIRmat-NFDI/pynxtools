# What is MPES?

The [NXmpes](https://fairmat-experimental.github.io/nexus-fairmat-proposal/9636feecb79bb32b828b1a9804269573256d7696/classes/contributed_definitions/NXmpes.html#nxmpes) application definition is an umbrella definition for all photo-emission related techniques, such as ARPES or XPS.

# How to use it?

This is an example to use the dataconvert with the `mpes` reader and the `NXmpes` application definition.
If you want to use some example data you can find small example files in [`tests/data/dataconverter/readers/mpes`](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/tests/data/dataconverter/readers/mpes).

```shell
dataconverter --reader mpes \\
    --nxdl NXmpes \\
    --input-file xarray_saved_small_calibration \\
    --input-file config_file.json \\
    --input-file eln_data.yaml \\
    --output mpes_example.nxs
```

The reader is a tailored parser for research data in a common format. This particular example is able to read and map hdf5 files, as well as json and yaml files. Feel free to contact FAIRmat if you want to create a parser for your research data.

For XPS data you may use the data in [`tests/data/dataconverter/readers/xps`](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/tests/data/dataconverter/readers/xps) with the command

```shell
dataconverter --reader xps \\
    --nxdl NXmpes \\
    --input-file eln_data.yaml \\
    --input-file In-situ_PBTTT_XPS_SPECS.xml \\
    --output xps_example.nxs
```

# Are there detailed examples?

Yes, [here](https://gitlab.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/-/tree/develop/docker/mpes) you can find exhaustive examples how to use `pynxtools` for your ARPES research data pipeline.

There is also an [example](https://gitlab.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/-/tree/develop/docker/xps) for using `pynxtools` for an XPS pipeline.
