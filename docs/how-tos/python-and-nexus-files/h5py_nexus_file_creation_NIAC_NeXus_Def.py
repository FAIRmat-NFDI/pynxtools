# Import h5py, to write an hdf5 file
import h5py
import numpy as np

# create a h5py file in writing mode with given name "NXopt_minimal_example", file extension "nxs"
f = h5py.File("NXopt_minimal_example_NIAC_NeXus_Def.nxs", "w")

# there are only 3 fundamental objects: >group<, >attribute< and >datafield<.


# create a >group< called "entry"
f.create_group("/entry")

# assign the >group< called "entry" an >attribute<
# The attribute is "NX_class"(a NeXus class) with the value of this class is "NXentry"
f["/entry"].attrs["NX_class"] = "NXentry"

# create >datafield< called "definition" inside the entry, and assign it the value "NXoptical_spectroscopy"
# This field is important, as it is used in validation process to identify the NeXus definition.
f["/entry/definition"] = "NXopt"


f["/entry/definition"].attrs["version"] = (
    "v2024.02 - Hardcored (i.e. no software generated version available)"
)

f["/entry/definition"].attrs["url"] = (
    "https://github.com/nexusformat/definitions/blob/0e3421f8cef02bfbaa6004e182e3d67dace7ef1b/contributed_definitions/NXopt.nxdl.xml"
)

f["/entry/experiment_identifier"] = "Measurement Nbr 12356789"


f["/entry/experiment_description"] = "This is a real experiment."

f["/entry/experiment_type"] = "Ellipsometry"

f["/entry/start_time"] = "2008-02-01T09:00:22+05"


f.create_group("/entry/user1")
f["/entry/user1"].attrs["NX_class"] = "NXuser"

f["/entry/user1/name"] = "Max Mustermann"

f["/entry/user1/email"] = "max@mustermann.de"


f.create_group("/entry/experiment_setup_1")
f["/entry/experiment_setup_1"].attrs["NX_class"] = "NXinstrument"

f["/entry/experiment_setup_1/calibration_status"] = "no calibration"

f["/entry/experiment_setup_1/model"] = "M2000"

f["/entry/experiment_setup_1/angle_of_incidence"] = float(40)
f["/entry/experiment_setup_1/angle_of_incidence"].attrs["units"] = "degree"


f.create_group("/entry/experiment_setup_1/software")
f["/entry/experiment_setup_1/software"].attrs["NX_class"] = "NXprocess"
f["/entry/experiment_setup_1/software"].attrs["url"] = "www.internet.com"
f["/entry/experiment_setup_1/software/program"] = "unknown"
f["/entry/experiment_setup_1/software/version"] = "version 0"

f.create_group("/entry/experiment_setup_1/excitation_beam_path")
f["/entry/experiment_setup_1/excitation_beam_path"].attrs["NX_class"] = "NXbeam_path"


f.create_group("/entry/experiment_setup_1/sample_stage")
f["/entry/experiment_setup_1/sample_stage"].attrs["NX_class"] = "NXsubentry"

f["/entry/experiment_setup_1/sample_stage/stage_type"] = "manual stage"

f.create_group("/entry/experiment_setup_1/sample_stage/environment_conditions")
f["/entry/experiment_setup_1/sample_stage/environment_conditions"].attrs["NX_class"] = (
    "NXenvironment"
)

f["/entry/experiment_setup_1/sample_stage/environment_conditions/medium"] = "water"


f.create_group("/entry/silicon_substrate")
f["/entry/silicon_substrate"].attrs["NX_class"] = "NXsample"

f["/entry/silicon_substrate/sample_name"] = "Si-111"

f["/entry/silicon_substrate/sample_type"] = "thin film"

f["/entry/silicon_substrate/layer_structure"] = "This is just a silicon wafer"

f["/entry/silicon_substrate/chemical_formula"] = "Si"

f["/entry/silicon_substrate/atom_types"] = "Si"

f["/entry/silicon_substrate/sample_history"] = "This sample was found in the lab B123"


f.create_group("/entry/data_collection")
f["/entry/data_collection"].attrs["NX_class"] = "NXprocess"

f["/entry/data_collection/data_identifier"] = "Nr. 1234"

f["/entry/data_collection/data_type"] = "intensity"


f["/entry/data_collection/measured_data"] = [100, 3, 13]


f.create_group("/entry/plot")
f["/entry/plot"].attrs["NX_class"] = "NXdata"
f["/entry/plot/wavelength_x"] = np.arange(100)
f["/entry/plot/intensity_y"] = np.arange(3)
f["/entry/plot"].attrs["axes"] = "wavelength_x"
f["/entry/plot"].attrs["signal"] = "intensity_y"


# f['/entry/dataset_example/x'] = X
# f['/entry/dataset_example/y'] = np.sin(X)
# f['/entry/dataset_example/y'].attrs['signal'] = 'y'
# f['/entry/dataset_example/y'].attrs['axes'] = 'x'
