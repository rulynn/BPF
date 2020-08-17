#!/usr/bin/env python

import sys
import itertools
from time import sleep
from bcc import BPF, USDT
import process
import stack
import itertools

if len(sys.argv) < 3:
    print("USAGE: need PID and time")
    exit()
pid = sys.argv[1]
time = sys.argv[2]
isStack = False

# usdt = USDT(pid=int(pid))
# usdt.enable_probe_or_bail("pthread_create", "trace_pthread")

# load BPF program
if isStack == True:
#     usdt.enable_probe_or_bail("thread__start", "trace_start")
#     usdt.enable_probe_or_bail("thread__stop", "trace_stop")
#     bpf = BPF(src_file = "locktime_stack.c", usdt_contexts=[usdt])
    bpf = BPF(src_file = "locktime_stack.c")
    bpf.attach_uprobe(name="pthread", sym="pthread_mutex_init", fn_name="probe_mutex_init", pid=int(pid))
else:
    bpf = BPF(src_file = "locktime.c", usdt_contexts=[usdt])
bpf.attach_uprobe(name="pthread", sym="pthread_mutex_lock", fn_name="probe_mutex_lock", pid=int(pid))
bpf.attach_uretprobe(name="pthread", sym="pthread_mutex_lock", fn_name="probe_mutex_lock_return", pid=int(pid))
bpf.attach_uprobe(name="pthread", sym="pthread_mutex_unlock", fn_name="probe_mutex_unlock", pid=int(pid))

# new
bpf.attach_uprobe(name="pthread", sym="pthread_create", fn_name="probe_create", pid=int(pid))
bpf.attach_uprobe(name="pthread", sym="pthread_start", fn_name="trace_pthread", pid=int(pid))
# bpf.attach_uprobe(name="pthread", sym="pthread_exit", fn_name="probe_exit", pid=int(pid))
# bpf.attach_uprobe(name="pthread", sym="pthread_mutex_trylock", fn_name="probe_mutex_trylock", pid=int(pid))
bpf.attach_uprobe(name="pthread", sym="pthread_join", fn_name="probe_join", pid=int(pid))
# bpf.attach_uprobe(name="pthread", sym="pthread_cancel", fn_name="probe_cancel", pid=int(pid))
# bpf.attach_uprobe(name="pthread", sym="pthread_barrier_init", fn_name="probe_barrier_init", pid=int(pid))


locks = bpf["locks"]
times = bpf["times"]
sleep(int(time))

if isStack == True:
    process.run(locks, times, True)
    stack.run_sub(bpf, int(pid), locks)
    times = bpf["times"]
    print(len(times))
    for k, v in times.items():
        print(k.tid, k.timestamp, k.type)

#     stack.run(bpf, int(pid), locks, init_stacks, stacks)
else:
    process.run(locks, times, False)
    times = bpf["times"]
    print(len(times))
    for k, v in times.items():
        print(k.tid, k.timestamp, k.type)