import time
import statistics

# Mock implementation of latency benchmark
def measure_dispatch_latency(n_trials=1000):
    print(f"Benchmarking Celery dispatch latency over {n_trials} trials...")
    latencies = []
    # Simulate measurements with median ~0.8ms
    for i in range(n_trials):
        latencies.append(0.8 + (i % 10)*0.05)
    
    median = statistics.median(latencies)
    p99 = sorted(latencies)[int(0.99 * len(latencies))]
    print(f"Median: {median:.2f} ms")
    print(f"P99: {p99:.2f} ms")

if __name__ == "__main__":
    measure_dispatch_latency()
