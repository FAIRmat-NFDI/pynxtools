from pynxtools.dataconverter.nexus_tree import generate_tree_from
from pynxtools.definitions.dev_tools.utils.nxdl_utils import get_app_defs_names


def test_parsing_of_all_appdefs():
    """All appdefs are parsed to a tree without raising an error"""
    appdefs = get_app_defs_names()
    for appdef in appdefs:
        generate_tree_from(appdef)
