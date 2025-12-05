# this now smells like dynamic programming
# for a given cell i, j we can wait to compute its neighboring paper count
# until we have decided if all its neighbors have been resolved
# on second thought I don't think this would work since there are circular dependencies
# and it would be unnecessarily complicated to resolve this within a dp framework
# I think we just follow up from solve1.py with minor changes:
# 1. Instead of returning a 1 for each paper roll we move, precompute the n_adj_paper for each cell and store in new table
# 2. Use a queue to move each paper.
#    - Queue is initialized with all the rolls we move on the first pass
#    - For every neighboring paper, we add it to the queue to re-check
# There's still some repeated computation here, but it's relatively efficient
# and might even still be faster than trying to use sliding windows or somehow track other states

import argparse

TEST_SOLUTION = 43

def solve(grid: list[list[str]]) -> int:
    def is_paper(i: int, j: int):
        return grid[i][j] == "@"
    
    def get_valid_neighbor_indices(i: int, j: int) -> list[tuple[int, int]]:
        return [
            (x, y) 
            for x in range(i-1, i+2) 
            for y in range(j-1, j+2) 
            if (x!=i or y!=j) and x >= 0 and x < len(grid) and y >= 0 and y < len(grid)
        ]

    def count_adj_paper(i: int, j: int) -> int:
        """Get a count of number of adjacent paper"""
        if is_paper(i, j):
            return sum([is_paper(x, y) for x, y in get_valid_neighbor_indices(i, j)])
        else:
            return -1

    solution = 0
    # -1 is sentinel value
    paper_counts = [[count_adj_paper(i, j) for j in range(len(grid[0]))] for i in range(len(grid))]
    move_queue = [(i, j) for i, row in enumerate(paper_counts) for j, adj_count in enumerate(row) if adj_count != -1 and adj_count < 4]
    while move_queue:
        i, j = move_queue.pop()
        # if we've already moved it will no longer be paper
        if is_paper(i, j):
            # mark as moved to prevent infinite looping
            grid[i][j] = "x"
            for x, y in get_valid_neighbor_indices(i, j):
                # don't bother updating counts if x, y isn't paper too
                if is_paper(x, y):
                    paper_counts[x][y] -= 1
                    # now we can move x, y
                    if paper_counts[x][y] < 4:
                        move_queue.append((x, y))
            solution += 1
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
        lines = [list(line.strip()) for line in inf.readlines()]
    
    solution = solve(lines)

    print(f"Output: {solution}")
    if args.test:
        if solution == TEST_SOLUTION:
            print("Correct!")
        else:
            print(f"Incorrect! Expected {TEST_SOLUTION}")