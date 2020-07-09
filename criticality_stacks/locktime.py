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

# stack.main(bpf, pid, locks, init_stacks, stacks)



def print_frame(bpf, pid, addr):
    print("\t\t%16s (%x)" % (bpf.sym(addr, pid, show_module=True, show_offset=True), addr))

def print_stack(bpf, pid, stacks, stack_id):
    for addr in stacks.walk(stack_id):
        print_frame(bpf, pid, addr)

def stack_fun():
    print("................... stack start ...................")
    mutex_ids = {}
    next_mutex_id = 1
    for k, v in init_stacks.items():
        mutex_id = "#%d" % next_mutex_id
        next_mutex_id += 1
        mutex_ids[k.value] = mutex_id
        print("init stack for mutex %x (%s)" % (k.value, mutex_id))
        print_stack(bpf, pid, stacks, v.value)
        print("")
    grouper = lambda (k, v): k.tid
    sorted_by_thread = sorted(locks.items(), key=grouper)
    locks_by_thread = itertools.groupby(sorted_by_thread, grouper)
    for tid, items in locks_by_thread:
        print("thread %d" % tid)
        for k, v in sorted(items, key=lambda (k, v): -v.wait_time_ns):
            #mutex_descr = mutex_ids[k.mtx] if k.mtx in mutex_ids else bpf.sym(k.mtx, pid)
            print("\tmtx %s ::: wait time %.2fus ::: hold time %.2fus ::: enter count %d" %
                  (k.mtx, v.wait_time_ns/1000.0, v.lock_time_ns/1000.0, v.enter_count))
            print_stack(bpf, pid, stacks, k.lock_stack_id)
            print("")

stack_fun()