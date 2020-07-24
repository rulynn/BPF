#!/bin/bash

# sh run_dacapo.sh 5

# dir
rm -rf out
mkdir out
time=$1

# -s large -n 5 -Xmx1024m
java -XX:+ExtendedDTraceProbes -XX:+PreserveFramePointer -jar ~/dacapo.jar -n 2 avrora &
sleep 1

pid=$(pgrep -f "avrora")
echo "program pid: "  $pid

# jstack
jstack $pid > out/out_stack.log &

output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid "unfoldall,dottedclass"`
chmod 777 locktime.py
./locktime.py $pid $time > out/out.log &

# flamegraph
cd out
output=`perf record -F 99 -p $pid -g -- sleep $time`
perf script -i perf.data &> perf.unfold
~/FlameGraph/stackcollapse-perf.pl perf.unfold &> perf.folded
~/FlameGraph/flamegraph.pl perf.folded > perf.svg





