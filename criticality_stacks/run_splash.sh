#!/bin/bash

# sh run_splash.sh 5

# dir
rm -rf out
mkdir out
time=$1

echo "start running program..."

 cd ~/splash2/codes/kernels/fft
 ./FFT -p8 -m26 &

#cd /root/splash2/codes/kernels/lu/non_contiguous_blocks
#./LU -p8 -n4096 &

#cd /root/splash2/codes/kernels/cholesky
#./CHOLESKY -p8 < inputs/tk29.O &

#cd /root/splash2/codes/apps/ocean/contiguous_partitions
#./OCEAN -p8 -n2050 &

pid=$(pgrep -f "FFT")

cd ~/bcc/learn/Master-Project/criticality_stacks
chmod 777 locktime.py
./locktime.py $pid $time > out.log

