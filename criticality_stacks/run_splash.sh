#!/bin/bash

# sh run_splash.sh 5

# dir
rm -rf out
mkdir out
time=$1

~/splash2/codes/kernels/fft/FFT -p8 -m26 &
pid=$(pgrep -f "FFT")

#~/splash2/codes/kernels/cholesky/CHOLESKY -p8 < inputs/tk29.O &
#pid=$(pgrep -f "CHOLESKY")

#~/splash2/codes/kernels/lu/non_contiguous_blocks/LU -p8 -n4096 &
#pid=$(pgrep -f "LU")


echo "program pid: "  $pid
chmod 777 locktime.py
./locktime.py $pid $time > out.log

