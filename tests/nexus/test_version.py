"""
Tests the version retrieval for the nexus definitions submodule
"""
from subprocess import run
from pynxtools.definitions.dev_tools.globals.nxdl import get_vcs_version


def test_git_is_runnable():
    """
    Check if git is generally runnable in this environment
    """
    run(["git", "describe", "--tags"], check=True)


def test_get_vcs_version():
    """
    Tests if we get a version string from nexus definitions
    """
    version = get_vcs_version()

    assert version is not None
    assert version
