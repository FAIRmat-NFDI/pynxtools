"""
Build wrapper for setuptools to create a nexus-version.txt file
containing the nexus definitions verison.
"""
import os
from subprocess import CalledProcessError, run
from typing import TYPE_CHECKING, Optional

from setuptools import build_meta as _orig
from setuptools.build_meta import *  # pylint: disable=wildcard-import,unused-wildcard-import

if TYPE_CHECKING:
    from setuptools_scm import ScmVersion


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


def _build_version(tag: str, distance: int, node: str, dirty: bool) -> str:
    if distance == 0 and not dirty:
        return f"{tag}"

    return f"{tag}.dev{distance}+{'dirty' if dirty else node}"


def _write_version_to_metadata():
    version = get_vcs_version()
    if version is None or not version:
        raise ValueError("Could not determine version from nexus_definitions")

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
    ret = _orig.build_wheel(wheel_directory, config_settings, metadata_directory)

    return ret


# pylint: disable=function-redefined
def build_sdist(sdist_directory, config_settings=None):
    """
    PEP 517 compliant build sdist hook.
    This is a wrapper for setuptools and adds a nexus version file.
    """
    _write_version_to_metadata()
    sdist_dir = _orig.build_sdist(sdist_directory, config_settings)
    return sdist_dir


def construct_version(version: "ScmVersion") -> str:
    """
    Constructs the pynxtools version
    """
    return _build_version(version.tag, version.distance, version.node, version.dirty)
