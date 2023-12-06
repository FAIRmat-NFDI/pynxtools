#!/bin/bash

datasource="../../../../paper_paper_paper/scidat_nomad_ebsd/bb_analysis/data/production_ebsd_pyxem/"

# 177_0007
# skip
# 177_0007 as it is one of the weird examples where the h5py library cannot traverse the content... let's not follow-up on this rabbit hole right now
# 177_0004 has only vertices
# 177_0005 has only edges
# 177_0006 has only surface facets
# 177_0008 out because old 6.0 format which does not store DIMENSIONS, ORIGIN, SHAPE under _SIMPL yet
# 177_0009 follows the new structure but has no EulerAngles only Phases thus without following with yet another logic the source for the 
# respective filter we have no chance to find the orientation data
# 226_0010 and _0011 are out because they do have only plain images (backscattered electron likely)
# 226_0013 is out because it has only plain optical image data no EBSD
# 244_0014 is out because it does not have any quantity whereby to generate a band contrast, confidence index, or mad on to generate a default plot

# 026_0007.h5 026_0027.h5 026_0029.h5 026_0030.h5 026_0033.h5 026_0039.h5 026_0041.h5 delmic hdf5 have no ebsd data
# 173_0056.h5oina has only eds data

# HDF5 files, 2D ESBD
examples="026_0046.h5oina 026_0049.h5oina 026_0050.h5oina 026_0052.h5oina 066_0013.h5 066_0015.h5 066_0016.h5 066_0023.h5 066_0025.h5 066_0034.h5 078_0004.h5 087_0021.h5 088_0009.h5 093_0045.h5oina 093_0047.h5oina 093_0048.h5oina 093_0051.h5oina 093_0053.h5oina 093_0054.h5oina 093_0055.h5oina 093_0058.h5oina 093_0059.h5oina 093_0060.h5oina 093_0062.h5oina 093_0063.h5oina 101_0040.h5 110_0012.h5 114_0017.h5 116_0008.h5 116_0014.h5 116_0018.h5 116_0019.h5 116_0020.h5 116_0022.h5 116_0037.h5 116_0042.h5 124_0002.h5 124_0036.h5 125_0006.h5 126_0038.h5 130_0003.h5 130_2082.h5 130_2083.h5 130_2084.h5 130_2085.h5 130_2086.h5 130_2087.h5 130_2088.h5 130_2089.h5 130_2090.h5 130_2091.h5 130_2092.h5 130_2093.h5 130_2094.h5 132_0005.h5 144_0043.h5 173_0056.h5oina 173_0057.h5oina 174_0031.h5 207_2081.edaxh5 208_0061.h5oina 212_2095.h5oina 229_2096.oh5 229_2097.oh5"
# dream3d files 3D ESBD
# examples="067_0003.dream3d 177_0004.dream3d 177_0005.dream3d 177_0006.dream3d 177_0008.dream3d 177_0009.dream3d 226_0010.dream3d 226_0011.dream3d 226_0012.dream3d 226_0013.dream3d 244_0014.dream3d SmallIN100_Final.dream3d"

# specific examples for testing purposes
examples="207_2081.edaxh5"
# examples="173_0057.h5oina"
# oxford, bruker, britton, edax old noncali, edax old calib, apex
# examples="173_0057.h5oina 130_0003.h5 088_0009.h5 116_0014.h5 229_2097.oh5 207_2081.edaxh5"
# examples="229_2096.oh5"  # this is the largest EBSD map, a composite
# examples="229_2097.oh5"
# examples="067_0003.dream3d SmallIN100_Final.dream3d 244_0014.dream3d"
# examples="244_0014.dream3d"
# examples="SmallIN100_Final.dream3d"
# examples="067_0003.dream3d"  # very large 3D EBSD takes ~40GB RAM for processing

for example in $examples; do
	echo $example
	dataconverter --reader em --nxdl NXroot --input-file $datasource$example --output debug.$example.nxs 1>stdout.$example.nxs.txt 2>stderr.$example.nxs.txt
done
