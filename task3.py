import os
import time
from concurrent.futures import ThreadPoolExecutor

STUDENT_ID = 230103317
NUM_ITERATIONS = 50_000_000

def unpadded_worker(shared_counts, thread_id):
    """Causes false sharing by frequently mutating adjacent memory slots."""
    for _ in range(NUM_ITERATIONS):
        shared_counts[thread_id] += 1

def padded_worker(shared_counts, thread_id):
    """Eliminates false sharing by using a local variable in CPU registers/cache."""
    local_count = 0
    for _ in range(NUM_ITERATIONS):
        local_count += 1
    shared_counts[thread_id] = local_count

def run_unpadded(num_threads):
    shared_counts = [0] * num_threads
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(unpadded_worker, shared_counts, i) for i in range(num_threads)]
        for f in futures:
            f.result()
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0, shared_counts

def run_padded(num_threads):
    shared_counts = [0] * num_threads
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(padded_worker, shared_counts, i) for i in range(num_threads)]
        for f in futures:
            f.result()
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0, shared_counts

def main():
    num_threads = os.cpu_count() or 2
    print(f"Student ID       : {STUDENT_ID}")
    print(f"Physical/Logical : {num_threads} cores")
    print(f"Iterations/Thread: {NUM_ITERATIONS:,}")
    print("=" * 60)

    # 1. Unpadded Shared Run
    unpadded_time, unpadded_res = run_unpadded(num_threads)
    print(f"Unpadded Shared Time : {unpadded_time:.2f} ms")

    # 2. Local / Padded Run
    padded_time, padded_res = run_padded(num_threads)
    print(f"Local / Padded Time  : {padded_time:.2f} ms")

    # 3. Execution Ratio
    ratio = unpadded_time / padded_time if padded_time > 0 else 1.0
    print("-" * 60)
    print(f"Execution Time Ratio : {ratio:.2f}x slowdown from False Sharing")
    print("=" * 60)

if __name__ == "__main__":
    main()