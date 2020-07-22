#!/bin/bash

# dir
rm -rf out
mkdir out
time=$1

name="SingleFun"

echo "start running program..."
cd ../java
java -XX:+ExtendedDTraceProbes $name &

pid=$(pgrep -f "$name")
echo "program pid: "  $pid

output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid`

cd ../learn/tools
output=`./profile.py -adf -p $pid $time > out.profile`
output=`~/FlameGraph/flamegraph.pl < out.profile > out.svg`