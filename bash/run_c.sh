#!/bin/bash

# sh run_c.sh 15
time=$1
burn_path="../resources"
out_path="../src/output"

rm -rf $out_path
mkdir $out_path
mkdir $out_path/stack

cd ../src/code
name="ThreadsWithExtraWork" #ThreadsWithLock
g++ Threads.c -o Threads -lpthread
./Threads &
cd ..

pid=$(pgrep -f "./Threads")
echo "program pid: " $pid

# eBPF
chmod 777 main/locktime.py
output=`main/locktime.py -l c -p $pid -t $time > output/out.log`



