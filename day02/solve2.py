# the key change in part 2 is that in order to be invalid, an ID must have the same pattern repeat at least twice
# this means 2 of our key assumptions are no longer valid:
# 1. we cannot rule out odd numbered buckets
# 2. the prefix length is not always fixed
# brute force is definitely not a good option here
# is it reasonable to build prefix combinations from 1 to n//3?
# say we are checking 1234123412341234
# we check prefix 1 -> fails
# check prefix 12 -> fails
# check prefix 123 -> fails
# check prefix 1234 -> passes
# but we can't do this for every combination...

# maybe instead we build the possible prefixes from the ranges of 1 to n//3
# so for bucket 100000-999999 we must check prefixes 1-9 and 10-99
# -> 101010, 111111, 121212
# I *think* this will work

# another assumption: ranges are not overlapping
# we actually kind of need to handle this anyway since, we could build repeated prefixes
# like 2 repeated 6 times is the same as 22 repeated 3 times for checking 222222

import argparse
from math import ceil

TEST_SOLUTION = 4174379265

def solve(buckets: list[str]) -> int:
    solution = 0
    visited = set()
    for bucket in preprocess_buckets(buckets):
        lower, upper = bucket.split("-")
        bucket_len = len(lower)
        # use //2 since we know patterns must repeat at least twice
        for n in range(1, (bucket_len//2)+1):
            # m -> number of times to repeat the prefix
            # e.g. for 10000 and prefix 1 we want to repeat 5 times, for prefix 10 we want to repeat 3 times
            m = ceil(bucket_len/n)
            # impossible to generate a valid combo for this prefix repeated m times
            if (n * m) % bucket_len:
                continue
            prefix_range = [str(prefix) for prefix in range(max(1, int(lower[:n])), int(upper[:n])+1)]
            for prefix in prefix_range:
                print(f"Checking {prefix} repeated {m} times in bucket {bucket}")
                candidate = prefix * m
                if candidate not in visited and candidate >= lower and candidate <= upper:
                    visited.add(candidate)
                    solution += int(candidate)
                    print(f"Found candidate {candidate} for bucket {bucket}")
    return solution

def preprocess_buckets(buckets: list[str]) -> list[str]:
    """
    Convert all buckets to be the same number of digits.
    **KEY CHANGE FROM PART 1: no longer remove odds
    E.g. 99-100001 -> 99-99, 100-999, 1000-9999, 100000-100001
    """
    new_buckets = []
    for bucket in buckets:
        lower, upper = bucket.split("-")
        # if lower and upper bound share same number of digits, keep as is
        if len(lower) == len(upper):
            new_buckets.append(bucket)
            print(f"Preserving bucket {bucket}")
        else:
            temp_buckets = []
            # build the new lower limit for upper bucket, e.g. 99-1001 -> 1000-1001
            temp_lower = 10**(len(upper)-1)
            temp_buckets.append(format_bucket(temp_lower, upper))
            # build the new upper limit for lower bucket, e.g. 99-1001 -> 99-99
            temp_upper = 10**(len(lower))-1
            temp_buckets.append(format_bucket(lower, temp_upper))
            # build the intermediate ranges
            # e.g. 99-100001 -> 1000-9999
            for i in range(len(lower)+1, len(upper)):
                temp_buckets.append(format_bucket(10**(i-1), (10**i)-1))
            print(f"Extracted buckets from range: {bucket} -> {temp_buckets}")
            new_buckets.extend(temp_buckets)
    return new_buckets

def format_bucket(i, j):
    return f"{i}-{j}"

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