#!/usr/bin/env python

import sys
import itertools
from time import sleep
from bcc import BPF
import process
import stack


if len(sys.argv) < 3:
    print("USAGE: need PID and time")
    exit()
pid = sys.argv[1]
time = sys.argv[2]
debug = 0

# load BPF program
bpf = BPF(src_file = "locktime_stack.c")
bpf.attach_uprobe(name="pthread", sym="pthread_mutex_init", fn_name="probe_mutex_init", pid=int(pid))
bpf.attach_uprobe(name="pthread", sym="pthread_mutex_lock", fn_name="probe_mutex_lock", pid=int(pid))
bpf.attach_uretprobe(name="pthread", sym="pthread_mutex_lock", fn_name="probe_mutex_lock_return", pid=int(pid))
bpf.attach_uprobe(name="pthread", sym="pthread_mutex_unlock", fn_name="probe_mutex_unlock", pid=int(pid))

locks = bpf["locks"]
init_stacks = bpf["init_stacks"]
stacks = bpf["stacks"]
sleep(int(time))
process.main(locks)
stack.main(locks, init_stacks, stacks)