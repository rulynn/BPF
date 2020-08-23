#!/usr/bin/env python

import sys
import itertools
from bcc import BPF, USDT
import process
import stack
import argparse
import itertools
import time
from time import sleep

# if len(sys.argv) < 3:
#     print("USAGE: need PID and time")
#     exit()
# pid = sys.argv[1]
# time = sys.argv[2]
# isStack = False

languages = ["c", "java"]

examples = """examples:
    ./locktime -l java -p 185    # trace Java threads in process 185
    ./uthreads -l none -p 12245  # trace only pthreads in process 12245
"""
parser = argparse.ArgumentParser(
    description="Trace thread creation/destruction events in " +
                "high-level languages.",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=examples)
parser.add_argument("-l", "--language", choices=languages + ["none"],
    help="language to trace (none for pthreads only)")
# parser.add_argument("pid", type=int, help="process id to attach to")
# parser.add_argument("-v", "--verbose", action="store_true",
#     help="verbose mode: print the BPF program (for debugging purposes)")
# parser.add_argument("--ebpf", action="store_true",
#     help=argparse.SUPPRESS)
parser.add_argument("-p", "--pid", type=int, help="profile process with this PID only")
parser.add_argument("-t", "--time", type=int, help="sample time")
args = parser.parse_args()


language = args.language
if not language:
    language = utils.detect_language(languages, args.pid)

usdt = USDT(pid=args.pid)


# load BPF program
if language == "java":
    usdt.enable_probe_or_bail("thread__start", "trace_start")
    usdt.enable_probe_or_bail("thread__stop", "trace_stop")
    usdt.enable_probe_or_bail("thread__park__begin", "trace_park_begin")
    usdt.enable_probe_or_bail("thread__park__end", "trace_park_end")
    usdt.enable_probe_or_bail("thread__unpark", "trace_unpark")

    bpf = BPF(src_file = "locktime_stack.c", usdt_contexts=[usdt])
    bpf.attach_uprobe(name="pthread", sym="pthread_mutex_init", fn_name="probe_mutex_init", pid=args.pid)
else:
#     usdt.enable_probe_or_bail("pthread_start", "trace_pthread")
    bpf = BPF(src_file = "locktime.c", usdt_contexts=[usdt])

bpf.attach_uprobe(name="pthread", sym="pthread_mutex_lock", fn_name="probe_mutex_lock", pid=args.pid)
bpf.attach_uretprobe(name="pthread", sym="pthread_mutex_lock", fn_name="probe_mutex_lock_return", pid=args.pid)
bpf.attach_uprobe(name="pthread", sym="pthread_mutex_unlock", fn_name="probe_mutex_unlock", pid=args.pid)

# new
bpf.attach_uprobe(name="pthread", sym="pthread_create", fn_name="probe_create", pid=args.pid)
# bpf.attach_uprobe(name="pthread", sym="pthread_exit", fn_name="probe_exit", pid=int(pid))
# bpf.attach_uprobe(name="pthread", sym="pthread_mutex_trylock", fn_name="probe_mutex_trylock", pid=int(pid))
#bpf.attach_uprobe(name="pthread", sym="pthread_join", fn_name="probe_join", pid=args.pid)
# bpf.attach_uprobe(name="pthread", sym="pthread_cancel", fn_name="probe_cancel", pid=int(pid))
# bpf.attach_uprobe(name="pthread", sym="pthread_barrier_init", fn_name="probe_barrier_init", pid=int(pid))

t = time.time()
print "Start : %s" % (int(round(t * 1000)))
sleep(args.time)
locks = bpf["locks"]
times = bpf["times"]
t = time.time()
print "End : %s" % (int(round(t * 1000)))

if language == "java":
    process.run(locks, times, True)
    stack.run_sub(bpf, args.pid, locks)
    print(len(times))
    for k, v in times.items():
        print(k.tid, k.timestamp, k.type, k.val, k.runtime_id)
    t = time.time(
    print "Finish : %s" % (int(round(t * 1000)))
#     stack.run(bpf, int(pid), locks, init_stacks, stacks)
else:
    process.run(locks, times, False)
    print(len(times))
    for k, v in times.items():
        print(k.tid, k.timestamp, k.type, k.val, k.runtime_id)
