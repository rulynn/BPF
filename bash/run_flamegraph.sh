#!/bin/bash

out_path="../out"
file_path="../criticality_stacks"

time=$1
pid=$2

output=`perf record -F 99 -p $pid -g -- sleep $time`
perf script -i perf.data &> perf.unfold
~/FlameGraph/stackcollapse-perf.pl perf.unfold &> perf.folded
~/FlameGraph/flamegraph.pl perf.folded > perf.svg