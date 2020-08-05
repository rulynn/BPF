#!/usr/bin/python
# @lint-avoid-python-3-compatibility-imports
#
# uthreads  Trace thread creation/destruction events in high-level languages.
#           For Linux, uses BCC, eBPF.
#
# USAGE: uthreads [-l {c,java,none}] [-v] pid
#
# Copyright 2016 Sasha Goldshtein
# Licensed under the Apache License, Version 2.0 (the "License")
#
# 25-Oct-2016   Sasha Goldshtein   Created this.

from __future__ import print_function
import argparse
from bcc import BPF, USDT, utils
import ctypes as ct
import time
import sys
import os
import time

languages = ["c", "java"]
pid = sys.argv[1]
sleeptime = sys.argv[2]


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


sleep(int(time))
start_ts = time.time()

print("start to print threads")
threads = bpf["threads"]
print(threads)
print(len(threads))
for k, event in threads.items():
    print(k, event)
    name = event.name
    if event.type == "pthread":
        name = bpf.sym(event.runtime_id, args.pid, show_module=True)
        tid = event.native_id
    else:
        tid = "R=%s/N=%s" % (event.runtime_id, event.native_id)
    print("%-8.3f %-16s %-8s %-30s" % (
        time.time() - start_ts, tid, event.type, name))

# def print_event(cpu, data, size):
#     event = ct.cast(data, ct.POINTER(ThreadEvent)).contents
#     name = event.name
#     if event.type == "pthread":
#         name = bpf.sym(event.runtime_id, int(pid), show_module=True)
#         tid = event.native_id
#     else:
#         tid = "R=%s/N=%s" % (event.runtime_id, event.native_id)
#     print("%-8.3f %-16s %-8s %-30s" % (
#         time.time() - start_ts, tid, event.type, name))
#
# bpf["threads"].open_perf_buffer(print_event)
# while 1:
#     try:
#         bpf.perf_buffer_poll()
#     except KeyboardInterrupt:
#         exit()