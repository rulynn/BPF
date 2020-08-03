#!/bin/bash

# Test Code Cache

time=$1
name="avrora"
dacapo_path="~"

# out path
rm -rf $out_path
mkdir $out_path
cd ../src

# Dacapo -s large -n 5 -Xmx1024m
starttime=`date +'%Y-%m-%d %H:%M:%S'`
start_seconds=$(date --date="$starttime" +%s);
start_timeStamp=$((start_seconds*1000+`date "+%N"`/1000000))
echo "start time: " $start_timeStamp "ms"

output=`java -XX:+PrintCodeCache -XX:ReservedCodeCacheSize=64M -XX:+ExtendedDTraceProbes -XX:+PreserveFramePointer -jar $dacapo_path/dacapo.jar -n 2 $name`

endtime=`date +'%Y-%m-%d %H:%M:%S'`
end_seconds=$(date --date="$endtime" +%s);
end_timeStamp=$((end_seconds*1000+`date "+%N"`/1000000))
echo "end time: " $end_timeStamp "ms"

echo "runtime: " $((end_timeStamp-start_timeStamp)) "ms"





