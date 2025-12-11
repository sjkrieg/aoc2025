# It's easy to compute the area of the rectangle from the points, say we have
# a = (x1, y1) and b = (x2, y2)
# area(a, b) = abs(x1 - x2) * abs(y1 - y2)
# the trick is how to efficiently decide the biggest value of all pairs
# we could compare all pairs directly in O(n^2) time but can we do it more efficiently?
# is it possible that the corners MUST be the max of one of the edges?
# I don't think we can assume that, unfortunately... just going to go with the O(n^2) solution for now

import argparse

TEST_SOLUTION = 50

def prep_input(lines: list[str]) -> tuple[list[int], list[int]]:
    splits = [line.split(",") for line in lines]
    xs, ys = zip(*splits)
    return list(map(int, xs)), list(map(int, ys))

def solve(xs: list[int], ys: list[int]) -> int:
    return max([get_area(x1, y1, x2, y2) for x1, y1 in zip(xs, ys) for x2, y2 in zip(xs, ys)])

def get_area(x1: int, y1: int, x2: int, y2: int) -> int:
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