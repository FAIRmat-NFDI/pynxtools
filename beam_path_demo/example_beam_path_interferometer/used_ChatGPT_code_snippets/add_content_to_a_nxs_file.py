import h5py
import numpy as np

# Source file name
source_filename = 'interferometer_v3.nxs'

# Destination file name (new name for the copy)
destination_filename = 'interferometer_v3_mod.nxs'
if True:
  # use os. to create a copy of a file named: "interferometer_v3_mod.nxs"
  import shutil
  # Copy the file
  shutil.copy2(source_filename, destination_filename)

  print(f"File '{source_filename}' copied to '{destination_filename}'.")


f = h5py.File("interferometer_v3_mod.nxs", "a")



f['/entry/instrument'].create_group('beams')   # make a subdirectory
f['/entry/instrument/beams'].attrs['NX_class'] = 'NXopt_beam_assembly'



f['/entry/instrument/beams/' + 'NEW_CONTENT'] = 'BLUBS!' 

if False:
    # Step 3: Open HDF5 file in write mode ('w') or append mode ('a')
    with h5py.File('interferometer_v3_mod.nxs', 'a') as file:
        # Step 4: Create datasets, groups, or attributes
        # Create a dataset with some data
        data = np.array([1, 2, 3, 4, 5])
        file.create_dataset('dataset_name', data=data)

        # Create a group and add a dataset inside the group
        group = file.create_group('group_name')
        group.create_dataset('another_dataset', data=np.random.random((3, 3)))

        # Create an attribute for the dataset
        file['dataset_name'].attrs['attribute_name'] = 'attribute_value'

    # Step 5: The file is automatically closed when exiting the 'with' block