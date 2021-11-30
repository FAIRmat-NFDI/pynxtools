from abc import ABC, abstractmethod
from typing import Tuple

class BaseReader(ABC):
    """
    The abstract class off of which to implement readers.

    The filename's prefix is the identifier. The '_reader.py' is snipped out.
    For this BaseReader with filename base_reader.py the ID  becomes 'base'

    For future reference:
    - Support links by setting the path in the template with the following object
       object = {"link": "/path/to/source/data"}
    """

    # pylint: disable=too-few-public-methods

    @abstractmethod
    def read(self, template: dict = None, file_paths: Tuple[str] = None) -> dict:
        """Reads data from given file and returns a filled template dictionary"""
        return template

READER = BaseReader
