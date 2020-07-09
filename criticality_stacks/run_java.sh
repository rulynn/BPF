#!/bin/bash

# dir
rm -rf out
mkdir out
time=$1


# Modify java program: Replace 'SingleFun' in java and java_name
# java program shows in ../java/
cd ../java

javac Threads.java

#java -XX:+ExtendedDTraceProbes Threads &
#sleep 1
java Threads &
sleep 1

pid=$(pgrep -f "Threads")
echo "program pid: "  $pid

cd ../criticality_stacks
chmod 777 locktime.py
./locktime.py $pid $time > out.log

kill -9 $pid
echo "eBPF finish"

