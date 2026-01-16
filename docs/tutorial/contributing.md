# Development guide

This tutorial will guide you through on how to set up a working environment for developing `pynxtools`.

## What should you should know before this tutorial?

- You should read our [guide on getting started](../getting-started.md).
- You should read the [installation tutorial](installation.md).

## What you will know at the end of this tutorial?

You will know

- how to setup your environment for developing `pynxtools`
- how to make changes to the software
- how to test the software
- how to contribute on GitHub
- how to use pynxtools as a NOMAD plugin

## Contributing

??? info "Structure of the `pynxtools` repository"
    The software tools are located inside [`src/pynxtools`](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/src/pynxtools). They are shipped with unit tests located in [`tests`](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/tests). Some examples from the scientific community are provided in [`examples`](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/examples). They guide you through the process of converting instrument data into the NeXus standard and visualizing the files' content.

### Setup

It is recommended to use python 3.11 with a dedicated virtual environment for this package. Learn how to manage [python versions](https://github.com/pyenv/pyenv) and [virtual environments](https://realpython.com/python-virtual-environments-a-primer/). We recommend using [`uv`](https://github.com/astral-sh/uv), an extremely fast manager Python package and project manager. In this tutorial, you will find paralleled descriptions, using either `uv` or a more classical approach using `venv` and `pip`.

Start by creating a virtual environment:

=== "uv"
    `uv` is capable of creating a virtual environment and install the required Python version at the same time.

    ```bash
    uv venv --python 3.11
    ```

=== "venv"

    Note that you will need to install the Python version manually beforehand.

    ```bash
    python -m venv .venv
    ```

That command creates a new virtual environment in a directory called .venv.

### Development installation

We start by cloning the repository:

```console
git clone https://github.com/FAIRmat-NFDI/pynxtools.git \\
    --branch master \\
    --recursive pynxtools
cd pynxtools
git submodule sync --recursive
git submodule update --init --recursive --jobs=4
```

Note that we are using the NeXus definitions as a [Git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules). The last two lines initiate the submodule and upgrade it to match the first used in pynxtools.

For the [ontology service](../learn/pynxtools/ontology-service.md), adding the [NeXusOntology](https://github.com/FAIRmat-NFDI/NeXusOntology/tree/oscars-project) as a git submodule is required. Here, it is recommended to use the sparse checkout:

```bash
git sparse-checkout init --no-cone
git sparse-checkout set "/*" '!ontology/NeXusOntology.owl' '!ontology/NeXusOntology_full.owl' '!ontology/NeXusOntology_full_testdata.owl'
```

Next, we install the package in editable mode (together with its dependencies):

=== "uv"

    ```bash
    uv pip install -e ".[dev]"
    ```

=== "pip"

    Note that you will need to install the Python version manually beforehand.

    ```bash
    pip install --upgrade pip
    pip install -e ".[dev]"
    ```

### Linting and formatting

We are using ruff and mypy for linting, formatting, and type checking. It is recommended to use the [pre-commit hook](https://pre-commit.com/#intro) available for ruff which formats the code and checks the linting before making an actual Git commit.

Install the precommit by running

```console
pre-commit install
```

from the root of this repository.

### Testing

There exist unit tests for the software written in [pytest](https://docs.pytest.org/en/stable/) which can be used as follows:

```console
pytest -sv tests
```

### Editing the documentation

We are using [mkdocs](https://www.mkdocs.org/) for the documentation. If you edit the documentation, you can build it locally. For this, you need to install an additional set of dependencies:

=== "uv"

    ```bash
    uv pip install -e ".[docs]"
    ```

=== "pip"

    ```bash
    pip install -e ".[docs]"
    ```
You can then serve the documentation locally by running

```console
mkdocs serve
```

### Running the examples

A number of examples exist which document how the tools can be used. For a standalone usage, convenient Jupyter notebooks are available for some of the tools. To use these notebooks, Jupyter and related tools have to be installed in the development environment as follows:

=== "uv"

    ```bash
    uv pip install jupyter
    uv pip install jupyterlab
    uv pip install jupyterlab_h5web
    ```

=== "pip"

    ```bash
    pip install jupyter
    pip install jupyterlab
    pip install jupyterlab_h5web
    ```

### Contributing to the package on Github

Once you are happy with the changes, please commit them on a separate branch and create a [pull request on GitHub](https://github.com/FAIRmat-NFDI/pynxtools/pulls). We run a number of GitHub actions that check the correct linting, run the tests in an isolated environment, and build the documentation. Once these pass and a peer review of the code has occurred, your code will be accepted.

## Developing pynxtools as a NOMAD plugin

If you plan to contribute to the NOMAD plugin functionality of `pynxtools`, it often makes sense to use the NOMAD development environment called `nomad-distro-dev`. You can learn more in the [NOMAD documentation](https://nomad-lab.eu/prod/v1/staging/docs/howto/develop/setup.html#nomad-distro-dev-development-environment-for-the-core-nomad-package-and-nomad-plugins).

## Troubleshooting

If you face any issues with the tool or when setting up the development environment, please create a new [Github Issue](https://github.com/FAIRmat-NFDI/pynxtools/issues/new?template=bug.yaml).
