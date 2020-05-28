#!/usr/bin/env python


'''
 tid 10540
 mtx 140286051165992 ::: start time 4466668547206.98us ::: wait time 24.28us ::: hold time 17.93us
 mtx 140286050976040 ::: start time 4466668547273.42us ::: wait time 6.67us ::: hold time 123.10us
 mtx 140286050846248 ::: start time 4466668547412.12us ::: wait time 6.32us ::: hold time 4.86us
 mtx 140286050976040 ::: start time 4466668547443.03us ::: wait time 6.59us ::: hold time 317.44us
 mtx 140286051165992 ::: start time 4466668547775.50us ::: wait time 6.30us ::: hold time 2.88us
 ...
 tid 10541
 mtx 140286050853416 ::: start time 4466668547464.24us ::: wait time 6.57us ::: hold time 7.88us
 mtx 140286050846248 ::: start time 4466668547496.15us ::: wait time 6.64us ::: hold time 228.56us
 mtx 140286050976040 ::: start time 4466668547739.79us ::: wait time 6.36us ::: hold time 3.14us
 mtx 140286050846248 ::: start time 4466668547757.39us ::: wait time 6.31us ::: hold time 124.19us
 mtx 140286050853416 ::: start time 4466668547896.45us ::: wait time 6.35us ::: hold time 2.73us
 ...
'''

class item_t:
    def __init__(self):
        self.mtx = 0
        self.start_time_ns = 0
        self.wait_time_ns = 0
        self.lock_time_ns = 0


output_data = {}
count = 0
start_time = 999999999999999
def collect_data(event):
    # TODO: How to identify the thread
    tmp = item_t()
    tmp.mtx = event.mtx
    tmp.start_time_ns = event.start_time_ns/1000.0
    tmp.wait_time_ns = event.wait_time_ns/1000.0
    tmp.lock_time_ns = event.lock_time_ns/1000.0

    if output_data.get(event.tid) == None:
        output_data[event.tid] = []
    output_data[event.tid].append(tmp)

    global start_time
    start_time = min(start_time, event.start_time_ns/1000.0)
    global count
    count = count + 1
    if count == 1000:
        statistical_data(output_data)

def statistical_data(output_data):
    #print("------ ", count, " ------")
    for k, v in output_data.items():
        print("\t tid %d" % (k))
        for item in v:
            print("\t mtx %d ::: start time %.2fus ::: wait time %.2fus ::: hold time %.2fus" %
            (item.mtx, item.start_time_ns, item.wait_time_ns, item.lock_time_ns))
    output_data.clear()


#def plot_data():
