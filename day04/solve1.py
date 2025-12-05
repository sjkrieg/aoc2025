# Seems like basically BFS with a sliding window?
# start at position (0, 0) then move both right one and down one in two separate function calls
# we might as well just compute the full window at each step rather than trying to slide
# since sliding would really only save a few operations at each step

# edge cases are basically just rolls of paper on the edges of the grid
# plus we have to make sure we don't visit the same cell twice

import argparse

TEST_SOLUTION = 13

def solve(grid: list[str]) -> int:
    def is_paper(i: int, j: int):
        return i >= 0 and i < len(grid) and j >= 0 and j < len(grid) and grid[i][j] == "@"

    def solve_helper(i: int, j: int) -> int:
        if i >= len(grid) or j >= len(grid[0]):
            return 0
        # check if count of adjacent paper is < 4
        # use if x!=i or y!=j to avoid counting the cell itself
        curr_result = int(
            is_paper(i, j) and
            sum([is_paper(x, y) for x in range(i-1, i+2) for y in range(j-1, j+2) if x!=i or y!=j]) < 4
        )
        # move to the right
        return curr_result + solve_helper(i+1, j)

    # run BFS from leftmost cell in each column
    return sum([solve_helper(0, j) for j in range(len(grid[0]))])

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
    
    solution = solve(lines)

    print(f"Output: {solution}")
    if args.test:
        if solution == TEST_SOLUTION:
            print("Correct!")
        else:
            print(f"Incorrect! Expected {TEST_SOLUTION}")