# Changes from part 1: Now we have to transpose the numbers within the columns
# Our solution should still work exactly the same after doing that during preprocessing

import argparse
from math import prod

TEST_SOLUTION = 3263827

def prep_input(lines: list[str]) -> list[str]:
    """Just handle the splits, we'll do int conversion and reindexing later."""
    return lines

def solve(lines: list[str]) -> int:
    solution = 0
    operators = []
    col_widths = []
    for char in lines[-1]:
        # create a new column / operator
        # use 0 instead of 1 to handle whitespace between columns
        if char == "+":
            operators.append("+")
            col_widths.append(0)
        # create a new column / operator
        # use 0 instead of 1 to handle whitespace between columns
        elif char == "*":
            operators.append("*")
            col_widths.append(0)
        # increment current operator
        # this assumes equal whitespace across operators
        elif char == " ":
            col_widths[-1] += 1
        else:
            raise ValueError(f"Received unexpected char in operator row {char}")
    # last operator has one fewer space than others
    col_widths[-1] += 1
    print(f"Found {len(operators)} columns with widths {col_widths}")
    raw_operands = lines[:-1]
    n_rows = len(lines) - 1
    col_offset = 0
    for op, size in zip(operators, col_widths):
        operand_buffer = []
        for j in range(col_offset, col_offset + size):
            tcol_buffer = []
            for i in range(n_rows):
                tcol_buffer.append(raw_operands[i][j])
            operand_buffer.append(int("".join(tcol_buffer)))
        print(f"Applying op {op} to transposed col {operand_buffer}")
        # finish processing column and move offset forward
        if op == "+":
            solution += sum(operand_buffer)
        elif op == "*":
            solution += prod(operand_buffer)
        col_offset += size + 1
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
        lines = [line for line in inf.readlines()]
    
    solution = solve(prep_input(lines))

    print(f"Output: {solution}")
    if args.test:
        if solution == TEST_SOLUTION:
            print("Correct!")
        else:
            print(f"Incorrect! Expected {TEST_SOLUTION}")