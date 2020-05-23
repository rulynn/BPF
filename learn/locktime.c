#include <linux/ptrace.h>

// 线程信息 key
struct thread_mutex_key {
    u32 tid;                // 线程id
    u64 mtx;                // 持有的锁
};
// 线程等待时间，线程持有时间，以及次数
struct thread_mutex_val {
    u64 wait_time_ns;
    u64 lock_time_ns;
    u64 enter_count;
};
// 线程开始获取锁开始时间
struct mutex_timestamp {
    u64 mtx;
    u64 timestamp;
};
// 线程持有锁时间 key
struct mutex_lock_time_key {
    u32 tid;
    u64 mtx;
};
// 线程持有锁时间 value
struct mutex_lock_time_val {
    u64 timestamp;
};

// Main info database about mutex and thread pairs
BPF_HASH(locks, struct thread_mutex_key, struct thread_mutex_val);

// Pid to the mutex address and timestamp of when the wait started
BPF_HASH(lock_start, u32, struct mutex_timestamp);

// Pid and mutex address to the timestamp of when the wait ended (mutex acquired) and the stack id
BPF_HASH(lock_end, struct mutex_lock_time_key, struct mutex_lock_time_val);

// TODO
BPF_STACK_TRACE(stacks, 4096);

// 开始尝试获取lock
int probe_mutex_lock(struct pt_regs *ctx)
{
    u64 now = bpf_ktime_get_ns();
    u32 pid = bpf_get_current_pid_tgid();

    struct mutex_timestamp val = {};
    val.mtx = PT_REGS_PARM1(ctx);
    val.timestamp = now;
    lock_start.update(&pid, &val);
    return 0;
}

// 获取到锁
int probe_mutex_lock_return(struct pt_regs *ctx)
{
    u64 now = bpf_ktime_get_ns();
    u32 pid = bpf_get_current_pid_tgid();

    // 计算等待时间， 开始获取锁的时间 - 获取到锁的时间
    struct mutex_timestamp *entry = lock_start.lookup(&pid);
    if (entry == 0)
        return 0;   // Missed the entry
    u64 wait_time = now - entry->timestamp;

    // 设置持有锁开始时间
    // If pthread_mutex_lock() returned 0, we have the lock
    if (PT_REGS_RC(ctx) == 0) {
        // Record the lock acquisition timestamp so that we can read it when unlocking
        struct mutex_lock_time_key key = {};
        key.mtx = entry->mtx;
        key.tid = pid;
        struct mutex_lock_time_val val = {};
        val.timestamp = now;
        lock_end.update(&key, &val);
    }
    // Record the wait time for this mutex-tid-stack combination even if locking failed
    struct thread_mutex_key tm_key = {};
    tm_key.mtx = entry->mtx;
    tm_key.tid = pid;

    struct thread_mutex_val *existing_tm_val, new_tm_val = {};
    existing_tm_val = locks.lookup_or_init(&tm_key, &new_tm_val);
    existing_tm_val->wait_time_ns += wait_time;
    if (PT_REGS_RC(ctx) == 0) {
        existing_tm_val->enter_count += 1;
    }
    lock_start.delete(&pid);
    return 0;
}

// 释放 lock
int probe_mutex_unlock(struct pt_regs *ctx)
{
    u64 now = bpf_ktime_get_ns();
    u64 mtx = PT_REGS_PARM1(ctx);
    u32 pid = bpf_get_current_pid_tgid();

    // key
    struct mutex_lock_time_key lock_key = {};
    lock_key.mtx = mtx;
    lock_key.tid = pid;

     // 计算锁的持有时间
    struct mutex_lock_time_val *lock_val = lock_end.lookup(&lock_key);
    if (lock_val == 0)
        return 0;   // Missed the lock of this mutex
    u64 hold_time = now - lock_val->timestamp;

    struct thread_mutex_key tm_key = {};
    tm_key.mtx = mtx;
    tm_key.tid = pid;

    struct thread_mutex_val *existing_tm_val = locks.lookup(&tm_key);
    if (existing_tm_val == 0)
        return 0;   // Couldn't find this record
    existing_tm_val->lock_time_ns += hold_time;
    lock_end.delete(&lock_key);
    return 0;
}


