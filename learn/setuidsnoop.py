#!/usr/bin/python

from __future__ import print_function
from bcc import BPF
from bcc.utils import ArgString, printb
import argparse
from time import strftime

# arguments
examples = """examples:
    ./setuidsnoop           # trace all setuid() signals
    ./setuidsnoop -p 181    # only trace PID 181
"""
parser = argparse.ArgumentParser(
    description="Trace signals issued by the setuid() syscall",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=examples)
parser.add_argument("-p", "--pid",
    help="trace this PID only")
args = parser.parse_args()
debug = 0

# define BPF program
bpf_text = """
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>
struct val_t {
   u64 pid;
   int uid;
   char comm[TASK_COMM_LEN];
};
struct data_t {
   u64 pid;
   int uid;
   int ret;
   char comm[TASK_COMM_LEN];
};
BPF_HASH(infotmp, u32, struct val_t);
BPF_PERF_OUTPUT(events);
int syscall__setuid(struct pt_regs *ctx, int uid)
{
    u32 pid = bpf_get_current_pid_tgid();
    FILTER
    struct val_t val = {.pid = pid};
    if (bpf_get_current_comm(&val.comm, sizeof(val.comm)) == 0) {
        val.uid = uid;
        infotmp.update(&pid, &val);
    }
    return 0;
};
int do_ret_sys_setuid(struct pt_regs *ctx)
{
    struct data_t data = {};
    struct val_t *valp;
    u32 pid = bpf_get_current_pid_tgid();
    valp = infotmp.lookup(&pid);
    if (valp == 0) {
        // missed entry
        return 0;
    }
    bpf_probe_read(&data.comm, sizeof(data.comm), valp->comm);
    data.pid = pid;
    data.uid = valp->uid;
    data.ret = PT_REGS_RC(ctx);
    events.perf_submit(ctx, &data, sizeof(data));
    infotmp.delete(&pid);
    return 0;
}
"""
if args.pid:
    bpf_text = bpf_text.replace('FILTER',
        'if (pid != %s) { return 0; }' % args.pid)
else:
    bpf_text = bpf_text.replace('FILTER', '')
if debug:
    print(bpf_text)

# initialize BPF
b = BPF(text=bpf_text)
setuid_fnname = b.get_syscall_fnname("setuid")
b.attach_kprobe(event=setuid_fnname, fn_name="syscall__setuid")
b.attach_kretprobe(event=setuid_fnname, fn_name="do_ret_sys_setuid")

# header
print("%-9s %-6s %-16s %-6s %s" % (
    "TIME", "PID", "COMM", "UID", "RESULT"))

# process event
def print_event(cpu, data, size):
    event = b["events"].event(data)
    printb(b"%-9s %-6d %-16s %-6d %d" % (strftime("%H:%M:%S").encode('ascii'),
        event.pid, event.comm, event.uid, event.ret))

# loop with callback to print_event
b["events"].open_perf_buffer(print_event)
while 1:
    try:
        b.perf_buffer_poll()
    except KeyboardInterrupt:
        exit()