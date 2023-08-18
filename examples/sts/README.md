# STS Reader
***Note: Though the reader name is STS reader it also supports STM type experiment. This is the first version of the reader according to the NeXus application definition [NXsts](https://github.com/FAIRmat-NFDI/nexus_definitions/blob/fairmat/contributed_definitions/NXsts.nxdl.xml) which is a generic template of concepts' definition for STS and STM experiments. Later on, both application definitions and readers specific to the STM, STS and AFM will be available. To stay upto date keep visiting this page time to time. From now onwards we will mention STS referring both STM and STS.***

Main goal of STS Reader is to transform different file formats from diverse STS lab into STS community standard [STS application definition](https://github.com/FAIRmat-NFDI/nexus_definitions/blob/fairmat/contributed_definitions/NXsts.nxdl.xml), community defined template that define indivisual concept associated with STS experiment constructed by SPM community.
## STS Example
It has diverse examples from several versions (Generic 5e and Generic 4.5) of Nanonis software for STS experiments at [https://gitlab.mpcdf.mpg.de](https://gitlab.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/-/tree/develop/docker/sts). But, to utilize that examples one must have an account at https://gitlab.mpcdf.mpg.de. If still you want to try the examples from the sts reader out, please reach out to [Rubel Mozumder](mozumder@physik.hu-berlin.de) or the docker container (discussed below).

To get a detailed overview of the sts reader implementation visit [pynxtools](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/pynxtools/dataconverter/readers/sts).

## STS deocker image
STS docker image contains all prerequisite tools (e.g. jupyter-notebook) and library to run STS reader. To use the image user needs to [install docker engine](https://docs.docker.com/engine/install/).

STS Image: `gitlab-registry.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/sts-jupyter:latest`

To run the STS image as a docker container copy the code below in a file `docker-compose.yaml`

```docker
# docker-compose.yaml

version: "3.9"

services:
    sts:
        image: gitlab-registry.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/sts-jupyter:latest
        ports:
            - 8888:8888
        volumes:
            - ./example:/home/jovyan/work_dir
        working_dir: /home/jovyan/work_dir
```

and launch the file from the same directory with `docker compose up` command.
