#!/bin/bash


# need perf-map-agent: change path
cd ../java
javac Threads.java
java -XX:+ExtendedDTraceProbes -XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints Threads &
sleep 1


pid=$(pgrep -f "Threads")
echo "program pid: "  $pid


output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid`


cd ../criticality_stacks_old
chmod 777 lockstat.py
./lockstat.py $pid > out_stack.log

echo "eBPF finish"