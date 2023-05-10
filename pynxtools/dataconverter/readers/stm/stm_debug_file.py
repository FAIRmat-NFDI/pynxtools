from pynxtools.dataconverter.readers.stm.bias_spec_data_parser import BiasSpectData
import os

if __name__ == "__main__":
    file_NAME = ('/home/rubel/Nomad-FAIRmat/NomadGH/GH_Clone/pynxtools/pynxtools/dataconverter/readers/stm/SPM_data_folder/'
                 'copy_Bias-Spectroscopy00026_Au_mica_2023_Y_A_diPAMY_154-211C_370C_1min_385C_30min_400C_1min_400C_30min_415_30min_430_30min_11min_20230418.dat')
    if os.path.isfile(file_NAME):
        b_s = BiasSpectData(file_NAME)
        b_s.get_data_nested_dict()
    else:
        print('Check for correct file')
