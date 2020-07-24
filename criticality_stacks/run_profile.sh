#!/bin/bash

# dir
rm -rf out
mkdir out
time=$1
name="avrora"
# -s large -n 5
java -XX:+ExtendedDTraceProbes -XX:+PreserveFramePointer -jar ~/dacapo.jar -n 2 $name &
sleep 1

pid=$(pgrep -f "$name")
echo "program pid: "  $pid

output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid "unfoldall,dottedclass"`
output=`~/bcc/tools/profile.py -adf -p $pid $time > out/out.profile`
#output=`~/FlameGraph/flamegraph.pl < out/out.profile > out/out.svg`
output=`../resources/flamegraph.pl < out/out.profile > out/out.svg`