#!/usr/bin/env python

import sys
import itertools
from time import sleep
from bcc import BPF
import dataprocess as dp


if len(sys.argv) < 3:
    print("USAGE: need PID and time")
    exit()
pid = sys.argv[1]
time = sys.argv[2]
debug = 0

# load BPF program
bpf = BPF(src_file = "locktime.c")
bpf.attach_uprobe(name="pthread", sym="pthread_mutex_lock", fn_name="probe_mutex_lock", pid=int(pid))
bpf.attach_uretprobe(name="pthread", sym="pthread_mutex_lock", fn_name="probe_mutex_lock_return", pid=int(pid))
bpf.attach_uprobe(name="pthread", sym="pthread_mutex_unlock", fn_name="probe_mutex_unlock", pid=int(pid))


locks = bpf["locks"]
sleep(int(time))
dp.default_calculation(locks)


# # process event
# def print_event(cpu, data, size):
#     event = bpf["events"].event(data)
#     dp.collect_data(event)
#
# # loop with callback to print_event
# bpf["events"].open_perf_buffer(print_event)
# while 1:
#     try:
#         bpf.perf_buffer_poll()
#     except KeyboardInterrupt:
#         exit()