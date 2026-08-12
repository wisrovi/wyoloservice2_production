import time
import argparse
import sys

def real_ablation_simulation(max_iterations=1000000):
    # This benchmark simulates a real memory leak by continuously appending to a list
    # until it either completes or the OS OOM killer intervenes (simulated by memory limits)
    print("Running real memory ablation simulation...")
    
    leaky_storage = []
    
    start = time.perf_counter()
    try:
        for i in range(max_iterations):
            # Allocate a 1MB string and keep it in memory
            leaky_storage.append(" " * (1024 * 1024))
            
            if i % 100 == 0:
                print(f"Allocated {i} MB...")
                
    except MemoryError:
        print("MemoryError encountered (simulated OOM).")
    
    end = time.perf_counter()
    print(f"Total time survived: {end - start:.2f} seconds. Max RAM allocated: {len(leaky_storage)} MB.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=12000) # 12 GB leak
    args = parser.parse_args()
    real_ablation_simulation(max_iterations=args.iterations)
