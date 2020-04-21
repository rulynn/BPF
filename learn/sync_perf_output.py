#!/usr/bin/python
#
# sync_timing.py    Trace time between syncs.
#                   For Linux, uses BCC, eBPF. Embedded C.
#
# Written as a basic example of tracing time between events.
#
# Copyright 2016 Netflix, Inc.
# Licensed under the Apache License, Version 2.0 (the "License")

from __future__ import print_function
from bcc import BPF
from bcc.utils import printb

# load BPF program
b = BPF(text="""
#include <uapi/linux/ptrace.h>
BPF_HASH(last);

// define output data structure in C
struct data_t {
    u32 pid;
    u64 ts;
    u64 delta;
};
    
BPF_PERF_OUTPUT(events);

int do_trace(struct pt_regs *ctx) {
    struct data_t data = {};
    
    u64 ts, *tsp, delta, key = 0;
    // attempt to read stored timestamp
    tsp = last.lookup(&key);
    if (tsp != 0) {
        delta = bpf_ktime_get_ns() - *tsp;
        if (delta < 1000000000) {
            // output if time is less than 1 second
            // bpf_trace_printk("%d\\n", delta / 1000000);
            data.pid = bpf_get_current_pid_tgid();
            data.ts = bpf_ktime_get_ns();
            data.delta = delta / 1000000;
            events.perf_submit(ctx, &data, sizeof(data));
        }
        last.delete(&key);
    }
    // update stored timestamp
    ts = bpf_ktime_get_ns();
    last.update(&key, &ts);
    return 0;
}
""")

b.attach_kprobe(event=b.get_syscall_fnname("sync"), fn_name="do_trace")
print("Tracing for quick sync's... Ctrl-C to end")

# process event
start = 0
def print_event(cpu, data, size):
    global start
    event = b["events"].event(data)
    if start == 0:
            start = event.ts
    ts = (float(event.ts - start)) / 1000000000
    ms = event.delta
    printb(b"At time %.2f s: multiple syncs detected, last %s ms ago" % (ts, ms))

b["events"].open_perf_buffer(print_event)
# format outputs
while 1:
    try:
        b.perf_buffer_poll()
    except KeyboardInterrupt:
        exit()