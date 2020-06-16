#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt


TIME = 15000000
INTERVAL = 20


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
        self.end_time = 0

def critical_calculation(locks):

    output_data = {}
    start_time_min = 999999999999999

    for k, v in locks.items():
        tmp = item_tid()
        tmp.mtx = k.mtx
        # start time: get the lock
        tmp.start_time = v.start_time_ns/1000.0 + v.wait_time_ns/1000.0
        # end time: release the lock
        tmp.end_time = tmp.start_time + v.lock_time_ns/1000.0

        if output_data.get(k.tid) == None:
            output_data[k.tid] = []
        output_data[k.tid].append(tmp)
        print("\t tid %d ::: start time %.2fus ::: end time %.2fus" % (k.tid, tmp.start_time, tmp.end_time))
        # Used to calculate relative time: time - (minimum start time)
        start_time_min = min(start_time_min, v.start_time_ns/1000.0)

    # plot critical stack
    critical_calculation_inner(output_data, start_time_min)
    # plot
    critical_calculation_inner_plot(output_data, start_time_min)

# plot critical stack
def critical_calculation_inner(output_data, start_time_min):

    tid_id = 0
    count_arr = []
    # Divide hold time into 20 time intervals
    for k, v in output_data.items():
        count_arr.append([0 for i in range(INTERVAL)])
        for item in v:
            start = (item.start_time - start_time_min) // (TIME // INTERVAL)
            end = (item.end_time - start_time_min) // (TIME // INTERVAL) + 1
            for i in range(int(start), int(end)):
                count_arr[tid_id][i] = 1
        tid_id = tid_id + 1

    # Calculate criticality: 1.0 / Number of threads running in the current interval?
    # TODO: 1.0 / Number of threads waiting in the current interval....
    ans = [0 for i in range(tid_id)]
    ans_sum = 0
    for i in range(0, INTERVAL):
        count = 0
        for j in range(0, tid_id):
            if count_arr[j][i] == 1:
                count = count + 1
        for j in range(0, tid_id):
            if count_arr[j][i] == 1:
                ans[j] = ans[j] + 1.0 / count
                ans_sum = ans_sum + 1.0 / count
    print(ans)
    print(ans_sum)
    # plot
    pre = 0
    for i in range(0, tid_id):
        plt.plot([0, 0], [pre/ans_sum, (pre + ans[i])/ans_sum])
        print(pre/ans_sum, (pre + ans[i])/ans_sum)
        pre = pre + ans[i]

    path = "out/critical.png"
    plt.savefig(path)

def critical_calculation_inner_plot(output_data, start_time_min):
    tid_id = 0
    for k, v in output_data.items():

        for item in v:
            start = (item.start_time - start_time_min) // (TIME // INTERVAL)
            end = (item.end_time - start_time_min) // (TIME // INTERVAL) + 1

            print("\t start time %.2fus ::: end time %.2fus" % (item.start_time - start_time_min, item.end_time - start_time_min))
            print("\t tid %d ::: start %d ::: end %d" % (tid_id, start, end))

            plt.plot([tid_id, tid_id], [start, end], color='dimgray')

        tid_id = tid_id + 1

    path = "out/" + str(tid_id) + ".png"
    plt.savefig(path)



