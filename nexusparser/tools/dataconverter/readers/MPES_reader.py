import numpy as np
import h5py 
from typing import Tuple
from base_reader import BaseReader
import yaml
import pprint


class Reader(BaseReader):
    
    def read(template, input_file): #For the case of one input file
        with h5py.File(input_file, 'r') as f:

            metadata= dict(f.attrs.items())

            for path in template:
                path_trunc= path.split('/')[-1]

                if path_trunc in metadata:
                    template[path]= metadata[path_trunc]
                    
        return template




READER = Reader
# pprint.pprint(READER.read(template, "fixed_metadata.h5"))





