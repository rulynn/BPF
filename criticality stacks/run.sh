#!/bin/bash

# sh run.sh jar/ Sync

# dir
rm -rf out
mkdir out

# java -jar dacapo.jar avrora
process=$1
pid=$(pgrep -f jar)
echo $pid
./locktime.py $pid > out.log