# STM Example
Several examples regarding several versions of Nanonis instrument are available in [https://gitlab.mpcdf.mpg.de](https://gitlab.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/-/tree/develop/docker/stm). But to get in that example one must have an account in https://gitlab.mpcdf.mpg.de. Stll you need to try the example stm reader out, please reach out [Rubel Mozumder](mozumder@physik.hu-berlin.de) or docker container (discussed below).

To get a detailed overview about the stm reader implementaion visit [github](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/pynxtools/dataconverter/readers/stm).

One can try stm image: `gitlab-registry.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/stm-jupyter:latest`

To run it as a docker container copy the code below in a file `docker-compose.yaml`

```docker
# docker-compose.yaml

versoin: "3.9"

services:
    stm:
        image: gitlab-registry.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/stm-jupyter:latest
        ports:
            - 8888:8888
        volumes:
            - ./example:/home/jovyan/work_dir
        working_dir: /home/jovyan/work_dir
```

and launch the file with `docker compose up` command.
