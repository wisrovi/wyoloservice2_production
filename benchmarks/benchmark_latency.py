import time
import statistics
import argparse
import subprocess
import os

def measure_real_dispatch_latency(n_trials=10, seeds=[42]):
    # This benchmark measures the actual overhead of spawning a task
    # We will use subprocess to measure the invocation time of a real python process
    # to simulate the overhead of spawning an executor vs a native thread.
    print("Running real dispatch latency benchmark...")
    
    for seed in seeds:
        latencies = []
        for i in range(n_trials):
            start = time.perf_counter()
            # Real work: spawn a python process that exits immediately
            subprocess.run(["python3", "-c", "pass"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            end = time.perf_counter()
            
            # Record latency in milliseconds
            latencies.append((end - start) * 1000)
            
        median = statistics.median(latencies)
        p95 = sorted(latencies)[int(0.95 * n_trials)]
        p99 = sorted(latencies)[int(0.99 * n_trials)]
        mean = statistics.mean(latencies)
        stdev = statistics.stdev(latencies) if len(latencies) > 1 else 0.0
        
        print(f"Results for N={n_trials} trials (Seed: {seed}):")
        print(f"Mean Dispatch Latency: {mean:.4f} ms (SD: {stdev:.4f})")
        print(f"Median: {median:.4f} ms, P99: {p99:.4f} ms")
        print("-" * 30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=100)
    args = parser.parse_args()
    measure_real_dispatch_latency(n_trials=args.trials, seeds=[42, 43, 44, 45, 46])
