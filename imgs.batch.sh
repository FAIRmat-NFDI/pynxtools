#!/bin/bash

datasource="../../../../paper_paper_paper/scidat_nomad_ebsd/bb_analysis/data/development_imgs/axon/"

# comments is detector mode
examples="kit/FeMoOx_AntiA_04_1k5x_CN.tif"
examples="ikz_robert/0c8nA_3deg_003_AplusB_test.tif"  # T1
examples="ikz_martin/ALN_baoh_021.tif"  # T2
examples="ikz_robert/T3_image.tif"
examples="ikz_robert/ETD_image.tif"  # ETD
examples="ikz_martin/NavCam_normal_vis_light_ccd.tif"  # NavCam
examples="0c8nA_3deg_003_AplusB_test.tif ALN_baoh_021.tif T3_image.tif ETD_image.tif NavCam_normal_vis_light_ccd.tif"
examples="axon/20210426T224437.049Raw0.png"  #axon
examples="ReductionOfFeOx.zip"

for example in $examples; do
	echo $example
	dataconverter --reader em --nxdl NXroot --input-file $datasource$example --output debug.$example.nxs 1>stdout.$example.nxs.txt 2>stderr.$example.nxs.txt
done
