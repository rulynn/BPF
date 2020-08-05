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
# java -XX:+PreserveFramePointer -jar ~/dacapo.jar -n 5 avrora
java -XX:+ExtendedDTraceProbes -XX:+PreserveFramePointer -Xmx256m -XX:ReservedCodeCacheSize=64M -jar ~/dacapo.jar -n 5 $name &

pid=$(pgrep -f "$name")
echo "program pid: " $pid

# jstack
output=`jstack $pid > output/out_stack.log`
# perf map
output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid "unfoldall,dottedclass"`
# eBPF
chmod 777 test.py
output=`./test.py -l java $pid $time > output/out.log`

