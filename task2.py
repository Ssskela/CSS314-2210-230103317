import os
import platform
import time
import numpy as np
from concurrent.futures import ProcessPoolExecutor

STUDENT_ID = 230103317

def chunk_sum(chunk):
    """Worker function to compute sum of a array slice."""
    return np.sum(chunk)

def parallel_sum(data, num_workers):
    """Distributes array summation across num_workers processes."""
    if num_workers == 1:
        return np.sum(data)
    
    # Split array into roughly equal chunks
    chunks = np.array_split(data, num_workers)
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        results = list(executor.map(chunk_sum, chunks))
        
    return sum(results)

def main():
    print(f"Student ID    : {STUDENT_ID}")
    print(f"Logical Cores : {os.cpu_count()}")
    print("=" * 65)

    # Generate 20,000,000 float64 elements
    seed = STUDENT_ID % 9967
    np.random.seed(seed)
    data = np.random.random(20_000_000).astype(np.float64)

    # Determine worker counts: [1, 2, 4, max_cores, max_cores * 2]
    max_cores = os.cpu_count() or 2
    worker_counts = sorted(list(set([1, 2, 4, max_cores, max_cores * 2])))
    
    P = 0.95  # 95% parallelizable fraction

    # Warmup / Baseline T(1)
    t0 = time.perf_counter()
    _ = parallel_sum(data, 1)
    t1 = time.perf_counter()
    t1_time_ms = (t1 - t0) * 1000.0

    print(f"{'Cores':<8} | {'Wall Time (ms)':<15} | {'Speedup S(p)':<13} | {'Amdahl Upper Bound':<18}")
    print("-" * 65)

    for p in worker_counts:
        t0 = time.perf_counter()
        _ = parallel_sum(data, p)
        t_p = time.perf_counter()
        wall_time_ms = (t_p - t0) * 1000.0

        # Speedup S(p) = T(1) / T(p)
        speedup = t1_time_ms / wall_time_ms if wall_time_ms > 0 else 1.0

        # Amdahl's Law: S_amdahl = 1 / ((1 - P) + (P / p))
        amdahl_bound = 1.0 / ((1.0 - P) + (P / p))

        print(f"{p:<8} | {wall_time_ms:<15.2f} | {speedup:<13.2f} | {amdahl_bound:<18.2f}")

    print("=" * 65)

if __name__ == "__main__":
    main()