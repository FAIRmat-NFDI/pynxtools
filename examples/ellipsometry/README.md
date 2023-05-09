# What is NXellipsometry?

The [NXellipsometry](https://fairmat-experimental.github.io/nexus-fairmat-proposal/9636feecb79bb32b828b1a9804269573256d7696/ellipsometry-structure.html#ellipsometry) application definition is a standard for converting ellipsometry data to make it FAIR.

# How to use it?

First you need to install nexusutuils, please follow the [install instructions](https://github.com/FAIRmat-NFDI/pynxtools) to set it up.
This is an example to use the dataconvert with the `ellips` reader and the `NXellipsometry` application definition.
Just execute

```shell
dataconverter --reader ellips --nxdl NXellipsometry --input-file eln_data.yaml --output SiO2onSi.nxs
```

in this directory.

# Are there detailed examples?

Yes, [here](https://gitlab.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/-/tree/develop/docker/ellips) you can find an exhaustive example how to use `pynxtools` for your ellipsometry research data pipeline.
