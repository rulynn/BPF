#include <linux/ptrace.h>

struct thread_mutex_key_t {
    u32 tid;
    u64 mtx;
    int lock_stack_id;
};
struct thread_mutex_val_t {
//    u64 start_time_ns;
//    u64 wait_time_ns;
//    u64 lock_time_ns;
//    u64 enter_count;
    u64 start_time_ns;   // time point
    u64 wait_time_ns;
    u64 spin_time_ns;
    u64 lock_time_ns;
    u64 enter_count;
};
struct mutex_timestamp_t {
    u64 mtx;
    u64 timestamp;
};
struct mutex_lock_time_key_t {
    u32 tid;
    u64 mtx;
};
struct mutex_lock_time_val_t {
    u64 timestamp;
    int stack_id;
};

// Mutex to the stack id which initialized that mutex
BPF_HASH(init_stacks, u64, int);
// Main info database about mutex and thread pairs
BPF_HASH(locks, struct thread_mutex_key_t, struct thread_mutex_val_t);
// Pid to the mutex address and timestamp of when the wait started
BPF_HASH(lock_start, u32, struct mutex_timestamp_t);
// Pid and mutex address to the timestamp of when the wait ended (mutex acquired) and the stack id
BPF_HASH(lock_end, struct mutex_lock_time_key_t, struct mutex_lock_time_val_t);
BPF_STACK_TRACE(stacks, 4096);

int probe_mutex_lock(struct pt_regs *ctx)
{
    u64 now = bpf_ktime_get_ns();
    u32 pid = bpf_get_current_pid_tgid();

    struct mutex_timestamp_t val = {};
    val.mtx = PT_REGS_PARM1(ctx);
    val.timestamp = now;
    lock_start.update(&pid, &val);
    return 0;
}

int probe_mutex_lock_return(struct pt_regs *ctx)
{
    u64 now = bpf_ktime_get_ns();
    u32 pid = bpf_get_current_pid_tgid();

    struct mutex_timestamp_t *entry = lock_start.lookup(&pid);
    if (entry == 0)
        return 0;   // Missed the entry
    u64 spin_time = now - entry->timestamp;
    int stack_id = stacks.get_stackid(ctx, BPF_F_REUSE_STACKID|BPF_F_USER_STACK);

    // If pthread_mutex_lock() returned 0, we have the lock
    if (PT_REGS_RC(ctx) == 0) {
        // Record the lock acquisition timestamp so that we can read it when unlocking
        struct mutex_lock_time_key_t key = {};
        key.mtx = entry->mtx;
        key.tid = pid;
        struct mutex_lock_time_val_t val = {};
        val.timestamp = now;
        val.stack_id = stack_id;
        lock_end.update(&key, &val);
    }

    struct thread_mutex_key_t tm_key = {};
    tm_key.mtx = entry->mtx;
    tm_key.tid = pid;
    tm_key.lock_stack_id = stack_id;

    struct thread_mutex_val_t *existing_tm_val, new_tm_val = {};
    existing_tm_val = locks.lookup_or_init(&tm_key, &new_tm_val);
    if (existing_tm_val == 0)
        return 0;   // Couldn't find this record
    existing_tm_val->spin_time_ns += spin_time;
    existing_tm_val->enter_count++;

    if (existing_tm_val->start_time_ns == 0) {
        existing_tm_val->start_time_ns = entry->timestamp;
        existing_tm_val->wait_time_ns = now - entry->timestamp;
        existing_tm_val->spin_time_ns -= existing_tm_val->wait_time_ns;
    }

    lock_start.delete(&pid);
    return 0;
}
int probe_mutex_unlock(struct pt_regs *ctx)
{
    u64 now = bpf_ktime_get_ns();
    u64 mtx = PT_REGS_PARM1(ctx);
    u32 pid = bpf_get_current_pid_tgid();

    struct mutex_lock_time_key_t lock_key = {};
    lock_key.mtx = mtx;
    lock_key.tid = pid;

    struct mutex_lock_time_val_t *lock_val = lock_end.lookup(&lock_key);
    if (lock_val == 0)
        return 0;   // Missed the lock of this mutex
    u64 hold_time = now - lock_val->timestamp;

    struct thread_mutex_key_t tm_key = {};
    tm_key.mtx = mtx;
    tm_key.tid = pid;
    tm_key.lock_stack_id = lock_val->stack_id;

    struct thread_mutex_val_t *existing_tm_val = locks.lookup(&tm_key);
    if (existing_tm_val == 0)
        return 0;   // Couldn't find this record
    existing_tm_val->lock_time_ns += hold_time;

    lock_end.delete(&lock_key);
    return 0;
}
 int probe_mutex_init(struct pt_regs *ctx)
 {
     int stack_id = stacks.get_stackid(ctx, BPF_F_REUSE_STACKID|BPF_F_USER_STACK);
     u64 mutex_addr = PT_REGS_PARM1(ctx);
     init_stacks.update(&mutex_addr, &stack_id);
     return 0;
 }