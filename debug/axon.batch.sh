#!/bin/bash

datasource="../../../../paper_paper_paper/scidat_nomad_ebsd/bb_analysis/data/development_axon/axon/"

# comments is detector mode
examples="axon/20210426T224437.049Raw0.png"  #axon
examples="ReductionOfFeOx.zip"  # Small.zip"

for example in $examples; do
	echo $example
	dataconverter --reader em --nxdl NXroot --input-file $datasource$example --output debug.$example.nxs 1>stdout.$example.nxs.txt 2>stderr.$example.nxs.txt
done
