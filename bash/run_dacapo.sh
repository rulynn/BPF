#!/bin/bash

# sh run_dacapo.sh 30

time=$1
name="avrora"
out_path="../out"
file_path="../criticality_stacks"
bash_path="../bash"

# out path
rm -rf $out_path
mkdir $out_path
cd $out_path

# Dacapo -s large -n 5 -Xmx1024m
java -XX:+ExtendedDTraceProbes -XX:+PreserveFramePointer -jar ~/dacapo.jar -n 2 $name &
sleep 1

pid=$(pgrep -f "$name")
echo "program pid: "  $pid " ::: time: " $time

# jstack
output=`jstack $pid > out_stack.log`
# perf map
output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid "unfoldall,dottedclass"`
# eBPF
chmod 777 $file_path/locktime.py
$file_path/locktime.py $pid $time > out.log &

#flamegraph
#output=`perf record -F 99 -p $pid -g -- sleep $time`
#
#perf script -i perf.data &> perf.unfold
#~/FlameGraph/stackcollapse-perf.pl perf.unfold &> perf.folded
#~/FlameGraph/flamegraph.pl perf.folded > perf.svg




