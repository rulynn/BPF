#!/bin/bash

# sh run_dacapo.sh 30

time=$1
name="avrora"
out_path="../out"
file_path="../criticality_stacks"

# out path
rm -rf out_path
mkdir out_path

# -s large -n 5 -Xmx1024m
java -XX:+ExtendedDTraceProbes -XX:+PreserveFramePointer -jar ~/dacapo.jar -n 2 $name &
sleep 1

pid=$(pgrep -f "$name")
echo "program pid: "  $pid

# jstack
output=`jstack $pid > $out_path/out_stack.log`
# perf map
output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid "unfoldall,dottedclass"`
# eBPF
chmod 777 $file_path/locktime.py
$file_path/locktime.py $pid $time > $out_path/out.log &

#flamegraph
sh run_flamegraph.sh $time $pid




