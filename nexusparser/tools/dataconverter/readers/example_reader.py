"""An example reader implementation for the DataConverter."""
from typing import Tuple

from nexusparser.tools.dataconverter.readers.base_reader import BaseReader


class ExampleReader(BaseReader):
    """An example reader implementation for the DataConverter."""

    # pylint: disable=too-few-public-methods

    # Whitelist for the NXDLs that the reader supports and can process
    supported_nxdls = ["NXsample", "NXspe"]

    def read(self, template: dict = None, file_paths: Tuple[str] = None) -> dict:
        """Reads data from given file and returns a filled template dictionary"""
        metadata = []

        for file_path in file_paths:
            file_extension = file_path[file_path.rindex("."):]
            with open(file_path, "r") as f:
                if file_extension == ".metadata_extension":
                    metadata = f.read()
        
        for value in metadata:
            # The entries in the template dict should correspond with what the dataconverter
            # outputs with --generate-template for a provided NXDL file
            template[f"/entry/instrument/metadata/{value}"] = value

        return template


# This has to be set to allow the convert script to use this reader. Set it to "MyDataReader".
READER = ExampleReader
