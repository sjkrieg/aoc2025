# changes from part 1
# instead of number of times the beam splits, we just need to count number of unique DFS paths
# this changes our solution as follows:
# - no longer modify manifold in place
# - now counts 2 "timeslines" for each split
# - simple to change our DFS to return a recursive sum

# key is to memoize results with lru_cache
# otherwise we will do lots of repeat computation across paths

import argparse
from functools import lru_cache

TEST_SOLUTION = 40
START = "S"
SPLITTER = "^"

def prep_input(lines: list[str]) -> list[str]:
    # convert list of str into list of list of chars so we can modify inplace
    return lines

def solve(manifold: list[list[str]]) -> int:
    solution = 0

    @lru_cache
    def dfs(i: int, j: int) -> int:
        # get sum of left and right subtrees
        print(i, j)
        if i >= len(manifold):
            # this timeline has ended, return 1 to add to the count
            return 1
        else:
            future_splits = 0
            if manifold[i][j] == SPLITTER:
                # move left/down if possible
                if j > 0:
                    future_splits += dfs(i+1, j-1)
                # move right/down if possible
                if j < len(manifold[0]) - 1:
                    future_splits += dfs(i+1, j+1)
            else:
                # move straight down
                future_splits += dfs(i+1, j)
            return future_splits

    return dfs(1, manifold[0].index(START))

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