# part 2 is pretty different from part 1
# most of our solution does not apply, but we still want to take a sorting approach
# if ranges were not overlapping we could simply take the differences, but we have to handle that
# sorting helps us do that

# case 1: distinct ranges, e.g. 1-3, 4-6, sorting and computing difference sum will work
# case 2: partial overlap, e.g. 1-3, 2-4, need to find a way to compare overlap
# case 3: enclosure, e.g. 1-5, 2-4, need to ignore 2-4
# case 4: chained overlap, e.g. 1-3, 2-4, 3-5
# edge case: edge overlap, e.g. 1-3, 3-5

# approach: we can handle overlaps by tracking the max of the sorted buckets
# take chained overlap example:
# 1-3 -> solution = (3-1)+1 = 3, current max=3
# 2-4 -> solution = solution + (new_highest - max(current_max, 2)) -> 4, current max=4
# to handle the ignored bucket case, we can simply ignore any buckets whose highest is not above the max

import argparse

TEST_SOLUTION = 14

def prep_input(lines: list[str]) -> list[tuple[int, int]]:
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
    print(f"Ignored {len(fresh_ids)} fresh IDs")

    return sorted(fresh_ranges)


def solve(fresh_ranges: list[tuple[int, int]]) -> int:
    """Fresh_ranges must be sorted."""
    solution = 0
    curr_max = 0
    for lower, upper in fresh_ranges:
        # handle enclosure case by skipping this bucket
        if upper <= curr_max:
            continue
        # this max() ensures we don't double count overlapping ranges
        # use curr_max+1 to avoid double counting the previous upper bound
        lower_to_add = max(curr_max+1, lower)
        # add 1 here since ranges are inclusive, e.g. range 1-3 counts as 3 IDs
        solution += (upper - lower_to_add + 1)
        curr_max = upper
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
    
    solution = solve(prep_input(lines))

    print(f"Output: {solution}")
    if args.test:
        if solution == TEST_SOLUTION:
            print("Correct!")
        else:
            print(f"Incorrect! Expected {TEST_SOLUTION}")