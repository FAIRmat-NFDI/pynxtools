# STM/STS reader
## Contact persion in FAIRmat for this reader
**Rubel Mozumder (mozumder@physik.hu-berlin.de)**
## Reader Notes:
- Reader builds on NXiv_sweep2
- Can parse bias spectroscopy (STS) from
    - Nanonis: Generic 5e, Generic 4.5
- Can parse STM from
    - Nanonis: Generic 5e, Generic 4.5

## Some usages:
- The data structure of the input data file can be investigate with the code below:
    ```
        from pynxtools.dataconverter.readers.stm import get_stm_raw_file_info
        from pynxtools.dataconverter.readers.stm import get_sts_raw_file_info

        # for stm (.sxm) file
        get_stm_raw_file_info('STM_nanonis_generic_5e.sxm')

        # for sts (.dat) file
        get_sts_raw_file_info('STS_nanonis_generic_5e_1.dat')
    ```
- To run STM reaader use the folowing code
    ```
    # Run STM reader

    !dataconverter \
    --reader stm \
    --nxdl NXiv_sweep2 \
    --input-file STM_nanonis_generic_5e.sxm \
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
    --input-file ./STS_nanonis_generic_5e_1.dat \
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
        ```
        sub_sections:
          Environment:
            section:
              m_annotations:
                eln:
                  overview: true
              quantities:
                ...
            sub_sections:
              position:
                section:
                  m_annotations:
                    eln:
                      overview: true
                  quantities:
                    x:
                      type: np.float64
                      value: <value>
                      unit: m
                      m_annotations:
                        eln:
                          component: NumberEditQuantity
                          defaultDisplayUnit: <No Default unit>
                      description: |
                        The scanning area in x position in the frame. (e.g. -890.53E-12) '
                    y:
                      type: np.float64
                      value: <value>
                      unit: m
                      m_annotations:
                        eln:
                          component: NumberEditQuantity
                          defaultDisplayUnit: m
                      description: |
                        The scanning area in y position in the frame. (e.g. 29.6968E-9) '
                    z:
                      type: np.float64
                      value: <value>
                      unit: m
                      m_annotations:
                        eln:
                          component: NumberEditQuantity
                          defaultDisplayUnit: m
                      description: |
                        The scanning area in x position in the frame. (e.g. 130.5E-9).

        ```
