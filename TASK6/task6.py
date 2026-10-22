import time
from threading import Thread, Lock

STUDENT_ID = 230103317
NUM_THREADS = 4
INCREMENTS_PER_THREAD = 2_000_000
EXPECTED_TOTAL = NUM_THREADS * INCREMENTS_PER_THREAD

# Shared state
unsynchronized_counter = 0
synchronized_counter = 0
lock = Lock()

def unsynchronized_worker():
    """Unsynchronized worker: race condition causes lost updates."""
    global unsynchronized_counter
    for _ in range(INCREMENTS_PER_THREAD):
        unsynchronized_counter += 1

def synchronized_worker():
    """Synchronized worker: uses Mutex lock to ensure atomic increments."""
    global synchronized_counter
    for _ in range(INCREMENTS_PER_THREAD):
        with lock:
            synchronized_counter += 1

def main():
    print(f"Student ID       : {STUDENT_ID}")
    print(f"Threads          : {NUM_THREADS}")
    print(f"Increments/Thread: {INCREMENTS_PER_THREAD:,}")
    print(f"Expected Total   : {EXPECTED_TOTAL:,}")
    print("=" * 65)

    # 1. Benchmark Unsynchronized Execution (Race Condition)
    t0 = time.perf_counter()
    threads = [Thread(target=unsynchronized_worker) for _ in range(NUM_THREADS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    t_unsync = (time.perf_counter() - t0) * 1000.0

    lost_updates = EXPECTED_TOTAL - unsynchronized_counter
    pct_lost = (lost_updates / EXPECTED_TOTAL) * 100.0

    print("--- [UNSYNCHRONIZED RUN (RACE CONDITION)] ---")
    print(f"Actual Value     : {unsynchronized_counter:,}")
    print(f"Lost Updates     : {lost_updates:,}")
    print(f"Data Loss (%)    : {pct_lost:.2f}%")
    print(f"Execution Time   : {t_unsync:.2f} ms")
    print("-" * 65)

    # 2. Benchmark Synchronized Execution (Mutex Lock)
    t0 = time.perf_counter()
    threads = [Thread(target=synchronized_worker) for _ in range(NUM_THREADS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    t_sync = (time.perf_counter() - t0) * 1000.0

    sync_loss = EXPECTED_TOTAL - synchronized_counter
    penalty_ratio = t_sync / t_unsync if t_unsync > 0 else 1.0

    print("--- [SYNCHRONIZED RUN (MUTEX LOCK)] ---")
    print(f"Actual Value     : {synchronized_counter:,}")
    print(f"Lost Updates     : {sync_loss:,}")
    print(f"Execution Time   : {t_sync:.2f} ms")
    print("-" * 65)
    print(f"Synchronization Penalty : {penalty_ratio:.2f}x slowdown")
    print("=" * 65)

if __name__ == "__main__":
    main()