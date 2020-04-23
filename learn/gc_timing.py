#!/usr/bin/python

from __future__ import print_function
from bcc import BPF, USDT
from bcc.utils import ArgString, printb
import argparse
from time import strftime

# arguments
examples = """examples:
    ./gcsnoop           # trace all gc
    ./gcsnoop -p 181    # only trace PID 181
"""
parser = argparse.ArgumentParser(
    description="Trace GC",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=examples)
parser.add_argument("-p", "--pid",
    help="trace this PID only")
args = parser.parse_args()
debug = 0

# define BPF program
bpf_text = """
#include <uapi/linux/ptrace.h>

// define output data structure in C
struct data_t {
    u32 pid;
    u64 ts;
    u64 delta;
};
BPF_PERF_OUTPUT(events);
BPF_HASH(time, u32);
int do_trace_begin(struct pt_regs *ctx) {
    u32 pid;
    u64 ts;
    
    pid = bpf_get_current_pid_tgid();
    ts = bpf_ktime_get_ns();
	time.update(&pid, &ts);
	return 0;

};

int do_trace_end(struct pt_regs *ctx) {
        
    struct data_t data = {};
    u32 pid;
    u64 ts, *tsp, delta;
    
    pid = bpf_get_current_pid_tgid();
    tsp = time.lookup(&pid);
    delta = bpf_ktime_get_ns() - *tsp;
     
    data.pid = pid;
    data.delta = delta / 1000;
    data.ts = bpf_ktime_get_ns();
    
    events.perf_submit(ctx, &data, sizeof(data));
    time.delete(&pid);
            
    return 0;
};

"""

if args.pid:
    bpf_text = bpf_text.replace('FILTER',
        'if (pid != %s) { return 0; }' % args.pid)
else:
    bpf_text = bpf_text.replace('FILTER', '')
if debug:
    print(bpf_text)

u = USDT(pid=int(args.pid))
u.enable_probe(probe="gc__begin", fn_name="do_trace_begin")
u.enable_probe(probe="gc__end", fn_name="do_trace_end")

# initialize BPF
b = BPF(text=bpf_text, usdt_contexts=[u])

# header
print("%-9s %-6s %-6s" % ("TIME", "PID", "USE TIME(ms)"))

# process event
def print_event(cpu, data, size):
    event = b["events"].event(data)
    printb(b"%-9s %-6s %-6s" % event.ts, event.pid, event.delta)

# loop with callback to print_event
b["events"].open_perf_buffer(print_event)
while 1:
    try:
        b.perf_buffer_poll()
    except KeyboardInterrupt:
        exit()