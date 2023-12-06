"""
Tests the version retrieval for the nexus definitions submodule
"""
import re

from pynxtools import get_nexus_version


def test_get_nexus_version():
    """
    Tests if we get a version string from nexus definitions
    """
    version = get_nexus_version()

    assert version is not None
    assert re.match(r"v\d{4}\.\d{2}\.post1\.dev\d+\+g[a-z0-9]", version)
