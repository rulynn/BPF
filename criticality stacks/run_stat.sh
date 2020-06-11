#!/bin/bash

# java -XX:+ExtendedDTraceProbes Single
# sh run_stat.sh

name="SingleFun"

java -XX:+ExtendedDTraceProbes $name &
echo "start runing program"

pid=$(pgrep -f $name)
echo "program pid: "  $pid

output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid`
echo "start perf map"

./lockstat.py $pid > out.log
echo "finish"

# kill -9 $pid