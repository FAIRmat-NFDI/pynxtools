# Import h5py, to write an hdf5 file
import h5py

# create a h5py file in writing mode with given name "NXopt_minimal_example", file extension "nxs"
f = h5py.File("NXopt_minimal_example.nxs", "w")

# there are only 3 fundamental objects: >group<, >attribute< and >datafield<.


# create a >group< called "entry"
f.create_group("/entry")

# assign the >group< called "entry" an >attribute<
# The attribute is "NX_class"(a NeXus class) with the value of this class is "NXentry"
f["/entry"].attrs["NX_class"] = "NXentry"

# create >datafield< called "definition" inside the entry, and assign it the value "NXoptical_spectroscopy"
# This field is important, as it is used in validation process to identify the NeXus definition.
f["/entry/definition"] = "NXoptical_spectroscopy"


f["/entry/definition"].attrs["version"] = (
    "2024.05.22 - Hardcored (i.e. no software generated version available)"
)

f["/entry/definition"].attrs["URL"] = (
    "https://github.com/FAIRmat-NFDI/nexus_definitions/blob/2811f38f8fab23a267c4868ec3820e334e7a1199/contributed_definitions/NXopt.nxdl.xml"
)

f["/entry/experiment_type"] = "transmission spectroscopy"

f.create_group("/entry/experiment_setup_1")
f["/entry/experiment_setup_1"].attrs["NX_class"] = "NXinstrument"
