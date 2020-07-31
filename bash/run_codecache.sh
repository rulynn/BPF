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
start_seconds=$(date --date="$starttime" +%s);
start_timeStamp=$((start_seconds*1000+`date "+%N"`/1000000))
echo "start time: " $start_timeStamp "ms"

output=`java -XX:+PrintCodeCache -XX:ReservedCodeCacheSize=2.5M -XX:+ExtendedDTraceProbes -XX:+PreserveFramePointer -jar ~/dacapo.jar -n 2 $name`

endtime=`date +'%Y-%m-%d %H:%M:%S'`
end_seconds=$(date --date="$endtime" +%s);
end_timeStamp=$((end_seconds*1000+`date "+%N"`/1000000))
echo "end time: " $end_timeStamp "ms"

echo "runtime: " $((end_timeStamp-start_timeStamp)) "ms"





