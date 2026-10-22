import os
import platform
import time
import numpy as np

STUDENT_ID = 230103317

def main():
    print(f"Student ID    : {STUDENT_ID}")
    print(f"OS Platform   : {platform.system()} {platform.release()} ({platform.architecture()[0]})")
    print(f"CPU Details   : {platform.processor() or platform.machine()}")
    print(f"Logical Cores : {os.cpu_count()}")
    print("-" * 50)

    print("Generating 20,000,000 float64 elements...")
    seed = STUDENT_ID % 9967
    np.random.seed(seed)
    data = np.random.random(20_000_000).astype(np.float64)

    t0 = time.perf_counter()
    
    total_sum = np.sum(data)
    std_dev = np.std(data)
    
    t1 = time.perf_counter()
    execution_time_ms = (t1 - t0) * 1000.0

    print(f"Sum           : {total_sum:.6f}")
    print(f"Std Deviation : {std_dev:.6f}")
    print(f"Execution Time: {execution_time_ms:.2f} ms")
    print("-" * 50)

if __name__ == "__main__":
    main()

#PS C:\Users\Asus> python task1.py | Tee-Object -FilePath task1_output.txt
#Student ID    : 230103317
#OS Platform   : Windows 11 (64bit)
#CPU Details   : Intel64 Family 6 Model 183 Stepping 1, GenuineIntel
#Logical Cores : 20
#--------------------------------------------------
#Generating 20,000,000 float64 elements...
#Sum           : 10000299.833176
#Std Deviation : 0.288682
#Execution Time: 102.04 ms