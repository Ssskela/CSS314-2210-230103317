import math
import random
import time
from threading import Thread, Lock

STUDENT_ID = 230103317
TOTAL_SAMPLES = 40_000_000
NUM_THREADS = 4
SAMPLES_PER_THREAD = TOTAL_SAMPLES // NUM_THREADS

# Shared PRNG and Lock for Strategy 1
shared_prng = random.Random()
shared_lock = Lock()

def shared_prng_worker(results, thread_id):
    """Worker using a shared PRNG instance guarded by a Mutex lock."""
    inside_circle = 0
    for _ in range(SAMPLES_PER_THREAD):
        with shared_lock:
            x = shared_prng.random()
            y = shared_prng.random()
        if x * x + y * y <= 1.0:
            inside_circle += 1
    results[thread_id] = inside_circle

def independent_prng_worker(results, thread_id):
    """Worker using thread-isolated PRNG seeded with (STUDENT_ID * 10) + thread_index."""
    seed_val = (STUDENT_ID * 10) + thread_id
    local_prng = random.Random(seed_val)
    inside_circle = 0
    for _ in range(SAMPLES_PER_THREAD):
        x = local_prng.random()
        y = local_prng.random()
        if x * x + y * y <= 1.0:
            inside_circle += 1
    results[thread_id] = inside_circle

def main():
    print(f"Student ID       : {STUDENT_ID}")
    print(f"Total Samples    : {TOTAL_SAMPLES:,}")
    print(f"Threads          : {NUM_THREADS}")
    print("=" * 70)

    # 1. Strategy 1: Shared PRNG with Lock
    results_shared = [0] * NUM_THREADS
    t0 = time.perf_counter()
    threads = [Thread(target=shared_prng_worker, args=(results_shared, i)) for i in range(NUM_THREADS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    t_shared_ms = (time.perf_counter() - t0) * 1000.0

    pi_shared = (4.0 * sum(results_shared)) / TOTAL_SAMPLES
    err_shared = abs(pi_shared - math.pi)

    print("--- [1. SHARED PRNG (MUTEX LOCKED)] ---")
    print(f"Computed Pi      : {pi_shared:.8f}")
    print(f"Absolute Error   : {err_shared:.8f}")
    print(f"Wall Time        : {t_shared_ms:.2f} ms")
    print("-" * 70)

    # 2. Strategy 2: Independent Thread-Local PRNG
    results_indep = [0] * NUM_THREADS
    t0 = time.perf_counter()
    threads = [Thread(target=independent_prng_worker, args=(results_indep, i)) for i in range(NUM_THREADS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    t_indep_ms = (time.perf_counter() - t0) * 1000.0

    pi_indep = (4.0 * sum(results_indep)) / TOTAL_SAMPLES
    err_indep = abs(pi_indep - math.pi)

    print("--- [2. INDEPENDENT PRNG (STATE ISOLATED)] ---")
    print(f"Computed Pi      : {pi_indep:.8f}")
    print(f"Absolute Error   : {err_indep:.8f}")
    print(f"Wall Time        : {t_indep_ms:.2f} ms")
    print("-" * 70)

    # 3. Speedup Factor
    speedup = t_shared_ms / t_indep_ms if t_indep_ms > 0 else 1.0
    print(f"PRNG State Isolation Speedup Factor : {speedup:.2f}x faster")
    print("=" * 70)

if __name__ == "__main__":
    main()