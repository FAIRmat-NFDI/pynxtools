#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ##MK add license

"""Parse LibreCalc/Excel table into JSON template dictionary."""

import json

import pandas as pd

import numpy as np

# create a json dictionary with all those entries of the NXDL
# for which the metadata/data can not be extracted from files but
# need to be specified by other means (e.g. human, control software,
# external databases)

# MYPREFIX='C:/Users/kuehbacm/Research/HU_HU_HU/FAIRmatSoftwareDevelopment/Sprint05/'
# sys.path.append(MYPREFIX)
PREFIX = ''
TESTFILE = 'NXapm.nxdl.Template.InformationSources.ods'

DEFAULTS = {'NX_FLOAT': 0.,
            'NX_CHAR': 'specify',
            'NX_INT': 0,
            'NX_UINT': 0,
            'NX_POSINT': 0,
            'NX_BOOLEAN': False,
            'NX_NUMBER': 0,
            'NX_DATE_TIME': '2009-06-30T18:30:00+02:00'}

# NEW ISSUE: make this a function call and become integrated into the apm reader


def ods_to_json_metadata_template(file_name):
    """Parse LibreCalc/Excel table into JSON template dictionary."""
    # file_name = PREFIX + TESTFILE
    tmp = pd.read_excel(file_name, sheet_name='Sheet1', engine="odf",
                        skiprows=2, keep_default_na=False, na_values=['_'])

    other_data_sources = {}
    vendor_files_sources = {}

    for rowidx in np.arange(0, tmp.shape[0]):
        nxdl_dtype = tmp.iloc[rowidx, 8]
        nxdl_enum = tmp.iloc[rowidx, 9]
        nxdl_path = tmp.iloc[rowidx, 10]
        nxdl_use = tmp.iloc[rowidx, 11]

        assert nxdl_use in [0, 1], \
            print("nxdl_use is not 0 or 1!")

        if nxdl_use == 1:
            print(nxdl_path)
            assert nxdl_dtype in DEFAULTS, \
                'Unresolvable nxdl_dtype ' + nxdl_dtype + ' !'
            if nxdl_enum == '':
                other_data_sources[nxdl_path] = DEFAULTS[nxdl_dtype]
            else:
                other_data_sources[nxdl_path] = nxdl_enum
        else:
            print(nxdl_path)
            assert nxdl_dtype in DEFAULTS, \
                'Unresolvable nxdl_dtype ' + nxdl_dtype + ' !'
            if nxdl_enum == '':
                vendor_files_sources[nxdl_path] = DEFAULTS[nxdl_dtype]
            else:
                vendor_files_sources[nxdl_path] = nxdl_enum

    with open(file_name + '.OtherMetaDataDefaults.json', 'w', encoding='utf-8') \
            as file_handle:
        json.dump(other_data_sources, file_handle,
                  ensure_ascii=False, indent=4)
        # ManuallyCollectedMetadata

    with open(file_name + '.FileParseableDefaults.json', 'w', encoding='utf-8') \
            as file_handle:
        json.dump(vendor_files_sources, file_handle,
                  ensure_ascii=False, indent=4)


ods_to_json_metadata_template(PREFIX + TESTFILE)
