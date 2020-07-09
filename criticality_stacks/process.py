#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy

TIME_MIN = {}
tid_list = []

class UNIT:
    def __init__(self):
        self.start_time = 0
        self.wait_time = 0
        self.spin_time = 0
        self.hold_time = 0
        self.enter_count = 0

class TIME:
    def __init__(self, status, tid, time):
        self.status = status
        self.tid = tid
        self.time = time


def run(locks):
    output_data = preprocessed(locks)
    # print(output_data)
    for k, v in output_data.items():
        ans, ans_sum = calculation_single(k, v)
        plot(k, ans, ans_sum)
        print("")

def preprocessed(locks):

    global TIME_MIN
    output_data = {}

    for k, v in locks.items():

        # tid list
        if k not in tid_list:
            tid_list.append(k.tid)

        tmp = UNIT()
        # start time: get the lock
        tmp.start_time = v.start_time_ns/1000.0
        # wait time
        tmp.wait_time = v.wait_time_ns/1000.0
        # spin time
        tmp.spin_time = v.spin_time_ns/1000.0
        # end time: release the lock
        tmp.hold_time = v.lock_time_ns/1000.0
        tmp.enter_count = v.enter_count
        print("origin data: ")
        print("\tstart %d ::: wait %d ::: spin %d ::: hold %d ::: enter count %d" % (tmp.start_time,
                    tmp.wait_time, tmp.spin_time, tmp.hold_time, tmp.enter_count))

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

#     print("------------------- tid list start -------------------")
#     print(tid_list)
#     print("------------------- tid list end -------------------\n\n")
    return output_data


def calculation_single(mtx, single_data):

    print("Single MTX: %d \n" % (mtx))
    global TIME_MIN
    global tid_list
    threadPointList = []
    # k: tid; v: unit
    for k, v in single_data.items():
        print("tid %d" % (k))
        for item in v:
            threadPointList.append(TIME(0, k, item.start_time - TIME_MIN[mtx]))
            threadPointList.append(TIME(1, k, item.start_time - TIME_MIN[mtx] + item.wait_time + item.hold_time))
            print("\tstart %d ::: wait %d ::: spin %d ::: hold %d ::: enter count %d" % (item.start_time - TIME_MIN[mtx],
            item.wait_time, item.spin_time, item.hold_time, item.enter_count))
    threadPointList.sort(key=lambda pair: pair.time)

#     print("................... thread point list ...................")
#     for item in threadPointList:
#         print("time %d ::: tid %d ::: status: %d" % (item.time, item.tid, item.status))

    return calculation_single_inner(threadPointList)




def calculation_single_inner(threadPointList):

    isHold = []
    ans = []
    lastStamp = 0
    maxTid = 0
    ans_sum = 0

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
                ans_sum += (threadPoint.time - lastStamp) * 1.0 / nowCount

        if threadPoint.status == 0:
            isHold[index] = True
        else:
            isHold[index] = False

        lastStamp = threadPoint.time
    print("ans list: ", ans)
    print(ans_sum)
    return ans, ans_sum



def countHold(isHold):
    count = 0
    for item in isHold:
        if item == True:
            count = count + 1
    return count

def plot(mtx, ans, ans_sum):

#     print("................... plot start ...................")

    if ans_sum == 0:
        print("WARNING: ans sum is 0 ::: mtx %d" % (mtx))
        return

    global tid_list

    # plot
    pre = []
    pre.append(0)
    pre.append(0)
    pre.append(0)
    pre.append(0)
    pre.append(0)
#     print(ans)
#     print(ans_sum)
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







# delete: memory error
#def calculation_single(mtx, single_data):
#
#     global TIME_MIN
#     global tid_list
#     count_wait = numpy.zeros((len(tid_list),MAX_TIME))
#     count_hold = numpy.zeros((len(tid_list),MAX_TIME))
#     print("----- mtx %d -----" % (mtx))
#     # k: tid; v: unit
#     for k, v in single_data.items():
#
#         print("tid %d" % (k))
#
#         for item in v:
#              start = item.start_time - TIME_MIN[mtx]
#              wait = item.wait_time
#              hold = item.hold_time
#
#              # TODO: deal with this error msg
#              if start > MAX_TIME or wait > MAX_TIME or hold > MAX_TIME:
#                 print("WARNING: LARGER THAN MAX_TIME!!! start %d ::: wait %d ::: hold %d" % (start, wait, hold))
#                 continue
#              print("start %d ::: wait %d ::: hold %d" % (start, wait, hold))
#              for i in range(int(start), int(start)+int(wait)+1):
#                 count_wait[tid_list.index(k)][i] = 1
#              for i in range(int(wait), int(wait)+int(hold)+1):
#                 count_hold[tid_list.index(k)][i] = 1
#
#     # calculate
#     ans = [0 for i in range(len(tid_list))]
#     ans_sum = 0
#     for i in range(0, MAX_TIME):
#         count = 1
#         for j in range(len(tid_list)):
#             if count_wait[j][i] == 1:
#                 count = count + 1
#         for j in range(len(tid_list)):
#             if count_hold[j][i] == 1:
#                 ans[j] = ans[j] + 1.0 / count
#                 ans_sum = ans_sum + 1.0 / count
#     return ans, ans_sum