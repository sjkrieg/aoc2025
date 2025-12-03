# alternate solution for solve2 trying a regex solution
# results:
# skrieg@skrieg-1526 day02 % python time.py 
# Running solve2.py 100 times...

# Total time: 2.6082 seconds
# Average per run: 0.0261 seconds
# Running solve2_alt.py 100 times...

# Total time: 91.3091 seconds
# Average per run: 0.9131 seconds

import argparse
import re

TEST_SOLUTION = 4174379265

def solve(buckets: list[str]) -> int:
    re_pattern = r"^([0-9]+?)\1+$"
    solution = 0
    for bucket in buckets:
        lower, upper = map(int, bucket.split("-"))
        for candidate in range(lower, upper+1):
            if re.match(re_pattern, str(candidate)):
                solution += candidate
    return solution

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", action="store_true")
    args = parser.parse_args()

    if args.test:
        inf = "test.txt"
    else:
        inf = "input.txt"

    with open(inf, "r") as inf:
        line = inf.read().strip()
    if "\n" in line:
        raise ValueError("Found newline in input, something went wrong")
    
    solution = solve(line.split(","))

    print(f"Output: {solution}")
    if args.test:
        if solution == TEST_SOLUTION:
            print("Correct!")
        else:
            print(f"Incorrect! Expected {TEST_SOLUTION}")

if __name__ == "__main__":
    main()