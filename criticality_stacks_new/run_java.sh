#!/bin/bash

# dir
rm -rf out
mkdir out
time=$1


# Modify java program: Replace 'SingleFun' in java and java_name
# java program shows in ../java/
name="SingleFun"
java_name="java SingleFun"

java ../java/$name &

pid=$(pgrep -f "$java_name")
echo "program pid: "  $pid

chmod 777 locktime.py
./locktime.py $pid $time > out.log

kill -9 $pid
echo "finish"

