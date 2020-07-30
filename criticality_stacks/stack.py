#!/usr/bin/env python

import itertools

def print_frame(bpf, pid, addr):
    print("\t\t%16s (%x)" % (bpf.sym(addr, pid, show_module=True, show_offset=True), addr))

def print_stack(bpf, pid, stacks, stack_id):
    for addr in stacks.walk(stack_id):
        print_frame(bpf, pid, addr)

def run(bpf, pid, locks, init_stacks, stacks):
    mutex_ids = {}
    next_mutex_id = 1
    for k, v in init_stacks.items():
        mutex_id = "#%d" % next_mutex_id
        next_mutex_id += 1
        mutex_ids[k.value] = mutex_id
        #print("init stack for mutex %x (%s)" % (k.value, mutex_id))
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


def test_stack(bpf):

    # output stacks
    missing_stacks = 0
    has_collision = False
    counts = bpf.get_table("counts")
    stack_traces = bpf.get_table("stack_traces")

    for k, v in sorted(counts.items(), key=lambda counts: counts[1].value):
        user_stack = [] if k.user_stack_id < 0 else \
            stack_traces.walk(k.user_stack_id)
        kernel_tmp = [] if k.kernel_stack_id < 0 else \
            stack_traces.walk(k.kernel_stack_id)

        user_stack = list(user_stack)
        kernel_stack = list(kernel_stack)
        print(user_stack)
#         line = [k.name]
#         # if we failed to get the stack is, such as due to no space (-ENOMEM) or
#         # hash collision (-EEXIST), we still print a placeholder for consistency
#         if not args.kernel_stacks_only:
#             if stack_id_err(k.user_stack_id):
#                 line.append(b"[Missed User Stack]")
#             else:
#                 line.extend([b.sym(addr, k.pid) for addr in reversed(user_stack)])
#         if not args.user_stacks_only:
#             line.extend([b"-"] if (need_delimiter and k.kernel_stack_id >= 0 and k.user_stack_id >= 0) else [])
#             if stack_id_err(k.kernel_stack_id):
#                 line.append(b"[Missed Kernel Stack]")
#             else:
#                 line.extend([aksym(addr) for addr in reversed(kernel_stack)])
#         print("%s %d" % (b";".join(line).decode('utf-8', 'replace'), v.value))