#!/bin/bash

# sh run_dacapo.sh 5


# dir
rm -rf out
mkdir out
time=$1

cd /root
java -jar dacapo.jar avrora &

pid=$(pgrep -f "avrora")
kill -STOP $pid

cd /root/bcc/learn/Master-Project/criticality_stacks
chmod 777 locktime.py

./locktime.py $pid $time > out.log &
kill -CONT $pid

