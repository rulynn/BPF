#!/usr/bin/env python


def main(init_stacks, stacks):
    while True:
        sleep(5)
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
                mutex_descr = mutex_ids[k.mtx] if k.mtx in mutex_ids else bpf.sym(k.mtx, pid)
                print("\tmutex %s ::: wait time %.2fus ::: hold time %.2fus ::: enter count %d" %
                      (mutex_descr, v.wait_time_ns/1000.0, v.lock_time_ns/1000.0, v.enter_count))
                print_stack(bpf, pid, stacks, k.lock_stack_id)
                print("")