# ASSUMPTIONS:
# - Each bank will always have at least two batteries (implied)
# - No batteries are 0 (stated in instructions)

# This seems pretty simple, I think we can be greedy and do a 2-pass max check
# The first pass we simply look for the highest integer EXCEPT the last position
# - This always works because even the smallest two digit number (10) is larger than the smallest one digit number (9)
# - We can always choose the first (leftmost) occurrence of the highest integer since they don't have to be adjacent
# On second pass we we look for the highest integer to the right of the result of first pass

# edge cases
# - bank has 2 or fewer batteries (doesn't seem to be an issue here)
# - there is a 9 in the last position (e.g second row on example input 81119) -> max is 89

import argparse

TEST_SOLUTION = 357

def prep_input(lines: list[str]) -> list[str]:
    return lines

def solve(lines: list[str]) -> int:
    solution = 0
    for bank in lines:
        bat1_idx = 0
        # check for highest battery excluding last position
        # bat1 is initialized to position 0 so we can start from 1
        for i in range(1, len(bank)-1):
            if bank[i] > bank[bat1_idx]:
                bat1_idx = i
        bat2_idx = bat1_idx + 1
        # check for highest battery to the right of bat1
        for j in range(bat2_idx+1, len(bank)):
            if bank[j] > bank[bat2_idx]:
                bat2_idx = j
        
        # increment solution
        combo = int(bank[bat1_idx] + bank[bat2_idx])
        solution += combo
        print(f"{bank} -> {combo}")

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
            print("Test is correct!")
        else:
            print(f"Test is incorrect! Expected {TEST_SOLUTION}")