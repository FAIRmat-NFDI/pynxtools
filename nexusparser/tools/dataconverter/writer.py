
class Writer:
    """
    The writer class for writing a Nexus file in accordance with a given NXDL.

    Attributes
    ----------
    data : dict
        dictionary containing the data to convert
    nxdl_path : str
        path to the nxdl file to use during conversion
    output_path : str
        path to the output Nexus file
    nxdl : dict
        stores xml data from given nxdl file to use during conversion
    """

    def __init__(self, data: dict = None, nxdl_path: str = None, output_path: str = None):
        """Constructs the necessary objects required by the Writer class."""
        self.data = data
        self.nxdl_path = nxdl_path
        self.output_path = output_path
        self.path = ""
        self.data_dict = {}

    def nxdl_to_attrs(self, path: str = '/') -> dict:
        """Return a dictionary of all the attributes at the given path in the NXDL"""
        self.path = path
        attrs = {}
        return attrs

    def write(self, data_dict: dict = None):
        """Writes the Nexus file with data from the reader and appropriate attrs from NXDL"""
        self.data_dict = data_dict
