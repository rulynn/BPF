#!/usr/bin/env python

import sys
import itertools
from time import sleep
from bcc import BPF
import process
import stack
import itertools

if len(sys.argv) < 3:
    print("USAGE: need PID and time")
    exit()
pid = sys.argv[1]
time = sys.argv[2]
isStack = True

# load BPF program
if isStack == True:
    bpf = BPF(src_file = "locktime_stack.c")
    bpf.attach_uprobe(name="pthread", sym="pthread_mutex_init", fn_name="probe_mutex_init", pid=int(pid))
else:
    bpf = BPF(src_file = "locktime.c")
bpf.attach_uprobe(name="pthread", sym="pthread_mutex_lock", fn_name="probe_mutex_lock", pid=int(pid))
bpf.attach_uretprobe(name="pthread", sym="pthread_mutex_lock", fn_name="probe_mutex_lock_return", pid=int(pid))
bpf.attach_uprobe(name="pthread", sym="pthread_mutex_unlock", fn_name="probe_mutex_unlock", pid=int(pid))

# new
bpf.attach_uprobe(name="pthread", sym="pthread_create", fn_name="probe_create", pid=int(pid))
bpf.attach_uprobe(name="pthread", sym="pthread_exit", fn_name="probe_exit", pid=int(pid))

locks = bpf["locks"]

sleep(int(time))
if isStack == True:
    process.run(locks, True)
    stack.run_sub(bpf, int(pid), locks)
    test = bpf["test"]
    print(len(test))
    for k, v in test.items():
        print(k.value, v.value)

#     stack.run(bpf, int(pid), locks, init_stacks, stacks)
else:
    process.run(locks, False)