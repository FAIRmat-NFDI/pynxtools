import os
from glob import glob
from subprocess import CalledProcessError, run
from typing import Optional

from setuptools import build_meta as _orig
from setuptools.build_meta import *


def get_vcs_version(tag_match="*[0-9]*") -> Optional[str]:
    """
    The version of the Nexus standard and the NeXus Definition language
    based on git tags and commits
    """
    try:
        return (
            run(
                ["git", "describe", "--tags", "--long", "--match", tag_match],
                cwd=os.path.join(os.path.dirname(__file__), "../pynxtools/definitions"),
                check=True,
                capture_output=True,
            )
            .stdout.decode("utf-8")
            .strip()
        )
    except (FileNotFoundError, CalledProcessError):
        return None


def _write_version_to_metadata(directory: str):
    version = get_vcs_version()
    if version is None or not version:
        raise ValueError("Could not determine version from nexus_definitions")

    with open(
        os.path.join(os.path.dirname(__file__), "nexus-version.txt"),
        "w+",
        encoding="utf-8",
    ) as file:
        file.write(version)


def build_editable(wheel_directory, config_settings=None, metadata_directory=None):
    _write_version_to_metadata(metadata_directory)
    ret = _orig.build_editable(wheel_directory, config_settings, metadata_directory)

    return ret


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    _write_version_to_metadata(metadata_directory)
    ret = _orig.build_wheel(wheel_directory, config_settings, metadata_directory)

    return ret


def build_sdist(sdist_directory, config_settings=None):
    _write_version_to_metadata(os.path.join(os.path.dirname(__file__), "../"))
    sdist_dir = _orig.build_sdist(sdist_directory, config_settings)
    return sdist_dir
