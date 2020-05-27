#!/bin/bash

# java -jar dacapo.jar avrora
pid=$(pgrep -f jar)
echo $pid
./locktime.py $pid > out.log