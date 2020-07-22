#!/bin/bash

# dir
rm -rf out
mkdir out
time=$1

# -s large -n 5
java -XX:+ExtendedDTraceProbes -XX:+PreserveFramePointer -XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints -Xmx128M -jar ~/dacapo.jar -n 2 avrora &
#sleep 1

pid=$(pgrep -f "avrora")
echo "program pid: "  $pid

# jstack
jstack $pid > out_stack.log &

output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid`

cd ../learn/tools
output=`profile.py -adf -p $pid $time > out.profile`
output=`~/FlameGraph/flamegraph.pl < out.profile > out.svg`