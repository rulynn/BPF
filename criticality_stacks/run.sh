#!/bin/bash

# java -jar dacapo.jar avrora
# java Single
# sh run.sh 5


# dir
rm -rf out
mkdir out

name="SingleFun"
java_name="java SingleFun"
time=$1

echo "start running program"
java ../java/$name &

echo "start get pid"
pid=$(pgrep -f "$java_name")
echo "program pid: "  $pid

echo "start running eBPF"
./locktime.py $pid $time > out.log
echo "finish"

echo "kill the program"
kill -9 $pid


