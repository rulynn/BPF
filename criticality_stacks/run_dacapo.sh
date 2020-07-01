#!/bin/bash

# java -jar dacapo.jar avrora
# java Single
# sh run_dacapo.sh 5


# dir
rm -rf out
mkdir out

# Modify java program: Replace 'SingleFun' in java and java_name
# java program shows in ../java/
name="SingleFun"
java_name="java SingleFun"
time=$1

echo "start running program..."
cd ../java
java $name &

echo "start get pid..."
pid=$(pgrep -f "$java_name")
echo "program pid: "  $pid

echo "start running eBPF..."
cd ../criticality_stacks
chmod 777 locktime.py
./locktime.py $pid $time > out.log

echo "start kill the program..."
kill -9 $pid
echo "finish"

