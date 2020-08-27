#!/bin/bash

time=$1
name="eclipse"
burn_path="../resources"
out_path="../src/output"


rm -rf $out_path
mkdir $out_path
mkdir $out_path/stack
cd ../src

# Dacapo -s large -n 5 -Xmx1024m -XX:ReservedCodeCacheSize=64M -XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints
java -XX:+ExtendedDTraceProbes -XX:+PreserveFramePointer -XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints -jar ~/dacapo.jar -n 5 $name &

pid=$(pgrep -f "$name")
echo "program pid: " $pid

# perf map
sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid "unfoldall,dottedclass" &

# eBPF
chmod 777 ../resources/profile.py
output=`../resources/profile -f $time $pid > $out_path/stack/all.log`

$burn_path/burn convert --type=folded $out_path/stack/all.log > $out_path/stack/all.log.json


