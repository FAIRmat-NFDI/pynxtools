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

We are using ruff and mypy for linting, formatting, and type checking. It is recommended to use the [pre-commit hook](https://pre-commit.com/#intro) available for ruff which formats the code and checks the linting before actually making an actual Git commit.

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

We are using [`mkdocs](https://www.mkdocs.org/) for the documentation. If you edit the documentation, you can build it locally. For this, you need to install an additional set of dependencies:

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

Once you are happy with the changes, please commit them on a separate branch and create a pull request on GitHub. We run a number of GitHub actions that check the correct linting, run the tests in an isolated environment, and build the documentation. Once these pass and a peer review of the code has occurred, your code will be accepted.

### Use of AI tools

We recognize the value of AI-assisted development and do not discourage its use. AI coding assistants can be helpful for tasks such as exploratory code generation, refactoring, and documentation updates.

At the same time, design decisions, software architecture, and acceptance of contributions must remain under human control.

!!! note "Policy under development"
    A formal policy on AI usage in contributions is still being developed. For now, we encourage judicious use.

For now, contributors are expected to follow these guidelines:

**Declaration of AI usage.**
If AI tools were used in preparing a contribution, this must be stated in the pull request description. The declaration must name the tool(s) used and briefly describe the scope of their involvement (e.g. "Used GitHub Copilot for initial design of X" or "Used Claude Code to assist with refactoring Y").

**Human authorship and responsibility.**
All AI-generated content must be reviewed, understood, and validated by the contributing author before submission. The contributor is fully responsible for the correctness, quality, and suitability of the code, regardless of how it was produced. Contributions that are evidently fully AI-produced with no human involvement will not be accepted.

**Code review.**
AI tools may be used as a supplementary aid during code review, but final review decisions must always be made by a human maintainer. Automated or AI-driven review does not substitute for human judgment on design, correctness, or scientific validity.

## Developing pynxtools as a NOMAD plugin

If you plan to contribute to the NOMAD plugin functionality of `pynxtools`, it often makes sense to use the NOMAD development environment called `nomad-distro-dev`. You can learn more in the [NOMAD documentation](https://nomad-lab.eu/prod/v1/staging/docs/howto/develop/setup.html#nomad-distro-dev-development-environment-for-the-core-nomad-package-and-nomad-plugins).

## Troubleshooting

If you face any issues with the tool or when setting up the development environment, please create a new [Github Issue](https://github.com/FAIRmat-NFDI/pynxtools/issues/new?template=bug.yaml).
