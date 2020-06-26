#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt


INTERVAL = 1000
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
    global TIME_MIN
    global TIME_MAX

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

        # Used to calculate relative time: time - TIME_MIN
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
    global TIME_MIN
    global TIME_MAX

    # Divide hold time into $INTERVAL time intervals
    for k, v in output_data.items():
        # init
        count_wait.append([0 for i in range(INTERVAL)])
        count_hold.append([0 for i in range(INTERVAL)])
        for item in v:
            # time: Time occupied by each time interval
            time = (TIME_MAX - TIME_MIN) // INTERVAL + 1
            # Calculate start time block and wait time block
            start = (item.start_time - TIME_MIN) // time
            wait = (item.wait_time - TIME_MIN) // time
            for i in range(int(start), int(wait)+1):
                count_wait[tid_id][i] = 1
            hold = (item.lock_time - TIME_MIN) // time
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

    # plot
    pre = []
    pre.append(0)
    pre.append(0)
    pre.append(0)
    print(ans)
    for i in range(0, tid_id):
        label = "thread " + str(i)
        width = 1

        #plt.plot([0, 0], [pre/ans_sum, (pre + ans[i])/ans_sum], label=label)

        #width = 1
        #p2 = plt.bar(0, (pre + ans[i])/ans_sum, width, bottom=pre/ans_sum, label=label)

        #print(pre/ans_sum, (pre + ans[i])/ans_sum)
        #pre = pre + ans[i]


        now = []
        now.append((pre[0] + ans[i])/ans_sum)
        now.append(0)
        now.append(0)
        plt.bar((1,2,3), now, width, bottom=pre, label=label)

        pre[0] = now[0]

        print(pre)
        print(now)

    plt.ylim(0,1)
    plt.legend()
    path = "out/critical.png"
    plt.savefig(path)

# print data
def critical_calculation_inner(output_data):
    tid_id = 0
    global TIME_MIN
    global TIME_MAX
    time = (TIME_MAX - TIME_MIN) // INTERVAL + 1
    print("max time %d ::: min time %d ::: time %d" % (TIME_MAX, TIME_MIN, time))
    for k, v in output_data.items():
        print("--- pid %d ---" % (k))
        for item in v:

            start = (item.start_time - TIME_MIN) // time
            wait = (item.wait_time - TIME_MIN) // time
            hold = (item.lock_time - TIME_MIN) // time

            print("\t mtx %d ::: start time %.2fus ::: wait time %.2fus ::: hold time %.2fus" % (item.mtx, item.start_time - TIME_MIN,
            item.wait_time - item.start_time, item.lock_time - item.wait_time))

#             plt.plot([tid_id, tid_id], [start, wait+1], color='dimgray')
#             plt.plot([tid_id, tid_id], [wait, hold+1], color='red')

        tid_id = tid_id + 1

#     plt.ylim(0,INTERVAL)
#     plt.xlabel("barrier")
#     plt.ylabel("time")
#     path = "out/threads.png"
#     plt.savefig(path)


def default_calculation(locks):
    output_data = {}
    start_time_min = 999999999999999
    for k, v in locks.items():
        # TODO: How to identify the thread
        tmp = item_mtx()
        tmp.tid = k.tid
        tmp.start_time_ns = v.start_time_ns/1000.0
        tmp.wait_time_ns = v.wait_time_ns/1000.0
        tmp.lock_time_ns = v.lock_time_ns/1000.0

        if output_data.get(k.mtx) == None:
            output_data[k.mtx] = []
        output_data[k.mtx].append(tmp)

        start_time_min = min(start_time_min, v.start_time_ns/1000.0)
    # plot
    default_calculation_inner(output_data, start_time_min)

def default_calculation_inner(output_data, start_time_min):
    tid_dict = {}
    tid_id = 0
    for k, v in output_data.items():
        print("\t mtx %d" % (k))
        for item in v:
            if tid_dict.get(item.tid) == None:
                tid_dict[item.tid] = tid_id
                tid_id = tid_id + 1

            x = [tid_dict[item.tid],tid_dict[item.tid]]
            start_time = item.start_time_ns - start_time_min
            print("\t tid %d ::: start time %.2fus ::: wait time %.2fus ::: hold time %.2fus" %
                                    (item.tid, start_time, item.wait_time_ns, item.lock_time_ns))

            plt.plot(x, [start_time, start_time + item.wait_time_ns], color='dimgray', label='wait')
            plt.plot(x, [start_time + item.wait_time_ns, start_time + item.wait_time_ns + item.lock_time_ns] ,
                        color='firebrick', label='hold')

        # output
        path = "out/" + str(k) + ".png"
        plt.savefig(path)
