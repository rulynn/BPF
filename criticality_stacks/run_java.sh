#!/bin/bash

# dir
rm -rf out
mkdir out
time=$1


# Modify java program: Replace 'SingleFun' in java and java_name
# java program shows in ../java/
cd ../java
name="Threads" #ThreadsWithLock
javac $name.java

java -XX:+ExtendedDTraceProbes -XX:+PreserveFramePointer $name &
sleep 1

#java Threads &
#sleep 1

pid=$(pgrep -f "$name")
echo "program pid: "  $pid

output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid`

cd ../criticality_stacks
chmod 777 locktime.py
./locktime.py $pid $time > out.log
echo "eBPF finish"

