import os
import sys
import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor

STUDENT_ID = 230103317
ARRAY_SIZE = 2_000_000

def serial_prefix_scan(arr):
    """Serial inclusive prefix sum."""
    return np.cumsum(arr)

def chunk_prefix_scan(chunk, offset):
    """Computes local inclusive prefix sum plus an incoming offset."""
    return np.cumsum(chunk) + offset

def parallel_prefix_scan(arr, num_workers):
    """2-Pass Parallel Prefix Scan:
    Pass 1: Split into chunks & compute chunk totals to get offset reduction.
    Pass 2: Apply cumulative offsets in parallel to each chunk.
    """
    if num_workers <= 1:
        return serial_prefix_scan(arr)

    chunks = np.array_split(arr, num_workers)
    
    # Step 1: Compute sum of each chunk
    chunk_sums = [np.sum(c) for c in chunks]
    
    # Step 2: Compute starting offsets for each chunk (exclusive scan of chunk sums)
    offsets = [0] + list(np.cumsum(chunk_sums)[:-1])

    # Step 3: Compute chunk prefix scans in parallel using calculated offsets
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [
            executor.submit(chunk_prefix_scan, chunks[i], offsets[i])
            for i in range(num_workers)
        ]
        scanned_chunks = [f.result() for f in futures]

    return np.concatenate(scanned_chunks)

def main():
    num_cores = os.cpu_count() or 2
    print(f"Student ID    : {STUDENT_ID}")
    print(f"Array Size    : {ARRAY_SIZE:,} elements")
    print(f"Worker Cores  : {num_cores}")
    print("=" * 65)

    # Generate 2,000,000 integers (values 1 to 10) using Student ID seed
    seed = STUDENT_ID % 9967
    np.random.seed(seed)
    data = np.random.randint(1, 11, size=ARRAY_SIZE, dtype=np.int64)

    # 1. Serial Inclusive Prefix Scan
    t0 = time.perf_counter()
    serial_out = serial_prefix_scan(data)
    t_serial_ms = (time.perf_counter() - t0) * 1000.0

    # 2. Parallel 2-Pass Chunked Prefix Scan
    t0 = time.perf_counter()
    parallel_out = parallel_prefix_scan(data, num_cores)
    t_parallel_ms = (time.perf_counter() - t0) * 1000.0

    # 3. Verification Constraint
    passed = parallel_out[-1] == serial_out[-1]
    status_str = "PASS" if passed else "FAIL"

    if not passed:
        print(f"VERIFICATION FAILURE: Parallel ({parallel_out[-1]}) != Serial ({serial_out[-1]})")
        sys.exit(1)

    # 4. Results & Timing Output
    speedup = t_serial_ms / t_parallel_ms if t_parallel_ms > 0 else 1.0

    print(f"{'Serial Time (ms)':<18} | {'Parallel Time (ms)':<20} | {'Speedup':<10} | {'Verification Status':<18}")
    print("-" * 65)
    print(f"{t_serial_ms:<18.2f} | {t_parallel_ms:<20.2f} | {speedup:<10.2f} | {status_str:<18}")
    print("=" * 65)

if __name__ == "__main__":
    main()