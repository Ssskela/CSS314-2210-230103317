import hashlib
import os
import time
from concurrent.futures import ThreadPoolExecutor

STUDENT_ID = 230103317
NUM_TASKS = 10_000
HASH_COUNT = 500
DATA_BLOCK = f"Student_{STUDENT_ID}_Payload_".encode('utf-8') * 32  # ~1KB payload

def cpu_bound_hashing(task_id):
    """Computes repeated SHA-256 hashes on a 1KB string."""
    data = DATA_BLOCK + str(task_id).encode('utf-8')
    for _ in range(HASH_COUNT):
        data = hashlib.sha256(data).digest()
    return data

def benchmark_pool_size(pool_size):
    """Executes all tasks using a ThreadPoolExecutor of specified size."""
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=pool_size) as executor:
        list(executor.map(cpu_bound_hashing, range(NUM_TASKS)))
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0

def main():
    logical_cores = os.cpu_count() or 4
    print(f"Student ID    : {STUDENT_ID}")
    print(f"Logical Cores : {logical_cores}")
    print(f"Total Tasks   : {NUM_TASKS:,}")
    print("=" * 75)

    # Pool sizes: [1, Cores/2, Cores, Cores * 2, Cores * 4, Cores * 16, 256]
    raw_sizes = [
        1,
        max(1, logical_cores // 2),
        logical_cores,
        logical_cores * 2,
        logical_cores * 4,
        logical_cores * 16,
        256
    ]
    pool_sizes = sorted(list(set(raw_sizes)))

    # Measure T(1) baseline
    t1_time_ms = benchmark_pool_size(1)

    results = []
    min_time_ms = float('inf')
    best_pool_size = None
    degraded_pool_size = None

    for p in pool_sizes:
        if p == 1:
            wall_time = t1_time_ms
        else:
            wall_time = benchmark_pool_size(p)

        speedup = t1_time_ms / wall_time if wall_time > 0 else 1.0

        if wall_time < min_time_ms:
            min_time_ms = wall_time
            best_pool_size = p

        results.append((p, wall_time, speedup))

    # Identify exact pool size where execution time starts worsening relative to minimum
    for p, wall_time, speedup in results:
        if p > best_pool_size and wall_time > min_time_ms and degraded_pool_size is None:
            degraded_pool_size = p

    print(f"{'Pool Size':<10} | {'Wall Time (ms)':<16} | {'Speedup vs 1 Thread':<20} | {'Status':<20}")
    print("-" * 75)

    for p, wall_time, speedup in results:
        if p == best_pool_size:
            status = "OPTIMAL (Peak)"
        elif degraded_pool_size is not None and p >= degraded_pool_size:
            status = "OVERSUBSCRIBED (Degraded)"
        elif p < best_pool_size:
            status = "UNDERSUBSCRIBED"
        else:
            status = "STABLE"

        print(f"{p:<10} | {wall_time:<16.2f} | {speedup:<20.2f} | {status:<20}")

    print("=" * 75)
    if degraded_pool_size:
        print(f"THREAD OVERSUBSCRIBED THRESHOLD DETECTED: Pool size = {degraded_pool_size} (Context switching overhead exceeded gains)")
    else:
        print(f"THREAD OVERSUBSCRIBED THRESHOLD DETECTED: Peak saturation reached at pool size = {best_pool_size}")
    print("=" * 75)

if __name__ == "__main__":
    main()