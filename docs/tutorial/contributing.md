# Development guide

This tutorial will guide you through on how to set up a working environment for developing `pynxtools`.

## What should you should know before this tutorial?

- You should read our [guide on getting started](../getting-started.md).
- You should read the [installation tutorial](installation.md).

## What you will know at the end of this tutorial?

You will know

- how to setup your environment for developing `pynxtools`, on its own or inside `nomad-distro-dev`
- which branch to use for which kind of change
- how to make changes to the software
- how to test the software
- how to contribute on GitHub
- how a new version is released

## Contributing

??? info "Structure of the `pynxtools` repository"
    The software tools are located inside [`src/pynxtools`](https://github.com/FAIRmat-NFDI/pynxtools/tree/develop/src/pynxtools). They are shipped with unit tests located in [`tests`](https://github.com/FAIRmat-NFDI/pynxtools/tree/develop/tests). Some examples from the scientific community are provided in [`examples`](https://github.com/FAIRmat-NFDI/pynxtools/tree/develop/examples). They guide you through the process of converting instrument data into the NeXus standard and visualizing the files' content.

### Branching model

`pynxtools` follows the same branching model as the core NOMAD packages.

| Branch | Role |
|---|---|
| `develop` | Default branch. All regular development PRs target this branch. |
| `main` | Released versions only. Only `release/*` branches are merged here, so its history is the release history. |
| `release/vX.Y.Z` | Temporary release branch, created from `develop` and merged into `main`. The version may carry a pre-release suffix, e.g. `release/vX.Y.Z-beta` or `release/vX.Y.Z-rc1`. |

| Activity | Branch |
|---|---|
| Feature development | `develop` |
| PR review and integration | `develop` |
| Selecting changes for a release | `release/vX.Y.Z` |
| Release-specific bug fixes | `release/vX.Y.Z` |
| Published release history | `main` |
| Porting release fixes back to ongoing development | Merge `release/vX.Y.Z` back into `develop` |

The `Check if source is release/*` workflow
([`.github/workflows/check-source-is-release.yml`](https://github.com/FAIRmat-NFDI/pynxtools/blob/develop/.github/workflows/check-source-is-release.yml))
allows PRs into `main` only from `release/*` branches. PRs from any other branch, **including `develop`**,
fail this check. It is enforced by marking it as a required status check in the branch protection rule
for `main`.

### Development installation

You can develop `pynxtools` in two ways:

- **Standalone**: a clone of `pynxtools` with its own virtual environment. This is described in this section.
- **Inside [`nomad-distro-dev`](https://github.com/FAIRmat-NFDI/nomad-distro-dev)**: `pynxtools` is one package of a local NOMAD installation. Use this if you work on the NOMAD plugin functionality of `pynxtools` or want to test it against NOMAD. See [Developing inside `nomad-distro-dev`](#developing-inside-nomad-distro-dev).

The sections after that ([Linting and formatting](#linting-and-formatting), [Testing](#testing), [Editing the documentation](#editing-the-documentation), [Running the examples](#running-the-examples)) show the commands for both setups.

It is recommended to use Python 3.11+ with a dedicated virtual environment. Learn how to manage [python versions](https://github.com/pyenv/pyenv) and [virtual environments](https://realpython.com/python-virtual-environments-a-primer/). We recommend using [`uv`](https://github.com/astral-sh/uv), an extremely fast Python package and project manager. In this tutorial, you will find paralleled descriptions, using either `uv` or a more classical approach using `venv` and `pip`.

Start by cloning the repository:

```console
git clone https://github.com/FAIRmat-NFDI/pynxtools.git \
    --branch develop \
    --recursive pynxtools
cd pynxtools
git submodule sync --recursive
git submodule update --init --recursive --jobs=4
```

Note that we are using the NeXus definitions as a [Git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules). The last two lines initiate the submodule and upgrade it to match the first used in pynxtools.

Next, create a virtual environment inside the repository and install the package in editable mode, together with its `dev` dependencies:

=== "uv"
    `uv` creates the virtual environment and installs the required Python version at the same time.

    ```bash
    uv venv --python 3.11
    uv pip install -e ".[dev]"
    ```

=== "pip"

    Note that you will need to install the Python version manually beforehand.

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -e ".[dev]"
    ```

This creates the virtual environment in a directory called `.venv`. Other extras are installed the same way, e.g. `".[dev,docs]"` for the documentation tools.

### Developing inside `nomad-distro-dev`

[`nomad-distro-dev`](https://github.com/FAIRmat-NFDI/nomad-distro-dev) is the development environment for NOMAD and its plugins (see also the [NOMAD documentation](https://nomad-lab.eu/prod/v1/staging/docs/howto/develop/setup.html#nomad-distro-dev-development-environment-for-the-core-nomad-package-and-nomad-plugins)). Set it up as described in its README. Then add `pynxtools` as a package and declare the extras you need:

```bash
cd nomad-distro-dev
git submodule add https://github.com/FAIRmat-NFDI/pynxtools.git packages/pynxtools
git submodule update --init --recursive
uv add packages/pynxtools --extra dev --extra docs
```

If you push to your own fork, use its URL in `git submodule add`. The second line also fetches the NeXus definitions inside `pynxtools`. The last line adds `"pynxtools[dev,docs]"` to the distro's `[project.dependencies]`, adds `pynxtools = { workspace = true }` to `[tool.uv.sources]`, and installs everything.

#### How the environment works

All packages in the distro share one environment, the `.venv` in the distro root. You do not create or activate a separate environment for `pynxtools`. `uv sync` is exact: it makes the environment match the distro's `pyproject.toml` and removes everything else, including anything installed with `uv pip install`. For example, after `uv pip install -e ".[docs]"`, the next `uv sync` removes the `docs` extra again, and `mkdocs` fails with `ModuleNotFoundError: No module named 'markdown_include'`.

#### Getting the `dev` and `docs` extras

There are three ways to get the extras of `pynxtools` (`dev`, `docs`, or any other) into the distro environment. You do not need the `nomad` extra here: it only adds `nomad-lab`, which the distro already provides from `packages/nomad-FAIR`.

1. **Declare them in the distro (persistent).** The `uv add` command above already does this. If `pynxtools` is already in your distro, change its entry in the distro's `pyproject.toml` instead and sync:

    ```toml
    dependencies = [
        ...
        "pynxtools[dev,docs]",
    ]
    ```

    ```bash
    uv sync
    ```

    Every later `uv sync` keeps the extras, and plain `uv run` commands work from `packages/pynxtools`. This is a change to your local distro checkout.

2. **Sync them once.** From the distro root, without changing any file:

    ```bash
    uv sync --all-packages --extra dev --extra docs
    ```

    The next plain `uv sync` removes them again. Add `--inexact` to keep packages you installed by hand with `uv pip install`. `--extra` applies to every workspace package that defines that extra.

3. **Request them per command.** From `packages/pynxtools`, add `--extra` to `uv run`, as shown in the sections below:

    ```bash
    uv run --extra dev pytest -sv tests
    ```

    `uv run` installs the extra if it is missing and does not remove anything else.

!!! warning "Run `uv sync` from the distro root"
    Do not run `uv sync --extra ...` inside `packages/pynxtools`, and do not use `uv sync --package pynxtools`. Both make the shared environment match `pynxtools` alone and uninstall NOMAD and the other plugins. If this happened, run `uv sync` from the distro root to restore the environment.

In the following sections, the `nomad-distro-dev` commands are run from `packages/pynxtools` and use `uv run --extra ...`. This works with all three options; with option 1, you can leave out `--extra`.

### Linting and formatting

We are using ruff and mypy for linting, formatting, and type checking. It is recommended to use the [pre-commit hook](https://pre-commit.com/#intro) available for ruff which formats the code and checks the linting before actually making an actual Git commit.

=== "Standalone"

    Install the pre-commit hook from the root of the repository (with the virtual environment activated):

    ```console
    pre-commit install
    ```

    To run the same checks as the CI:

    ```console
    ruff check src/pynxtools tests
    ruff format --check src/pynxtools tests
    mypy src/pynxtools tests
    ```

=== "Inside nomad-distro-dev"

    From `packages/pynxtools`:

    ```bash
    uv run --extra dev pre-commit install
    uv run --extra dev ruff check src/pynxtools tests
    uv run --extra dev ruff format --check src/pynxtools tests
    uv run --extra dev mypy src/pynxtools tests
    ```

    `uv run poe lint` from the distro root runs ruff over every package in the distro. Use the commands above to check only `pynxtools`, as the CI does.

### Testing

There exist unit tests for the software written in [pytest](https://docs.pytest.org/en/stable/).

=== "Standalone"

    ```console
    pytest -sv tests
    ```

    The tests in `tests/nomad` need the `nomad-lab` package. The CI runs them with `nomad-lab` installed. To run them standalone, install the `nomad` extra, e.g. `uv pip install -e ".[dev,nomad]"`, or run them inside `nomad-distro-dev`.

=== "Inside nomad-distro-dev"

    From `packages/pynxtools`:

    ```bash
    uv run --extra dev pytest -sv tests
    ```

    NOMAD is already installed in the distro, so the tests in `tests/nomad` run as well.

### Editing the documentation

We use [`mkdocs`](https://www.mkdocs.org/) for the documentation. To serve it locally:

=== "Standalone (uv)"

    ```bash
    uv run --extra docs --extra nomad mkdocs serve
    ```

    `uv run` creates a `uv.lock` file in the repository. Do not commit it.

=== "Standalone (pip)"

    With the virtual environment activated:

    ```bash
    pip install -e ".[docs,nomad]"
    python -m mkdocs serve
    ```

=== "Inside nomad-distro-dev"

    From `packages/pynxtools`:

    ```bash
    uv run --extra docs mkdocs serve
    ```

    If you declared the extras in the distro ([option 1](#getting-the-dev-and-docs-extras)), you can leave out `--extra docs`:

    ```bash
    uv run mkdocs serve
    ```

The `nomad` extra is needed because the [CLI reference](../reference/cli-api.md) documents the `pynx nomad` commands, which import NOMAD. Inside `nomad-distro-dev`, NOMAD is already installed.

The documentation is served at [http://127.0.0.1:8000/](http://127.0.0.1:8000/) and reloads when you edit files in `docs/`.

### Running the examples

A number of examples exist which document how the tools can be used. For a standalone usage, convenient Jupyter notebooks are available for some of the tools. To use these notebooks, Jupyter and related tools are needed:

=== "Standalone (uv)"

    ```bash
    uv pip install jupyter jupyterlab jupyterlab_h5web
    ```

=== "Standalone (pip)"

    ```bash
    pip install jupyter jupyterlab jupyterlab_h5web
    ```

=== "Inside nomad-distro-dev"

    `uv sync` would remove Jupyter if you installed it with `uv pip install`. Instead, add it to a single command with `--with`, from `packages/pynxtools`:

    ```bash
    uv run --with jupyterlab --with jupyterlab_h5web jupyter lab
    ```

### Contributing to the package on Github

Once you are happy with the changes, commit them on a separate branch created from `develop` and open a pull request against `develop`:

```console
git switch develop && git pull
git switch -c <short-descriptive-name>
# commit your changes, then
git push -u origin <short-descriptive-name>
```

Never open a pull request against `main`: it receives only `release/*` branches. We run a number of GitHub actions that check the correct linting, run the tests in an isolated environment, and build the documentation. Once these pass and a peer review of the code has occurred, your code will be accepted.

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

## Release workflow

1. Create the release branch from `develop`:

    ```console
    git switch develop && git pull
    git switch -c release/vX.Y.Z
    git push -u origin release/vX.Y.Z
    ```

2. Commit only release-specific changes on this branch (version bumps, changelog, last-minute bug fixes).
   New features keep going into `develop`.
3. Bump `version` in `CITATION.cff` to `X.Y.Z`, including any pre-release suffix (e.g. `0.1.2-rc1` for the tag `v0.1.2-rc1`).
   The publish workflow fails if it differs from the tag.
4. Open a PR from `release/vX.Y.Z` into `main`. Do not merge yet!
5. Create a GitHub release with the tag `vX.Y.Z` and select `release/vX.Y.Z` as its target branch. The publish workflow refuses to upload to PyPI if the release does not target `release/vX.Y.Z`
   or if the tagged commit is not on that branch.
6. Once CI passes and the release is published to PyPI, merge the PR.
7. If you fixed anything directly on the release branch, open a PR from `release/vX.Y.Z` into `develop` so the fixes are not lost in ongoing development.
8. Delete the `release/vX.Y.Z` branch.

## Troubleshooting

If you face any issues with the tool or when setting up the development environment, please create a new [Github Issue](https://github.com/FAIRmat-NFDI/pynxtools/issues/new?template=bug.yaml).
