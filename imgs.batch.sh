#!/bin/bash

datasource="../../../../paper_paper_paper/scidat_nomad_ebsd/bb_analysis/data/production_imgs/"

examples="ALN_baoh_021.tif FeMoOx_AntiA_04_1k5x_CN.tif"

for example in $examples; do
	echo $example
	dataconverter --reader em --nxdl NXroot --input-file $datasource$example --output debug.$example.nxs 1>stdout.$example.nxs.txt 2>stderr.$example.nxs.txt
done
