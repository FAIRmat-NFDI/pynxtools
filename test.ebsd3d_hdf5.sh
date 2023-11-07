#!/bin/bash

Examples="067_0003 177_0004 177_0005 177_0006 177_0007 177_0008 177_0009 226_0010 226_0011 226_0012 226_0013 244_0014 SmallIN100_Final"

Examples="SmallIN100_Final"
for example in $Examples; do
	echo $example
	dataconverter --reader em --nxdl NXroot --input-file $example.dream3d --output debug.$example.dream3d.nxs 1>stdout.$example.dream3d.nxs.txt 2>stderr.$example.dream3d.nxs.txt
done
