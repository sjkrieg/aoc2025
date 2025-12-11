# wording of the question is a little weird, maybe will be more relevant for part 2
# however, for part 1, we only care about the number of splits
# this means we don't care at all about the directions of splits or merging/etc.
# we basically just count 1 for every carat ^ that has a beam go into it

# this is an easy DFS problem, we just have to decide if we want to go top down or bottom up
# for top down:
# - start at top
# - traverse down until we get a carat
# - increment total number of splits, then fork
# - repeat until done

# for bottom up:
# - start from each carat on the bottom
# - traverse straight up until a carat is on either side
# - increment and switch lanes

# I think top down will be better since we can traverse straight down

import argparse

TEST_SOLUTION = 21
START = "S"
PASS_THROUGH = "."
SPLITTER = "^"
CHECKED = "*"

def prep_input(lines: list[str]) -> list[list[str]]:
    # convert list of str into list of list of chars so we can modify inplace
    return [list(line) for line in lines]

def solve(manifold: list[list[str]]) -> int:
    solution = 0

    def dfs(i: int, j: int) -> None:
        # i rows, j cols
        # continue straight down jth column until i == len(rows)
        # if encounter carat, fork with j-1 and j+1
        # also modify carat inplace to avoid double counts
        if i < len(manifold):
            if manifold[i][j] == SPLITTER:
                nonlocal solution
                solution += 1
                manifold[i][j] = CHECKED
                # move left/down and right/down
                if j > 0:
                    dfs(i+1, j-1)
                if j < len(manifold[0]) - 1:
                    dfs(i+1, j+1)
            elif manifold[i][j] == PASS_THROUGH:
                # move straight down
                dfs(i+1, j)
            # otherwise is probably already checked, do nothing

    dfs(1, manifold[0].index(START))
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