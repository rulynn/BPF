#!/bin/bash

# java -jar dacapo.jar avrora
# java Single
# sh run.sh 5


# dir
rm -rf out
mkdir out

# Modify java program: Replace 'SingleFun' in java and java_name
# java program shows in ../java/
name="FMM"
time=$1

#echo "start running program..."
#cd /root/splash2/codes/apps/fmm
#./FMM &

echo "start get pid..."
pid=$(pgrep -f "$name")
echo "program pid: "  $pid

echo "start running eBPF..."
cd /root/bcc/learn/Master-Project/criticality_stacks
chmod 777 locktime.py
./locktime.py $pid $time > out.log

echo "start kill the program..."
kill -9 $pid
echo "finish"

