from pynxtools.definitions.dev_tools.globals.nxdl import get_vcs_version


def test_get_vcs_version():
    """
    Tests if we get a version string from nexus definitions
    """
    version = get_vcs_version()

    assert version is not None
    assert version
