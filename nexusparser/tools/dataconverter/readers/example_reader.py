from typing import Tuple

from readers.base_reader import BaseReader


class ExampleReader(BaseReader):

    # pylint: disable=too-few-public-methods

    def read(self, template: dict = None, file_paths: Tuple[str] = None) -> dict:
        # Fill the template
        for path in file_paths:
            print(path)

        return template


# This has to be set to allow the convert script to use this reader. Set it to "MyDataReader".
READER = ExampleReader
