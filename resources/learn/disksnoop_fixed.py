#!/usr/bin/python
#
# disksnoop.py	Trace block device I/O: basic version of iosnoop.
#		For Linux, uses BCC, eBPF. Embedded C.
#
# Written as a basic example of tracing latency.
#
# Copyright (c) 2015 Brendan Gregg.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# 11-Aug-2015	Brendan Gregg	Created this.

from __future__ import print_function
from bcc import BPF
from bcc.utils import printb

# load BPF program
b = BPF(text="""
BPF_HASH(time);
BPF_HASH(size);
TRACEPOINT_PROBE(block, block_rq_issue) {
	u64 pid = args->dev;
    u64 ts = bpf_ktime_get_ns();
	time.update(&pid, &ts);
	u64 blocksize = args->bytes;
	size.update(&pid, &blocksize);
    return 0;
}
TRACEPOINT_PROBE(block, block_rq_complete) {
	u64 pid = args->dev;
    u64 *tsp, delta, *blocksize;
	tsp = time.lookup(&pid);
	blocksize = size.lookup(&pid);
	if (tsp != 0 && blocksize != 0) {
		delta = bpf_ktime_get_ns() - *tsp;
		bpf_trace_printk("%d %d\\n", *blocksize, delta / 1000);
	}
	return 0;
}
""")


# header
print("%-18s %-7s %8s" % ("TIME(s)", "BLOCKSIZE", "LAT(ms)"))

# format output
while 1:
	try:
		(task, pid, cpu, flags, ts, msg) = b.trace_fields()

		(blocksize, time) = msg.split()
		ms = float(int(time, 10)) / 1000

		printb(b"%-18.9f %-7s %8.2f" % (ts, blocksize, ms))
	except KeyboardInterrupt:
		exit()
