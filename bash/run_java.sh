#!/bin/bash


# sh run_java.sh 60

time=$1
burn_path="../resources"
out_path="../src/output"

rm -rf $out_path
mkdir $out_path
mkdir $out_path/stack

# Modify java program: Replace 'SingleFun' in java and java_name
# java program shows in ../java/
cd ../src/code
name="ThreadsWithLock2" #ThreadsWithLock
javac $name.java
# -Xmx2m -XX:ReservedCodeCacheSize=16M
java -XX:+ExtendedDTraceProbes -XX:+PreserveFramePointer -XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints $name &
#sleep 1
cd ..

pid=$(pgrep -f "$name")
echo "program pid: " $pid
echo "now timeStamp: " $[$(date +%s%N)/1000000]

# jstack
output=`jstack $pid > output/out_stack.log`
echo "jstack timeStamp: " $[$(date +%s%N)/1000000]
# perf map

sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid "unfoldall,dottedclass" &
#echo "perf timeStamp: " $[$(date +%s%N)/1000000]

# eBPF
chmod 777 main/locktime.py
output=`main/locktime.py -l java -p $pid -t $time> output/out.log`
echo "eBPF timeStamp: " $[$(date +%s%N)/1000000]

# burn: convert data to json
chmod 777 $burn_path/burn
for file in output/stack/*; do
    echo $file
    $burn_path/burn convert --type=folded $file > $file.json
done