#!/bin/bash

Examples="067_0003 177_0004 177_0005 177_0006 177_0008 177_0009 226_0010 226_0011 226_0012 226_0013 244_0014 SmallIN100_Final"
Examples="067_0003 SmallIN100_Final 244_0014"
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


# Examples="SmallIN100_Final"
# Examples="244_0014"
for example in $Examples; do
	echo $example
	dataconverter --reader em --nxdl NXroot --input-file $example.dream3d --output debug.$example.dream3d.nxs 1>stdout.$example.dream3d.nxs.txt 2>stderr.$example.dream3d.nxs.txt
done
