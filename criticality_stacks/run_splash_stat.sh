#!/bin/bash

echo "start running program..."
cd /root/splash2/codes/kernels/radix
./RADIX -p2 -n1048576 &

echo "start get pid..."
pid=$(pgrep -f "RADIX")
echo "program pid: "  $pid

echo "start perf map"
output=`sh ~/perf-map-agent/bin/create-java-perf-map.sh $pid`

echo "start running eBPF"
cd /root/bcc/learn/Master-Project/learn
chmod 777 lockstat.py
./lockstat.py $pid > out.log