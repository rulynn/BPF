#!/bin/bash


# need perf-map-agent: change path

name="SingleFun"

echo "start running program..."
cd ../java
java -XX:+ExtendedDTraceProbes $name &

echo "start get pid..."
pid=$(pgrep -f "$name")
echo "program pid: "  $pid

echo "start perf map"
output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid`

echo "start running eBPF"
cd ../learn
chmod 777 lockstat.py
./lockstat.py $pid > out.log

echo "start kill the program..."
kill -9 $pid
echo "finish"