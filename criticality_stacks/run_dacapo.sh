#!/bin/bash

# sh run_dacapo.sh 5

# dir
rm -rf out
mkdir out
time=$1

# -s large -n 5
java -XX:+ExtendedDTraceProbes -XX:+PreserveFramePointer -XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints -Xmx1024m -jar ~/dacapo.jar -n 2 avrora &
sleep 1

pid=$(pgrep -f "avrora")
echo "program pid: "  $pid

# jstack
jstack $pid > out_stack.log &

output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid "unfoldall,dottedclass"`
chmod 777 locktime.py
./locktime.py $pid $time > out.log &

# flamegraph
output=`perf record -F 99 -p $pid -g -- sleep $time`
perf script -i perf.data &> perf.unfold
~/FlameGraph/stackcollapse-perf.pl perf.unfold &> perf.folded
~/FlameGraph/flamegraph.pl perf.folded > perf.svg





