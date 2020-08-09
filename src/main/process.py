#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy
import itertools
import plotStatic as plot

TIME_MIN = {}
tid_list = []
ans = []
total = 0
TIME_MAX = 0
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


def run(locks, status):
    output_data = preprocessed(locks)
    for k, v in output_data.items():
        calculation_single(k, v)
    plot.run(tid_list, ans, total, status)

def preprocessed(locks):

    global TIME_MIN
    global TIME_MAX
    output_data = {}

    grouper = lambda (k, v): k.tid
    sorted_by_thread = sorted(locks.items(), key=grouper)
    locks_by_thread = itertools.groupby(sorted_by_thread, grouper)
    for tid, items in locks_by_thread:
        #print("thread %d" % tid)
        for k, v in sorted(items, key=lambda (k, v): -v.wait_time_ns):

             if k not in tid_list:
                tid_list.append(k.tid)

             tmp = UNIT(v.start_time_ns/1000.0, v.wait_time_ns/1000.0 + v.spin_time_ns/1000.0, v.lock_time_ns/1000.0, v.enter_count)
             #print("\tmutex %s ::: start %.2fus ::: wait %.2fus ::: spin %.2fus ::: hold %.2fus ::: enter count %d" %
             #   (k.mtx, v.start_time_ns/1000.0, v.wait_time_ns/1000.0, v.spin_time_ns/1000.0, v.lock_time_ns/1000.0, v.enter_count))

             # save data
             if output_data.get(k.mtx) == None:
                 output_data[k.mtx] = {}
             if output_data[k.mtx].get(k.tid) == None:
                 output_data[k.mtx][k.tid] = []
             output_data[k.mtx][k.tid].append(tmp)

             # Used to calculate relative time: time - TIME_MIN
             if TIME_MIN.get(k.mtx) == None:
                 TIME_MIN[k.mtx] = 999999999999999
             TIME_MIN[k.mtx] = min(TIME_MIN[k.mtx], tmp.start_time)
             TIME_MAX = max(TIME_MAX, tmp.start_time + tmp.wait_time + tmp.hold_time)

    return output_data

# def calculation_single(mtx, single_data):
#
#     #print("------------------- Single MTX start: %d -------------------\n" % (mtx))
#     global TIME_MIN
#     global tid_list
#     threadPointList = []
#     # k: tid; v: unit
#     for k, v in single_data.items():
#         #print("tid: %d" % (k))
#         for item in v:
#             threadPointList.append(TIME(0, k, item.start_time - TIME_MIN[mtx]))
#             threadPointList.append(TIME(1, k, item.start_time - TIME_MIN[mtx] + item.wait_time + item.hold_time))
#             #print("\tstart %.2f ::: wait %.2f ::: spin %.2f ::: hold %.2f ::: enter count %d" % (item.start_time - TIME_MIN[mtx],
#             #item.wait_time, item.spin_time, item.hold_time, item.enter_count))
#     threadPointList.sort(key=lambda pair: pair.time)
#
# #     print("................... thread point list ...................")
# #     for item in threadPointList:
# #         print("time %d ::: tid %d ::: status: %d" % (item.time, item.tid, item.status))
#
#     return calculation_single_inner(threadPointList)

def calculation_single(mtx, single_data):

    #print("------------------- Single MTX start: %d -------------------\n" % (mtx))
    global TIME_MIN
    global TIME_MAX
    global tid_list
    threadPointList = []
    # k: tid; v: unit
    for k, v in single_data.items():
        #print("tid: %d" % (k))
        pre_time = 0
        last_time = 0
        grouper = lambda k: k.start_time
        v.sort(key=grouper)
        for item in v:
            threadPointList.append(TIME(0, k, pre_time))
            threadPointList.append(TIME(1, k, item.start_time - TIME_MIN[mtx]))
            print("start time %d ::: end time %d" % (pre_time, item.start_time - TIME_MIN[mtx]))
            pre_time = item.start_time - TIME_MIN[mtx] + item.wait_time
            last_time = item.start_time - TIME_MIN[mtx] + item.wait_time + item.hold_time
        # TODO solve end time thread exit time
        threadPointList.append(TIME(0, k, pre_time))
        threadPointList.append(TIME(1, k, last_time))
        print("start time %d ::: end time %d" % (pre_time, last_time))

    threadPointList.sort(key=lambda pair: pair.time)
    return calculation_single_inner(threadPointList)


def calculation_single_inner(threadPointList):

    global ans
    global total

    isHold = []
    lastStamp = 0
    maxTid = 0

    # TODO: update
    for i in range(0, len(tid_list)):
        isHold.append(False)
        ans.append(0.0)

    for threadPoint in threadPointList:
        #maxTid = threadPoint.tid if maxTid < threadPoint.tid else maxTid
        nowCount = countHold(isHold)
        index = tid_list.index(threadPoint.tid)
        #print("tid %d ::: nowCount %d ::: index %d" % (threadPoint.tid, nowCount, index))

        for i in range(0, len(tid_list)):
            if isHold[i] == True:
                ans[i] += (threadPoint.time - lastStamp) * 1.0 / nowCount
                total += (threadPoint.time - lastStamp) * 1.0 / nowCount

        if threadPoint.status == 0:
            isHold[index] = True
        else:
            isHold[index] = False

        lastStamp = threadPoint.time
    return ans, total



def countHold(isHold):
    count = 0
    for item in isHold:
        if item == True:
            count = count + 1
    return count