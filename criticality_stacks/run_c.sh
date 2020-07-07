#!/bin/bash

# dir
rm -rf out
mkdir out
time=$1


# Modify java program: Replace 'SingleFun' in java and java_name
# java program shows in ../java/
name="SingleFun"
java_name="java SingleFun"

cd ../java
g++ SingleFun.c -o SingleFun
./SingleFun

pid=$(pgrep -f "$name")
echo "program pid: "  $pid

cd ../criticality_stacks
chmod 777 locktime.py
./locktime.py $pid $time > out.log

kill -9 $pid
echo "eBPF finish"






