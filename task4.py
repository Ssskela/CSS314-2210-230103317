import time
from concurrent.futures import ThreadPoolExecutor

STUDENT_ID = 230103317
NUM_ITEMS = 1000
NUM_WORKERS = 4

def simulate_work(item_index):
    """Simulates non-uniform workload cost: sleep(0.0001 * (i % 20))."""
    cost = 0.0001 * (item_index % 20)
    if cost > 0:
        time.sleep(cost)
    return item_index

def run_strategy_a_static():
    """Strategy A: Static chunk distribution (equal blocks per core)."""
    # Pre-split 1000 items into 4 equal chunks of 250 items
    chunks = [list(range(i * 250, (i + 1) * 250)) for i in range(NUM_WORKERS)]
    
    thread_finish_times = [0.0] * NUM_WORKERS
    t_start = time.perf_counter()

    def static_worker(worker_id, item_chunk):
        for item in item_chunk:
            simulate_work(item)
        thread_finish_times[worker_id] = time.perf_counter()

    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        futures = [executor.submit(static_worker, i, chunks[i]) for i in range(NUM_WORKERS)]
        for f in futures:
            f.result()

    t_end = time.perf_counter()
    total_time_ms = (t_end - t_start) * 1000.0
    
    # Delta between first and last thread finishing
    min_finish = min(thread_finish_times)
    max_finish = max(thread_finish_times)
    completion_delta_ms = (max_finish - min_finish) * 1000.0

    return total_time_ms, completion_delta_ms

def run_strategy_b_dynamic(chunk_size=5):
    """Strategy B: Dynamic scheduling / work-stealing queue (chunk_size = 5)."""
    thread_finish_times = []
    t_start = time.perf_counter()

    def dynamic_worker(item_chunk):
        for item in item_chunk:
            simulate_work(item)
        thread_finish_times.append(time.perf_counter())

    # Create chunks of size 5
    items = list(range(NUM_ITEMS))
    chunks = [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]

    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        # executor.map dynamically distributes chunks as workers become free
        list(executor.map(dynamic_worker, chunks))

    t_end = time.perf_counter()
    total_time_ms = (t_end - t_start) * 1000.0
    
    min_finish = min(thread_finish_times)
    max_finish = max(thread_finish_times)
    completion_delta_ms = (max_finish - min_finish) * 1000.0

    return total_time_ms, completion_delta_ms

def main():
    print(f"Student ID    : {STUDENT_ID}")
    print(f"Total Items   : {NUM_ITEMS}")
    print(f"Workers       : {NUM_WORKERS}")
    print("=" * 65)

    # Benchmark Strategy A: Static Chunking
    stat_time, stat_delta = run_strategy_a_static()

    # Benchmark Strategy B: Dynamic Scheduling
    dyn_time, dyn_delta = run_strategy_b_dynamic(chunk_size=5)

    print(f"{'Scheduling Strategy':<30} | {'Total Time (ms)':<16} | {'Finish Delta (ms)':<16}")
    print("-" * 65)
    print(f"{'Strategy A (Static Chunks)':<30} | {stat_time:<16.2f} | {stat_delta:<16.2f}")
    print(f"{'Strategy B (Dynamic Queue)':<30} | {dyn_time:<16.2f} | {dyn_delta:<16.2f}")
    print("=" * 65)
    
    ratio = stat_time / dyn_time if dyn_time > 0 else 1.0
    print(f"Dynamic Scheduling Speedup Ratio: {ratio:.2f}x")

if __name__ == "__main__":
    main()