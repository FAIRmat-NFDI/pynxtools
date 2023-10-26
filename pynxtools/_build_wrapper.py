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
                cwd=os.path.join(os.path.dirname(__file__), "definitions"),
                check=True,
                capture_output=True,
            )
            .stdout.decode("utf-8")
            .strip()
        )
    except (FileNotFoundError, CalledProcessError):
        return None


def _write_version_to_metadata(metadata_directory: str, dist_dir: str = None):
    with open(
        os.path.join(metadata_directory, dist_dir, "nexus-version.txt")
        if dist_dir is not None
        else os.path.join(metadata_directory, "nexus-version.txt"),
        "w+",
        encoding="utf-8",
    ) as file:
        file.write(get_vcs_version())


def prepare_metadata_for_build_editable(metadata_directory, config_settings=None):
    dist_dir = _orig.prepare_metadata_for_build_wheel(
        metadata_directory, config_settings
    )
    _write_version_to_metadata(metadata_directory, dist_dir)
    return dist_dir


def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
    dist_dir = _orig.prepare_metadata_for_build_wheel(
        metadata_directory, config_settings
    )
    _write_version_to_metadata(metadata_directory, dist_dir)
    return dist_dir


def build_editable(wheel_directory, config_settings=None, metadata_directory=None):
    # _write_version_to_metadata(metadata_directory)
    ret = _orig.build_editable(wheel_directory, config_settings, metadata_directory)

    return ret


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    # _write_version_to_metadata(metadata_directory)
    ret = _orig.build_wheel(wheel_directory, config_settings, metadata_directory)

    return ret
