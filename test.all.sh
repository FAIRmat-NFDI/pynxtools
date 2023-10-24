#!/bin/bash


# dataconverter --reader em --nxdl NXroot --input-file 130_0003.h5 --output debug.bruker.nxs 1>stdout.bruker.txt 2>stderr.bruker.txt
# dataconverter --reader em --nxdl NXroot --input-file 207_2081.edaxh5 --output debug.apex.nxs 1>stdout.apex.txt 2>stderr.apex.txt
# dataconverter --reader em --nxdl NXroot --input-file 229_2097.oh5 --output debug.edax.nxs 1>stdout.edax.txt 2>stderr.edax.txt
# dataconverter --reader em --nxdl NXroot --input-file 088_0009.h5 --output debug.britton.nxs 1>stdout.britton.txt 2>stderr.britton.txt

# 026_0007.h5 026_0027.h5 026_0029.h5 026_0030.h5 026_0033.h5 026_0039.h5 026_0041.h5 delmic hdf5 have no ebsd data
# 173_0056.h5oina has only eds data

Examples="026_0046.h5oina 026_0049.h5oina 026_0050.h5oina 026_0052.h5oina 066_0013.h5 066_0015.h5 066_0016.h5 066_0023.h5 066_0025.h5 066_0034.h5 078_0004.h5 087_0021.h5 088_0009.h5 093_0045.h5oina 093_0047.h5oina 093_0048.h5oina 093_0051.h5oina 093_0053.h5oina 093_0054.h5oina 093_0055.h5oina 093_0058.h5oina 093_0059.h5oina 093_0060.h5oina 093_0062.h5oina 093_0063.h5oina 101_0040.h5 110_0012.h5 114_0017.h5 116_0008.h5 116_0014.h5 116_0018.h5 116_0019.h5 116_0020.h5 116_0022.h5 116_0037.h5 116_0042.h5 124_0002.h5 124_0036.h5 125_0006.h5 126_0038.h5 130_0003.h5 130_2082.h5 130_2083.h5 130_2084.h5 130_2085.h5 130_2086.h5 130_2087.h5 130_2088.h5 130_2089.h5 130_2090.h5 130_2091.h5 130_2092.h5 130_2093.h5 130_2094.h5 132_0005.h5 144_0043.h5 173_0056.h5oina 173_0057.h5oina 174_0031.h5 207_2081.edaxh5 208_0061.h5oina 212_2095.h5oina 229_2096.oh5 229_2097.oh5"

# Examples="207_2081.edaxh5"
# Examples="173_0057.h5oina"
for example in $Examples; do
	echo $example
	dataconverter --reader em --nxdl NXroot --input-file $example --output debug.$example.nxs 1>stdout.$example.nxs.txt 2>stderr.$example.nxs.txt
done
