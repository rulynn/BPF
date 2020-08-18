#include <linux/ptrace.h>
#include <linux/sched.h>
// key: thread info
struct thread_mutex_key {
    u32 tid;                // thread id
    u64 mtx;                // lock id
};
// value: thread info
struct thread_mutex_val {
    u64 start_time_ns;   // time point
    u64 wait_time_ns;
    u64 spin_time_ns;
    u64 lock_time_ns;
    u64 enter_count;
};
struct mutex_timestamp {
    u64 mtx;
    u64 timestamp;
};

// Main info database about mutex and thread pairs
BPF_HASH(locks, struct thread_mutex_key, struct thread_mutex_val);
// Pid to the mutex address and timestamp of when the wait started
BPF_HASH(lock_start, u32, struct mutex_timestamp);
// Pid and mutex address to the timestamp of when the wait ended (mutex acquired) and the stack id
BPF_HASH(lock_end, struct thread_mutex_key, u64);
BPF_STACK_TRACE(stacks, 4096);

// Thread starts to acquire the lock
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

// Thread acquired the lock
int probe_mutex_lock_return(struct pt_regs *ctx)
{
    u64 now = bpf_ktime_get_ns();
    u32 pid = bpf_get_current_pid_tgid();

    // Calculate the waiting time
    struct mutex_timestamp *entry = lock_start.lookup(&pid);
    if (entry == 0)
        return 0;   // Missed the entry
    u64 spin_time = now - entry->timestamp;

    // key
    struct thread_mutex_key key = {};
    key.mtx = entry->mtx;
    key.tid = pid;

    if (PT_REGS_RC(ctx) == 0) {
        // Record the lock acquisition timestamp so that we can read it when unlockin
        lock_end.update(&key, &now);
    }
    // Record the wait time for this mutex-tid-stack combination even if locking failed
    struct thread_mutex_val *existing_tm_val, new_tm_val = {};
    existing_tm_val = locks.lookup_or_init(&key, &new_tm_val);
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

// Thread release lock
int probe_mutex_unlock(struct pt_regs *ctx)
{
    u64 now = bpf_ktime_get_ns();
    u64 mtx = PT_REGS_PARM1(ctx);
    u32 pid = bpf_get_current_pid_tgid();

    // key
    struct thread_mutex_key key = {};
    key.mtx = mtx;
    key.tid = pid;

     // Calculate lock holding time
    u64 *lock_val;
    lock_val = lock_end.lookup(&key);
    if (lock_val == 0)
        return 0;   // Missed the lock of this mutex
    u64 hold_time = now - *lock_val;
    struct thread_mutex_val *existing_tm_val = locks.lookup(&key);
    if (existing_tm_val == 0)
        return 0;   // Couldn't find this record
    existing_tm_val->lock_time_ns += hold_time;

    lock_end.delete(&key);
    return 0;
}

struct time_k {
    u32 tid;
    u64 timestamp;
    char type[8];
};

BPF_HASH(times, struct time_k);

int trace_pthread(struct pt_regs *ctx) {
    char type[] = "pthread";
    u64 now = bpf_ktime_get_ns();
    struct time_k unit = {};
    unit.timestamp = now;
    unit.tid = bpf_get_current_pid_tgid();
    __builtin_memcpy(&unit.type, type, sizeof(unit.type));
    times.increment(unit);
    return 0;
}


int probe_create(struct pt_regs *ctx){
    char type[] = "create";
    u64 now = bpf_ktime_get_ns();
    struct time_k unit = {};
    unit.timestamp = now;
    unit.tid = bpf_get_current_pid_tgid();
    __builtin_memcpy(&unit.type, type, sizeof(unit.type));
    times.increment(unit);
    return 0;
}
//
//int probe_exit(struct pt_regs *ctx){
//    u64 now = bpf_ktime_get_ns();
//    struct test_unit unit = {};
//    unit.timestamp = now;
//    unit.tid = bpf_get_current_pid_tgid();
//    unit.mtx = PT_REGS_PARM1(ctx);
//    //bpf_probe_read(&unit.mtx, sizeof(unit.mtx), (void *)PT_REGS_PARM1(ctx));
//    unit.type = 2;
//    test.increment(unit);
//    return 0;
//}
//

int probe_join(struct pt_regs *ctx){
    char type[] = "join";
    u64 now = bpf_ktime_get_ns();
    struct time_k unit = {};
    unit.timestamp = now;
    //unit.tid = bpf_get_current_pid_tgid();
    unit.tid = PT_REGS_PARM1(ctx);
    __builtin_memcpy(&unit.type, type, sizeof(unit.type));
    times.increment(unit);
    return 0;
}


int trace_join(struct pt_regs *ctx){
  char type[] = "join_ret";
  u64 now = bpf_ktime_get_ns();
  struct time_k unit = {};
  unit.timestamp = now;
  // unit.tid = bpf_get_current_pid_tgid();
  unit.tid = PT_REGS_PARM1(ctx);
  __builtin_memcpy(&unit.type, type, sizeof(unit.type));
  times.increment(unit);
  return 0;
}

