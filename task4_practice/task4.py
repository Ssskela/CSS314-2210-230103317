import time
import numpy as np
from multiprocessing import Process, Queue
from multiprocessing.shared_memory import SharedMemory

STUDENT_ID = 230103317

def ipc_pipe_worker(queue):
    """Worker for Path A: Receives serialized array via IPC Queue."""
    data = queue.get()
    _ = np.sum(data)

def shared_mem_worker(shm_name, shape, dtype):
    """Worker for Path B: Attaches to Zero-Copy Shared Memory."""
    existing_shm = SharedMemory(name=shm_name)
    data = np.ndarray(shape, dtype=dtype, buffer=existing_shm.buf)
    _ = np.sum(data)
    existing_shm.close()

def benchmark_path_a_ipc(data):
    """Path A: Measures IPC Queue serialization and transfer overhead."""
    queue = Queue()
    p = Process(target=ipc_pipe_worker, args=(queue,))
    p.start()
    
    t0 = time.perf_counter()
    queue.put(data)
    p.join()
    t1 = time.perf_counter()
    
    return (t1 - t0) * 1000.0

def benchmark_path_b_shared_memory(data):
    """Path B: Measures Zero-Copy Shared Memory transfer overhead."""
    shm = SharedMemory(create=True, size=data.nbytes)
    shm_arr = np.ndarray(data.shape, dtype=data.dtype, buffer=shm.buf)
    shm_arr[:] = data[:]  # Write data into shared memory buffer

    p = Process(target=shared_mem_worker, args=(shm.name, data.shape, data.dtype))
    
    t0 = time.perf_counter()
    p.start()
    p.join()
    t1 = time.perf_counter()
    
    shm.close()
    shm.unlink()
    return (t1 - t0) * 1000.0

def main():
    print(f"Student ID : {STUDENT_ID}")
    print("=" * 70)

    n_sizes = [100_000, 1_000_000, 10_000_000]
    
    seed = STUDENT_ID % 9967
    np.random.seed(seed)

    print(f"{'Array Size (N)':<15} | {'Path A IPC (ms)':<18} | {'Path B Zero-Copy (ms)':<22} | {'Speedup':<10}")
    print("-" * 70)

    for N in n_sizes:
        data = np.random.random(N).astype(np.float64)

        time_ipc = benchmark_path_a_ipc(data)
        time_shm = benchmark_path_b_shared_memory(data)

        speedup = time_ipc / time_shm if time_shm > 0 else 1.0

        print(f"{N:<15,} | {time_ipc:<18.2f} | {time_shm:<22.2f} | {speedup:<10.2f}x")

    print("=" * 70)

if __name__ == "__main__":
    main()