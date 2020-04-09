#!/usr/bin/python

from __future__ import print_function
from bcc import BPF
from bcc.utils import printb

# load BPF program
b = BPF(text="""
#include <uapi/linux/ptrace.h>

BPF_HASH(last);

int do_trace(struct pt_regs *ctx) {
    u64 ts, *tsp, delta, *count, count_cur, key = 0, count_key = 1;
    // update count
    count = last.lookup(&count_key);
    if (count == 0) {
        count_cur = 1;
    }
    else {
        count_cur = *count + 1;
        last.delete(&count_key);
    }
    last.update(&count_key, &count_cur);

    // attempt to read stored timestamp
    tsp = last.lookup(&key);
    if (tsp != 0) {
        delta = bpf_ktime_get_ns() - *tsp;
        if (delta < 1000000000) {
            // output if time is less than 1 second
            bpf_trace_printk("%d,%d\\n", count_cur, delta / 1000000);
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

# format output
start = 0
while 1:
    try:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
        [cnt, ms] = msg.split(",")
        if start == 0:
            start = ts
        ts = ts - start
        print("At time %.2f s: %s syncs detected, last %s ms ago" % (ts, cnt, ms))
    except KeyboardInterrupt:
        exit()