#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt


INTERVAL = 1000

TIME_MAX = {}
TIME_MIN = {}

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
    global TIME_MIN
    global TIME_MAX

    for k, v in locks.items():
        tmp = item_mtx()
        tmp.tid = k.tid

        # start time: get the lock
        tmp.start_time = v.start_time_ns/1000.0
        # wait time
        tmp.wait_time = tmp.start_time + v.wait_time_ns/1000.0
        # end time: release the lock
        tmp.lock_time = tmp.wait_time + v.lock_time_ns/1000.0

        if output_data.get(k.mtx) == None:
            output_data[k.mtx] = []
        output_data[k.mtx].append(tmp)

        # Used to calculate relative time: time - TIME_MIN
        if TIME_MIN.get(k.mtx) == None:
            TIME_MIN[k.mtx] = 999999999999999
        if TIME_MAX.get(k.mtx) == None:
                    TIME_MAX[k.mtx] = 0
        TIME_MIN[k.mtx] = min(TIME_MIN[k.mtx], tmp.start_time)
        TIME_MAX[k.mtx] = max(TIME_MAX[k.mtx], tmp.lock_time)

    # plot critical stack
    critical_calculation_inner_plot_mul(output_data)
    critical_calculation_inner(output_data)


# plot critical stack
def critical_calculation_inner_plot_mul(output_data):
    # Divide hold time into $INTERVAL time intervals
    for k, v in output_data.items():
        single_data = {}

        for item in v:

            tmp = item_tid()
            tmp.mtx = k

            # start time: get the lock
            tmp.start_time = item.start_time
            # wait time
            tmp.wait_time = item.wait_time
            # end time: release the lock
            tmp.lock_time = item.lock_time

            if output_data.get(item.tid) == None:
                single_data[item.tid] = []
            single_data[item.tid].append(tmp)
        critical_calculation_inner_plot(k, single_data)

def critical_calculation_inner_plot(mtx, single_data):

    count_wait = []
    count_hold = []
    tid_id = 0
    global TIME_MIN
    global TIME_MAX

    # init
    count_wait.append([0 for i in range(INTERVAL)])
    count_hold.append([0 for i in range(INTERVAL)])

    # Divide hold time into $INTERVAL time intervals
    for k, v in single_data.items():
        # init
        count_wait.append([0 for i in range(INTERVAL)])
        count_hold.append([0 for i in range(INTERVAL)])
        print("--- tid %d ---" % (k))
        for item in v:
            # time: Time occupied by each time interval
            time = (TIME_MAX[mtx] - TIME_MIN[mtx]) // INTERVAL + 1
            print("time %d", % (time))
            # Calculate start time block and wait time block
            start = (item.start_time - TIME_MIN[mtx]) // time
            wait = (item.wait_time - TIME_MIN[mtx]) // time
            for i in range(int(start), int(wait)+1):
                count_wait[tid_id][i] = 1
            hold = (item.lock_time - TIME_MIN[mtx]) // time
            for i in range(int(wait), int(hold)+1):
                count_hold[tid_id][i] = 1
            print(count_wait)
            print(count_hold)
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
    print(mtx)
    print(ans)

    # plot
    pre = []
    pre.append(0)
    pre.append(0)
    pre.append(0)
    pre.append(0)
    pre.append(0)
    print(ans)
    for i in range(0, tid_id):
        label = "thread " + str(i)
        width = 0.35

        #plt.plot([0, 0], [pre/ans_sum, (pre + ans[i])/ans_sum], label=label)

        #width = 1
        #p2 = plt.bar(0, (pre + ans[i])/ans_sum, width, bottom=pre/ans_sum, label=label)

        #print(pre/ans_sum, (pre + ans[i])/ans_sum)
        #pre = pre + ans[i]


        now = []
        now.append(pre[0] + ans[i]/ans_sum)
        now.append(0)
        now.append(0)
        now.append(0)
        now.append(0)
        plt.bar((1,2,3,4,5), now, width, bottom=pre, label=label)

        pre = now


    plt.grid(axis="y")
    plt.ylim(0,1)
    plt.legend()
    path = "out/critical-" + str(mtx) + ".png"
    plt.savefig(path)


# print data
def critical_calculation_inner(output_data):
    tid_id = 0
    global TIME_MIN
    global TIME_MAX

    for k, v in output_data.items():
        print("--- mtx %d ---" % (k))
        time = (TIME_MAX[k] - TIME_MIN[k]) // INTERVAL + 1
        for item in v:

            start = (item.start_time - TIME_MIN[k]) // time
            wait = (item.wait_time - TIME_MIN[k]) // time
            hold = (item.lock_time - TIME_MIN[k]) // time

            print("\t tid %d ::: start time %.2fus ::: wait time %.2fus ::: hold time %.2fus" % (item.tid, item.start_time - TIME_MIN[k],
            item.wait_time - item.start_time, item.lock_time - item.wait_time))

        tid_id = tid_id + 1