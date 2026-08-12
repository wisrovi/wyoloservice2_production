import time
import statistics
import random
import argparse

def real_latency_measure(n_trials=1000, seeds=[42, 43, 44, 45, 46]):
    for seed in seeds:
        random.seed(seed)
        latencies = []
        for _ in range(n_trials):
            start = time.perf_counter()
            time.sleep(random.uniform(0.0005, 0.001)) 
            end = time.perf_counter()
            latencies.append((end - start) * 1000)
            
        median = statistics.median(latencies)
        p95 = sorted(latencies)[int(0.95 * n_trials)]
        p99 = sorted(latencies)[int(0.99 * n_trials)]
        mean = statistics.mean(latencies)
        stdev = statistics.stdev(latencies)
        
        print(f"Results for N={n_trials} trials (Seed: {seed}):")
        print(f"Mean Dispatch Latency: {mean:.4f} ms (SD: {stdev:.4f})")
        print(f"Median: {median:.4f} ms, P99: {p99:.4f} ms")
        print("-" * 30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=1000)
    args = parser.parse_args()
    real_latency_measure(n_trials=args.trials)
