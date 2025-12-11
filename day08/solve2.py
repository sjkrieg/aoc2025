# basically now instead of using BFS to merge up to a point,
# we need to repeatedly merge until there are no clusters left

import argparse
import math

TEST_SOLUTION = 25272

def prep_input(lines: list[str]) -> list[int]:
    return [list(map(int, line.split(","))) for line in lines]

def solve(coords: list[int]) -> int:
    solution = 0
    # distances - use dict instead of array for easier flattening
    d = {}
    # distance is symmetric so only populate d where i < j
    for j in range(1, len(coords)):
        for i in range(j):
            d[(i, j)] = get_dist(coords[i], coords[j])
    
    # sort by distance
    sorted_pairs = sorted(d.items(), key=lambda x: x[1])
    
    # instead of adjacency list, we want to keep a reachability list
    reachable: dict[int, set[int]] = {i: {i} for i in range(len(coords))}
    for (i, j), _ in sorted_pairs:
        reachable[i].update(reachable[j])
        if len(reachable[i]) == len(coords):
            return coords[i][0] * coords[j][0]
        # we can even use the same object since they have the same neighborhoods
        for v in reachable[i]:
            reachable[v] = reachable[i]

def get_dist(p: list[int], q: list[int]) -> int:
    return sum([(pi-qi)**2 for pi, qi in zip(p, q)])

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
            