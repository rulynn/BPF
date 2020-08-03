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

def run2(bpf, pid, locks):

    init_stacks = bpf["init_stacks"]
    stacks = bpf["stacks"]
    counts = bpf["counts"]

    mutex_ids = {}
    next_mutex_id = 1
    for k, v in init_stacks.items():
       mutex_id = "#%d" % next_mutex_id
       next_mutex_id += 1
       mutex_ids[k.value] = mutex_id
       dealStack(bpf, stacks, v.value)
       print("")
    grouper = lambda (k, v): k.tid
    sorted_by_thread = sorted(locks.items(), key=grouper)
    locks_by_thread = itertools.groupby(sorted_by_thread, grouper)
    for tid, items in locks_by_thread:
       #print("thread %d" % tid)
       for k, v in sorted(items, key=lambda (k, v): -v.wait_time_ns):
           #print("\tmutex %s ::: wait time %.2fus ::: hold time %.2fus ::: enter count %d" %
           #      (k.mtx, v.wait_time_ns/1000.0, v.lock_time_ns/1000.0, v.enter_count))
           #print_stack(bpf, pid, stacks, k.lock_stack_id)
           dealStack(bpf, stacks, k.lock_stack_id)
           print("")

def dealStack(bpf, stacks, stack_id):
    user_stack = [] if stack_id < 0 else stacks.walk(stack_id)

    user_stack = list(user_stack)
    line = [k.name]
    line.extend([bpf.sym(addr, k.pid) for addr in reversed(user_stack)])
    print("%s %d" % (b";".join(line).decode('utf-8', 'replace'), v.value))

def test_stack(bpf):
    # output stacks
    missing_stacks = 0
    has_collision = False
    counts = bpf.get_table("counts")
    stack_traces = bpf.get_table("stack_traces")

    for k, v in sorted(counts.items(), key=lambda counts: counts[1].value):
        user_stack = [] if k.user_stack_id < 0 else \
            stack_traces.walk(k.user_stack_id)

        user_stack = list(user_stack)
        #line = [k.name]
        line = ""
        # if we failed to get the stack is, such as due to no space (-ENOMEM) or
        # hash collision (-EEXIST), we still print a placeholder for consistency
        line.extend([bpf.sym(addr, k.pid) for addr in reversed(user_stack)])
        print("%s %d" % (b";".join(line).decode('utf-8', 'replace'), v.value))


# # output stacks
# missing_stacks = 0
# has_collision = False
# counts = b.get_table("counts")
# stack_traces = b.get_table("stack_traces")
# for k, v in sorted(counts.items(), key=lambda counts: counts[1].value):
#     # handle get_stackid errors
#     if not args.user_stacks_only and stack_id_err(k.kernel_stack_id):
#         missing_stacks += 1
#         # hash collision (-EEXIST) suggests that the map size may be too small
#         has_collision = has_collision or k.kernel_stack_id == -errno.EEXIST
#     if not args.kernel_stacks_only and stack_id_err(k.user_stack_id):
#         missing_stacks += 1
#         has_collision = has_collision or k.user_stack_id == -errno.EEXIST
#
#     user_stack = [] if k.user_stack_id < 0 else \
#         stack_traces.walk(k.user_stack_id)
#     kernel_tmp = [] if k.kernel_stack_id < 0 else \
#         stack_traces.walk(k.kernel_stack_id)
#
#     # fix kernel stack
#     kernel_stack = []
#     if k.kernel_stack_id >= 0:
#         for addr in kernel_tmp:
#             kernel_stack.append(addr)
#         # the later IP checking
#         if k.kernel_ip:
#             kernel_stack.insert(0, k.kernel_ip)
#
#     if args.folded:
#         # print folded stack output
#         user_stack = list(user_stack)
#         kernel_stack = list(kernel_stack)
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
#     else:
#         # print default multi-line stack output
#         if not args.user_stacks_only:
#             if stack_id_err(k.kernel_stack_id):
#                 print("    [Missed Kernel Stack]")
#             else:
#                 for addr in kernel_stack:
#                     print("    %s" % aksym(addr))
#         if not args.kernel_stacks_only:
#             if need_delimiter and k.user_stack_id >= 0 and k.kernel_stack_id >= 0:
#                 print("    --")
#             if stack_id_err(k.user_stack_id):
#                 print("    [Missed User Stack]")
#             else:
#                 for addr in user_stack:
#                     print("    %s" % b.sym(addr, k.pid).decode('utf-8', 'replace'))
#         print("    %-16s %s (%d)" % ("-", k.name.decode('utf-8', 'replace'), k.pid))
#         print("        %d\n" % v.value)
#
# # check missing
# if missing_stacks > 0:
#     enomem_str = "" if not has_collision else \
#         " Consider increasing --stack-storage-size."
#     print("WARNING: %d stack traces could not be displayed.%s" %
#         (missing_stacks, enomem_str),
#         file=stderr)