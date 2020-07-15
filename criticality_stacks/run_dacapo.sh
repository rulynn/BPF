#!/bin/bash

# sh run_dacapo.sh 5

# dir
rm -rf out
mkdir out
name=$1
time=$2

java -XX:+PreserveFramePointer -jar ~/dacapo.jar -n 2 $name &
sleep 1

pid=$(pgrep -f "$name")
echo "program pid: "  $pid

# jstack
jstack $pid

output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid "unfoldall,dottedclass"`

chmod 777 locktime.py
./locktime.py $pid $time > out.log
echo "eBPF finish"





