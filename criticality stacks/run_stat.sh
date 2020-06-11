#!/bin/bash

# java -XX:+ExtendedDTraceProbes Single
# sh run_stat.sh

java -XX:+ExtendedDTraceProbes Single &
echo "start runing program"

pid=$(pgrep -f "Single")
echo "program pid: "  $pid

output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid`
echo "start perf map"

./lockstat.py $pid > out.log
echo "finish"

# kill -9 $pid