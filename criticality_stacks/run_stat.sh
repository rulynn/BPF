#!/bin/bash

# java -XX:+ExtendedDTraceProbes Single
# sh run_stat.sh

name="SingleFun"

echo "start running program"
java -XX:+ExtendedDTraceProbes $name &

echo "start get pid"
pid=$(pgrep -f $name)
echo "program pid: "  $pid

echo "start perf map"
output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid`

echo "start running eBPF"
./lockstat.py $pid > out.log
echo "finish"

# kill -9 $pid