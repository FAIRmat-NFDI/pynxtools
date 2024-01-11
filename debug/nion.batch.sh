#!/bin/bash

datasource="../../../../paper_paper_paper/scidat_nomad_ebsd/bb_analysis/data/development_nion/"

# examples="a.zip.nionswift b.zip.nionswift"
examples="2022-02-18_Metadata_Kuehbach.zip.nionswift"


for example in $examples; do
	echo $example
	dataconverter --reader em --nxdl NXroot --input-file $datasource$example --output debug.$example.nxs 1>stdout.$example.nxs.txt 2>stderr.$example.nxs.txt
done
