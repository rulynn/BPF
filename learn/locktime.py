#!/usr/bin/env python

import sys
import itertools
from time import sleep
from bcc import BPF

class item_t:
    def __init__(self):
        self.mtx = 0
        self.start_time_ns = 0
        self.wait_time_ns = 0
        self.lock_time_ns = 0

if len(sys.argv) < 2:
    print("USAGE: need PID")
    exit()
pid = sys.argv[1]
debug = 0

# load BPF program
bpf = BPF(src_file = "locktime.c")
bpf.attach_uprobe(name="pthread", sym="pthread_mutex_lock", fn_name="probe_mutex_lock", pid=int(pid))
bpf.attach_uretprobe(name="pthread", sym="pthread_mutex_lock", fn_name="probe_mutex_lock_return", pid=int(pid))
bpf.attach_uprobe(name="pthread", sym="pthread_mutex_unlock", fn_name="probe_mutex_unlock", pid=int(pid))

output_data = {}
count = 0
# process event
def print_event(cpu, data, size):
    event = bpf["events"].event(data)
    # print(dir(event))
    # print("\t tid %d ::: mtx %d ::: start time %.2fus ::: wait time %.2fus ::: hold time %.2fus" %
    #     (event.tid, event.mtx, event.start_time_ns/1000.0, event.wait_time_ns/1000.0, event.lock_time_ns/1000.0))


    tmp = item_t()
    tmp.mtx = event.mtx
    tmp.start_time_ns = event.start_time_ns/1000.0
    tmp.wait_time_ns = event.wait_time_ns/1000.0
    tmp.lock_time_ns = event.lock_time_ns/1000.0

    if output_data.get(event.tid) == None:
        output_data[event.tid] = []
    output_data[event.tid].append(tmp)

    global count
    count = count + 1
    if count % 200 == 0:
        statistical_data(output_data)


def statistical_data(output_data):
    print("------ ", count, " ------")
    for k, v in output_data.items():
        print("\t tid %d" % (k))
        for item in v:
            print("\t mtx %d ::: start time %.2fus ::: wait time %.2fus ::: hold time %.2fus" %
            (item.mtx, item.start_time_ns, item.wait_time_ns, item.lock_time_ns))



# loop with callback to print_event
bpf["events"].open_perf_buffer(print_event)
while 1:
    try:
        bpf.perf_buffer_poll()
    except KeyboardInterrupt:
        exit()