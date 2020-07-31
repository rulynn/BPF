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
starttime=`date +'%Y-%m-%d %H:%M:%S'`
output=`java -XX:+ExtendedDTraceProbes -XX:+PreserveFramePointer -XX:ReservedCodeCacheSize=512M -jar ~/dacapo.jar -n 2 $name`
endtime=`date +'%Y-%m-%d %H:%M:%S'`
start_seconds=$(date --date="$starttime" +%s);
end_seconds=$(date --date="$endtime" +%s);
echo "runtime:"$((end_seconds-start_seconds))"s"


#flamegraph
#output=`perf record -F 99 -p $pid -g -- sleep $time`
#
#perf script -i perf.data &> perf.unfold
#~/FlameGraph/stackcollapse-perf.pl perf.unfold &> perf.folded
#~/FlameGraph/flamegraph.pl perf.folded > perf.svg




