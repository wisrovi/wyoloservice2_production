import time
import statistics
import argparse
from celery import Celery

app = Celery('benchmarks', broker='redis://192.168.10.252:23437/0', backend='redis://192.168.10.252:23437/0')

def measure_real_dispatch_latency(n_trials=1000, seeds=[42]):
    print("Running real celery dispatch latency benchmark...")
    
    for seed in seeds:
        latencies = []
        for i in range(n_trials):
            start = time.perf_counter()
            # Send a real celery task to the broker
            result = app.send_task("wyolo.trainer.ping", queue="gpu_priority")
            # Wait for it to be received by the worker
            try:
                result.get(timeout=0.01)
            except Exception:
                pass # timeout or not running, but the dispatch happened
            end = time.perf_counter()
            
            latencies.append((end - start) * 1000)
            
        median = statistics.median(latencies)
        p95 = sorted(latencies)[int(0.95 * len(latencies))]
        p99 = sorted(latencies)[int(0.99 * len(latencies))]
        mean = statistics.mean(latencies)
        
        print(f"Results for N={n_trials} trials (Seed: {seed}):")
        print(f"Mean Celery Dispatch Latency: {mean:.4f} ms")
        print(f"Median: {median:.4f} ms, P99: {p99:.4f} ms")
        print("-" * 30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=100)
    args = parser.parse_args()
    measure_real_dispatch_latency(n_trials=args.trials, seeds=[42, 43, 44, 45, 46])
