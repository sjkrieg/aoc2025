# this is definitely brute forcible but let's try for an efficient solution
# i.e. instead of iterating over every number in the range we'll try a string-based approach
# that uses prefix matching to generate the candidate IDs from the range information
# this will probably be longer code but would be way more efficient for large ranges/numbers

# probably start by splitting each range into "buckets" with the same length
# e.g. 95-115 -> 95-99, 100-115
# we can immediately discard any buckets with an odd length

# EXAMPLE 1: 95-1150
# have to check buckets 95 and 1150
# 1150 -> prefix 11, suffix = 50 -> duplicate prefix -> 1111 -> check if less than top range -> true
# but this doesn't catch 1010. so maybe we need to iterate over prefix ranges?

# EXAMPLE 2: 95-115116
# should include 99, 1010, 1111, 1212, 1313, 1414, ..., 115115
# OK this makes sense, we need to iterate over a range of the prefixes
# if we do some smart preprocessing this will be very efficient

# after splitting into buckets it should be pretty easy to validate the prefixes
# instead of iterating over each value in the range, we can instead
# generate the combinations from the available prefixes and check if they fall within the bucket
# EXAMPLE 3: 1000-9999
# for prefixes 10, 11, 12, ..., 99, we simply duplicate the prefixes to 1010, 1111, etc. and make sure its valid

# EXAMPLE 4: 1000000000-9999999999
# instead of looping however many millions of times, we just have to generate 10000 strings

import argparse

TEST_SOLUTION = 1227775554

def solve(buckets: list[str]) -> int:
    solution = 0
    for bucket in preprocess_buckets(buckets):
        lower, upper = bucket.split("-")
        if len(lower) % 2 or len(upper) % 2:
            raise ValueError(f"No odd-length buckets allowed! {bucket}")
        lower_prefix, upper_prefix = lower[:len(lower)//2], upper[:len(upper)//2]

        # build prefix range for the current bucket, e.g. for 1000-9999 we check prefixes 10, 11, ..., 99
        # use max(1, lower_prefix) here to handle edge case where lower_prefix is 0, e.g. if lower range is single digit
        prefix_buckets = [str(prefix) for prefix in range(max(1, int(lower_prefix)), int(upper_prefix)+1)]
        for prefix in prefix_buckets:
            # we already know buckets must have even number of chars,
            # just need to check if its within the range
            candidate = prefix + prefix
            if candidate >= lower and candidate <= upper:
                solution += int(candidate)
                print(f"Found invalid ID {candidate} from bucket {bucket}")
    return solution

def preprocess_buckets(buckets: list[str]) -> list[str]:
    """
    Convert all ranges to buckets with the same number of digits and remove odds.
    E.g. 99-100001 -> 99-99, 1000-9999, 100000-100001
    """
    new_buckets = []
    for bucket in buckets:
        lower, upper = bucket.split("-")
        # if lower and upper bound share same number of digits, keep as is
        if len(lower) == len(upper):
            if len(lower) % 2:
                print(f"Discarding odd bucket {bucket}")
            else:
                new_buckets.append(bucket)
                print(f"Preserving bucket {bucket}")
        else:
            temp_buckets = []
            # build the new lower limit for upper bucket, e.g. 99-1001 -> 1000-1001
            if not (len(upper) % 2):
                temp_lower = 10**(len(upper)-1)
                temp_buckets.append(format_bucket(temp_lower, upper))
            # build the new upper limit for lower bucket, e.g. 99-1001 -> 99-99
            if not (len(lower) % 2):
                temp_upper = 10**(len(lower))-1
                temp_buckets.append(format_bucket(lower, temp_upper))
            # build the intermediate ranges
            # e.g. 99-100001 -> 1000-9999
            for i in range(len(lower)+1, len(upper)):
                if i % 2:
                    continue
                temp_buckets.append(format_bucket(10**(i-1), (10**i)-1))
            print(f"Extracted buckets from range: {bucket} -> {temp_buckets}")
            new_buckets.extend(temp_buckets)
    return new_buckets

def format_bucket(i, j):
    return f"{i}-{j}"

if __name__ == "__main__":
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