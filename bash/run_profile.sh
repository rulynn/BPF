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
name="Threads" #ThreadsWithLock
javac $name.java
# -Xmx2m -XX:ReservedCodeCacheSize=16M
java -XX:+ExtendedDTraceProbes -XX:+PreserveFramePointer -XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints $name &
#sleep 1
cd ..

pid=$(pgrep -f "$name")
echo "program pid: " $pid

# jstack
output=`jstack $pid > output/out_stack.log`
# perf map
output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid "unfoldall,dottedclass"`


# eBPF
chmod 777 ../resources/learn/lockstat.py
output=`../resources/learn/lockstat.py $pid`
