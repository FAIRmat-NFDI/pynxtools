"""An example reader implementation for the DataConverter."""
from typing import Tuple

from readers.base_reader import BaseReader


class ExampleReader(BaseReader):
    """An example reader implementation for the DataConverter."""

    # pylint: disable=too-few-public-methods

    def read(self, template: dict = None, file_paths: Tuple[str] = None) -> dict:
        """Reads data from given file and returns a filled template dictionary"""

        # Fill the template
        for path in file_paths:
            print(path)

        return template


# This has to be set to allow the convert script to use this reader. Set it to "MyDataReader".
READER = ExampleReader
