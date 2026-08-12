import time
import argparse
import docker

def real_docker_ablation(memory_limit="11g"):
    print(f"Running real Docker OOM test with memory_limit={memory_limit}...")
    try:
        client = docker.from_env()
    except Exception as e:
        print(f"Docker is not available: {e}. Skipping real execution.")
        return
        
    start = time.perf_counter()
    try:
        # Run a container that allocates memory until it gets killed
        container = client.containers.run(
            "python:3.10-slim",
            command='python -c "a = []; \\nwhile True: a.append(\' \' * 1024 * 1024)"',
            mem_limit=memory_limit,
            detach=True
        )
        container.wait() # Will exit with 137 when OOM killed
    except Exception as e:
        print(f"Container failed: {e}")
        
    end = time.perf_counter()
    print(f"Docker OOM survival time: {end - start:.2f} seconds.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=str, default="11g")
    args = parser.parse_args()
    real_docker_ablation(memory_limit=args.limit)
