import os
from pynxtools.nomad.utils import get_package_filepath

nxs_filepath = get_package_filepath()

if not os.path.exists(nxs_filepath):
    print(f"Generating NeXus package at {nxs_filepath}.")
    import pynxtools.nomad.schema
else:
    print(f"NeXus package already existed at {nxs_filepath}.")
