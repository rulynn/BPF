#!/bin/bash

# sh run.sh

# dir
rm -rf out
mkdir out

# java -jar dacapo.jar avrora
# sh run.sh 5
time=$1
pid=$(pgrep -f "java Sync")
echo $pid
./locktime.py $pid $time > out.log