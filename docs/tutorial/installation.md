# Installation guide

The document is the entry point for anybody that is new to the NeXus data format and to FAIRmat/NOMAD. It serves as a guide to getting started with the `pynxtools` software.

## What should you should know before this tutorial?

However, to get started, it does not hurt to  the following explanations:

- You should have read our [guide on getting started](../getting-started.md)

## What you will know at the end of this tutorial?

You will know

- how to install `pynxtools`
- how to configure your `pynxtools` installation
- how to install `pynxtools` together with NOMAD

## Setup

It is recommended to use python 3.11 with a dedicated virtual environment for this package. Learn how to manage [python versions](https://github.com/pyenv/pyenv) and [virtual environments](https://realpython.com/python-virtual-environments-a-primer/).

There are many alternatives to managing virtual environments and package dependencies (requirements). We recommend using [`uv`](https://github.com/astral-sh/uv), an extremely fast manager Python package and project manager. In this tutorial, you will find paralleled descriptions, using either `uv` or a more classical approach using `venv` and `pip`.

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
That command creates a new virtual environment in a directory called `.venv`.

## Installation

Install the latest stable version of this package from PyPI with

=== "uv"

    ```bash
    uv pip install pynxtools
    ```

=== "pip"


    ```bash
    pip install pynxtools
    ```

You can also install the latest _development_ version with

=== "uv"

    ```bash
    uv pip install git+https://github.com/FAIRmat-NFDI/pynxtools.git
    ```

=== "pip"


    ```bash
    pip install git+https://github.com/FAIRmat-NFDI/pynxtools.git
    ```

### Configuring your `pynxtools` installation

`pynxtools` comes with a list of [built-in readers](../reference/built-in-readers.md) that can be used after after pip installation. In addition, `pynxtools` supports a [plugin mechanism](../how-tos/pynxtools/build-a-plugin.md) for adding file readers for different experimental techniques. The different [FAIRmat-supported plugins](../reference/plugins.md) can be installed together with `pynxtools` by passing the name of the plugin as an extra to the install call. For example, for the `pynxtools-mpes` plugin, you can run:

=== "uv"

    ```bash
    uv pip install pynxtools[mpes]
    ```

=== "pip"


    ```bash
    pip install pynxtools[mpes]
    ```

In addition, you can also install _all_ of the pynxtools reader plugins which are maintained by FAIRmat by passing the `[convert]` extra to the install call:

=== "uv"

    ```bash
    uv pip install pynxtools[convert]
    ```

=== "pip"


    ```bash
    pip install pynxtools[convert]
    ```

Note that in this case, the latest version of the plugin(s) from PyPI are installed.

### How to install `pynxtools` with NOMAD

To use `pynxtools` with NOMAD, simply install it in the same environment as the `nomad-lab` package. NOMAD will recognize `pynxtools` as a plugin automatically and offer automatic parsing of `.nxs` files. In addition, NOMAD will install a schema for NeXus application definitions.

## Start using `pynxtools`

That's it! You can now use `pynxtools` and the plugins that you have installed!