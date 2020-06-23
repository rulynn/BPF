#!/bin/bash

# java -jar dacapo.jar avrora
# java Single
# sh run.sh 5


# dir
rm -rf out
mkdir out

echo "start running program..."
cd /root/splash2/codes/apps/radix
./RADIX -p2 -n104857600 &

echo "start get pid..."
pid=$(pgrep -f "RADIX")
echo "program pid: "  $pid

echo "start running eBPF..."
cd /root/bcc/learn/Master-Project/criticality_stacks
chmod 777 locktime.py
./locktime.py $pid > out.log

#echo "start kill the program..."
#kill -9 $pid
#echo "finish"
