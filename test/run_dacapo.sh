#!/bin/bash

# sh run_dacapo.sh 30

time=$1
name="avrora"
burn_path="../resources"
out_path="output"

rm -rf $out_path
mkdir $out_path
mkdir $out_path/stack

# Dacapo -s large -n 5 -Xmx1024m -XX:ReservedCodeCacheSize=64M -XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints
#
java -XX:+ExtendedDTraceProbes -XX:+PreserveFramePointer -Xmx256m -XX:ReservedCodeCacheSize=64M -jar ~/dacapo.jar -n 5 $name &

pid=$(pgrep -f "$name")
echo "program pid: " $pid

# jstack
output=`jstack $pid > output/out_stack.log`
# perf map
output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid "unfoldall,dottedclass"`
# eBPF
chmod 777 locktime_test.py
output=`./locktime_test.py $pid $time > output/out.log`
# burn: convert data to json
chmod 777 $burn_path/burn
for file in output/stack/*; do
    echo $file
    $burn_path/burn convert --type=folded $file > $file.json
done





#flamegraph
#output=`perf record -F 99 -p $pid -g -- sleep $time`
#
#perf script -i perf.data &> perf.unfold
#~/FlameGraph/stackcollapse-perf.pl perf.unfold &> perf.folded
#~/FlameGraph/flamegraph.pl perf.folded > perf.svg



