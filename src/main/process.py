#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy
import itertools
import plotStatic as plot

# version 1
TIME_MIN = 9999999999999999999
tid_list = []
threadPointList = []
ans = []
total = 0
class UNIT:
    def __init__(self, start_time, wait_time, hold_time, enter_count):
        self.start_time = start_time
        self.wait_time = wait_time
        self.hold_time = hold_time
        self.enter_count = enter_count

class TIME:
    def __init__(self, status, tid, time):
        self.status = status
        self.tid = tid
        self.time = time

class WAIT:
    def __init__(self, start, end):
        self.start = start
        self.end = end


def run(locks, times, status):

    global TIME_MIN

    # deal data
    output_data = preprocessed(locks)

    # deal start time and stop time
    start_times = {}
    stop_times = {}
    for k, v in times.items():
        print(k.tid, k.timestamp, k.type)
        if (k.type == "pthread" or k.type == "start"):
            start_times[k.tid] = k.timestamp/1000.0
            TIME_MIN = min(TIME_MIN, k.timestamp/1000.0)
        if (k.type == "stop"):
            stop_times[k.tid] = k.timestamp/1000.0

    # start calculate
    for k, v in output_data.items():
        calculation_single(k, v, start_times, stop_times)

    threadPointList.sort(key=lambda pair: pair.time)
    calculation_single_inner(threadPointList)
#     for item in threadPointList:
#         print("\ttid %d ::: time %d ::: status %d" % (item.tid, item.time, item.status))

    # start plot
    plot.run(tid_list, ans, total, status)

def preprocessed(locks):

    global TIME_MIN
    output_data = {}

    grouper = lambda (k, v): k.tid
    sorted_by_thread = sorted(locks.items(), key=grouper)
    locks_by_thread = itertools.groupby(sorted_by_thread, grouper)
    for tid, items in locks_by_thread:
        print("thread %d" % tid)
        for k, v in sorted(items, key=lambda (k, v): -v.wait_time_ns):

             if k not in tid_list:
                tid_list.append(k.tid)

             tmp = UNIT(v.start_time_ns/1000.0, v.wait_time_ns/1000.0 + v.spin_time_ns/1000.0, v.lock_time_ns/1000.0, v.enter_count)
             print("\tmutex %s ::: start %.2fus ::: wait %.2fus ::: hold %.2fus ::: enter count %d" % (k.mtx, v.start_time_ns/1000.0, v.wait_time_ns/1000.0 + v.spin_time_ns/1000.0, v.lock_time_ns/1000.0, v.enter_count))

             # save data
             if output_data.get(k.tid) == None:
                 output_data[k.tid] = []
             output_data[k.tid].append(tmp)

             # Used to calculate relative time: time - TIME_MIN
             TIME_MIN = min(TIME_MIN, tmp.start_time)

    return output_data


def calculation_single(tid, data, start_times, stop_times):


    global TIME_MIN
    global tid_list
    global threadPointList

    grouper = lambda x: x.start_time
    sorted_data = sorted(data, key=grouper)

    pre_time = int(start_times.get(tid) or 0) - TIME_MIN
    last_time = int(stop_times.get(tid) or 0) - TIME_MIN
    print("tid: %d ::: thread start time %d ::: thread end time %d" % (tid, pre_time, last_time))

    waitPointList = []
    start = -1
    end = -1
    for item in sorted_data:
        print("\tstart %.2fus ::: wait %.2fus ::: hold %.2fus" % (item.start_time - TIME_MIN, item.wait_time, item.hold_time))
        if start == -1:
            start = item.start_time - TIME_MIN
            end = item.start_time + item.wait_time - TIME_MIN
        elif item.start_time - TIME_MIN < end:
            end = max(end, item.start_time + item.wait_time - TIME_MIN)
        else:
            print("\twait start time %d ::: wait end time %d" % (start, end))
            waitPointList.append(WAIT(start, end))
            start = item.start_time - TIME_MIN
            end = item.start_time + item.wait_time - TIME_MIN
        last_time = max(last_time, item.start_time + item.wait_time + item.hold_time - TIME_MIN)
    print("\twait start time %d ::: wait end time %d" % (start, end))
    waitPointList.append(WAIT(start, end))

    print("---------------------------")
    for item in waitPointList:
        if int(pre_time) >= 0:
            threadPointList.append(TIME(0, tid, pre_time))
            threadPointList.append(TIME(1, tid, item.start))
            print("\tstart time %d ::: end time %d" % (pre_time, item.start))
        pre_time = item.end
    threadPointList.append(TIME(0, tid, pre_time))
    threadPointList.append(TIME(1, tid, last_time))
    print("\tstart time %d ::: end time %d" % (pre_time, last_time))


def calculation_single_inner(threadPointList):

    global ans
    global total
    global tid_list

    isHold = []
    lastStamp = 0
    maxTid = 0

    # TODO: update
    for i in range(0, len(tid_list)):
        isHold.append(False)
        ans.append(0.0)

    for threadPoint in threadPointList:
        nowCount = countHold(isHold)
        index = tid_list.index(threadPoint.tid)
        for i in range(0, len(tid_list)):
            if isHold[i] == True:
                ans[i] += (threadPoint.time - lastStamp) * 1.0 / nowCount
                total += (threadPoint.time - lastStamp) * 1.0 / nowCount

        if threadPoint.status == 0:
            isHold[index] = True
        else:
            isHold[index] = False

        lastStamp = threadPoint.time

    for i in range(len(tid_list)):
        if ans[i] == 0:
            continue
        print("tid %d ::: ans %.2f" % (tid_list[i], ans[i]))

    return ans, total

def countHold(isHold):
    count = 0
    for item in isHold:
        if item == True:
            count = count + 1
    return count