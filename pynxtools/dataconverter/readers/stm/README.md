# STM/STS reader
## Contact persion in FAIRmat for this reader
**Rubel Mozumder (mozumder@physik.hu-berlin.de)**
## Reader Notes:
- Reader builds on NXiv_sweep2
- Can parse bias spectroscopy (STS) from
    - Nanonis: Generic 5e, 
- Can parse STM from
    - Nanonis: Generic 5e

## Some usages:
- The data structure of the input data file can be investigate with the code below:
    ```
        from pynxtools.dataconverter.readers.stm.stm_file_parser import get_stm_raw_file_info
        from pynxtools.dataconverter.readers.stm.bias_spec_file_parser import get_sts_raw_file_info

        # for stm (.sxm) file
        get_stm_raw_file_info('TiSe2_2303a_annealing_300C_5min_evaporate_Pyrene_1_0070.sxm')

        # for sts (.dat) file
        get_sts_raw_file_info('221122_Au_5K00014_from_Palma_team.dat')
    ```
- To run STM reaader use the folowing code
    ```
    # Run STM reader

    !dataconverter \
    --reader stm \
    --nxdl NXiv_sweep2 \
    --input-file TiSe2_2303a_annealing_300C_5min_evaporate_Pyrene_1_0070.sxm \
    --input-file ../config_file_for_sxm.json \
    --input-file ./Nanonis_Eln.yaml \
    --output final_stm_dev_.nxs

    ```
- Run STS reader with
    ```
    # Run STS reader

    !dataconverter \
    --reader stm \
    --nxdl NXiv_sweep2 \
    --input-file ./Bias-Spectroscopy00026_Au_mica_2023_Y_A_diPAMY_154-211C_370C_1min_385C_30min_400C_1min_400C_30min_415_30min_430_30min_11min_20230418.dat \
    --input-file ../config_file_for_dat.json \
    --input-file Nanonis_Eln.yaml \
    --output ./final_sts_dev.nxs
    ```
    
- Utilization of ELN
    - The structure of is Hierarchical type, a small part of eln as follows-
        ``` 
         Instrument:
          Environment:
            position:
              x:
                value: null
                unit: null
              y:
                value: null
                unit: null
        ```
     - To add any extra field please follow correct Hierarchy according to application definition NXiv_sweep2. 
       For example, extend dimension of position
         `````` 
          Instrument:
          Environment:
            position:
              x:
                value: <value>
                unit: <physical unit>
              y:
                value: <value>
                unit: <physical unit>
              z:
                value: <value>
                unit: <physical unit>
        ```
    