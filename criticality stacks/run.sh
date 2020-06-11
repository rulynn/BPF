#!/bin/bash

# sh run.sh

# dir
rm -rf out
mkdir out

# java -jar dacapo.jar avrora
# java -XX:+ExtendedDTraceProbes Single
# sh run.sh 5
time=$1
pid=$(pgrep -f "java Single")
echo $pid
./locktime.py $pid $time > out.log