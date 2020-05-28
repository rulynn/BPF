#!/bin/bash

# dir
rm -rf out
mkdir out

# java -jar dacapo.jar avrora
pid=$(pgrep -f jar)
echo $pid
./locktime.py $pid > out.log