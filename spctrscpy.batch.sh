#!/bin/bash

datasource="../../../../paper_paper_paper/scidat_nomad_ebsd/bb_analysis/data/development_spctrscpy/"

# apex examples ikz, pdi
# examples="ikz/VInP_108_L2.h5 ikz/GeSn_13.h5 pynx/46_ES-LP_L1_brg.bcf pynx/1613_Si_HAADF_610_kx.emd pynx/EELS_map_2_ROI_1_location_4.dm3 pynx/H5OINA_examples_Specimen_1_Map_EDS_+_EBSD_Map_Data_2.h5oina"
examples="ikz/VInP_108_L2.h5"
examples="pdi/InGaN_nanowires_spectra.edaxh5"

for example in $examples; do
	echo $example
	dataconverter --reader em --nxdl NXroot --input-file $datasource$example --output debug.$example.nxs 1>stdout.$example.nxs.txt 2>stderr.$example.nxs.txt
done
