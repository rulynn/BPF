#!/bin/bash

# sh run_dacapo.sh 30/18

time=$1
name="eclipse"
burn_path="../resources"
out_path="../src/output"


rm -rf $out_path
mkdir $out_path
mkdir $out_path/stack
cd ../src

# Dacapo -s large -n 5 -Xmx1024m -XX:ReservedCodeCacheSize=64M -XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints
java -XX:+ExtendedDTraceProbes -XX:+PreserveFramePointer -XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints -jar ~/dacapo.jar $name &

pid=$(pgrep -f "$name")
echo "program pid: " $pid
echo "now timeStamp: " $[$(date +%s%N)/1000000]

# jstack
output=`jstack $pid > output/out_stack.log`
echo "jstack timeStamp: " $[$(date +%s%N)/1000000]
# perf map
#output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid "unfoldall,dottedclass"`
#echo "perf timeStamp: " $[$(date +%s%N)/1000000]
# eBPF
chmod 777 main/locktime.py
output=`main/locktime.py -l java -p $pid -t $time> output/out.log`
echo "eBPF timeStamp: " $[$(date +%s%N)/1000000]

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




