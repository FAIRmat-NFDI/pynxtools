"""
Tests the version retrieval for the nexus definitions submodule
"""
from pynxtools import get_nexus_version


def test_get_nexus_version():
    """
    Tests if we get a version string from nexus definitions
    """
    version = get_nexus_version()

    assert version is not None
    assert version
