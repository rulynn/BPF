struct thread_event_t {
    u32 pid;
    u32 tid;
    u64 runtime_id;
    u64 native_id;
    char type[8];
    char name[80];
};

BPF_HASH(threads, struct thread_event_t);
//BPF_PERF_OUTPUT(threads);

int trace_pthread(struct pt_regs *ctx) {
    struct thread_event_t te = {};
    u64 start_routine = 0;
    char type[] = "pthread";
    te.native_id = bpf_get_current_pid_tgid() & 0xFFFFFFFF;
    bpf_usdt_readarg(2, ctx, &start_routine);
    te.runtime_id = start_routine;  // This is really a function pointer
    __builtin_memcpy(&te.type, type, sizeof(te.type));
    //threads.perf_submit(ctx, &te, sizeof(te));
    u32 pid = bpf_get_current_pid_tgid();
        te.tid = pid;
        te.time = bpf_ktime_get_ns();
        threads.increment(te);
    return 0;
}

int trace_start(struct pt_regs *ctx) {
    char type[] = "start";
    struct thread_event_t te = {};
    u64 nameptr = 0, id = 0, native_id = 0;
    bpf_usdt_readarg(1, ctx, &nameptr);
    bpf_usdt_readarg(3, ctx, &id);
    bpf_usdt_readarg(4, ctx, &native_id);
    bpf_probe_read_user(&te.name, sizeof(te.name), (void *)nameptr);
    te.runtime_id = id;
    te.native_id = native_id;
    __builtin_memcpy(&te.type, type, sizeof(te.type));
    //threads.perf_submit(ctx, &te, sizeof(te));
    u32 pid = bpf_get_current_pid_tgid();
        te.tid = pid;
        te.time = bpf_ktime_get_ns();
        threads.increment(te);
    return 0;
}

int trace_stop(struct pt_regs *ctx) {
    char type[] = "stop";
    struct thread_event_t te = {};
    u64 nameptr = 0, id = 0, native_id = 0;
    bpf_usdt_readarg(1, ctx, &nameptr);
    bpf_usdt_readarg(3, ctx, &id);
    bpf_usdt_readarg(4, ctx, &native_id);
    bpf_probe_read_user(&te.name, sizeof(te.name), (void *)nameptr);
    te.runtime_id = id;
    te.native_id = native_id;
    __builtin_memcpy(&te.type, type, sizeof(te.type));
    //threads.perf_submit(ctx, &te, sizeof(te));
    u32 pid = bpf_get_current_pid_tgid();
        te.tid = pid;
        te.time = bpf_ktime_get_ns();
        threads.increment(te);
    return 0;
}