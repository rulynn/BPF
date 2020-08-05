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
isStack = True
usdt = USDT(pid=int(pid))
usdt.enable_probe_or_bail("pthread_start", "trace_pthread")

language = "java"

if language == "c":
    # Nothing to add
    pass
elif language == "java":
    usdt.enable_probe_or_bail("thread__start", "trace_start")
    usdt.enable_probe_or_bail("thread__stop", "trace_stop")

bpf = BPF(src_file = "test.c", usdt_contexts=[usdt])
print("Tracing thread events in process %d (language: %s)... Ctrl-C to quit." %
      (int(pid), language or "none"))
print("%-8s %-16s %-8s %-30s" % ("TIME", "ID", "TYPE", "DESCRIPTION"))

class ThreadEvent(ct.Structure):
    _fields_ = [
        ("runtime_id", ct.c_ulonglong),
        ("native_id", ct.c_ulonglong),
        ("type", ct.c_char * 8),
        ("name", ct.c_char * 80),
        ]

# load BPF program
if isStack == True:
    bpf = BPF(src_file = "locktime_test.c", usdt_contexts=[usdt])
    bpf.attach_uprobe(name="pthread", sym="pthread_mutex_init", fn_name="probe_mutex_init", pid=int(pid))
else:
    bpf = BPF(src_file = "locktime.c", usdt_contexts=[usdt])

bpf.attach_uprobe(name="pthread", sym="pthread_mutex_lock", fn_name="probe_mutex_lock", pid=int(pid))
bpf.attach_uretprobe(name="pthread", sym="pthread_mutex_lock", fn_name="probe_mutex_lock_return", pid=int(pid))
bpf.attach_uprobe(name="pthread", sym="pthread_mutex_unlock", fn_name="probe_mutex_unlock", pid=int(pid))


locks = bpf["locks"]

sleep(int(time))
#process.run(locks)
if isStack == True:
    start_ts = time.time()

    print("start to print threads")
    threads = bpf["threads"]
    print(threads)
    print(len(threads))
    for k, event in threads.items():
        #event = ct.cast(event, ct.POINTER(ThreadEvent)).contents
        print(k.runtime_id)
        #print(event.value)
        name = event.name
        if event.type == "pthread":
            name = bpf.sym(event.runtime_id, args.pid, show_module=True)
            tid = event.native_id
        else:
            tid = "R=%s/N=%s" % (event.runtime_id, event.native_id)
        print("%-8.3f %-16s %-8s %-30s" % (
            time.time() - start_ts, tid, event.type, name))
    #stack.run2(bpf, int(pid), locks)
    #stack.run(bpf, int(pid), locks, init_stacks, stacks)
    #stack.test_stack(bpf)