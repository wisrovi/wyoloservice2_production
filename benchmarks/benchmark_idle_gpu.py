import time
import argparse
import subprocess
import statistics

def get_gpu_utilization():
    try:
        output = subprocess.check_output(["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"])
        return float(output.decode().strip().split('\n')[0])
    except Exception:
        return 0.0 # No GPU

def measure_idle_gpu(duration=120):
    print("Measuring real GPU utilization via nvidia-smi...")
    utils = []
    start = time.time()
    while time.time() - start < duration:
        utils.append(get_gpu_utilization())
        time.sleep(1.0)
    
    avg_util = statistics.mean(utils) if utils else 0
    idle = 100.0 - avg_util
    print(f"Average GPU Utilization: {avg_util:.2f}% (Idle: {idle:.2f}%) over {duration} seconds.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=120)
    args = parser.parse_args()
    measure_idle_gpu(duration=args.duration)
