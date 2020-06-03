#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt



'''
 mtx 140583477212712
 tid 9821 ::: start time 4559337579091.74us ::: wait time 12.09us ::: hold time 11.74us
 tid 9829 ::: start time 4559337578253.24us ::: wait time 6.44us ::: hold time 3843.74us
 tid 9821 ::: start time 4559337676390.89us ::: wait time 11.44us ::: hold time 9.55us
 tid 9829 ::: start time 4559337675631.71us ::: wait time 6.37us ::: hold time 801.48us
 ...
 mtx 140583474812712
 tid 9829 ::: start time 4559337550801.24us ::: wait time 8.10us ::: hold time 9.87us
 tid 9829 ::: start time 4559337564650.30us ::: wait time 13.37us ::: hold time 10.42us
 tid 9826 ::: start time 4559337556437.01us ::: wait time 6.29us ::: hold time 8580.89us
 tid 9829 ::: start time 4559337655876.76us ::: wait time 13.17us ::: hold time 8.95us
 ...
'''

class item_t:
    def __init__(self):
        self.tid = 0
        self.start_time_ns = 0
        self.wait_time_ns = 0
        self.lock_time_ns = 0

output_data = {}
#count = 0
start_time_min = 999999999999999
def collect_data(locks):
    for k, v in locks.items():
        # TODO: How to identify the thread
        tmp = item_t()
        tmp.tid = k.tid
        tmp.start_time_ns = v.start_time_ns/1000.0
        tmp.wait_time_ns = v.wait_time_ns/1000.0
        tmp.lock_time_ns = v.lock_time_ns/1000.0

        if output_data.get(k.mtx) == None:
            output_data[k.mtx] = []
        output_data[k.mtx].append(tmp)

        global start_time_min
        start_time_min = min(start_time_min, v.start_time_ns/1000.0)
    # plot
    plot_data(output_data)

def statistical_data(locks):
    for k, v in locks.items():
        print("\t tid %d ::: mtx %d" % (k.tid, k.mtx))
        print("\t start time %.2fus ::: wait time %.2fus ::: hold time %.2fus ::: enter count %d" %
            (v.start_time_ns, v.wait_time_ns, v.lock_time_ns, v.enter_count))
#     for k, v in output_data.items():
#         print("\t mtx %d" % (k))
#         for item in v:
#             print("\t tid %d ::: start time %.2fus ::: wait time %.2fus ::: hold time %.2fus" %
#             (item.tid, item.start_time_ns, item.wait_time_ns, item.lock_time_ns))
#     output_data.clear()

tid_dict = {}
tid_id = 0
def plot_data(output_data):
    for k, v in output_data.items():
        print("\t mtx %d" % (k))
        for item in v:
            global tid_id
            global tid_dict
            if tid_dict.get(item.tid) == None:
                tid_dict[item.tid] = tid_id
                tid_id = tid_id + 1

            print("\t tid %d ::: start time %.2fus ::: wait time %.2fus ::: hold time %.2fus" %
                        (item.tid, item.start_time_ns, item.wait_time_ns, item.lock_time_ns))

            x = [tid_dict[item.tid],tid_dict[item.tid]]
            start_time = item.start_time_ns - start_time_min
            plt.plot(x, [start_time, start_time + item.wait_time_ns], color='dimgray', label='wait')
            plt.plot(x, [start_time + item.wait_time_ns, start_time + item.wait_time_ns + item.lock_time_ns] , color='firebrick', label='hold')

        # output
        path = "out/" + str(k) + ".png"
        plt.savefig(path)

    output_data.clear()

