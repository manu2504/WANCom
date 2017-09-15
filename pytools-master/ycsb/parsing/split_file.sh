#!/bin/bash

# Configuration stuff

# fspec=/home/kirillb/data_sets_nc/drc/17.06.08.AZEvaluations/5x.cluster.zing/initial_samples/plane_DC_RR_LOCAL_ONE_VTRACE_51_450_LONG/2017-06-16_20:33:02_1/FRANi1_wl1_ycsb.ycsb
# num_files=8

fspec=$1
num_files=$2
base_name=$3

# Work out lines per file.

total_lines=$(wc -l <${fspec})
((lines_per_file = (total_lines + num_files - 1) / num_files))

# Split the actual file, maintaining lines.

split -d -a 2 --lines=${lines_per_file} ${fspec} ${base_name}.

# Debug information

# echo "Total lines     = ${total_lines}"
# echo "Lines  per file = ${lines_per_file}"
# wc -l ${base_name}.*