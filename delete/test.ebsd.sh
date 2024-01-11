#!/bin/bash

src_prefix="~/Research/paper_paper_paper/scidat_nomad_ebsd/bb_analysis/data/production_ebsd"
src_pyxem="${src_prefix}_pyxem"
src_mtex="${src_prefix}_mtex"
echo "$src_prefix"
echo "$src_pyxem"
echo "$src_mtex"
ohfiles="${src_pyxem}/*.oh5"
cmd="ls ${ohfiles}"
$cmd

