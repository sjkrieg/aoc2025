import argparse
import subprocess
import time

def main():
    # Number of times to run
    parser = argparse.ArgumentParser()
    parser.add_argument("script_path", type=str)
    parser.add_argument("-n", "--n_runs", default=100, type=int)
    args = parser.parse_args()

    print(f"Running {args.script_path} {args.n_runs} times...")

    start_time = time.perf_counter()

    for i in range(args.n_runs):
        # Run the script, capture_output=True hides the print statements
        subprocess.run(["python", args.script_path], capture_output=True)

    end_time = time.perf_counter()

    total_time = end_time - start_time
    average_time = total_time / args.n_runs

    print(f"Total time: {total_time:.4f} seconds")
    print(f"Average per run: {average_time:.4f} seconds")

if __name__ == "__main__":
    main()