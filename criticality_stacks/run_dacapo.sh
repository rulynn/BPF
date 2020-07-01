#!/bin/bash

# sh run_dacapo.sh 5


# dir
rm -rf out
mkdir out
time=$1

cd /root
java -jar dacapo.jar -n 5 avrora &

pid=$(pgrep -f "avrora")
cd /root/bcc/learn/Master-Project/criticality_stacks

chmod 777 locktime.py
./locktime.py $pid $time > out.log &

chmod 777 lockstat.py
./locktime.py $pid > out_stack.log &

