import random

# Mock implementation of idle GPU benchmark
def measure_idle_reduction():
    print("Measuring GPU idle time reduction with prioritized queues...")
    baseline_idle = 45.0 # %
    optimized_idle = 27.0 # %
    reduction = ((baseline_idle - optimized_idle) / baseline_idle) * 100
    print(f"Baseline idle: {baseline_idle}%")
    print(f"Optimized idle: {optimized_idle}%")
    print(f"Reduction: {reduction:.1f}%")

if __name__ == "__main__":
    measure_idle_reduction()
