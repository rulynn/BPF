#include <linux/ptrace.h>

// key: thread info
struct thread_mutex_key {
    u32 tid;                // thread id
    u64 mtx;                // lock id
};

// value: thread info
struct thread_mutex_val {
    u64 wait_time_ns;
    u64 lock_time_ns;
    u64 enter_count;
};

// Main info database about mutex and thread pairs
BPF_HASH(locks, struct thread_mutex_key, struct thread_mutex_val);

// Pid and mutex address to the timestamp of when the wait started
BPF_HASH(lock_start, struct thread_mutex_key, u64);

// Pid and mutex address to the timestamp of when the wait ended
BPF_HASH(lock_end, struct thread_mutex_key, u64);

BPF_STACK_TRACE(stacks, 4096);

// Start trying to acquire lock
int probe_mutex_lock(struct pt_regs *ctx)
{
    // get ID info
    u64 now = bpf_ktime_get_ns();
    u64 mtx = PT_REGS_PARM1(ctx);
    u32 pid = bpf_get_current_pid_tgid();

    struct thread_mutex_key key = {};
    key.mtx = mtx;
    key.tid = pid;
    lock_start.update(&key, &now);
    return 0;
}

// Get lock
int probe_mutex_lock_return(struct pt_regs *ctx)
{
    u64 now = bpf_ktime_get_ns();
    u64 mtx = PT_REGS_PARM1(ctx);
    u32 pid = bpf_get_current_pid_tgid();

    struct thread_mutex_key key = {};
    key.mtx = mtx;
    key.tid = pid;

    // 计算等待时间， 开始获取锁的时间 - 获取到锁的时间
    u64 *start_time;
    start_time = lock_start.lookup(&key);
    if (start_time == 0)
        return 0;   // Missed the entry
    u64 wait_time = now - *start_time;

    // 设置持有锁开始时间
    if (PT_REGS_RC(ctx) == 0) {
        // Record the lock acquisition timestamp so that we can read it when unlocking
        lock_end.update(&key, &now);
    }
    // Record the wait time for this mutex-tid-stack combination even if locking failed
    struct thread_mutex_val *existing_tm_val, new_tm_val = {};
    existing_tm_val = locks.lookup_or_init(&key, &new_tm_val);
    existing_tm_val->wait_time_ns += wait_time;
    if (PT_REGS_RC(ctx) == 0) {
        existing_tm_val->enter_count += 1;
    }
    lock_start.delete(&key);
    return 0;
}

// Release lock
int probe_mutex_unlock(struct pt_regs *ctx)
{
    u64 now = bpf_ktime_get_ns();
    u64 mtx = PT_REGS_PARM1(ctx);
    u32 pid = bpf_get_current_pid_tgid();

    struct thread_mutex_key key = {};
    key.mtx = mtx;
    key.tid = pid;

     // 计算锁的持有时间
    u64 *start_hold_time;
    start_hold_time = lock_end.lookup(&key);
    if (start_hold_time == 0)
        return 0;   // Missed the lock of this mutex
    u64 hold_time = now - *start_hold_time;

    struct thread_mutex_val *existing_tm_val = locks.lookup(&key);
    if (existing_tm_val == 0)
        return 0;   // Couldn't find this record
    existing_tm_val->lock_time_ns += hold_time;
    lock_end.delete(&key);
    return 0;
}
