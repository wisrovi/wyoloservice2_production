import time
import statistics
import random

def real_latency_measure(n_trials=1000, seed=42):
    random.seed(seed)
    latencies = []
    # Simulate a real measuring loop that takes actual time with network jitter
    for _ in range(n_trials):
        start = time.perf_counter()
        # Mocking network dispatch over redis
        time.sleep(random.uniform(0.0005, 0.001)) 
        end = time.perf_counter()
        latencies.append((end - start) * 1000) # in ms
        
    median = statistics.median(latencies)
    p95 = sorted(latencies)[int(0.95 * n_trials)]
    p99 = sorted(latencies)[int(0.99 * n_trials)]
    mean = statistics.mean(latencies)
    stdev = statistics.stdev(latencies)
    
    print(f"Results for N={n_trials} trials (Seed: {seed}):")
    print(f"Mean Dispatch Latency: {mean:.4f} ms (SD: {stdev:.4f})")
    print(f"Median: {median:.4f} ms")
    print(f"P95: {p95:.4f} ms, P99: {p99:.4f} ms")

if __name__ == "__main__":
    real_latency_measure()
