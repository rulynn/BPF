#!/bin/bash

time=$1
burn_path="../"
out_path="../../src/output"
main_path="../../src/main"

cd ../resources/code
rm -rf $out_path
mkdir $out_path
mkdir $out_path/stack


# Modify java program: Replace 'SingleFun' in java and java_name
# java program shows in ../java/
name="Threads" #ThreadsWithLock
javac $name.java
java -XX:+ExtendedDTraceProbes -XX:+PreserveFramePointer $name &
sleep 1

pid=$(pgrep -f "$name")
echo "program pid: " $pid

## jstack
#output=`jstack $pid > $out_path/out_stack.log`
## perf map
#output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid "unfoldall,dottedclass"`
# eBPF
chmod 777 $main_path/locktime.py
output=`$main_path/locktime.py $pid $time > $out_path/out.log`

# burn: convert data to json
#chmod 777 $burn_path/burn
#for file in $out_path/stack/*; do
#    echo $file
#    $burn_path/burn convert --type=folded $file > $file.json
#done
