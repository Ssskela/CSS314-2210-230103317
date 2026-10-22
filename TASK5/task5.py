import os
import time
import numpy as np
from concurrent.futures import ProcessPoolExecutor

STUDENT_ID = 230103317

def vector_worker(x_chunk, a, b):
    """Computes y = a * x + b for a single array chunk."""
    return a * x_chunk + b

def serial_axpy(x, a, b):
    """Single-threaded serial vector operation."""
    return a * x + b

def parallel_axpy(x, a, b, num_workers):
    """Multi-threaded/process vector operation."""
    if num_workers <= 1 or x.size < 1000:
        return serial_axpy(x, a, b)
    
    chunks = np.array_split(x, num_workers)
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(vector_worker, chunk, a, b) for chunk in chunks]
        results = [f.result() for f in futures]
    return np.concatenate(results)

def main():
    num_cores = os.cpu_count() or 2
    print(f"Student ID    : {STUDENT_ID}")
    print(f"Logical Cores : {num_cores}")
    print("=" * 70)

    # Array sizes N to test
    n_sizes = [100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000]
    a, b = 2.5, 1.5

    seed = STUDENT_ID % 9967
    np.random.seed(seed)

    print(f"{'Array Size (N)':<15} | {'Serial (ms)':<12} | {'Parallel (ms)':<13} | {'Faster Method':<15}")
    print("-" * 70)

    crossover_point = None
    prev_faster = None

    for N in n_sizes:
        x = np.random.random(N).astype(np.float64)

        # Benchmark Serial Execution (averaged over 3 runs)
        t0 = time.perf_counter()
        for _ in range(3):
            _ = serial_axpy(x, a, b)
        t_serial_ms = ((time.perf_counter() - t0) / 3.0) * 1000.0

        # Benchmark Parallel Execution (averaged over 3 runs)
        t0 = time.perf_counter()
        for _ in range(3):
            _ = parallel_axpy(x, a, b, num_cores)
        t_parallel_ms = ((time.perf_counter() - t0) / 3.0) * 1000.0

        faster = "PARALLEL" if t_parallel_ms < t_serial_ms else "SERIAL"

        # Programmatically detect when PARALLEL shifts from slower to faster
        if prev_faster == "SERIAL" and faster == "PARALLEL" and crossover_point is None:
            crossover_point = (prev_N, N)

        prev_faster = faster
        prev_N = N

        print(f"{N:<15,} | {t_serial_ms:<12.4f} | {t_parallel_ms:<13.4f} | {faster:<15}")

    print("=" * 70)
    
    if crossover_point:
        print(f"EXACT CROSSOVER POINT DETECTED: Between N = {crossover_point[0]:,} and N = {crossover_point[1]:,}")
    else:
        print("EXACT CROSSOVER POINT DETECTED: Parallel overhead exceeds benefits across tested N range.")
    print("=" * 70)

if __name__ == "__main__":
    main()