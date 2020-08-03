#!/bin/bash

# sh run_dacapo.sh 30

time=$1
name="avrora"
perf_path="~"
dacapo_path="~"
burn_path="../resources"

# out path
rm -rf $out_path
mkdir $out_path
cd ../src

# Dacapo -s large -n 5 -Xmx1024m -XX:ReservedCodeCacheSize=64M -XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints
java -XX:+ExtendedDTraceProbes -XX:+PreserveFramePointer  -jar $dacapo_path/dacapo.jar -n 2 $name &

pid=$(pgrep -f "$name")
echo "program pid: " $pid

# jstack
output=`jstack $pid > output/out_stack.log`
# perf map
output=`sh $perf_path/perf-map-agent/bin/create-java-perf-map.sh $pid "unfoldall,dottedclass"`
# eBPF
chmod 777 main/locktime.py
output=`main/locktime.py $pid $time > output/out.log`
# burn: convert data to json
chmod 777 burn
$burn_path/burn convert --type=folded output/out.log > output/out.json




#flamegraph
#output=`perf record -F 99 -p $pid -g -- sleep $time`
#
#perf script -i perf.data &> perf.unfold
#~/FlameGraph/stackcollapse-perf.pl perf.unfold &> perf.folded
#~/FlameGraph/flamegraph.pl perf.folded > perf.svg




