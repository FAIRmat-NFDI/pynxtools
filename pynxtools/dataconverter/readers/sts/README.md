# STS reader
***Note: Though the reader name is STS reader it also supports STM experiment species. This is the first version of the reader according to the NeXus application definition [NXsts](https://github.com/FAIRmat-NFDI/nexus_definitions/blob/fairmat/contributed_definitions/NXsts.nxdl.xml) which is a generic template of concepts' definition for STS and STM experiments. Later on, the application definitions and readers specific to the STM, STS and AFM will be available. To stay upto date keep visiting this page time to time. From now onwards we will mention STS referring both STM and STS.***

The prime purpose of the reader is to transform lab-defined data into community-defined concepts constructed by the SPM community which allows experimentalists to store, organize, search, analyze, and share experiments data (only with the help of NOMAD) within the scientific community. To utilize the reader one needs a data file from the experiment, a config file (to connect concepts and raw data from the experimental data file), and an eln file (to add user-defined data that does not come along the experimental data file).
## Contact persion in FAIRmat for this reader
**Rubel Mozumder (mozumder@physik.hu-berlin.de)**
## Reader Notes:
- Reader builds on [NXsts](https://github.com/FAIRmat-NFDI/nexus_definitions/blob/fairmat/contributed_definitions/NXsts.nxdl.xml) application definition
- Needs an experimental file, a config file and a eln file
- Can parse Scanning Tunneling Spectroscopy (STS) from
    - Nanonis: Generic 5e, Generic 4.5
- Can parse Scanning Tunneling Microscopy (STM) from
    - Nanonis: Generic 5e, Generic 4.5

## Some usages:
- The data structure of the input data file can be investigate with the code below:
    ```
        from pynxtools.dataconverter.readers.sts import get_stm_raw_file_info
        from pynxtools.dataconverter.readers.sts import get_sts_raw_file_info

        # for stm (.sxm) file
        get_stm_raw_file_info('STM_nanonis_generic_5e.sxm')

        # for sts (.dat) file
        get_sts_raw_file_info('STS_nanonis_generic_5e_1.dat')
    ```
It returns a text file in working directory.

- To run STS reaader for STM experiment file using the following code
    ```
    # Run STM reader

    !dataconverter \
    --reader sts \
    --nxdl NXsts \
    --input-file STM_nanonis_generic_5e.sxm \
    --input-file ../config_file_for_sxm.json \
    --input-file ./Nanonis_Eln.yaml \
    --output final_stm_dev_.nxs
    ```

- Run STS reader for STS experiment file using the following code
    ```
    # Run STS reader

    !dataconverter \
    --reader sts \
    --nxdl NXsts \
    --input-file ./STS_nanonis_generic_5e_1.dat \
    --input-file ../config_file_for_dat.json \
    --input-file Nanonis_Eln.yaml \
    --output ./final_sts_dev.nxs
    ```

- Utilization of ELN:

  Users are free two types of elns with extension `.yaml` and `.scheme.archive.yaml`, the first one does not mention data type but the second one does. While using the first one, usres are responsible to use correct data from from application definition while the second one illustrate the data type. To add any extra or user difined fields, the eln can be used following the correct hierarchy.
    - The structure of the eln_data.yaml (must be consistent with concepts Hierarchy according
    to the NXsts application definition.)
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
     - The structure of the scheme eln (e.g. eln.scheme.archive.yaml) any extra field please follow correct Hierarchy according to application definition NXsts.
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
## Config file:
- To update (if needed) the config file please follow the rules:
  - The dictionary in config files have the following meaning?
    ```
    "/ENTRY[entry]/INSTRUMENT[instrument]/lock_in/harmonic_order_N": {"D1": {"value": "/Lock-in/Harmonic D1/value"},
                                                                      "D2": {"value": "/Lock-in/Harmonic D2/value"}},
    ```
    Here, the `N` in field `harmonic_order_N`, can be considered as the name of dimensions, can be replaced by `D1` and `D2` to  write two `harmonic_order`.
  - List for the same concept
    ```
    "/ENTRY[entry]/INSTRUMENT[instrument]/piezo_config/active_calib": ["/Piezo Configuration/Active Calib.",
                                                                       "/Piezo Calibration/Active Calib."],
    ```
    For different type of software versions the raw data path could be different for the same
    concept. For example, Nanonis software `generic 5e` has `/Piezo Configuration/Active Calib.`
    and generic 4.5 has `/Piezo Calibration/Active Calib.` for the same concept `/ENTRY[entry]/INSTRUMENT[instrument]/piezo_config/active_calib`.
