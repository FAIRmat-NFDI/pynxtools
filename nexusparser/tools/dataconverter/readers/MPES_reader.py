import h5py 
from nexusparser.tools.dataconverter.readers.base_reader import BaseReader
import pprint
import os

class MPESReader(BaseReader):
    
    def read(self, template, file_paths):

        for file_path in file_paths:
            add_path= '' if os.path.exists(file_path) else 'readers\\input_files\\' 
            file= add_path+file_path
            file_name= file.split('\\')[-1]

            if file_name == 'fixed_metadata.h5':

                with h5py.File(file, 'r') as f:
                    metadata= dict(f.attrs.items())

                    for path in template:

                        if path in metadata:
                            template[path]= metadata[path]

            elif file_name == 'binned.h5':
                pass
                    
        return template



READER = MPESReader





