#!/bin/bash

# dir
rm -rf out
mkdir out
time=$1

# -s large -n 5
java -XX:+PreserveFramePointer -jar ~/dacapo.jar -n 2 avrora &

pid=$(pgrep -f "$name")
echo "program pid: "  $pid

output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid`

cd ../learn/tools
output=`./profile.py -adf -p $pid $time > out.profile`
output=`~/FlameGraph/flamegraph.pl < out.profile > out.svg`