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

# Dacapo -s large -n 5 -Xmx1024m -XX:ReservedCodeCacheSize=64M
java -XX:ReservedCodeCacheSize=64M -XX:+ExtendedDTraceProbes -XX:+PreserveFramePointer -jar ~/dacapo.jar -n 2 $name &
sleep 1

pid=$(pgrep -f "$name")
echo "program pid: " $pid

# jstack
output=`jstack $pid > out_stack.log`
# perf map
output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid "unfoldall,dottedclass"`
#burn
#curl -L "https://dl.bintray.com/mspier/binaries/burn/1.0.1/linux/amd64/burn" -o burn &
# eBPF
chmod 777 $file_path/locktime.py
output=`$file_path/locktime.py $pid $time > out.log`
#chmod 777 burn
#./burn convert out.log




#flamegraph
#output=`perf record -F 99 -p $pid -g -- sleep $time`
#
#perf script -i perf.data &> perf.unfold
#~/FlameGraph/stackcollapse-perf.pl perf.unfold &> perf.folded
#~/FlameGraph/flamegraph.pl perf.folded > perf.svg




