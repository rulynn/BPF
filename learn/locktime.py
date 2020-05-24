#!/usr/bin/env python

import sys
import itertools
from time import sleep
from bcc import BPF

def attach(bpf, pid):
    bpf.attach_uprobe(name="pthread", sym="pthread_mutex_lock", fn_name="probe_mutex_lock", pid=pid)
    bpf.attach_uretprobe(name="pthread", sym="pthread_mutex_lock", fn_name="probe_mutex_lock_return", pid=pid)
    bpf.attach_uprobe(name="pthread", sym="pthread_mutex_unlock", fn_name="probe_mutex_unlock", pid=pid)

def run(pid):
    bpf = BPF(src_file = "locktime.c")
    attach(bpf, pid)
    locks = bpf["locks"]
    lock_start = bpf["lock_start"]
    lock_end = bpf["lock_end"]

    while True:
        sleep(5)

        print("----- locks ----- ")
        for k, v in locks.items():
            print("\t tid %d ::: mtx %d ::: wait time %.2fus ::: hold time %.2fus ::: enter count %d" %
                                  (k.tid, k.mtx, v.wait_time_ns/1000.0, v.lock_time_ns/1000.0, v.enter_count))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("USAGE: %s pid" % sys.argv[0])
    else:
        run(int(sys.argv[1]))