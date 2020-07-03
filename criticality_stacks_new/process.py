#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy

MAX_TIME = 50000
TIME_MIN = {}
tid_list = []

class unit:
    def __init__(self):
        self.start_time = 0
        self.wait_time = 0
        self.hold_time = 0

def critical_calculation(locks):
    output_data = preprocessed(locks)
    # print(output_data)
    for k, v in output_data.items():
        ans, ans_sum = calculation_single(k, v)
        plot(k, ans, ans_sum)

def preprocessed(locks):

    global TIME_MIN
    output_data = {}

    for k, v in locks.items():

        # tid list
        if k not in tid_list:
            tid_list.append(k.tid)

        tmp = unit()
        # start time: get the lock
        tmp.start_time = v.start_time_ns/1000.0
        # wait time
        tmp.wait_time = tmp.start_time + v.wait_time_ns/1000.0
        # end time: release the lock
        tmp.hold_time = tmp.wait_time + v.lock_time_ns/1000.0

#         # save data
        if output_data.get(k.mtx) == None:
            output_data[k.mtx] = {}
        if output_data[k.mtx].get(k.tid) == None:
            output_data[k.mtx][k.tid] = []
        output_data[k.mtx][k.tid].append(tmp)

        # Used to calculate relative time: time - TIME_MIN
        if TIME_MIN.get(k.mtx) == None:
            TIME_MIN[k.mtx] = 999999999999999
        TIME_MIN[k.mtx] = min(TIME_MIN[k.mtx], tmp.start_time)

    return output_data


def calculation_single(mtx, single_data):

    global TIME_MIN
    global tid_list
    count_wait = numpy.zeros((len(tid_list),MAX_TIME))
    count_hold = numpy.zeros((len(tid_list),MAX_TIME))
    print(tid_list)
    # k: tid; v: unit
    for k, v in single_data.items():

        print("tid %d" % (k))

        for item in v:
             start = item.start_time - TIME_MIN[mtx]
             wait = item.wait_time - TIME_MIN[mtx]
             hold = item.hold_time - TIME_MIN[mtx]

             # TODO: deal with this error msg
             if start > MAX_TIME or wait > MAX_TIME or hold > MAX_TIME:
                print("WARNING: LARGER THAN MAX_TIME!!! start %d ::: wait %d ::: hold %d" % (start, wait, hold))
                continue
             print("start %d ::: wait %d ::: hold %d" % (start, wait, hold))
             for i in range(int(start), int(wait)+1):
                count_wait[tid_list.index(k)][i] = 1
             for i in range(int(wait), int(hold)+1):
                count_hold[tid_list.index(k)][i] = 1

    # calculate
    ans = [0 for i in range(len(tid_list))]
    ans_sum = 0
    for i in range(0, MAX_TIME):
        count = 1
        for j in range(len(tid_list)):
            if count_wait[j][i] == 1:
                count = count + 1
        for j in range(len(tid_list)):
            if count_hold[j][i] == 1:
                ans[j] = ans[j] + 1.0 / count
                ans_sum = ans_sum + 1.0 / count
    return ans, ans_sum

def plot(mtx, ans, ans_sum):

    global tid_list

    # plot
    pre = []
    pre.append(0)
    pre.append(0)
    pre.append(0)
    pre.append(0)
    pre.append(0)
    print(ans)
    for i in range(len(tid_list)):
        label = "thread " + str(i)
        width = 0.35

        now = []
        now.append(pre[0] + ans[i]/ans_sum)
        now.append(0)
        now.append(0)
        now.append(0)
        now.append(0)
        plt.bar((1,2,3,4,5), now, width, bottom=pre, label=label)

        pre = now


    #plt.grid(axis="y")
    plt.ylim(0,1)
    #plt.legend()
    path = "out/critical-" + str(mtx) + ".png"
    plt.savefig(path)