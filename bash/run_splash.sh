#!/bin/bash

# sh run_splash.sh 37

time=$1
burn_path="../resources"
out_path="../src/output"

rm -rf $out_path
mkdir $out_path
cd ../src

#~/splash2/codes/kernels/fft/FFT -p8 -m26 &
#pid=$(pgrep -f "FFT")

#~/splash2/codes/kernels/cholesky/CHOLESKY -p8 < ~/splash2/codes/kernels/cholesky/inputs/tk29.O &
#pid=$(pgrep -f "CHOLESKY")

~/splash2/codes/kernels/lu/non_contiguous_blocks/LU -p8 -n4096 &
pid=$(pgrep -f "LU")

echo "program pid: " $pid

chmod 777 main/locktime.py
output=`main/locktime.py -l c -p $pid -t $time > output/out.log`


