#!/bin/bash

# sh run_splash.sh 5


# dir
rm -rf out
mkdir out
time=$1

echo "start running program..."


# 2 ** 22 = 4,194,304
# 2 ** 26 = 67,108,864
#cd /root/splash2/codes/kernels/fft
#./FFT -p8 -m26 &

# 1024*1024
#begin_time=`date +%s%N`
cd /root/splash2/codes/kernels/lu/non_contiguous_blocks
./LU -p8 -n4096 &

# TODO: not success, too quick
#cd /root/splash2/codes/kernels/cholesky
#./CHOLESKY -p8 < inputs/tk29.O &

#cd /root/splash2/codes/apps/ocean/contiguous_partitions
#./OCEAN -p8 -n2050 &

#echo "start get pid..."
pid=$(pgrep -f "LU")
echo "program pid: "  $pid

#echo "start running eBPF..."
cd /root/bcc/learn/Master-Project/criticality_stacks
chmod 777 locktime.py

#end_time=`date +%s%N`
#subtime=`expr $end_time - $begin_time`
#echo $subtime
./locktime.py $pid $time > out.log
