"""
Tests the version retrieval for the nexus definitions submodule
"""

import re

from pynxtools import get_definitions_url

# Regex pattern to match a valid GitHub repo URL
GITHUB_URL_REGEX = r"^https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/?$"


def test_get_definitions_url():
    """
    Tests if we get a valid GitHub URL from the text value stored in the
    remote_definitions_url.txt file.
    """
    definitions_url = get_definitions_url()

    assert definitions_url is not None
    assert re.match(GITHUB_URL_REGEX, definitions_url)
