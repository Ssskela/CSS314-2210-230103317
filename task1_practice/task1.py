import os
import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor

STUDENT_ID = 230103317
MATRIX_DIM = 8000

def row_major_worker(matrix_slice):
    """Mode A: Iterates linearly across rows (cache-friendly)."""
    return np.sum(matrix_slice)

def column_major_worker(matrix, col_indices):
    """Mode B: Strided access down columns across rows (causes cache misses)."""
    total = 0.0
    rows = matrix.shape[0]
    for col in col_indices:
        for row in range(rows):
            total += matrix[row, col]
    return total

def run_mode_a_row_major(matrix, num_workers):
    # Slice matrix along rows (contiguous sub-arrays)
    row_chunks = np.array_split(matrix, num_workers, axis=0)
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        results = list(executor.map(row_major_worker, row_chunks))
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0, sum(results)

def run_mode_b_column_major(matrix, num_workers):
    # Split column indices across workers
    col_indices = np.arange(MATRIX_DIM)
    col_chunks = np.array_split(col_indices, num_workers)
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(column_major_worker, matrix, chunk) for chunk in col_chunks]
        results = [f.result() for f in futures]
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0, sum(results)

def main():
    num_cores = os.cpu_count() or 2
    print(f"Student ID    : {STUDENT_ID}")
    print(f"Logical Cores : {num_cores}")
    print(f"Matrix Size   : {MATRIX_DIM} x {MATRIX_DIM} float64 ({MATRIX_DIM * MATRIX_DIM * 8 / (1024**2):.2f} MB)")
    print("=" * 65)

    # Generate 8,000 x 8,000 float64 matrix using Student ID seed
    seed = STUDENT_ID % 9967
    np.random.seed(seed)
    matrix = np.random.random((MATRIX_DIM, MATRIX_DIM)).astype(np.float64)

    # 1. Mode A: Row-Major Traversal
    time_mode_a, sum_a = run_mode_a_row_major(matrix, num_cores)
    print(f"Mode A (Row-Major Linear) Runtime   : {time_mode_a:.2f} ms")

    # 2. Mode B: Column-Major Strided Traversal
    time_mode_b, sum_b = run_mode_b_column_major(matrix, num_cores)
    print(f"Mode B (Column-Major Strided) Runtime: {time_mode_b:.2f} ms")

    # 3. Cache Penalty Factor Calculation
    penalty_factor = time_mode_b / time_mode_a if time_mode_a > 0 else 1.0
    print("-" * 65)
    print(f"Cache Penalty Factor ((Mode B) / (Mode A)) : {penalty_factor:.2f}x slowdown")
    print("=" * 65)

if __name__ == "__main__":
    main()