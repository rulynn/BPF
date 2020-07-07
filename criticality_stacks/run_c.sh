#!/bin/bash

# dir
rm -rf out
mkdir out
time=$1


# Modify java program: Replace 'SingleFun' in java and java_name
# java program shows in ../java/

cd ../java
g++ Threads.c -o Threads
./Threads &

pid=$(pgrep -f "./Threads")
echo "program pid: "  $pid

cd ../criticality_stacks
chmod 777 locktime.py
./locktime.py $pid $time > out.log
echo "eBPF finish"






