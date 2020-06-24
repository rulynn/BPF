#!/bin/bash

# java -jar dacapo.jar avrora
# java Single
# sh run.sh 5


# dir
rm -rf out
mkdir out
time=$1

echo "start running program..."

#cd /root/splash2/codes/kernels/radix
#./RADIX -p2 -n104857600 &

#cd /root/splash2/codes/kernels/cholesky
#./CHOLESKY -p2 < inputs/tk29.O

# 2 ** 22 = 4,194,304
cd /root/splash2/codes/kernels/fft
./FFT -p2 -m22


echo "start get pid..."
pid=$(pgrep -f "RADIX")
echo "program pid: "  $pid

echo "start running eBPF..."
cd /root/bcc/learn/Master-Project/criticality_stacks
chmod 777 locktime.py
./locktime.py $pid $time > out.log

#echo "start kill the program..."
#kill -9 $pid
#echo "finish"
