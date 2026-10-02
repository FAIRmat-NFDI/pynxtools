import h5py
import numpy as np





f = h5py.File("interferometer_v4.nxs", "w")

f.create_group('entry')
f['/entry'].attrs['NX_class'] = 'NXentry'
f['/entry/definition'] = 'NXopt'

f['/entry/'].create_group('instrument')
f['/entry/instrument'].attrs['NX_class'] = 'NXinstrument' # to specifcy that its
                                          #the NXinstrument class and not NXuser



# define a geometric relationship of optical element itself
f['/entry/instrument/reference_system'] = 'geometric'
# define a z-axis transformation of the beam by this optical element
#f['/entry/instrument/reference_system'] = 'z-axis'

# Define this at the intstrument level. And for each element, which did not specifcy an own transfermatrix, assume
# an identity matrix for the respective formalism
#f['/entry/instrument/transfer_matrix_formalisms'] = ['aperture','focal length', 'jones matrix', 'transmission', 'reflectivity']



##########################
##########################
f['/entry/instrument'].create_group('source')   # make a subdirectory
f['/entry/instrument/source'].attrs['NX_class'] = 'NXopt_element'
# we give this field an attribute




f['/entry/instrument/source/previous_opt_element'] = '.'  # convention that it does not depend on anything / startpoint
# ^ this is a field / dataset



# here a dataset is created and assigned to "element_purpose"
f['/entry/instrument/source/element_purpose'] = 'This is the light source for the experiment'

if False:
    #.create group, is a group. This group will then contain datasets (strings, arrays)
    f['/entry/instrument/source'].create_group('output_beam_source')
    f['/entry/instrument/source/output_beam_source'].attrs['NX_class'] = 'NXbeam'  # rhs has to be named as the "goal" clas
    #    """Groups work like dictionaries, and datasets work like NumPy arrays"""


    #distance(NX_FLOAT)
    #incident_wavelength(NX_FLOAT)

    # distance to next element is removed, because only the distance to the previous element is of relevance. 
    # !!THIS!! source does not have a previous element
    f['/entry/instrument/source/output_beam_source/distance'] = 1
    #f['/entry/instrument/source/source_beam/distance'] = np.nan
    f['/entry/instrument/source/output_beam_source/distance'].attrs['units'] = 'm'

    # always relate to the previous optical element, as done in "depends_on"
    #f['/entry/instrument/source/source_beam/distance'].attrs['doc'] = "This beams distance to the respective next optical element."
    f['/entry/instrument/source/output_beam_source/distance'].attrs['doc'] = "This beams distance to the respective previous optical element."

    f['/entry/instrument/source/output_beam_source/final_energy'] = 8
    f['/entry/instrument/source/output_beam_source/final_energy'].attrs['units'] = 'mW'

    f['/entry/instrument/source/output_beam_source/final_wavelength'] = 325
    f['/entry/instrument/source/output_beam_source/final_wavelength'].attrs['units'] = 'nm'

    f['/entry/instrument/source/output_beam_source/final_polarization_stokes'] = np.array([1,-1,0,0], dtype=np.float64)
    #f['/entry/instrument/source/source_beam/incident_polarization_stokes'].attrs['units'] = 'arbitrary'


f['/entry/instrument/source'].create_group('geometric_position')
f['/entry/instrument/source/geometric_position'].attrs['NX_class'] = 'NXtransformation'


#f['/entry/instrument/source/position'].create_group('axis_position_coordinates')
f['/entry/instrument/source/geometric_position/axis_position_coordinates'] = np.sqrt(2)
f['/entry/instrument/source/geometric_position/axis_position_coordinates'].attrs['units'] = 'm'

# this is how the "\@vector:" is assigned
f['/entry/instrument/source/geometric_position/axis_position_coordinates'].attrs['vector'] = np.array([-1,1,0])
f['/entry/instrument/source/geometric_position/axis_position_coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/source/geometric_position/axis_position_coordinates'].attrs['depends_on'] = '.' #

# offset_units especially the attribute for the offset
if False:
    f['/entry/instrument/source'].create_group('transfer_matrix_table')
    f['/entry/instrument/source/transfer_matrix_table'].attrs['NX_class'] = 'NXdata'


    f['/entry/instrument/source/transfer_matrix_table/datatype_N'] = h5py.SoftLink('/entry/instrument/transfer_matrix_formalisms') 

    #f['/entry/instrument/source/transfer_matrix_table/datatype_N/enumeration'] = ['aperture','focal length', 'jones matrix']

    f['/entry/instrument/source/transfer_matrix_table/column_names'] = ['Aperture','Focal Length', 'JM00','JM01', 'JM10', 'JM11']

    f['/entry/instrument/source/transfer_matrix_table/transfer_matrix_data_0'] = 5
    f['/entry/instrument/source/transfer_matrix_table/transfer_matrix_data_0'].attrs['units'] = "mm"

    f['/entry/instrument/source/transfer_matrix_table/transfer_matrix_data_1'] = np.inf
    f['/entry/instrument/source/transfer_matrix_table/transfer_matrix_data_1'].attrs['units'] = "mm"

    f['/entry/instrument/source/transfer_matrix_table/transfer_matrix_data_2'] = np.array([[1,0],[0,0]])
    f['/entry/instrument/source/transfer_matrix_table/transfer_matrix_data_2'].attrs['units'] = "a.u."

    #f['/entry/instrument/source/transfer_matrix_table/transfer_matrix_data_3'] = np.nan
    #f['/entry/instrument/source/transfer_matrix_table/transfer_matrix_data_3'].attrs['units'] = "a.u."

    #f['/entry/instrument/source/transfer_matrix_table/transfer_matrix_data_4'] = np.nan
    #f['/entry/instrument/source/transfer_matrix_table/transfer_matrix_data_4'].attrs['units'] = "a.u."


##########################
##########################
f['/entry/instrument'].create_group('beamsplitter01')
f['/entry/instrument/beamsplitter01'].attrs['NX_class'] = 'NXopt_element'   # create group



# logical sequence of elements
f['/entry/instrument/beamsplitter01/previous_opt_element'] = '/entry/instrument/source' # create dataset

f['/entry/instrument/beamsplitter01/element_purpose'] = 'Splitting up the incident beam into two seperate beams with 90° angle between them.'
if False:
    f['/entry/instrument/beamsplitter01/input_beam_bs1'] = h5py.SoftLink('/entry/instrument/source/output_beam_source')

if False:
    ### create the beams comming from beamsplitter01
    f['/entry/instrument/beamsplitter01'].create_group('output_beam_bs1_straight')
    f['/entry/instrument/beamsplitter01/output_beam_bs1_straight'].attrs['NX_class'] = 'NXbeam'  


    # if this distance property of the NXbeam is used, then its origin is refered to the origin of the optical element it leaves
    f['/entry/instrument/beamsplitter01/output_beam_bs1_straight/distance'] = 1
    f['/entry/instrument/beamsplitter01/output_beam_bs1_straight/distance'].attrs['units'] = 'm'

    f['/entry/instrument/beamsplitter01/output_beam_bs1_straight/distance'].attrs['doc'] = "This beams distance to the respective previous optical element."

    f['/entry/instrument/beamsplitter01/output_beam_bs1_straight/final_energy'] = 4
    f['/entry/instrument/beamsplitter01/output_beam_bs1_straight/final_energy'].attrs['units'] = 'mW'

    f['/entry/instrument/beamsplitter01/output_beam_bs1_straight/final_wavelength'] = 325
    f['/entry/instrument/beamsplitter01/output_beam_bs1_straight/final_wavelength'].attrs['units'] = 'nm'

    f['/entry/instrument/beamsplitter01/output_beam_bs1_straight/final_polarization_stokes'] = np.array([1,-1,0,0], dtype=np.float64)


    ### create the beams comming from beamsplitter01
    f['/entry/instrument/beamsplitter01'].create_group('output_beam_bs1_reflected')
    f['/entry/instrument/beamsplitter01/output_beam_bs1_reflected'].attrs['NX_class'] = 'NXbeam'  

    f['/entry/instrument/beamsplitter01/output_beam_bs1_reflected/distance'] = 1
    f['/entry/instrument/beamsplitter01/output_beam_bs1_reflected/distance'].attrs['units'] = 'm'

    f['/entry/instrument/beamsplitter01/output_beam_bs1_reflected/distance'].attrs['doc'] = "This beams distance to the respective previous optical element."

    f['/entry/instrument/beamsplitter01/output_beam_bs1_reflected/final_energy'] = 4
    f['/entry/instrument/beamsplitter01/output_beam_bs1_reflected/final_energy'].attrs['units'] = 'mW'

    f['/entry/instrument/beamsplitter01/output_beam_bs1_reflected/final_wavelength'] = 325
    f['/entry/instrument/beamsplitter01/output_beam_bs1_reflected/final_wavelength'].attrs['units'] = 'nm'

    f['/entry/instrument/beamsplitter01/output_beam_bs1_reflected/final_polarization_stokes'] = np.array([1,-1,0,0], dtype=np.float64)


# We describe an actual geomtric description
f['/entry/instrument/beamsplitter01'].create_group('geometric_position')
f['/entry/instrument/beamsplitter01/geometric_position'].attrs['NX_class'] = 'NXtransformation'


#f['/entry/instrument/source/position'].create_group('axis_position_coordinates')
f['/entry/instrument/beamsplitter01/geometric_position/axis_position_coordinates'] = 1 #or np.abs( '/entry/instrument/beamsplitter01/position/axis_position_coordinates.attrs['vector']' )
f['/entry/instrument/beamsplitter01/geometric_position/axis_position_coordinates'].attrs['units'] = 'm'

# this is how the "\@vector:" is assigned
f['/entry/instrument/beamsplitter01/geometric_position/axis_position_coordinates'].attrs['vector'] = np.array([0,1,0])
f['/entry/instrument/beamsplitter01/geometric_position/axis_position_coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/beamsplitter01/geometric_position/axis_position_coordinates'].attrs['depends_on'] = '.' #or? '/entry/instrument/source/position/axis_position_coordinates'


# we describe a z-axis transformation
f['/entry/instrument/beamsplitter01'].create_group('z_axis')
f['/entry/instrument/beamsplitter01/z_axis'].attrs['NX_class'] = 'NXtransformation'



# beam going through the beam splitter [z-axis is not changing, the transformation is identity, which is a zero meter translation]
f['/entry/instrument/beamsplitter01/z_axis/straight_direction'] = 0 #or np.abs( '/entry/instrument/beamsplitter01/position/axis_position_coordinates.attrs['vector']' )
f['/entry/instrument/beamsplitter01/z_axis/straight_direction'].attrs['units'] = 'm'
f['/entry/instrument/beamsplitter01/z_axis/straight_direction'].attrs['vector'] = np.array([1,0,0])
f['/entry/instrument/beamsplitter01/z_axis/straight_direction'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/beamsplitter01/z_axis/straight_direction'].attrs['depends_on'] = '/entry/instrument/source/z_axis/output_beam' #or? '/entry/instrument/source/position/axis_position_coordinates'


# beam going through the beam splitter [z-axis is reflected by 90°, which is implemented by 90° rotation ]
f['/entry/instrument/beamsplitter01/z_axis/reflected_direction'] = 90 #or np.abs( '/entry/instrument/beamsplitter01/position/axis_position_coordinates.attrs['vector']' )
f['/entry/instrument/beamsplitter01/z_axis/reflected_direction'].attrs['units'] = 'degrees'
f['/entry/instrument/beamsplitter01/z_axis/reflected_direction'].attrs['vector'] = np.array([1,0,0])
f['/entry/instrument/beamsplitter01/z_axis/reflected_direction'].attrs['transformation_type'] = 'rotation'
f['/entry/instrument/beamsplitter01/z_axis/reflected_direction'].attrs['depends_on'] = '/entry/instrument/source/z_axis/output_beam' #or? '/entry/instrument/source/position/axis_position_coordinates'


####

if False:
    f['/entry/instrument/beamsplitter01'].create_group('transfer_matrix_table')
    f['/entry/instrument/beamsplitter01/transfer_matrix_table'].attrs['NX_class'] = 'NXdata'

    f['/entry/instrument/beamsplitter01/transfer_matrix_table/datatype_N'] = h5py.SoftLink('/entry/instrument/transfer_matrix_formalisms')

    #f['/entry/instrument/beamsplitter01/transfer_matrix_table/datatype_N/enumeration'] = ['aperture','focal length', 'jones matrix']

    f['/entry/instrument/beamsplitter01/transfer_matrix_table/column_names'] = ['Jones Matrix', 'Transmission', 'Reflectivity']



    #f['/entry/instrument/beamsplitter01/transfer_matrix_table/transfer_matrix_data_0'] = np.nan #?
    #f['/entry/instrument/beamsplitter01/transfer_matrix_table/transfer_matrix_data_0'].attrs['units'] = "mm"

    #f['/entry/instrument/beamsplitter01/transfer_matrix_table/transfer_matrix_data_1'] = np.inf
    #f['/entry/instrument/beamsplitter01/transfer_matrix_table/transfer_matrix_data_1'].attrs['units'] = "mm"

    f['/entry/instrument/beamsplitter01/transfer_matrix_table/transfer_matrix_data_2'] = np.array([[1,0],[0,1]])
    f['/entry/instrument/beamsplitter01/transfer_matrix_table/transfer_matrix_data_2'].attrs['units'] = "a.u."

    f['/entry/instrument/beamsplitter01/transfer_matrix_table/transfer_matrix_data_3'] = np.array([[np.linspace(300, 800, 251)], [0+0.5*np.abs(np.sin(3.5*np.pi / 1 * np.linspace(0, 1, 251)))]])
    f['/entry/instrument/beamsplitter01/transfer_matrix_table/transfer_matrix_data_3'].attrs['units'] = "a.u."

    f['/entry/instrument/beamsplitter01/transfer_matrix_table/transfer_matrix_data_4'] = np.array([[np.linspace(300, 800, 251)], [1-0.5*np.abs(np.sin(3.5*np.pi / 1 * np.linspace(0, 1, 251)))]])
    f['/entry/instrument/beamsplitter01/transfer_matrix_table/transfer_matrix_data_4'].attrs['units'] = "a.u."




##########################
##########################
f['/entry/instrument'].create_group('beamsplitter02')
f['/entry/instrument/beamsplitter02'].attrs['NX_class'] = 'NXopt_element'

# Use list for multiple dependencies
f['/entry/instrument/beamsplitter02/previous_opt_element'] = ['/entry/instrument/mirror01','/entry/instrument/mirror02']


f['/entry/instrument/beamsplitter02/element_purpose'] = 'Superposition two incident beams to be able to observe interference effects.'
if False:
    f['/entry/instrument/beamsplitter02/input_beam_mirror01'] = h5py.SoftLink('/entry/instrument/mirror01/output_beam_mirror1') 
    f['/entry/instrument/beamsplitter02/input_beam_mirror02'] = h5py.SoftLink('/entry/instrument/mirror02/output_beam_mirror2') 

    f['/entry/instrument/beamsplitter02/ouput_beam_bs2_superpos_to_detector01'] = h5py.SoftLink('/entry/instrument/beamsplitter02/input_beam_mirror01') 
    f['/entry/instrument/beamsplitter02/ouput_beam_bs2_superpos_to_detector02'] = h5py.SoftLink('/entry/instrument/beamsplitter02/input_beam_mirror02') 

f['/entry/instrument/beamsplitter02'].create_group('geometric_position')
f['/entry/instrument/beamsplitter02/geometric_position'].attrs['NX_class'] = 'NXtransformation'

f['/entry/instrument/beamsplitter02/geometric_position/axis_position_coordinates'] = 1
f['/entry/instrument/beamsplitter02/geometric_position/axis_position_coordinates'].attrs['units'] = 'm'


f['/entry/instrument/beamsplitter02/geometric_position/axis_position_coordinates'].attrs['vector'] = np.array([1,0,0])
f['/entry/instrument/beamsplitter02/geometric_position/axis_position_coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/beamsplitter02/geometric_position/axis_position_coordinates'].attrs['depends_on'] = '.' #

if False:
    f['/entry/instrument/beamsplitter02/transfer_matrix_table/datatype_N'] = h5py.SoftLink('/entry/instrument/transfer_matrix_formalisms')

    f['/entry/instrument/beamsplitter02/transfer_matrix_table/column_names'] = ['Jones Matrix', 'Transmission', 'Reflectivity', 'Propagation Direction']

    #f['/entry/instrument/beamsplitter02/transfer_matrix_table/transfer_matrix_data_0'] = np.nan #?
    #f['/entry/instrument/beamsplitter02/transfer_matrix_table/transfer_matrix_data_0'].attrs['units'] = "mm"

    #f['/entry/instrument/beamsplitter02/transfer_matrix_table/transfer_matrix_data_1'] = np.inf
    #f['/entry/instrument/beamsplitter02/transfer_matrix_table/transfer_matrix_data_1'].attrs['units'] = "mm"

    f['/entry/instrument/beamsplitter02/transfer_matrix_table/transfer_matrix_data_2'] = np.array([[1,0],[0,1]])
    f['/entry/instrument/beamsplitter02/transfer_matrix_table/transfer_matrix_data_2'].attrs['units'] = "a.u."

    f['/entry/instrument/beamsplitter02/transfer_matrix_table/transfer_matrix_data_3'] = np.array([[np.linspace(300, 800, 251)], [0.25+0.5*0.5*np.abs(np.sin(3.5*np.pi / 1 * np.linspace(0, 1, 251)))]])
    f['/entry/instrument/beamsplitter02/transfer_matrix_table/transfer_matrix_data_3'].attrs['units'] = "a.u."

    f['/entry/instrument/beamsplitter02/transfer_matrix_table/transfer_matrix_data_4'] = np.array([[np.linspace(300, 800, 251)], [0.75-0.5*0.5*np.abs(np.sin(3.5*np.pi / 1 * np.linspace(0, 1, 251)))]])
    f['/entry/instrument/beamsplitter02/transfer_matrix_table/transfer_matrix_data_4'].attrs['units'] = "a.u."


if False:
    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i1o1/JonesMatr'] = np.array([[1,0],[0,1]])
    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i1o1/JonesMatr'].attrs['units'] = "a.u."

    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i1o1/Transmiss'] = np.array([0.5])
    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i1o1/Transmiss'].attrs['units'] = "a.u."

    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i1o1/Refl'] = np.array([0.01])
    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i1o1/Refl'].attrs['units'] = "a.u."

    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i1o1/Prop-Direct'] = np.array([[0,-1,0],[0,0,0],[0,0,0]])
    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i1o1/Prop-Direct'].attrs['units'] = "a.u."


    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i1o2/JonesMatr'] = np.array([[1,0],[0,1]])
    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i1o2/JonesMatr'].attrs['units'] = "a.u."

    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i1o2/Transmiss'] = np.array([0.5])
    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i1o2/Transmiss'].attrs['units'] = "a.u."

    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i1o2/Refl'] = np.array([0.01])
    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i1o2/Refl'].attrs['units'] = "a.u."

    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i1o2/Prop-Direct'] = np.array([[0,0,0],[0,1,0],[0,0,0]])
    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i1o2/Prop-Direct'].attrs['units'] = "a.u."


    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i2o1/JonesMatr'] = np.array([[1,0],[0,1]])
    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i2o1/JonesMatr'].attrs['units'] = "a.u."

    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i2o1/Transmiss'] = np.array([0.5])
    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i2o1/Transmiss'].attrs['units'] = "a.u."

    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i2o1/Refl'] = np.array([0.01])
    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i2o1/Refl'].attrs['units'] = "a.u."

    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i2o1/Prop-Direct'] = np.array([[1,0,0],[0,0,0],[0,0,0]])
    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i2o1/Prop-Direct'].attrs['units'] = "a.u."


    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i2o2/JonesMatr'] = np.array([[1,0],[0,1]])
    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i2o2/JonesMatr'].attrs['units'] = "a.u."

    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i2o2/Transmiss'] = np.array([0.5])
    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i2o2/Transmiss'].attrs['units'] = "a.u."

    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i2o2/Refl'] = np.array([0.01])
    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i2o2/Refl'].attrs['units'] = "a.u."

    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i2o2/Prop-Direct'] = np.array([[0,0,0],[-1,0,0],[0,0,0]])
    f['/entry/instrument/beamsplitter02/TraMa_table/TraMa_i2o2/Prop-Direct'].attrs['units'] = "a.u."

##########################
##########################
f['/entry/instrument'].create_group('mirror01')
f['/entry/instrument/mirror01'].attrs['NX_class'] = 'NXopt_element'

f['/entry/instrument/mirror01/previous_opt_element'] = '/entry/instrument/beamsplitter01'

f['/entry/instrument/mirror01/element_purpose'] = 'Redirect the first beam from the beamsplitter01.'
if False:
    f['/entry/instrument/mirror01/input_beam'] = h5py.SoftLink('/entry/instrument/beamsplitter01/output_beam_bs1_straight')

    f['/entry/instrument/mirror01'].create_group('output_beam_mirror1')
    f['/entry/instrument/mirror01/output_beam_mirror1'].attrs['NX_class'] = 'NXbeam'

    f['/entry/instrument/mirror01/output_beam_mirror1/distance'] = 1
    f['/entry/instrument/mirror01/output_beam_mirror1/distance'].attrs['units'] = 'm'

    f['/entry/instrument/mirror01/output_beam_mirror1/distance'].attrs['doc'] = "This beams distance to the respective previous optical element."

    f['/entry/instrument/mirror01/output_beam_mirror1/final_energy'] = 4
    f['/entry/instrument/mirror01/output_beam_mirror1/final_energy'].attrs['units'] = 'mW'

    f['/entry/instrument/mirror01/output_beam_mirror1/final_wavelength'] = 325
    f['/entry/instrument/mirror01/output_beam_mirror1/final_wavelength'].attrs['units'] = 'nm'

    f['/entry/instrument/mirror01/output_beam_mirror1/final_polarization_stokes'] = np.array([1,-1,0,0], dtype=np.float64)

    f['/entry/instrument/mirror01/output_beam_mirror1/propagation_directtion'] = [0,-1,0]


f['/entry/instrument/mirror01'].create_group('geometric_position')
f['/entry/instrument/mirror01/geometric_position'].attrs['NX_class'] = 'NXtransformation'

f['/entry/instrument/mirror01/geometric_position/axis_position_coordinates'] = np.sqrt(2)
f['/entry/instrument/mirror01/geometric_position/axis_position_coordinates'].attrs['units'] = 'm'


f['/entry/instrument/mirror01/geometric_position/axis_position_coordinates'].attrs['vector'] = np.array([1,1,0])
f['/entry/instrument/mirror01/geometric_position/axis_position_coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/mirror01/geometric_position/axis_position_coordinates'].attrs['depends_on'] = '.' #

if False:
    f['/entry/instrument/mirror01/transfer_matrix_table/datatype_N'] = h5py.SoftLink('/entry/instrument/transfer_matrix_formalisms')
    f['/entry/instrument/mirror01/transfer_matrix_table/column_names'] = ['Aperture', 'Jones Matrix', 'Transmission', 'Reflectivity']


    f['/entry/instrument/mirror01/transfer_matrix_table/transfer_matrix_data_0'] = 15
    f['/entry/instrument/mirror01/transfer_matrix_table/transfer_matrix_data_0'].attrs['units'] = "mm"

    #f['/entry/instrument/mirror01/transfer_matrix_table/transfer_matrix_data_1'] = np.inf
    #f['/entry/instrument/mirror01/transfer_matrix_table/transfer_matrix_data_1'].attrs['units'] = "mm"

    f['/entry/instrument/mirror01/transfer_matrix_table/transfer_matrix_data_2'] = np.array([[1,0],[0,-1]])
    f['/entry/instrument/mirror01/transfer_matrix_table/transfer_matrix_data_2'].attrs['units'] = "a.u."

    f['/entry/instrument/mirror01/transfer_matrix_table/transfer_matrix_data_3'] = 0.99
    f['/entry/instrument/mirror01/transfer_matrix_table/transfer_matrix_data_3'].attrs['units'] = "a.u."

    f['/entry/instrument/mirror01/transfer_matrix_table/transfer_matrix_data_4'] = 0.01
    f['/entry/instrument/mirror01/transfer_matrix_table/transfer_matrix_data_4'].attrs['units'] = "a.u."


##########################
##########################
f['/entry/instrument'].create_group('mirror02')
f['/entry/instrument/mirror02'].attrs['NX_class'] = 'NXopt_element'

f['/entry/instrument/mirror02/previous_opt_element'] = '/entry/instrument/beamsplitter01'

f['/entry/instrument/mirror02/element_purpose'] = 'Redirect the second beam from the beamsplitter01.'

#f['/entry/instrument/mirror02'].create_group('bs1_beam02')
#f['/entry/instrument/mirror02/bs1_beam_02'].attrs['NX_class'] = 'NXbeam'  


# 1. change to straight and reflected beam
# 2. add all beams between the optical elements
#f['/entry/instrument/mirror02/bs1_beam02/identical_to'] = '/entry/instrument/beamsplitter01/bs1_beam02'
if False:
    f['/entry/instrument/mirror02/input_beam'] = h5py.SoftLink('/entry/instrument/beamsplitter01/output_beam_bs1_reflected') 
# f['external_link'] = h5py.ExternalLink('tall.h5', 'g1/g1.1') # first is the actual file, the second is the path in the file

if False:
    # two different solutions to create a link
    f['/entry/instrument/mirror02'].create_group('output_beam_mirror2')
    f['/entry/instrument/mirror02/output_beam_mirror2'].attrs['NX_class'] = 'NXbeam'  

    f['/entry/instrument/mirror02/output_beam_mirror2/distance'] = 1
    f['/entry/instrument/mirror02/output_beam_mirror2/distance'].attrs['units'] = 'm'

    f['/entry/instrument/mirror02/output_beam_mirror2/distance'].attrs['doc'] = "This beams distance to the respective previous optical element."

    f['/entry/instrument/mirror02/output_beam_mirror2/final_energy'] = 4
    f['/entry/instrument/mirror02/output_beam_mirror2/final_energy'].attrs['units'] = 'mW'

    f['/entry/instrument/mirror02/output_beam_mirror2/final_wavelength'] = 325
    f['/entry/instrument/mirror02/output_beam_mirror2/final_wavelength'].attrs['units'] = 'nm'

    f['/entry/instrument/mirror02/output_beam_mirror2/final_polarization_stokes'] = np.array([1,-1,0,0], dtype=np.float64)

    f['/entry/instrument/mirror02/output_beam_mirror2/propagation_directtion'] = [1,0,0]

f['/entry/instrument/mirror02'].create_group('geometric_position')
f['/entry/instrument/mirror02/geometric_position'].attrs['NX_class'] = 'NXtransformation'

f['/entry/instrument/mirror02/geometric_position/axis_position_coordinates'] = 0
f['/entry/instrument/mirror02/geometric_position/axis_position_coordinates'].attrs['units'] = 'm'


f['/entry/instrument/mirror02/geometric_position/axis_position_coordinates'].attrs['vector'] = np.array([0,0,0])
f['/entry/instrument/mirror02/geometric_position/axis_position_coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/mirror02/geometric_position/axis_position_coordinates'].attrs['depends_on'] = '.' #
if False:
    f['/entry/instrument/mirror02/transfer_matrix_table/datatype_N'] = h5py.SoftLink('/entry/instrument/transfer_matrix_formalisms')
    f['/entry/instrument/mirror02/transfer_matrix_table/column_names'] = ['Aperture', 'Jones Matrix', 'Transmission', 'Reflectivity']


    f['/entry/instrument/mirror02/transfer_matrix_table/transfer_matrix_data_0'] = 15
    f['/entry/instrument/mirror02/transfer_matrix_table/transfer_matrix_data_0'].attrs['units'] = "mm"

    #f['/entry/instrument/mirror02/transfer_matrix_table/transfer_matrix_data_1'] = np.inf
    #f['/entry/instrument/mirror02/transfer_matrix_table/transfer_matrix_data_1'].attrs['units'] = "mm"

    f['/entry/instrument/mirror02/transfer_matrix_table/transfer_matrix_data_2'] = np.array([[1,0],[0,-1]])
    f['/entry/instrument/mirror02/transfer_matrix_table/transfer_matrix_data_2'].attrs['units'] = "a.u."

    f['/entry/instrument/mirror02/transfer_matrix_table/transfer_matrix_data_3'] = 0.99
    f['/entry/instrument/mirror02/transfer_matrix_table/transfer_matrix_data_3'].attrs['units'] = "a.u."

    f['/entry/instrument/mirror02/transfer_matrix_table/transfer_matrix_data_4'] = 0.01
    f['/entry/instrument/mirror02/transfer_matrix_table/transfer_matrix_data_4'].attrs['units'] = "a.u."

##########################
##########################
f['/entry/instrument'].create_group('detector01')
f['/entry/instrument/detector01'].attrs['NX_class'] = 'NXopt_element'

f['/entry/instrument/detector01/previous_opt_element'] = '/entry/instrument/beamsplitter02'

f['/entry/instrument/detector01/element_purpose'] = 'Measuring the interference effect from the first final beam'

if False:
    f['/entry/instrument/detector01/input_beam_detector1'] = h5py.SoftLink('/entry/instrument/beamsplitter02/ouput_beam_bs2_superpos_to_detector01')

f['/entry/instrument/detector01'].create_group('geometric_position')
f['/entry/instrument/detector01/geometric_position'].attrs['NX_class'] = 'NXtransformation'

f['/entry/instrument/detector01/geometric_position/axis_position_coordinates'] = 2
f['/entry/instrument/detector01/geometric_position/axis_position_coordinates'].attrs['units'] = 'm'


f['/entry/instrument/detector01/geometric_position/axis_position_coordinates'].attrs['vector'] = np.array([1,0,0])
f['/entry/instrument/detector01/geometric_position/axis_position_coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/detector01/geometric_position/axis_position_coordinates'].attrs['depends_on'] = '.' #

if False:
    f['/entry/instrument/detector01/transfer_matrix_table/datatype_N'] = h5py.SoftLink('/entry/instrument/transfer_matrix_formalisms')
    f['/entry/instrument/detector01/transfer_matrix_table/column_names'] = ['Aperture','Focal Length', 'Jones Matrix']

    f['/entry/instrument/detector01/transfer_matrix_table/transfer_matrix_data_0'] = 10
    f['/entry/instrument/detector01/transfer_matrix_table/transfer_matrix_data_0'].attrs['units'] = "mm"

    #f['/entry/instrument/detector01/transfer_matrix_table/transfer_matrix_data_1'] = 700
    #f['/entry/instrument/detector01/transfer_matrix_table/transfer_matrix_data_1'].attrs['units'] = "mm"

    f['/entry/instrument/detector01/transfer_matrix_table/transfer_matrix_data_2'] = np.array([[1,0],[0,0]])
    f['/entry/instrument/detector01/transfer_matrix_table/transfer_matrix_data_2'].attrs['units'] = "a.u."

    #f['/entry/instrument/detector01/transfer_matrix_table/transfer_matrix_data_3'] = 0.99
    #f['/entry/instrument/detector01/transfer_matrix_table/transfer_matrix_data_3'].attrs['units'] = "a.u."

    #f['/entry/instrument/detector01/transfer_matrix_table/transfer_matrix_data_4'] = 0.01
    #f['/entry/instrument/detector01/transfer_matrix_table/transfer_matrix_data_4'].attrs['units'] = "a.u."

##########################
##########################
f['/entry/instrument'].create_group('detector02')
f['/entry/instrument/detector02'].attrs['NX_class'] = 'NXopt_element'

f['/entry/instrument/detector02/previous_opt_element'] = '/entry/instrument/beamsplitter02'

f['/entry/instrument/detector02/element_purpose'] = 'Measuring the interference effect from the first final beam'
if False:
    f['/entry/instrument/detector02/input_beam_detector2'] = h5py.SoftLink('/entry/instrument/beamsplitter02/ouput_beam_bs2_superpos_to_detector02')

f['/entry/instrument/detector02'].create_group('geometric_position')
f['/entry/instrument/detector02/geometric_position'].attrs['NX_class'] = 'NXtransformation'

f['/entry/instrument/detector02/geometric_position/axis_position_coordinates'] = np.sqrt(2)
f['/entry/instrument/detector02/geometric_position/axis_position_coordinates'].attrs['units'] = 'm'


f['/entry/instrument/detector02/geometric_position/axis_position_coordinates'].attrs['vector'] = np.array([1,-1,0])
f['/entry/instrument/detector02/geometric_position/axis_position_coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/detector02/geometric_position/axis_position_coordinates'].attrs['depends_on'] = '.' #

if False:
    f['/entry/instrument/detector02/transfer_matrix_table/datatype_N'] = h5py.SoftLink('/entry/instrument/transfer_matrix_formalisms')
    f['/entry/instrument/detector02/transfer_matrix_table/column_names'] = ['Aperture','Focal Length', 'Jones Matrix']


    f['/entry/instrument/detector02/transfer_matrix_table/transfer_matrix_data_0'] = 10
    f['/entry/instrument/detector02/transfer_matrix_table/transfer_matrix_data_0'].attrs['units'] = "mm"

    #f['/entry/instrument/detector02/transfer_matrix_table/transfer_matrix_data_1'] = 700
    #f['/entry/instrument/detector02/transfer_matrix_table/transfer_matrix_data_1'].attrs['units'] = "mm"

    f['/entry/instrument/detector02/transfer_matrix_table/transfer_matrix_data_2'] = np.array([[1,0],[0,0]])
    f['/entry/instrument/detector02/transfer_matrix_table/transfer_matrix_data_2'].attrs['units'] = "a.u."

    #f['/entry/instrument/detector02/transfer_matrix_table/transfer_matrix_data_3'] = 0.99
    #f['/entry/instrument/detector02/transfer_matrix_table/transfer_matrix_data_3'].attrs['units'] = "a.u."

    #f['/entry/instrument/detector02/transfer_matrix_table/transfer_matrix_data_4'] = 0.01
    #f['/entry/instrument/detector02/transfer_matrix_table/transfer_matrix_data_4'].attrs['units'] = "a.u."


# ##########################
# ##########################
# f['/entry/instrument'].create_group('opt_elements')   # make a subdirectory
# f['/entry/instrument/opt_elements'].attrs['NX_class'] = 'NXopt_element_list'
# #or this:
# #f['/entry/instrument/opt_elements/source'].attrs['NX_class'] = 'NXopt_element'



# f['/entry/instrument/opt_elements'].create_group('source')
# f['/entry/instrument/opt_elements/source'].create_group('geometric_position')
# f['/entry/instrument/opt_elements/source/geometric_position'].attrs['NX_class'] = 'NXtransformation'

# f['/entry/instrument/opt_elements/source/previous_opt_element'] = '/entry/instrument/beamsplitter01'

# f['/entry/instrument/opt_elements/source/geometric_position/axis_position_coordinates'] = np.sqrt(2)
# f['/entry/instrument/opt_elements/source/geometric_position/axis_position_coordinates'].attrs['units'] = 'm'

# # this is how the "\@vector:" is assigned
# f['/entry/instrument/opt_elements/source/geometric_position/axis_position_coordinates'].attrs['vector'] = np.array([-1,1,0])
# f['/entry/instrument/opt_elements/source/geometric_position/axis_position_coordinates'].attrs['transformation_type'] = 'translation'
# f['/entry/instrument/opt_elements/source/geometric_position/axis_position_coordinates'].attrs['depends_on'] = '.' #

# # offset_units especially the attribute for the offset


# f['/entry/instrument/opt_elements/source/aperture'] = 5
# f['/entry/instrument/opt_elements/source/aperture'].attrs['units'] = "mm"

# f['/entry/instrument/opt_elements/source/focal_length'] = np.inf
# f['/entry/instrument/opt_elements/source/focal_length'].attrs['units'] = "mm"

# f['/entry/instrument/opt_elements/source/output_polarization'] = np.array([[1,0]])
# f['/entry/instrument/opt_elements/source/output_polarization'].attrs['units'] = "a.u."



unity_div = 0
unity_atten = 1

#################################
#### Talk with sandor ###########
#################################
f['/entry/instrument'].create_group('opt_transfer_matrix_tables')   # make a subdirectory
f['/entry/instrument/opt_transfer_matrix_tables'].attrs['NX_class'] = 'NXoptical_assembly'
f['/entry/instrument/opt_transfer_matrix_tables/matrix_elements'] = ['attenuation','divergence'] # specicic elements which we are interested in



#f['/entry/instrument/opt_transfer_matrix_tables'].create_group('transfer_matrix_table_opt_element_1')   # make a subdirectory
#f['/entry/instrument/opt_transfer_matrix_tables/transfer_matrix_table_opt_element_1'].attrs['NX_class'] = 'NXtransfer_matrix_table'

#f['/entry/instrument/opt_transfer_matrix_tables/transfer_matrix_table_opt_element_1/matrix'] = [[0.5,0],[0,unity_div]] # should be 2x2 np.array

#################################
#### Source #####################
#################################

f['/entry/instrument/opt_transfer_matrix_tables'].create_group('TMT_source')
f['/entry/instrument/opt_transfer_matrix_tables/TMT_source'].attrs['NX_class'] = 'NXtransfer_matrix_table'

f['/entry/instrument/opt_transfer_matrix_tables/TMT_source/matrix_beamsplitter01'] = [[1,0],[0,0]] 
f['/entry/instrument/opt_transfer_matrix_tables/TMT_source/matrix_beamsplitter01'].attrs['beam_pos'] = 'start'

#################################
#### Beam Splitter 1 ############
#################################

f['/entry/instrument/opt_transfer_matrix_tables'].create_group('TMT_beamsplitter01')
f['/entry/instrument/opt_transfer_matrix_tables/TMT_beamsplitter01'].attrs['NX_class'] = 'NXtransfer_matrix_table'


bs1_tsr = 0.6 #beam splitter 1 transmission splitting ratio
f['/entry/instrument/opt_transfer_matrix_tables/TMT_beamsplitter01/matrix_source_mirror01'] = [[bs1_tsr,0],[0,unity_div]]
f['/entry/instrument/opt_transfer_matrix_tables/TMT_beamsplitter01/matrix_source_mirror02'] = [[1-bs1_tsr,0],[0,unity_div]]
#f['/entry/instrument/opt_transfer_matrix_tables'].create_group('TMT_bs1_2')
#f['/entry/instrument/opt_transfer_matrix_tables/TMT_bs1_2'].attrs['NX_class'] = 'NXtransfer_matrix_table'

#f['/entry/instrument/opt_transfer_matrix_tables/TMT_bs1_2/matrix'] = [[1-bs1_tsr,0],[0,unity_div]]


#################################
#### Beam Splitter 2 ############
#################################

#straight
bs2_tsr=0.9
f['/entry/instrument/opt_transfer_matrix_tables'].create_group('TMT_beamsplitter02')
f['/entry/instrument/opt_transfer_matrix_tables/TMT_beamsplitter02'].attrs['NX_class'] = 'NXtransfer_matrix_table'

f['/entry/instrument/opt_transfer_matrix_tables/TMT_beamsplitter02/matrix_mirror01_detector01'] = [[bs2_tsr,0],[0,unity_div]]
f['/entry/instrument/opt_transfer_matrix_tables/TMT_beamsplitter02/matrix_mirror01_detector02'] = [[(1-bs2_tsr)*0.8,0],[0,unity_div]]
f['/entry/instrument/opt_transfer_matrix_tables/TMT_beamsplitter02/matrix_mirror02_detector01'] = [[bs2_tsr*0.8,0],[0,unity_div]]
f['/entry/instrument/opt_transfer_matrix_tables/TMT_beamsplitter02/matrix_mirror02_detector02'] = [[1-bs2_tsr,0],[0,unity_div]]

#reflected
#f['/entry/instrument/opt_transfer_matrix_tables'].create_group('TMT_bs2_2')
#f['/entry/instrument/opt_transfer_matrix_tables/TMT_bs2_2'].attrs['NX_class'] = 'NXtransfer_matrix_table'

#f['/entry/instrument/opt_transfer_matrix_tables/TMT_bs2_2/matrix'] = [[1-bs1_tsr,0],[0,unity_div]]

#straight
#f['/entry/instrument/opt_transfer_matrix_tables'].create_group('TMT_bs2_3')
#f['/entry/instrument/opt_transfer_matrix_tables/TMT_bs2_3'].attrs['NX_class'] = 'NXtransfer_matrix_table'

#f['/entry/instrument/opt_transfer_matrix_tables/TMT_bs2_3/matrix'] = [[bs1_tsr,0],[0,unity_div]]

#reflected
#f['/entry/instrument/opt_transfer_matrix_tables'].create_group('TMT_bs2_4')
#f['/entry/instrument/opt_transfer_matrix_tables/TMT_bs2_4'].attrs['NX_class'] = 'NXtransfer_matrix_table'

#f['/entry/instrument/opt_transfer_matrix_tables/TMT_bs2_4/matrix'] = [[1-bs1_tsr,0],[0,unity_div]]


#################################
#### Detector 1 #################
#################################

f['/entry/instrument/opt_transfer_matrix_tables'].create_group('TMT_detector01')
f['/entry/instrument/opt_transfer_matrix_tables/TMT_detector01'].attrs['NX_class'] = 'NXtransfer_matrix_table'

f['/entry/instrument/opt_transfer_matrix_tables/TMT_detector01/matrix_beamsplitter02'] = [[0.01,0],[0,0]]
f['/entry/instrument/opt_transfer_matrix_tables/TMT_detector01/matrix_beamsplitter02'].attrs['beam_pos'] = 'end'



#################################
#### Detector 2 #################
#################################

f['/entry/instrument/opt_transfer_matrix_tables'].create_group('TMT_detector02')
f['/entry/instrument/opt_transfer_matrix_tables/TMT_detector02'].attrs['NX_class'] = 'NXtransfer_matrix_table'

f['/entry/instrument/opt_transfer_matrix_tables/TMT_detector02/matrix_beamsplitter02'] = [[0.01,0],[0,0]]
f['/entry/instrument/opt_transfer_matrix_tables/TMT_detector02/matrix_beamsplitter02'].attrs['beam_pos'] = 'end'


#################################
#### Mirror 1 ###################
#################################


f['/entry/instrument/opt_transfer_matrix_tables'].create_group('TMT_mirror01')
f['/entry/instrument/opt_transfer_matrix_tables/TMT_mirror01'].attrs['NX_class'] = 'NXtransfer_matrix_table'

f['/entry/instrument/opt_transfer_matrix_tables/TMT_mirror01/matrix_beamsplitter01_beamsplitter02'] = [[0.3,0],[0,-0.08]]



#################################
#### Mirror 2 ###################
#################################

f['/entry/instrument/opt_transfer_matrix_tables'].create_group('TMT_mirror02')
f['/entry/instrument/opt_transfer_matrix_tables/TMT_mirror02'].attrs['NX_class'] = 'NXtransfer_matrix_table'

f['/entry/instrument/opt_transfer_matrix_tables/TMT_mirror02/matrix_beamsplitter01_beamsplitter02'] = [[0.8,0],[0,-0.02]]

#################################
#### . ###################
#################################
if False:
    f['/entry/instrument/opt_transfer_matrix_tables'].create_group('TMT_.')
    f['/entry/instrument/opt_transfer_matrix_tables/TMT_.'].attrs['NX_class'] = 'NXtransfer_matrix_table'

    f['/entry/instrument/opt_transfer_matrix_tables/TMT_./matrix'] = [[1,0],[0,0]]




f['/entry/instrument/'].create_group('opt_beams_formalisms')
f['/entry/instrument/opt_beams_formalisms'].attrs['NX_class'] = 'NXopt_beam_assembly'

f['/entry/instrument/opt_beams_formalisms/vector_elements'] = ['attenuation','divergence']

f['/entry/instrument'].create_group('beam01')
f['/entry/instrument/beam01'].attrs['NX_class'] = 'NXopt_beam'

f['/entry/instrument'].create_group('BS1_to_Mirror_1_Beam')
f['/entry/instrument/BS1_to_Mirror_1_Beam'].attrs['NX_class'] = 'NXopt_beam'
f['/entry/instrument/BS1_to_Mirror_1_Beam/prev_opt_element'] = '/entry/instrument/beamsplitter01'
f['/entry/instrument/BS1_to_Mirror_1_Beam/next_opt_element'] = '/entry/instrument/mirror01'

f['/entry/instrument'].create_group('beam03')
f['/entry/instrument/beam03'].attrs['NX_class'] = 'NXopt_beam'

#f['/entry/instrument'].create_group('beam04')
#f['/entry/instrument/beam04'].attrs['NX_class'] = 'NXopt_beam'

f['/entry/instrument'].create_group('beam05')
f['/entry/instrument/beam05'].attrs['NX_class'] = 'NXopt_beam'

f['/entry/instrument'].create_group('final_beam_detector_1')
f['/entry/instrument/final_beam_detector_1'].attrs['NX_class'] = 'NXopt_beam'
f['/entry/instrument/final_beam_detector_1/prev_opt_element'] = '/entry/instrument/beamsplitter02'
f['/entry/instrument/final_beam_detector_1/next_opt_element'] = '/entry/instrument/detector01'


f['/entry/instrument'].create_group('beam07')
f['/entry/instrument/beam07'].attrs['NX_class'] = 'NXopt_beam'









# #f['/entry/instrument/opt_elements/list_of_tech_parameters'] = [""]
# #blackbox-with description
# #diffraction gratings
# #optical filters
# #lenses
# #mirrors
# #prisms
# #ND filter / Reflection Filter / Optical attenuator
# #beam splitter
# # compensator (Babinet–Soleil)
# # retarder Lambda/4 Lambda/2
# # depolarizer
# # diaphragm / aperture
# # Diffractive beam splitter
# # Etalon (Gires-Tournois)
# # lens
# # optical isolator (i.e optical diode)
#     # different types
# # microcavity
# # pinhole
# # polarizer
# # q-plate?
# # retroreflector
# # waveguide
# # spatial filter
# # waveguide
# # waveplate
# # zone plate


