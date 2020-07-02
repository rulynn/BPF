#!/bin/bash

# Need perf-map-agent and FlameGraph: change path

name="SingleFun"

echo "start running program..."
cd ../java
java -XX:+ExtendedDTraceProbes $name &

echo "start get pid..."
pid=$(pgrep -f "$name")
echo "program pid: "  $pid

echo "start perf map"
output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid`

echo "start profile"
cd ../learn/tools
output=`profile.py -adf -p $pid 15 > out.profile`

echo "start flamegraph"
output=`~/FlameGraph/flamegraph.pl < out.profile > out.svg`