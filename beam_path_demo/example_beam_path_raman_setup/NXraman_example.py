
import h5py
import numpy as np
#import datetime
#import os

#import pandas as pd

# create a h5py file with name and in write mode
f = h5py.File("NXraman_example_v3.nxs", "w")


#create a group, called "entry"
f.create_group('/entry')

#assign the group "entry" the attribute "nexus_class" with the value "NXentry"
f['/entry'].attrs['NX_class'] = 'NXentry'




f['/entry/definition'] = 'NXraman'
f['/entry/definition'].attrs['url'] = 'https://github.com/FAIRmat-NFDI/nexus_definitions/blob/2811f38f8fab23a267c4868ec3820e334e7a1199/contributed_definitions/NXraman.nxdl.xml'
f['/entry/definition'].attrs['version'] = '2024.05.21 - Hardcored (i.e. no Software version available)'

#create a group
f.create_group('/entry/instrument/')

#assign attribute
f['/entry/instrument'].attrs['NX_class'] = 'NXinstrument'

#create a field and give it a value
f['/entry/experiment_description'] = 'A custom build UV Raman setup with backscattering configuration. '

f['/entry/experiment_type'] = 'Raman spectroscopy'


f['/entry/raman_experiment_type'] = 'non-resonant Raman spectroscopy'







f.create_group('/entry/instrument/device_information')
f['/entry/instrument/device_information'].attrs['NX_class'] = 'NXfabrication'

f['/entry/instrument/device_information/vendor'] = 'n.A.'
f['/entry/instrument/device_information/model'] = 'Custom Build'
f['/entry/instrument/device_information/construction_year'] = 2009
f['/entry/instrument/device_information/construction_year'].attrs['NX_class'] = 'NX_DATE_TIME'

f.create_group('/entry/instrument/software_Labspec5')
f['/entry/instrument/software_Labspec5'].attrs['NX_class'] = 'NXprogram'

f['/entry/instrument/software_Labspec5/program'] = 'LabSpec 5'
f['/entry/instrument/software_Labspec5/program'].attrs['version'] = '5.64.15'
f['/entry/instrument/software_Labspec5/program'].attrs['url'] = 'NXprogram'
f['/entry/instrument/software_Labspec5/vendor'] = 'HORIBA Scientific'
f['/entry/instrument/software_Labspec5/capability'] = 'This software allows the control of monochromator and CCD settings. Measurements can be started in defined areas as well as calibrations for the respective data output. The dataouput is in .ngs or .txt files. Multiple measurements can be merged automatically or raw-data output is as well available without background subtraction.'


f.create_group('/entry/instrument/software_MikroMove')
f['/entry/instrument/software_MikroMove'].attrs['NX_class'] = 'NXprogram'

f['/entry/instrument/software_MikroMove/program'] = 'MikroMove'
f['/entry/instrument/software_MikroMove/program'].attrs['version'] = '2.0.7.12'
f['/entry/instrument/software_MikroMove/vendor'] = 'Princton Instruments'
f['/entry/instrument/software_MikroMove/capability'] = 'Control of the sample lateral position by two coupled linear stages.'



f.create_group('/entry/instrument/software_PI_E-816_PZT')
f['/entry/instrument/software_PI_E-816_PZT'].attrs['NX_class'] = 'NXprogram'

f['/entry/instrument/software_PI_E-816_PZT/program'] = 'PZTControl'
f['/entry/instrument/software_PI_E-816_PZT/program'].attrs['version'] = '3.0.6.1'
f['/entry/instrument/software_PI_E-816_PZT/vendor'] = 'Princton Instruments'
f['/entry/instrument/software_PI_E-816_PZT/capability'] = 'Control of the focus position via piezo-electric stage. The objective lens is fixed to this stage.'

f['/entry/instrument/angle_reference_frame'] = 'sample normal centered'


f.create_group('/entry/instrument/wavelength_resolution')
f['/entry/instrument/wavelength_resolution'].attrs['NX_class'] = 'NXresolution'
f['/entry/instrument/wavelength_resolution/physical_quantity'] = 'wavelength'
f['/entry/instrument/wavelength_resolution/type'] = 'derived'
f['/entry/instrument/wavelength_resolution/resolution'] = 5
f['/entry/instrument/wavelength_resolution/resolution'].attrs['unit'] = 'pm'










f['/entry/instrument/scattering_configuration'] = 'z(xx)z'
f['/entry/instrument/scattering_configuration'].attrs['NX_class'] = 'NX_CHAR'

f['/entry/instrument/scattering_configuration'].attrs['non_orthogonal_base_vectors'] = np.array([[0,0,1],[1,0,0],[1,0,0],[0,0,1]])


f.create_group('/entry/instrument/reference_frames')
f['/entry/instrument/reference_frames'].attrs['NX_class'] = 'NXcoordinate_system_set'

f.create_group('/entry/instrument/reference_frames/laboratory_coordinate_system')
f['/entry/instrument/reference_frames/laboratory_coordinate_system'].attrs['NX_class'] = 'NXcoordinate_system'

f['/entry/instrument/reference_frames/laboratory_coordinate_system/origin'] = 'Marking on optical table close to the front left pole.'
f['/entry/instrument/reference_frames/laboratory_coordinate_system/type'] = 'cartesian'
f['/entry/instrument/reference_frames/laboratory_coordinate_system/alias'] = 'laboratory_system'
f['/entry/instrument/reference_frames/laboratory_coordinate_system/handedness'] = 'right_handed'
f['/entry/instrument/reference_frames/laboratory_coordinate_system/x'] = [1,0,0]
f['/entry/instrument/reference_frames/laboratory_coordinate_system/x_direction'] = 'Along short edge of optical table'
f['/entry/instrument/reference_frames/laboratory_coordinate_system/y'] = [0,1,0]
f['/entry/instrument/reference_frames/laboratory_coordinate_system/y_direction'] = 'Along long edge of optical table'
f['/entry/instrument/reference_frames/laboratory_coordinate_system/z'] = [0,0,1]
f['/entry/instrument/reference_frames/laboratory_coordinate_system/z_direction'] = 'antiparallel to gravitation'


f.create_group('/entry/instrument/reference_frames/beam_coordinate_system')
f['/entry/instrument/reference_frames/beam_coordinate_system'].attrs['NX_class'] = 'NXcoordinate_system'
f['/entry/instrument/reference_frames/beam_coordinate_system/origin'] = 'Point where the incident beam direction hits the sample surface'
f['/entry/instrument/reference_frames/beam_coordinate_system/type'] = 'cartesian'
f['/entry/instrument/reference_frames/beam_coordinate_system/alias'] = 'beam_system'
f['/entry/instrument/reference_frames/beam_coordinate_system/handedness'] = 'right_handed'
f['/entry/instrument/reference_frames/beam_coordinate_system/x'] = [1,0,0]
f['/entry/instrument/reference_frames/beam_coordinate_system/x_direction'] = '(mostly) perpendictular to gravitation, i.e. relation to laboratory depends on beam direction'
f['/entry/instrument/reference_frames/beam_coordinate_system/y'] = [0,1,0]
f['/entry/instrument/reference_frames/beam_coordinate_system/y_direction'] = '(mostly) antiparallel to grativation, i.e. relation to laboratory depends on beam direction'
f['/entry/instrument/reference_frames/beam_coordinate_system/z'] = [0,0,1]
f['/entry/instrument/reference_frames/beam_coordinate_system/z_direction'] = 'beam propagation direction, i.e. relation to laboratory depends on beam position'

f.create_group('/entry/instrument/reference_frames/sample_normal_coordinate_system')
f['/entry/instrument/reference_frames/sample_normal_coordinate_system'].attrs['NX_class'] = 'NXcoordinate_system'
f['/entry/instrument/reference_frames/sample_normal_coordinate_system/origin'] = 'Sample surface where the incident beam points'
f['/entry/instrument/reference_frames/sample_normal_coordinate_system/type'] = 'cartesian'
f['/entry/instrument/reference_frames/sample_normal_coordinate_system/alias'] = 'sample_system'
f['/entry/instrument/reference_frames/sample_normal_coordinate_system/handedness'] = 'right_handed'
f['/entry/instrument/reference_frames/sample_normal_coordinate_system/x'] = [1,0,0]
f['/entry/instrument/reference_frames/sample_normal_coordinate_system/x_direction'] = 'first surface inplane direction, arbitrary as relation to crystal'
f['/entry/instrument/reference_frames/sample_normal_coordinate_system/y'] = [0,1,0]
f['/entry/instrument/reference_frames/sample_normal_coordinate_system/y_direction'] = 'second surface inplane direction'
f['/entry/instrument/reference_frames/sample_normal_coordinate_system/z'] = [0,0,1]
f['/entry/instrument/reference_frames/sample_normal_coordinate_system/z_direction'] = 'surface normal direction'

f.create_group('/entry/instrument/reference_frames/crystal_coordinate_system')
f['/entry/instrument/reference_frames/crystal_coordinate_system'].attrs['NX_class'] = 'NXcoordinate_system'
f['/entry/instrument/reference_frames/crystal_coordinate_system/origin'] = 'Center of a silicon atom.'
f['/entry/instrument/reference_frames/crystal_coordinate_system/alias'] = 'crystal_system'








f['/entry/instrument/calibration_status'] =  'no calibration'

f['/entry/instrument/angle_of_incidence'] = 180
f['/entry/instrument/angle_of_incidence'].attrs['units'] = 'degree'

f['/entry/instrument/angle_of_detection'] = 0
f['/entry/instrument/angle_of_detection'].attrs['units'] = 'degree'

f['/entry/instrument/angle_of_incident_and_detection_beam'] = 180
f['/entry/instrument/angle_of_incident_and_detection_beam'].attrs['units'] = 'degree'


f['/entry/instrument/lateral_focal_point_offset'] = 0
f['/entry/instrument/lateral_focal_point_offset'].attrs['units'] = 'mm'
















f.create_group('/entry/instrument/sample_stage')
f['/entry/instrument/sample_stage'].attrs['NX_class'] = 'NXmanipulator'

f['/entry/instrument/sample_stage/stage_type'] = 'scanning stage'

f['/entry/instrument/sample_stage/beam_sample_relation'] = 'Beam hit the sample in the middle, with at least 2mm distance towards all edges'

f['/entry/instrument/incident_source_wavelength'] = '532'
f['/entry/instrument/incident_source_wavelength'].attrs['NX_class'] = 'NX_NUMBER'
#f['/entry/instrument/incident_source_wavelength'].attrs['units'] = 'NX_WAVELENGTH'
f['/entry/instrument/incident_source_wavelength'].attrs['units'] = 'nm'




#f['/entry/instrument/scattering_configuration/non_orthogonal_base_vectors'] = np.array([[0,0,1],[1,0,0],[1,0,0],[0,0,1]])


import h5py
#import cv2  # Assuming you have OpenCV installed

# Read the image file
#image_path = 'networkx_raman_setup_graph.png'
#image = cv2.imread(image_path)[::-1]

# OpenCV reads images in BGR format, convert to RGB
#image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

f.create_group('/entry/instrument/beam_path')
f['/entry/instrument/beam_path'].attrs['NX_class'] = 'NXbeam_path'

#f.create_dataset('/entry/instrument/beam_path/networkx', data=image)


with open("networkx_raman_setup_graphv2.png", "rb") as image_file:
    image_data = image_file.read()

f.create_dataset("/entry/instrument/beam_path/networkx", data=np.void(image_data))


with open("setup_sketch_white_background_2v2.png", "rb") as image_file:
    image_data = image_file.read()

f.create_dataset("/entry/instrument/beam_path/paper_sketch", data=np.void(image_data))





inst_path = '/entry/instrument/' 

name_source = "source_532nm-Laser-Source"
path_source_full = inst_path + name_source

name_lens = "Mitutoyo VIS-NIR"
name_lens_full = inst_path + name_lens

name_detector = 'Symphony BI CCD'
name_detector_full = inst_path + name_detector


name_hwp_1 = 'SmallHWP' 
name_hwp_1_full = inst_path + name_hwp_1

name_hwp_2 = 'LargeHWP' 
name_hwp_2_full = inst_path + name_hwp_2

name_monochromator = 'U1000'
name_monochromator_full= inst_path + name_monochromator

name_sample = 'Si-111_01'
name_sample_full= inst_path + name_sample









coordinates_beam_devices=np.transpose(np.loadtxt("coordinates_optical_elements_raman_setup.txt",  delimiter="\t"))


beam_dev_radius = coordinates_beam_devices[0]
beam_dev_x_unit_vec = coordinates_beam_devices[1]
beam_dev_y_unit_vec = coordinates_beam_devices[2]






f.create_group('/entry/instrument/instrument_calibration_MonochromatorU1000')
f['/entry/instrument/instrument_calibration_MonochromatorU1000'].attrs['NX_class'] = 'NXsubentry'

f['/entry/instrument/instrument_calibration_MonochromatorU1000/device_path'] = name_monochromator_full
f['/entry/instrument/instrument_calibration_MonochromatorU1000/calibration_method'] = 'Spectral lines of a Ag lamp'
f['/entry/instrument/instrument_calibration_MonochromatorU1000/calibration_accuracy'] = 10
f['/entry/instrument/instrument_calibration_MonochromatorU1000/calibration_accuracy'].attrs['unit'] = 'pm'
f['/entry/instrument/instrument_calibration_MonochromatorU1000/calibration_status'] = 'calibration time provided'
f['/entry/instrument/instrument_calibration_MonochromatorU1000/calibration_time']= 2023



f.create_group('/entry/instrument/beam_laser_source')
f['/entry/instrument/beam_laser_source'].attrs['NX_class'] = 'NXbeam'

f['/entry/instrument/beam_laser_source/extent'] = 1
f['/entry/instrument/beam_laser_source/extent'].attrs['unit'] = 'mm'

f['/entry/instrument/beam_laser_source/average_power'] = 100
f['/entry/instrument/beam_laser_source/average_power'].attrs['unit'] = 'mW'


f['/entry/instrument/beam_laser_source/beam_polarization_type'] = 'linear'


f['/entry/instrument/beam_laser_source/previous_device'] = '/entry/instrument/AUXopt_source'
f['/entry/instrument/beam_laser_source/next_device'] = '/entry/instrument/LaserLineFilter'



f.create_group('/entry/instrument/beam_incident_sample')
f['/entry/instrument/beam_incident_sample'].attrs['NX_class'] = 'NXbeam'


f['/entry/instrument/beam_incident_sample/incident_wavelength'] = 532.12
f['/entry/instrument/beam_incident_sample/incident_wavelength'].attrs['unit'] = 'nm'

f['/entry/instrument/beam_incident_sample/incident_wavelength_spread'] = 5
f['/entry/instrument/beam_incident_sample/incident_wavelength_spread'].attrs['unit'] = 'pm'


f['/entry/instrument/beam_incident_sample/incident_polarization'] = np.array([1,1,0,0])

f['/entry/instrument/beam_incident_sample/extent'] = 3
f['/entry/instrument/beam_incident_sample/extent'].attrs['unit'] = 'mm'

f['/entry/instrument/beam_incident_sample/average_power'] = 8
f['/entry/instrument/beam_incident_sample/average_power'].attrs['unit'] = 'mW'

f['/entry/instrument/beam_incident_sample/associated_source'] = path_source_full

f['/entry/instrument/beam_incident_sample/beam_polarization_type'] = 'linear'


f['/entry/instrument/beam_incident_sample/previous_device'] = '/entry/instrument/AUXincident_light_optics/'
f['/entry/instrument/beam_incident_sample/next_device'] = '/entry/instrument/AUXsample_as_beam_element'


f.create_group('/entry/instrument/experiment_identifier')
f['/entry/instrument/experiment_identifier'].attrs['NX_class'] = 'NXidentifier'

f['/entry/instrument/experiment_identifier/identifier'] = 'Leipzig University, Grundmann Group, TA 309, UV Raman setup'
f['/entry/instrument/experiment_identifier/is_persistent'] = 'false'





# Auxillary Beam devices
f.create_group('/entry/instrument/AUXopt_source')
f['/entry/instrument/AUXopt_source'].attrs['NX_class'] = 'NXbeam_device'
f['/entry/instrument/AUXopt_source'].attrs['device'] = path_source_full
f['/entry/instrument/AUXopt_source/previous_devices'] = '.'


f['/entry/instrument/AUXopt_source'].create_group('location')
f['/entry/instrument/AUXopt_source/location'].attrs['NX_class'] = 'NXtransformations'
f['/entry/instrument/AUXopt_source/location/coordinates'] = beam_dev_radius[29]
f['/entry/instrument/AUXopt_source/location/coordinates'].attrs['units'] = 'm'

# this is how the "\@vector:" is assigned
f['/entry/instrument/AUXopt_source/location/coordinates'].attrs['vector'] = np.array([beam_dev_x_unit_vec[29],beam_dev_y_unit_vec[29],0])
f['/entry/instrument/AUXopt_source/location/coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/AUXopt_source/location/coordinates'].attrs['depends_on'] = '.' #



f.create_group('/entry/instrument/AUXincident_light_optics')
f['/entry/instrument/AUXincident_light_optics'].attrs['NX_class'] = 'NXbeam_device'
f['/entry/instrument/AUXincident_light_optics'].attrs['device'] = name_lens_full

f['/entry/instrument/AUXincident_light_optics/previous_devices'] =  '/entry/instrument/AUXpolarization_manipulator_1'

# add coordinates via NXtransformaitons
f['/entry/instrument/AUXincident_light_optics'].create_group('location')
f['/entry/instrument/AUXincident_light_optics/location'].attrs['NX_class'] = 'NXtransformations'
f['/entry/instrument/AUXincident_light_optics/location/coordinates'] =  beam_dev_radius[10]
f['/entry/instrument/AUXincident_light_optics/location/coordinates'].attrs['units'] = 'm'
f['/entry/instrument/AUXincident_light_optics/location/coordinates'].attrs['vector'] = np.array([beam_dev_x_unit_vec[10],beam_dev_y_unit_vec[10],0])
f['/entry/instrument/AUXincident_light_optics/location/coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/AUXincident_light_optics/location/coordinates'].attrs['depends_on'] = '.' #



f.create_group('/entry/instrument/AUXscattered_light_optics')
f['/entry/instrument/AUXscattered_light_optics'].attrs['NX_class'] = 'NXbeam_device'

f['/entry/instrument/AUXscattered_light_optics'].attrs['device'] = name_lens_full

f['/entry/instrument/AUXscattered_light_optics/previous_devices'] =  '/entry/instrument/AUXsample_as_beam_element'

# add coordinates via NXtransformaitons
f['/entry/instrument/AUXscattered_light_optics'].create_group('location')
f['/entry/instrument/AUXscattered_light_optics/location'].attrs['NX_class'] = 'NXtransformations'
f['/entry/instrument/AUXscattered_light_optics/location/coordinates'] = beam_dev_radius[10]
f['/entry/instrument/AUXscattered_light_optics/location/coordinates'].attrs['units'] = 'm'
f['/entry/instrument/AUXscattered_light_optics/location/coordinates'].attrs['vector'] = np.array([beam_dev_x_unit_vec[10],beam_dev_y_unit_vec[10],0])
f['/entry/instrument/AUXscattered_light_optics/location/coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/AUXscattered_light_optics/location/coordinates'].attrs['depends_on'] = '.' #


f.create_group('/entry/instrument/AUXopt_detector')
f['/entry/instrument/AUXopt_detector'].attrs['NX_class'] = 'NXbeam_device'

f['/entry/instrument/AUXopt_detector'].attrs['device'] = name_detector_full

f['/entry/instrument/AUXopt_detector/previous_devices'] =  '/entry/instrument/AUXopt_monochromator'



# add coordinates via NXtransformaitons
f['/entry/instrument/AUXopt_detector'].create_group('location')
f['/entry/instrument/AUXopt_detector/location'].attrs['NX_class'] = 'NXtransformations'
f['/entry/instrument/AUXopt_detector/location/coordinates'] = beam_dev_radius[30]
f['/entry/instrument/AUXopt_detector/location/coordinates'].attrs['units'] = 'm'
f['/entry/instrument/AUXopt_detector/location/coordinates'].attrs['vector'] = np.array([beam_dev_x_unit_vec[30],beam_dev_y_unit_vec[30],0])
f['/entry/instrument/AUXopt_detector/location/coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/AUXopt_detector/location/coordinates'].attrs['depends_on'] = '.' #

f.create_group('/entry/instrument/AUXpolarization_manipulator_1')
f['/entry/instrument/AUXpolarization_manipulator_1'].attrs['NX_class'] = 'NXbeam_device'

f['/entry/instrument/AUXpolarization_manipulator_1'].attrs['device'] = name_hwp_1_full

f['/entry/instrument/AUXpolarization_manipulator_1/previous_devices'] =  ['/entry/instrument/Beamsplitter', '/entry/instrument/AUXscattered_light_optics']

# add coordinates via NXtransformaitons
f['/entry/instrument/AUXpolarization_manipulator_1'].create_group('location')
f['/entry/instrument/AUXpolarization_manipulator_1/location'].attrs['NX_class'] = 'NXtransformations'
f['/entry/instrument/AUXpolarization_manipulator_1/location/coordinates'] = beam_dev_radius[12]
f['/entry/instrument/AUXpolarization_manipulator_1/location/coordinates'].attrs['units'] = 'm'
f['/entry/instrument/AUXpolarization_manipulator_1/location/coordinates'].attrs['vector'] = np.array([beam_dev_x_unit_vec[12],beam_dev_y_unit_vec[12],0])
f['/entry/instrument/AUXpolarization_manipulator_1/location/coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/AUXpolarization_manipulator_1/location/coordinates'].attrs['depends_on'] = '.' #


f.create_group('/entry/instrument/AUXpolarization_manipulator_2')
f['/entry/instrument/AUXpolarization_manipulator_2'].attrs['NX_class'] = 'NXbeam_device'

f['/entry/instrument/AUXpolarization_manipulator_2'].attrs['device'] = name_hwp_2_full

f['/entry/instrument/AUXpolarization_manipulator_2/previous_devices'] =  '/entry/instrument/Beamsplitter'

# add coordinates via NXtransformaitons
f['/entry/instrument/AUXpolarization_manipulator_2'].create_group('location')
f['/entry/instrument/AUXpolarization_manipulator_2/location'].attrs['NX_class'] = 'NXtransformations'
f['/entry/instrument/AUXpolarization_manipulator_2/location/coordinates'] = beam_dev_radius[8]
f['/entry/instrument/AUXpolarization_manipulator_2/location/coordinates'].attrs['units'] = 'm'
f['/entry/instrument/AUXpolarization_manipulator_2/location/coordinates'].attrs['vector'] = np.array([beam_dev_x_unit_vec[8],beam_dev_y_unit_vec[8],0])
f['/entry/instrument/AUXpolarization_manipulator_2/location/coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/AUXpolarization_manipulator_2/location/coordinates'].attrs['depends_on'] = '.' #


f.create_group('/entry/instrument/AUXopt_monochromator')
f['/entry/instrument/AUXopt_monochromator'].attrs['NX_class'] = 'NXbeam_device'

f['/entry/instrument/AUXopt_monochromator'].attrs['device'] = name_monochromator_full

f['/entry/instrument/AUXopt_monochromator/previous_devices'] =  '/entry/instrument/MClens'

# add coordinates via NXtransformaitons
f['/entry/instrument/AUXopt_monochromator'].create_group('location')
f['/entry/instrument/AUXopt_monochromator/location'].attrs['NX_class'] = 'NXtransformations'
f['/entry/instrument/AUXopt_monochromator/location/coordinates'] = beam_dev_radius[5]
f['/entry/instrument/AUXopt_monochromator/location/coordinates'].attrs['units'] = 'm'
f['/entry/instrument/AUXopt_monochromator/location/coordinates'].attrs['vector'] = np.array([beam_dev_x_unit_vec[5],beam_dev_y_unit_vec[5],0])
f['/entry/instrument/AUXopt_monochromator/location/coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/AUXopt_monochromator/location/coordinates'].attrs['depends_on'] = '.' #


f.create_group('/entry/instrument/AUXsample_as_beam_element')
f['/entry/instrument/AUXsample_as_beam_element'].attrs['NX_class'] = 'NXbeam_device'

f['/entry/instrument/AUXsample_as_beam_element'].attrs['device'] = name_sample_full

f['/entry/instrument/AUXsample_as_beam_element/previous_devices'] =  '/entry/instrument/AUXscattered_light_optics'

# add coordinates via NXtransformaitons
f['/entry/instrument/AUXsample_as_beam_element'].create_group('location')
f['/entry/instrument/AUXsample_as_beam_element/location'].attrs['NX_class'] = 'NXtransformations'
f['/entry/instrument/AUXsample_as_beam_element/location/coordinates'] = beam_dev_radius[11]
f['/entry/instrument/AUXsample_as_beam_element/location/coordinates'].attrs['units'] = 'm'
f['/entry/instrument/AUXsample_as_beam_element/location/coordinates'].attrs['vector'] = np.array([beam_dev_x_unit_vec[11],beam_dev_y_unit_vec[11],0])
f['/entry/instrument/AUXsample_as_beam_element/location/coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/AUXsample_as_beam_element/location/coordinates'].attrs['depends_on'] = '.' #


# Additional beam Path elements
f.create_group('/entry/instrument/LaserLineFilter')
f['/entry/instrument/LaserLineFilter'].attrs['NX_class'] = 'NXbeam_device'
f['/entry/instrument/LaserLineFilter/previous_devices'] =  '/entry/instrument/AUXopt_source'

# add coordinates via NXtransformaitons
f['/entry/instrument/LaserLineFilter'].create_group('location')
f['/entry/instrument/LaserLineFilter/location'].attrs['NX_class'] = 'NXtransformations'
f['/entry/instrument/LaserLineFilter/location/coordinates'] = beam_dev_radius[28]
f['/entry/instrument/LaserLineFilter/location/coordinates'].attrs['units'] = 'm'
f['/entry/instrument/LaserLineFilter/location/coordinates'].attrs['vector'] = np.array([beam_dev_x_unit_vec[28],beam_dev_y_unit_vec[28],0])
f['/entry/instrument/LaserLineFilter/location/coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/LaserLineFilter/location/coordinates'].attrs['depends_on'] = '.' #



# Additional beam Path elements
f.create_group('/entry/instrument/LensL1_35mm')
f['/entry/instrument/LensL1_35mm'].attrs['NX_class'] = 'NXbeam_device'
f['/entry/instrument/LensL1_35mm/previous_devices'] =  '/entry/instrument/LaserLineFilter'

# add coordinates via NXtransformaitons
f['/entry/instrument/LensL1_35mm'].create_group('location')
f['/entry/instrument/LensL1_35mm/location'].attrs['NX_class'] = 'NXtransformations'
f['/entry/instrument/LensL1_35mm/location/coordinates'] = beam_dev_radius[27]
f['/entry/instrument/LensL1_35mm/location/coordinates'].attrs['units'] = 'm'
f['/entry/instrument/LensL1_35mm/location/coordinates'].attrs['vector'] = np.array([beam_dev_x_unit_vec[27],beam_dev_y_unit_vec[27],0])
f['/entry/instrument/LensL1_35mm/location/coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/LensL1_35mm/location/coordinates'].attrs['depends_on'] = '.' #

f.create_group('/entry/instrument/Pinhole')
f['/entry/instrument/Pinhole'].attrs['NX_class'] = 'NXbeam_device'
f['/entry/instrument/Pinhole/previous_devices'] =  '/entry/instrument/LensL1_35mm'

# add coordinates via NXtransformaitons
f['/entry/instrument/Pinhole'].create_group('location')
f['/entry/instrument/Pinhole/location'].attrs['NX_class'] = 'NXtransformations'
f['/entry/instrument/Pinhole/location/coordinates'] = beam_dev_radius[26]
f['/entry/instrument/Pinhole/location/coordinates'].attrs['units'] = 'm'
f['/entry/instrument/Pinhole/location/coordinates'].attrs['vector'] = np.array([beam_dev_x_unit_vec[26],beam_dev_y_unit_vec[26],0])
f['/entry/instrument/Pinhole/location/coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/Pinhole/location/coordinates'].attrs['depends_on'] = '.' #

f.create_group('/entry/instrument/LensL2_130mm')
f['/entry/instrument/LensL2_130mm'].attrs['NX_class'] = 'NXbeam_device'
f['/entry/instrument/LensL2_130mm/previous_devices'] =  '/entry/instrument/Pinhole'
# add coordinates via NXtransformaitons
f['/entry/instrument/LensL2_130mm'].create_group('location')
f['/entry/instrument/LensL2_130mm/location'].attrs['NX_class'] = 'NXtransformations'
f['/entry/instrument/LensL2_130mm/location/coordinates'] = beam_dev_radius[25]
f['/entry/instrument/LensL2_130mm/location/coordinates'].attrs['units'] = 'm'
f['/entry/instrument/LensL2_130mm/location/coordinates'].attrs['vector'] = np.array([beam_dev_x_unit_vec[25],beam_dev_y_unit_vec[25],0])
f['/entry/instrument/LensL2_130mm/location/coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/LensL2_130mm/location/coordinates'].attrs['depends_on'] = '.' #


f.create_group('/entry/instrument/Mirror1')
f['/entry/instrument/Mirror1'].attrs['NX_class'] = 'NXbeam_device'
f['/entry/instrument/Mirror1/previous_devices'] =  '/entry/instrument/LensL2_130mm'

# add coordinates via NXtransformaitons
f['/entry/instrument/Mirror1'].create_group('location')
f['/entry/instrument/Mirror1/location'].attrs['NX_class'] = 'NXtransformations'
f['/entry/instrument/Mirror1/location/coordinates'] = beam_dev_radius[14]
f['/entry/instrument/Mirror1/location/coordinates'].attrs['units'] = 'm'
f['/entry/instrument/Mirror1/location/coordinates'].attrs['vector'] = np.array([beam_dev_x_unit_vec[14],beam_dev_y_unit_vec[14],0])
f['/entry/instrument/Mirror1/location/coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/Mirror1/location/coordinates'].attrs['depends_on'] = '.' #

f.create_group('/entry/instrument/Beamsplitter')
f['/entry/instrument/Beamsplitter'].attrs['NX_class'] = 'NXbeam_device'
f['/entry/instrument/Beamsplitter/previous_devices'] =  ['/entry/instrument/Mirror1', '/entry/instrument/AUXpolarization_manipulator_1']


# add coordinates via NXtransformaitons
f['/entry/instrument/Beamsplitter'].create_group('location')
f['/entry/instrument/Beamsplitter/location'].attrs['NX_class'] = 'NXtransformations'
f['/entry/instrument/Beamsplitter/location/coordinates'] = beam_dev_radius[9]
f['/entry/instrument/Beamsplitter/location/coordinates'].attrs['units'] = 'm'
f['/entry/instrument/Beamsplitter/location/coordinates'].attrs['vector'] = np.array([beam_dev_x_unit_vec[9],beam_dev_y_unit_vec[9],0])
f['/entry/instrument/Beamsplitter/location/coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/Beamsplitter/location/coordinates'].attrs['depends_on'] = '.' #


f.create_group('/entry/instrument/Mirror2')
f['/entry/instrument/Mirror2'].attrs['NX_class'] = 'NXbeam_device'
f['/entry/instrument/Mirror2/previous_devices'] =  '/entry/instrument/spectral_filter_EdgeFilter'

# add coordinates via NXtransformaitons
f['/entry/instrument/Mirror2'].create_group('location')
f['/entry/instrument/Mirror2/location'].attrs['NX_class'] = 'NXtransformations'
f['/entry/instrument/Mirror2/location/coordinates'] = beam_dev_radius[2]
f['/entry/instrument/Mirror2/location/coordinates'].attrs['units'] = 'm'
f['/entry/instrument/Mirror2/location/coordinates'].attrs['vector'] = np.array([beam_dev_x_unit_vec[2],beam_dev_y_unit_vec[2],0])
f['/entry/instrument/Mirror2/location/coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/Mirror2/location/coordinates'].attrs['depends_on'] = '.' #

f.create_group('/entry/instrument/MClens')
f['/entry/instrument/MClens'].attrs['NX_class'] = 'NXbeam_device'
f['/entry/instrument/MClens/previous_devices'] =  '/entry/instrument/Mirror2'

# add coordinates via NXtransformaitons
f['/entry/instrument/MClens'].create_group('location')
f['/entry/instrument/MClens/location'].attrs['NX_class'] = 'NXtransformations'
f['/entry/instrument/MClens/location/coordinates'] = beam_dev_radius[4]
f['/entry/instrument/MClens/location/coordinates'].attrs['units'] = 'm'
f['/entry/instrument/MClens/location/coordinates'].attrs['vector'] = np.array([beam_dev_x_unit_vec[4],beam_dev_y_unit_vec[4],0])
f['/entry/instrument/MClens/location/coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/MClens/location/coordinates'].attrs['depends_on'] = '.' #



f.create_group('/entry/instrument/' + name_source)
f[path_source_full].attrs['NX_class'] = 'NXsource'


f[path_source_full+'/name'] = 'Coherent Compass 315M'
#f[path_source_full+'/name'].attrs['short_name'] = 'NXsource'

f[path_source_full+'/type'] = 'laser'

f[path_source_full+'/probe'] = 'visible light'

f[path_source_full+'/power'] = 100
f[path_source_full+'/power'].attrs['NX_class'] = 'NX_FLOAT'
f[path_source_full+'/power'].attrs['unit'] = 'mW'

f[path_source_full+'/wavelength'] = 532
f[path_source_full+'/wavelength'].attrs['NX_class'] = 'NX_WAVELENGTH'
f[path_source_full+'/wavelength'].attrs['unit'] = 'nm'

f[path_source_full+'/associated_beam'] = '/entry/instrument/beam_laser_source'



f.create_group(path_source_full + '/device_information')
f[path_source_full + '/device_information'].attrs['NX_class'] = 'NXfabrication'

f[path_source_full + '/device_information/vendor'] = 'Coherent, Inc.'
f[path_source_full + '/device_information/model'] = 'Compass(TM) 315M'

#f.create_group(path_source_full + '/device_characteristics')
#f[path_source_full + '/device_characteristics'].attrs['NX_class'] = 'NXdata'

#f[path_source_full + '/device_characteristics/model'] = 'Compass(TM) 315M'




if False:
    df4=pd.read_csv("laser_line_measurement_532nm.txt",delimiter="\t",header=None)
    data_laser_distrib_wavelength = (df4.iloc[0:,int(0)]).to_numpy()
    data_laser_distrib_counts = (df4.iloc[0:,int(1)]).to_numpy()#/2.5

    f[path_source_full+'/distribution'] = np.array([data_laser_distrib_wavelength,data_laser_distrib_counts])
    f[path_source_full+'/distribution'].attrs['NX_class'] = 'NXdata'
    f[path_source_full+'/distribution'].attrs['unit'] = ['nm','cts']


simple_data=np.transpose(np.loadtxt("raman_data_for_nexus_file/laser_line_measurement_532nm_short.txt",  delimiter="\t"))[1]
laserline_int_signal =np.transpose(np.loadtxt("raman_data_for_nexus_file/laser_line_measurement_532nm_short.txt",  delimiter="\t"))[1]
wavelength_axes = np.transpose(np.loadtxt("raman_data_for_nexus_file/laser_line_measurement_532nm_short.txt",  delimiter="\t"))[0]


f.create_group(path_source_full + '/device_characteristics')
f[path_source_full + '/device_characteristics'].attrs['NX_class'] = 'NXdata'
f[path_source_full+'/device_characteristics/name'] = 'Spectral intensity distribution'
f[path_source_full+'/device_characteristics/wavelength'] = wavelength_axes
f[path_source_full+'/device_characteristics/wavelength'].attrs['long_name'] = 'Wavelength [nm]'
f[path_source_full+'/device_characteristics/intensity'] = laserline_int_signal
f[path_source_full+'/device_characteristics/intensity'].attrs['signal'] = 'intensity'
f[path_source_full+'/device_characteristics/intensity'].attrs['axes'] = 'wavelength'
f[path_source_full+'/device_characteristics/intensity'].attrs['long_name'] = 'Intensity [cts]'

f[path_source_full+'/device_characteristics/temperature'] = np.ones(len(wavelength_axes))
f[path_source_full+'/device_characteristics/temperature'].attrs['signal'] = 'temperature'


f.create_group('/entry/instrument/' + name_detector)
f[name_detector_full].attrs['NX_class'] = 'NXdetector'

f[name_detector_full+'/detector_channel_type'] = 'multichannel'

f[name_detector_full+'/detector_type'] = 'CCD'

f[name_detector_full+'/description'] = 'Symphony 2048 x 512 Cryogenic Back Illuminated UV Sensitive CCD Detector'
f[name_detector_full+'/x_pixel_size'] = 13.5
f[name_detector_full+'/x_pixel_size'].attrs['unit'] = 'µm'
f[name_detector_full+'/y_pixel_size'] = 13.5
f[name_detector_full+'/y_pixel_size'].attrs['unit'] = 'µm'

f.create_group(name_detector_full + '/device_characteristics')
f[name_detector_full + '/device_characteristics'].attrs['NX_class'] = 'NXdata'


#simple_data=np.transpose(np.loadtxt("laser_line_measurement_532nm_short.txt",  delimiter="\t"))[1]
det_eff =np.transpose(np.loadtxt("raman_data_for_nexus_file/detector_efficiency_vs_wavelength.txt",  delimiter="\t"))[1]
det_wavelength =np.transpose(np.loadtxt("raman_data_for_nexus_file/detector_efficiency_vs_wavelength.txt",  delimiter="\t"))[0]


f[name_detector_full+'/device_characteristics/wavelength'] = det_wavelength
f[name_detector_full+'/device_characteristics/wavelength'].attrs['long_name'] = 'Wavelength [nm]'
f[name_detector_full+'/device_characteristics/name'] = 'Average pixel quantum efficiency - Wavelength dependent'
f[name_detector_full+'/device_characteristics/QE'] = det_eff
f[name_detector_full+'/device_characteristics/QE'].attrs['signal'] = 'QE'
f[name_detector_full+'/device_characteristics/QE'].attrs['axes'] = 'wavelength'
f[name_detector_full+'/device_characteristics/QE'].attrs['long_name'] = 'Quantum Efficiency'

f.create_group(name_detector_full + '/device_information')
f[name_detector_full + '/device_information'].attrs['NX_class'] = 'NXfabrication'

f[name_detector_full + '/device_information/vendor'] = 'Jobin Yvon'
f[name_detector_full + '/device_information/model'] = 'Symphony BI UV CCD'



f.create_group(name_detector_full + '/raw_data')
f[name_detector_full + '/raw_data'].attrs['NX_class'] = 'NXdata'

f[name_detector_full + '/raw_data/note'] = 'The raw data is intended to be located here. This is not shown in this example file.'



f.create_group('/entry/instrument/' + name_monochromator)
f[name_monochromator_full].attrs['NX_class'] = 'NXmonochromator'


f.create_group(name_monochromator_full + '/device_characteristics')
f[name_monochromator_full + '/device_characteristics'].attrs['NX_class'] = 'NXdata'

#simple_data=np.transpose(np.loadtxt("laser_line_measurement_532nm_short.txt",  delimiter="\t"))[1]
grating_refl =np.transpose(np.loadtxt("raman_data_for_nexus_file/grating_reflectivity.txt",  delimiter="\t"))[1]
grating_wavelength =np.transpose(np.loadtxt("raman_data_for_nexus_file/grating_reflectivity.txt",  delimiter="\t"))[0]


f[name_monochromator_full+'/device_characteristics/wavelength'] = grating_wavelength
f[name_monochromator_full+'/device_characteristics/wavelength'].attrs['long_name'] = 'Wavelength [nm]'
f[name_monochromator_full+'/device_characteristics/refl'] = grating_refl
f[name_monochromator_full+'/device_characteristics/name'] = 'Horizontal polarized grating reflection efficiency'
f[name_monochromator_full+'/device_characteristics/refl'].attrs['signal'] = 'refl'
f[name_monochromator_full+'/device_characteristics/refl'].attrs['axes'] = 'wavelength'
f[name_monochromator_full+'/device_characteristics/refl'].attrs['long_name'] = 'Reflectivity'


f.create_group(name_monochromator_full + '/device_characteristics2')
f[name_monochromator_full + '/device_characteristics2'].attrs['NX_class'] = 'NXdata'

#simple_data=np.transpose(np.loadtxt("laser_line_measurement_532nm_short.txt",  delimiter="\t"))[1]
grating_refl =np.transpose(np.loadtxt("raman_data_for_nexus_file/grating_reflectivity_vertical.txt",  delimiter="\t"))[1]
grating_wavelength =np.transpose(np.loadtxt("raman_data_for_nexus_file/grating_reflectivity_vertical.txt",  delimiter="\t"))[0]


f[name_monochromator_full+'/device_characteristics2/wavelength'] = grating_wavelength
f[name_monochromator_full+'/device_characteristics2/wavelength'].attrs['long_name'] = 'Wavelength [nm]'
f[name_monochromator_full+'/device_characteristics2/refl'] = grating_refl
f[name_monochromator_full+'/device_characteristics2/name'] = 'Horizontal polarized grating reflection efficiency'
f[name_monochromator_full+'/device_characteristics2/refl'].attrs['signal'] = 'refl'
f[name_monochromator_full+'/device_characteristics2/refl'].attrs['axes'] = 'wavelength'
f[name_monochromator_full+'/device_characteristics2/refl'].attrs['long_name'] = 'Reflectivity'







f.create_group('/entry/instrument/incident_light_lens')
f['/entry/instrument/incident_light_lens'].attrs['NX_class'] = 'NXlens_opt'
f['/entry/instrument/incident_light_lens/lens_diameter'] = 3
f['/entry/instrument/incident_light_lens/lens_diameter'].attrs['unit'] = 'mm'

f.create_group('/entry/instrument/incident_light_lens/substrate')
f['/entry/instrument/incident_light_lens/substrate'].attrs['NX_class'] = 'NXsample'

f['/entry/instrument/incident_light_lens/substrate/substrate_material'] = 'CaF2'

f.create_group('/entry/instrument/incident_light_lens/device_information')
f['/entry/instrument/incident_light_lens/device_information'].attrs['NX_class'] = 'NXdata'

obj_transm =np.transpose(np.loadtxt("raman_data_for_nexus_file/transmission_mitutoyo_obj.txt",  delimiter="\t"))[1]
obj_wavelength =np.transpose(np.loadtxt("raman_data_for_nexus_file/transmission_mitutoyo_obj.txt",  delimiter="\t"))[0]


f['/entry/instrument/incident_light_lens/device_information/wavelength'] = obj_wavelength
f['/entry/instrument/incident_light_lens/device_information/wavelength'].attrs['long_name'] = 'Wavelength [nm]'
f['/entry/instrument/incident_light_lens/device_information/transm'] = obj_transm
f['/entry/instrument/incident_light_lens/device_information/name'] = 'Spectral transmission'
f['/entry/instrument/incident_light_lens/device_information/transm'].attrs['signal'] = 'transm'
f['/entry/instrument/incident_light_lens/device_information/transm'].attrs['axes'] = 'wavelength'
f['/entry/instrument/incident_light_lens/device_information/transm'].attrs['long_name'] = 'Transmission'






f['/entry/instrument/incident_light_lens/type'] = 'objective'

f['/entry/instrument/incident_light_lens/numerical_aperture'] = 0.42
f['/entry/instrument/incident_light_lens/numerical_aperture'].attrs['NX_class'] = 'NX_NUMBER'


f['/entry/instrument/incident_light_lens/magnification'] = 50
f['/entry/instrument/incident_light_lens/magnification'].attrs['NX_class'] = 'NX_NUMBER'




f.create_group('/entry/instrument/scattered_light_lens')
f['/entry/instrument/scattered_light_lens'].attrs['NX_class'] = 'NXlens_opt'

f['/entry/instrument/scattered_light_lens/type'] = 'objective'

f['/entry/instrument/scattered_light_lens/numerical_aperture'] = 0.42
f['/entry/instrument/scattered_light_lens/numerical_aperture'].attrs['NX_class'] = 'NX_NUMBER'


f['/entry/instrument/scattered_light_lens/magnification'] = 50
f['/entry/instrument/scattered_light_lens/magnification'].attrs['NX_class'] = 'NX_NUMBER'





f.create_group('/entry/instrument/waveplate_1')
f['/entry/instrument/waveplate_1'].attrs['NX_class'] = 'NXwaveplate'

f['/entry/instrument/waveplate_1/type'] = 'zero-order waveplate'

f['/entry/instrument/waveplate_1/retardance'] = 'half-wave plate'

f['/entry/instrument/waveplate_1/wavelengths'] = 532
f['/entry/instrument/waveplate_1/wavelengths'].attrs['units'] = 'nm'

f['/entry/instrument/waveplate_1/diameter'] = 15
f['/entry/instrument/waveplate_1/diameter'].attrs['units'] = 'mm'

f.create_group('/entry/instrument/waveplate_2')
f['/entry/instrument/waveplate_2'].attrs['NX_class'] = 'NXwaveplate'

f['/entry/instrument/waveplate_2/type'] = 'achromatic waveplate'

f['/entry/instrument/waveplate_2/retardance'] = 'half-wave plate'

f['/entry/instrument/waveplate_2/wavelengths'] = np.array([720,450])
f['/entry/instrument/waveplate_2/wavelengths'].attrs['units'] = 'nm'

f['/entry/instrument/waveplate_2/diameter'] = 15
f['/entry/instrument/waveplate_2/diameter'].attrs['units'] = 'mm'




f.create_group('/entry/instrument/polarization_filter')
f['/entry/instrument/polarization_filter'].attrs['NX_class'] = 'NXbeam_device'


f['/entry/instrument/polarization_filter/filter_mechanism'] = 'Birefringent polarizers'
f['/entry/instrument/polarization_filter/specific_polarization_filter_type'] = 'Glan-Thompson'

f['/entry/instrument/polarization_filter/previous_devices'] =  '/entry/instrument/AUXpolarization_manipulator_2'

# add coordinates via NXtransformaitons
f['/entry/instrument/polarization_filter'].create_group('location')
f['/entry/instrument/polarization_filter/location'].attrs['NX_class'] = 'NXtransformations'
f['/entry/instrument/polarization_filter/location/coordinates'] = beam_dev_radius[7]
f['/entry/instrument/polarization_filter/location/coordinates'].attrs['units'] = 'm'
f['/entry/instrument/polarization_filter/location/coordinates'].attrs['vector'] = np.array([beam_dev_x_unit_vec[7],beam_dev_y_unit_vec[7],0])
f['/entry/instrument/polarization_filter/location/coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/polarization_filter/location/coordinates'].attrs['depends_on'] = '.' #




f.create_group('/entry/instrument/spectral_filter_EdgeFilter')
f['/entry/instrument/spectral_filter_EdgeFilter'].attrs['NX_class'] = 'NXbeam_device'


f['/entry/instrument/spectral_filter_EdgeFilter/filter_type'] = 'long-pass filter'


f['/entry/instrument/spectral_filter_EdgeFilter/intended_use'] = 'raylight line removal'
f['/entry/instrument/spectral_filter_EdgeFilter/intended_use_freetext'] = 'Remove raylight scattered and reflected laser light to avoid intense straylight on the CCD.'

# fill in later transmission characteristics
#f['/entry/instrument/spectral_filter_EdgeFilter/filter_characteristics'] = np.transpose(np.array([[3],[2]]))

f['/entry/instrument/spectral_filter_EdgeFilter/previous_devices'] =  '/entry/instrument/polarization_filter'

# add coordinates via NXtransformaitons
f['/entry/instrument/spectral_filter_EdgeFilter'].create_group('location')
f['/entry/instrument/spectral_filter_EdgeFilter/location'].attrs['NX_class'] = 'NXtransformations'
f['/entry/instrument/spectral_filter_EdgeFilter/location/coordinates'] = beam_dev_radius[6]
f['/entry/instrument/spectral_filter_EdgeFilter/location/coordinates'].attrs['units'] = 'm'
f['/entry/instrument/spectral_filter_EdgeFilter/location/coordinates'].attrs['vector'] = np.array([beam_dev_x_unit_vec[6],beam_dev_y_unit_vec[6],0])
f['/entry/instrument/spectral_filter_EdgeFilter/location/coordinates'].attrs['transformation_type'] = 'translation'
f['/entry/instrument/spectral_filter_EdgeFilter/location/coordinates'].attrs['depends_on'] = '.' #



















f.create_group('/entry/silicon_substrate/')
f['/entry/silicon_substrate'].attrs['NX_class'] = 'NXsample'


f['/entry/silicon_substrate/sample_name'] = name_sample
f['/entry/silicon_substrate/physical_form'] = 'single crystal substrate'
f['/entry/silicon_substrate/chemical_formula'] = 'Si'
f['/entry/silicon_substrate/description'] = 'This is a simple silicon substrate used to demonstrate a default Raman dataset.'
f['/entry/silicon_substrate/atom_types'] = 'Si'

f.create_group('/entry/silicon_substrate/history')
f['/entry/silicon_substrate/history'].attrs['NX_class'] = 'NXhistory'

f['/entry/silicon_substrate/history/notes'] = 'This sample was bought commercially. Its a broken part of a 111-oriented wafer.'


f.create_group('/entry/silicon_substrate/temperature')
f['/entry/silicon_substrate/temperature'].attrs['NX_class'] = 'NXenvironment'

f['/entry/silicon_substrate/temperature/name'] = 'Sample temperature estimation'

f.create_group('/entry/silicon_substrate/temperature/digital_thermometer')
f['/entry/silicon_substrate/temperature/digital_thermometer'].attrs['NX_class'] = 'NXsensor'

f['/entry/silicon_substrate/temperature/digital_thermometer/value'] = 23
f['/entry/silicon_substrate/temperature/digital_thermometer/value'].attrs['unit'] = '°C'



f.create_group('/entry/silicon_substrate/environment')
f['/entry/silicon_substrate/environment'].attrs['NX_class'] = 'NXenvironment'

f['/entry/silicon_substrate/environment/name'] = 'Atmospheric conditions'
f['/entry/silicon_substrate/environment/sample_medium'] = 'air'

f['/entry/silicon_substrate/thickness'] = '500'
f['/entry/silicon_substrate/thickness'].attrs['unit'] = 'µm'

f['/entry/silicon_substrate/thickness_determination'] = 'Vendor specification'

f['/entry/silicon_substrate/layer_structure'] = 'Silicon substrate with intrinsic oxide layer of about 2nm'

#2024-04-15T12:08:08+00:00 
#+01



#Si_532_spalt100_t180_akku1_z(unpol)z_80wn1300_2267





#f.create_group('/entry/start_time/')
#f['/entry/start_time'].attrs['NX_class'] = 'NX_DATE_TIME'

f['/entry/start_time'] = '2022-06-10T20:13:18+02' # only a string now - how to implement ISO8601 time stamp in hdf5?
f['/entry/start_time'].attrs['NX_class'] = 'NX_DATE_TIME'

#f['/entry/instrument/scattering_configuration'] = 'z(xx)z'
#f['/entry/instrument/scattering_configuration'].attrs['NX_class'] = 'NX_CHAR'



f.create_group('/entry/user/')
f['/entry/user'].attrs['NX_class'] = 'NXuser'

f['/entry/user/name'] = 'Ron Hildebrandt'
f['/entry/user/role'] = 'PhD Student / Experimentator'
f['/entry/user/affiliation'] = 'Leipzig University'
f['/entry/user/address'] = 'Linnéstraße 5, 04103 Leipzig, Germany'
f['/entry/user/email'] = 'ron.hildebrandt@physik.uni-leipzig.de'
f['/entry/user/telephone_number'] = '+49 341 97 32615'

f.create_group('/entry/user/identifier_1')
f['/entry/user/identifier_1'].attrs['NX_class'] = 'NXidentifier'

f['/entry/user/identifier_1/service'] = 'ORCID'
f['/entry/user/identifier_1/idenfitier'] = 'https://orcid.org/0000-0001-6932-604X'
f['/entry/user/identifier_1/is_persistent'] = 'TRUE'



f.create_group('/entry/raman_spectrum_raw_data/')
f['/entry/raman_spectrum_raw_data'].attrs['NX_class'] = 'NXdata'

raman_spec_int =np.transpose(np.loadtxt("raman_data_for_nexus_file/Si_532_spalt100_t180_akku1_z(unpol)z_80wn1300_2267.txt",  delimiter="\t"))[1]
raman_spec_wavenumber =np.transpose(np.loadtxt("raman_data_for_nexus_file/Si_532_spalt100_t180_akku1_z(unpol)z_80wn1300_2267.txt",  delimiter="\t"))[0]



f['/entry/raman_spectrum_raw_data/data_type'] = 'CCD integrated single spectrum'


f['/entry/raman_spectrum_raw_data/raman_shift'] = raman_spec_wavenumber
f['/entry/raman_spectrum_raw_data/raman_shift'].attrs['long_name'] = 'Raman Shift [cm-1]'
f['/entry/raman_spectrum_raw_data/raman_int'] = raman_spec_int
f['/entry/raman_spectrum_raw_data/raman_int'].attrs['signal'] = 'raman_int'
f['/entry/raman_spectrum_raw_data/raman_int'].attrs['axes'] = 'raman_shift'
f['/entry/raman_spectrum_raw_data/raman_int'].attrs['long_name'] = 'Intensity [cts]'


f.create_group('/entry/measurement_data_calibration/')
f['/entry/measurement_data_calibration'].attrs['NX_class'] = 'NXprocess'

f['/entry/measurement_data_calibration/note'] = 'Here calibrated data can be stored, which could replace the default data plot of the NeXus file.'
f['/entry/measurement_data_calibration/note'].attrs['NX_class'] = 'NXnote'



f.create_group('/entry/derived_parameters/')
f['/entry/derived_parameters'].attrs['NX_class'] = 'NXprocess'


f['/entry/derived_parameters/note'] = 'Here mathematical methods or operations can be stored to extract or process the measurement data. By this for example the peak position, width and center could be stored with a simple lorentzian oscillator model.'
f['/entry/derived_parameters/note'].attrs['NX_class'] = 'NXnote'

