"""
Build wrapper for setuptools to create a nexus-version.txt file
containing the nexus definitions version.
"""

import os
from subprocess import CalledProcessError, run
from typing import Optional

try:
    from setuptools import build_meta as _orig
    from setuptools.build_meta import *  # pylint: disable=wildcard-import,unused-wildcard-import
except ImportError:
    pass


def get_vcs_version(tag_match="*[0-9]*") -> str | None:
    """
    The version of the Nexus standard and the NeXus Definition language
    based on git tags and commits
    """
    try:
        cwd = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../pynxtools/definitions")
        )
        return (
            run(
                [
                    "git",
                    "describe",
                    "--dirty",
                    "--tags",
                    "--long",
                    "--abbrev=8",
                    "--match",
                    tag_match,
                ],
                cwd=cwd,
                # Prevent git from walking up past the definitions directory.
                # Without this, git falls back to the pynxtools repo when definitions
                # has no .git (e.g. in a non-editable install inside the source tree).
                env={**os.environ, "GIT_CEILING_DIRECTORIES": os.path.dirname(cwd)},
                check=True,
                capture_output=True,
            )
            .stdout.decode("utf-8")
            .strip()
        )
    except (FileNotFoundError, CalledProcessError):
        return None


def _write_version_to_metadata():
    version = get_vcs_version()
    if version is None or not version:
        return

    with open(
        os.path.join(os.path.dirname(__file__), "nexus-version.txt"),
        "w+",
        encoding="utf-8",
    ) as file:
        file.write(version)


def get_definitions_submodule_url():
    """
    The URL of the definitions submodule in pynxtools.
    """
    submodule_path = "src/pynxtools/definitions"

    try:
        # Define the command to run
        url_line = run(
            [
                "git",
                "config",
                "--file",
                ".git/config",
                "--get-regexp",
                f"^submodule\\.{submodule_path}\\.url",
            ],
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()

        if url_line:
            url = url_line.split(" ")[1]
            return url
        else:
            return None

    except (FileNotFoundError, CalledProcessError):
        return None


def _write_definitions_remote_url():
    """Write the URL of the definitions remote to file."""
    remote_repo_url = get_definitions_submodule_url()
    if remote_repo_url is None or not remote_repo_url:
        return

    with open(
        os.path.join(os.path.dirname(__file__), "remote_definitions_url.txt"),
        "w+",
        encoding="utf-8",
    ) as file:
        file.write(remote_repo_url)


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):  # type: ignore[no-redef]
    """
    PEP 517 compliant build wheel hook.
    This is a wrapper for setuptools and adds a nexus version file and a
    file with the remote of the definitions submodule.
    """
    _write_version_to_metadata()
    _write_definitions_remote_url()
    return _orig.build_wheel(wheel_directory, config_settings, metadata_directory)


def build_sdist(sdist_directory, config_settings=None):  # type: ignore[no-redef]
    """
    PEP 517 compliant build sdist hook.
    This is a wrapper for setuptools and adds a nexus version file and a
    file with the remote of the definitions submodule.
    """
    _write_version_to_metadata()
    _write_definitions_remote_url()
    return _orig.build_sdist(sdist_directory, config_settings)
