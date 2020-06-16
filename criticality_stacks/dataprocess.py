#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt


INTERVAL = 20
TIME_MAX = 0
TIME_MIN = 999999999999999

class item_mtx:
    def __init__(self):
        self.tid = 0
        self.start_time_ns = 0
        self.wait_time_ns = 0
        self.lock_time_ns = 0


class item_tid:
    def __init__(self):
        self.mtx = 0
        self.start_time = 0
        self.wait_time = 0
        self.lock_time = 0

def critical_calculation(locks):

    output_data = {}


    for k, v in locks.items():
        tmp = item_tid()
        tmp.mtx = k.mtx

        # start time: get the lock
        tmp.start_time = v.start_time_ns/1000.0
        # wait time
        tmp.wait_time = tmp.start_time + v.wait_time_ns/1000.0
        # end time: release the lock
        tmp.lock_time = tmp.wait_time + v.lock_time_ns/1000.0

        if output_data.get(k.tid) == None:
            output_data[k.tid] = []
        output_data[k.tid].append(tmp)

        # Used to calculate relative time: time - (minimum start time)
        TIME_MIN = min(TIME_MIN, tmp.start_time)
        TIME_MAX = max(TIME_MAX, tmp.lock_time)

    # plot critical stack
    critical_calculation_inner_plot(output_data)
    critical_calculation_inner(output_data)


# plot critical stack
def critical_calculation_inner_plot(output_data):
    tid_id = 0
    count_wait = []
    count_hold = []
    # Divide hold time into $INTERVAL time intervals
    for k, v in output_data.items():
        # init
        count_wait.append([0 for i in range(INTERVAL)])
        count_hold.append([0 for i in range(INTERVAL)])
        for item in v:
            start = (item.start_time - TIME_MIN) // (TIME_MAX // INTERVAL + 1)
            wait = (item.wait_time - TIME_MIN) // (TIME_MAX // INTERVAL + 1)
            for i in range(int(start), int(wait)+1):
                count_wait[tid_id][i] = 1
            hold = (item.lock_time - TIME_MIN) // (TIME_MAX // INTERVAL + 1)
            for i in range(int(wait), int(hold)+1):
                count_hold[tid_id][i] = 1
        tid_id = tid_id + 1

    # Calculate criticality: 1.0 / Number of threads waiting in the current interval....
    ans = [0 for i in range(tid_id)]
    ans_sum = 0
    for i in range(0, INTERVAL):
        count = 0
        for j in range(0, tid_id):
            if count_wait[j][i] == 1:
                count = count + 1
        # ZeroDivisionError
        if count == 0:
            continue
        for j in range(0, tid_id):
            if count_hold[j][i] == 1:
                ans[j] = ans[j] + 1.0 / count
                ans_sum = ans_sum + 1.0 / count
#     print(ans)
#     print(ans_sum)
    # plot
    pre = 0
    for i in range(0, tid_id):
        label = "thread " + str(i)
        plt.plot([0, 0], [pre/ans_sum, (pre + ans[i])/ans_sum], label=label)
        # print(pre/ans_sum, (pre + ans[i])/ans_sum)
        pre = pre + ans[i]

    plt.ylim(0,1)
    path = "out/critical.png"
    plt.savefig(path)

# print data
def critical_calculation_inner(output_data):
    tid_id = 0
    for k, v in output_data.items():
        print("========= pid %d =========" % (k))
        for item in v:
            start = (item.start_time - TIME_MIN) // (TIME_MAX // INTERVAL + 1)
            wait = (item.wait_time - TIME_MIN) // (TIME_MAX // INTERVAL + 1)
            hold = (item.lock_time - TIME_MIN) // (TIME_MAX // INTERVAL + 1)

            print("\t mtx %d ::: start time %.2fus ::: wait time %.2fus ::: hold time %.2fus :::start block %d ::: wait block %d ::: hold block %d" % (item.mtx, item.start_time - start_time_min,
            item.wait_time - TIME_MIN, item.lock_time - TIME_MIN, start, wait, hold))

            plt.plot([tid_id, tid_id], [start, wait+1], color='dimgray')
            plt.plot([tid_id, tid_id], [wait, hold+1], color='red')

        tid_id = tid_id + 1

    plt.ylim(0,INTERVAL)
    plt.xlabel("barrier")
    plt.ylabel("time")
    path = "out/threads.png"
    plt.savefig(path)


