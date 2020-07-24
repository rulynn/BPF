#!/usr/bin/env python

import itertools

def print_frame(bpf, pid, addr):
    print("\t\t%16s (%x)" % (bpf.sym(addr, pid, show_module=True, show_offset=True), addr))

def print_stack(bpf, pid, stacks, stack_id):
    for addr in stacks.walk(stack_id):
        print_frame(bpf, pid, addr)

def run(bpf, pid, locks, init_stacks, stacks):
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
            print("\tmutex %s ::: wait time %.2fus ::: hold time %.2fus ::: enter count %d" %
                  (k.mtx, v.wait_time_ns/1000.0, v.lock_time_ns/1000.0, v.enter_count))
            print_stack(bpf, pid, stacks, k.lock_stack_id)
            print("")