# I assume that all the rows and columns will have the same number of elements
# pretty easy to just use a stack then

import argparse

TEST_SOLUTION = 4277556

def prep_input(lines: list[str]) -> list[list[str]]:
    """Just handle the splits, we'll do int conversion and reindexing later."""
    prepped_lines = [line.strip().split() for line in lines]
    size = len(prepped_lines[0])
    for i, line in enumerate(prepped_lines):
        if len(line) != size:
            raise ValueError(f"Line {i} has unexpected length {len(line)} -- expected {size}: {line}")
    print(f"Read {len(prepped_lines)} lines with {len(prepped_lines[0])} operators/operands each")
    return prepped_lines

def solve(lines: list[list[str]]) -> int:
    results = [int(val) for val in lines[0]]
    operators = lines[-1]
    for line in lines[1:-1]:
        for i in range(len(line)):
            if operators[i] == "+":
                results[i] += int(line[i])
            elif operators[i] == "*":
                results[i] *= int(line[i])
            else:
                raise ValueError(f"Encounted unexpected operator {operators[i]}")
    return sum(results)

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