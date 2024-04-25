"""
Build wrapper for setuptools to create a nexus-version.txt file
containing the nexus definitions verison.
"""

import os
from subprocess import CalledProcessError, run
from typing import Optional

from setuptools import build_meta as _orig
from setuptools.build_meta import *  # pylint: disable=wildcard-import,unused-wildcard-import


def get_vcs_version(tag_match="*[0-9]*") -> Optional[str]:
    """
    The version of the Nexus standard and the NeXus Definition language
    based on git tags and commits
    """
    try:
        return (
            run(
                [
                    "git",
                    "describe",
                    "--dirty",
                    "--tags",
                    "--long",
                    "--match",
                    tag_match,
                ],
                cwd=os.path.join(os.path.dirname(__file__), "../pynxtools/definitions"),
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


# pylint: disable=function-redefined
def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    """
    PEP 517 compliant build wheel hook.
    This is a wrapper for setuptools and adds a nexus version file.
    """
    _write_version_to_metadata()
    return _orig.build_wheel(wheel_directory, config_settings, metadata_directory)


# pylint: disable=function-redefined
def build_sdist(sdist_directory, config_settings=None):
    """
    PEP 517 compliant build sdist hook.
    This is a wrapper for setuptools and adds a nexus version file.
    """
    _write_version_to_metadata()
    return _orig.build_sdist(sdist_directory, config_settings)
