# This is a classic range matching problem
# Brute force definitely is super inefficient
# If we know ranges are small we could build a set of all fresh IDs
# But if ranges are even somewhat large this could be really inefficient too
# The ranges are overlapping so an easy search that just finds the closest range might fail
# e.g. if we have ranges 14-16 and 13-20, ID 17 might first find range 14-16 and fail
# we COULD address this by looking for all ranges based on a sorted smaller but then that sort of defeats the purpose of sorting
# but when we are looking at multiple IDs, we could sort them too and search in order
# in other words, we sort both IDs and buckets and iterate over the buckets, looking for matches

# putting this all together, let's compare complexity of sorting vs non-sorting method
# let n = number of fresh ids, let m = number of id ranges
# for unsorted method we would have O(n*m) time
# for sorting we would have O(nlogn) + O(mlogm) for sorting, then O(m+n) for search
# from a time standpoint sorting is always more efficient

# so we will proceed as follows with:
# sort fresh ids, sort fresh ranges by opening
# use two pointers, one for each list

import argparse

TEST_SOLUTION = 3

def prep_input(lines: list[str]) -> tuple[list[tuple[int, int]], list[int]]:
    """Convert input to a list of (lower, upper) range tuples, and list of ingredient IDs."""
    fresh_ranges = []
    for i in range(len(lines)):
        if not lines[i]:
            break
        lower, upper = lines[i].split("-")
        fresh_ranges.append((int(lower), int(upper)))
    print(f"Loaded {len(fresh_ranges)} fresh ID ranges")

    fresh_ids = []
    for i in range(i+1, len(lines)):
        fresh_ids.append(int(lines[i]))
    print(f"Loaded {len(fresh_ids)} fresh IDs")

    return (sorted(fresh_ranges), sorted(fresh_ids))


def solve(fresh_ranges: list[tuple[int, int]], fresh_ids: list[int]) -> int:
    """Both fresh_ranges and fresh_ids must be sorted."""
    solution = 0
    i, j = 0, 0
    while i < len(fresh_ranges) and j < len(fresh_ids):
        # if current id is too low, it won't be in any range, so skip to next ID
        if fresh_ids[j] < fresh_ranges[i][0]:
            j += 1
        # if current id is too high, this bucket won't capture any more IDs, so move to next bucket
        elif fresh_ids[j] > fresh_ranges[i][1]:
            i += 1
        # current ID is a match for this bucket, increment solution and move to next ID
        else:
            solution += 1
            j += 1

    return solution

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", action="store_true")
    args = parser.parse_args()

    if args.test:
        inf = "test.txt"
    else:
        inf = "input.txt"

    with open(inf, "r") as inf:
        lines = [line.strip() for line in inf.readlines()]
    
    solution = solve(*prep_input(lines))

    print(f"Output: {solution}")
    if args.test:
        if solution == TEST_SOLUTION:
            print("Correct!")
        else:
            print(f"Incorrect! Expected {TEST_SOLUTION}")