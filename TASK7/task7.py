import os
import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor

STUDENT_ID = 230103317
NUM_ELEMENTS = 30_000_000

def kernel_a_worker(a_chunk):
    """Kernel A (Memory-Bound): Vector copy B[i] = A[i]."""
    return np.copy(a_chunk)

def kernel_b_worker(a_chunk):
    """Kernel B (Compute-Bound): Trigonometric math operations."""
    return np.sin(a_chunk) * np.cos(a_chunk) + np.tan(a_chunk)

def run_parallel_kernel(kernel_func, data, num_workers):
    chunks = np.array_split(data, num_workers)
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        results = list(executor.map(kernel_func, chunks))
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0

def main():
    max_cores = os.cpu_count() or 2
    worker_counts = sorted(list(set([1, 2, max_cores])))

    print(f"Student ID       : {STUDENT_ID}")
    print(f"Array Size       : {NUM_ELEMENTS:,} elements")
    print(f"Max Cores        : {max_cores}")
    print("=" * 70)

    # Generate data array
    seed = STUDENT_ID % 9967
    np.random.seed(seed)
    A = np.random.random(NUM_ELEMENTS).astype(np.float64)

    # --- BENCHMARK KERNEL A (MEMORY-BOUND) ---
    t1_mem = run_parallel_kernel(kernel_a_worker, A, 1)
    mem_results = []
    
    print("\n--- [KERNEL A: MEMORY-BOUND (VECTOR COPY)] ---")
    print(f"{'Cores':<8} | {'Wall Time (ms)':<15} | {'Speedup':<10} | {'Efficiency':<12}")
    print("-" * 55)
    for p in worker_counts:
        t_p = run_parallel_kernel(kernel_a_worker, A, p)
        speedup = t1_mem / t_p if t_p > 0 else 1.0
        efficiency = speedup / p
        mem_results.append((p, t_p, speedup, efficiency))
        print(f"{p:<8} | {t_p:<15.2f} | {speedup:<10.2f} | {efficiency:<12.2%}")

    # --- BENCHMARK KERNEL B (COMPUTE-BOUND) ---
    t1_comp = run_parallel_kernel(kernel_b_worker, A, 1)
    comp_results = []

    print("\n--- [KERNEL B: COMPUTE-BOUND (TRIGONOMETRIC MATH)] ---")
    print(f"{'Cores':<8} | {'Wall Time (ms)':<15} | {'Speedup':<10} | {'Efficiency':<12}")
    print("-" * 55)
    for p in worker_counts:
        t_p = run_parallel_kernel(kernel_b_worker, A, p)
        speedup = t1_comp / t_p if t_p > 0 else 1.0
        efficiency = speedup / p
        comp_results.append((p, t_p, speedup, efficiency))
        print(f"{p:<8} | {t_p:<15.2f} | {speedup:<10.2f} | {efficiency:<12.2%}")

    # --- ANALYSIS & SATURATION SUMMARY ---
    print("\n" + "=" * 70)
    mem_max_eff = mem_results[-1][3]
    comp_max_eff = comp_results[-1][3]

    if mem_max_eff < comp_max_eff:
        stalled_kernel = "Kernel A (Memory-Bound)"
    else:
        stalled_kernel = "Kernel B (Compute-Bound)"

    print(f"ANALYSIS SUMMARY:")
    print(f"Kernel A Max-Core Efficiency : {mem_max_eff:.2%}")
    print(f"Kernel B Max-Core Efficiency : {comp_max_eff:.2%}")
    print(f"SATURATION DIAGNOSIS        : {stalled_kernel} stalled in scaling due to memory channel saturation.")
    print("=" * 70)

if __name__ == "__main__":
    main()