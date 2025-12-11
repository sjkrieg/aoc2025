# Okay this is a pretty significant change from part 1
# Basically, now any tiles that are outside the edge of the polygon disqualify a pair of points from being selectable
# So we need a quick way to test if the rectangle touches any illegal tiles
# There are so many edge cases for potential efficient solutions...

# Let's try this: first, draw a full outline of the polygon
# Then do BFS to fill it in
# This will be tricky since there can be overlaps, etc.,
# And the full matrix is very large, so I think it will be too much to check every single cell
# Maybe we can do a smart BFS where we move orthogonal to the previous pair of lines

# after that it shouldn't be too bad to trace the border of each rectangle to verify if it's valid

import argparse
import numpy as np
from itertools import combinations
from tqdm import tqdm

TEST_SOLUTION = 24

def prep_input(lines: list[str]) -> tuple[list[int], list[int]]:
    splits = [line.split(",") for line in lines]
    xs, ys = zip(*splits)
    return list(map(int, xs)), list(map(int, ys))

def solve(xs: list[int], ys: list[int]) -> int:
    grid = make_outline(xs, ys)
    print(f"Initialized grid {grid.shape} with sum {grid.sum()}")
    print(grid)
    
    # get middle of first horizontal line - we then know either up or down is inside the polygon
    # this is not robust for edge cases but oh well
    def get_flood_seed(i):
        """Get a seed square to start flood fill from. The seed must be the following:
        - NOT part of an edge
        - adjacent to an edge
        - the cell across the edge from a seed must NOT be part of an edge
        - this helps guide our flood search
        """
        while xs[i-1] != xs[i] and abs(ys[i-1] - ys[i] < 2):
            i += 1
            if i == len(xs):
                raise ValueError("Your dumb solution got stuck")
        # these points form a horizontal line
        x1, y1 = xs[i-1], ys[i-1]
        x2, y2 = xs[i], ys[i]
        ycand = (y1+y2)//2
        xcand1, xcand2 = x1-1, x1+1
        # if either candidate is on a different border, try again
        if grid[xcand1][ycand] or grid[xcand2][ycand]:
            return get_flood_seed(i)
        else:
            # valid return
            if is_contained(xcand1, ycand):
                return (xcand1, ycand)
            elif is_contained(xcand2, ycand):
                return (xcand2, ycand)
            else:
                raise ValueError("Your algorithm didn't work bud")
    
    def is_contained(x, y):
        """Is (x, y) within a polygon (not accurate for points on a line)"""
        l = grid[:x, y].sum()
        r = grid[x+1:, y].sum()
        d = grid[x, :y].sum()
        u = grid[x, y+1:].sum()
        return l % 2 and r % 2 and d % 2 and u % 2

    bfs_queue = {get_flood_seed(0)}
    i = 0
    print(f"Starting flood fill from {bfs_queue}")
    while bfs_queue:
        x, y = bfs_queue.pop()
        i += 1
        print(f"Visiting {x}, {y} (queue size {len(bfs_queue)}, visit count {i})")
        if not grid[x][y]:
            grid[x][y] = 1
            bfs_queue.update({(x-1, y), (x+1, y), (x, y-1), (x, y+1)})
        # if grid[x][y] is 1, it's border or we've already visited
    print("Done with flood fill!")

    def is_cell_safe(i, j) -> bool:
        return grid[i][j]

    def is_border_safe(x1: int, y1: int, x2: int, y2: int) -> bool:
        # check x1 to x2 on y1/y2 axis
        for i in range(min(x1, x2), max(x1, x2)+1):
            if (not is_cell_safe(i, y1)) or (not is_cell_safe(i, y2)):
                return False
        # check y1 to y2 on x1/x2 axis
        # can skip y1 and y2 since those are corners already checked above
        for j in range(min(y1, y2)+1, max(y1, y2)):
            if (not is_cell_safe(x1, j)) or (not is_cell_safe(x2, j)):
                return False
        return True

    combos = list(combinations(list(zip(xs, ys)), r=2))
    for (x1, y1), (x2, y2) in tqdm(sorted(combos, key=lambda p: get_area(*p), reverse=True)):
        if is_border_safe(x1, y1, x2, y2):
            return get_area((x1, y1), (x2, y2))


def make_outline(xs: list[int], ys: list[int]):
    # add 1 to grid length for one-indexing
    grid = np.zeros((max(xs)+1, max(ys)+1), dtype=np.byte)
    # make edges -- also connect first to last record
    for i in range(len(xs)):
        x, y = xs[i], ys[i]
        xprev, yprev = xs[i-1], ys[i-1]

        # make edges between previous and current
        # points are on same y-axis, step along yaxis
        if x == xprev:
            # always go lower to higher
            if y < yprev:
                yprev, y = y, yprev
            for ystep in range(yprev, y+1):
                grid[x][ystep] = 1
        # points are on same x-axis, step along y-axis
        if y == yprev:
            # always go lower to higher
            if x < xprev:
                xprev, x = x, xprev
            for xstep in range(xprev, x):
                grid[xstep][y] = 1

    return grid


def get_area(x1, y1, x2, y2) -> int:
    return (abs(x1-x2) + 1) * (abs(y1-y2) + 1)

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