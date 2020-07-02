#!/bin/bash

# sh run_dacapo.sh 5


# dir
rm -rf out
mkdir out
time=$1

java -jar ~/dacapo.jar -n 2 avrora &
pid=$(pgrep -f "avrora")

cd /root/bcc/learn/Master-Project/criticality_stacks

chmod 777 locktime.py
./locktime.py $pid $time > out.log &

chmod 777 lockstat.py
output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid`
./lockstat.py $pid > out_stack.log &



