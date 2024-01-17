#!/bin/bash

datasource="../../../../../paper_paper_paper/scidat_nomad_ebsd/bb_analysis/data/development_spctrscpy/pdi/"
datasource="../../../../../paper_paper_paper/scidat_nomad_ebsd/bb_analysis/data/development_spctrscpy/ikz/"
datasource="../../../../../paper_paper_paper/scidat_nomad_ebsd/bb_analysis/data/development_spctrscpy/fhi/"

# apex examples ikz, pdi
# examples="ikz/VInP_108_L2.h5 ikz/GeSn_13.h5 pynx/46_ES-LP_L1_brg.bcf pynx/1613_Si_HAADF_610_kx.emd pynx/EELS_map_2_ROI_1_location_4.dm3 pynx/H5OINA_examples_Specimen_1_Map_EDS_+_EBSD_Map_Data_2.h5oina"
examples="InGaN_nanowires_spectra.edaxh5"
examples="AlGaO.nxs"
examples="GeSi.nxs"
examples="GeSn_13.nxs"
# examples="VInP_108_L2.h5"
examples="CG71113 1513 HAADF-DF4-DF2-BF 1.2 Mx STEM.emd"
examples="CG71113 1138 Ceta 660 mm Camera.emd"
examples="CG71113 1125 Ceta 1.1 Mx Camera.emd"
examples="CG71113 1412 EDS-HAADF-DF4-DF2-BF 4.8 Mx SI.emd"

for example in "$examples"; do
	echo $example
	dataconverter --reader em --nxdl NXroot --input-file "$datasource$example" --output "debug.$example.nxs" 1>"stdout.$example.nxs.txt" 2>"stderr.$example.nxs.txt"
done
