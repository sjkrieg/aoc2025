# Now instead of looking for just 2 batteries, we need 12
# Changes from part 1:
# All our assumptions still hold, we just need reformulate our solution as a nested loop that runs n=12 times

# edge cases:
# row is exactly 12 batteries
# selected batteries are the first 12 of the row
# selected batteries are last 12 of the row
# i.e. need to be very careful of off by one errors during our looping

import argparse

TEST_SOLUTION = 3121910778619

def prep_input(lines: list[str]) -> list[str]:
    return lines

def solve(lines: list[str]) -> int:
    solution = 0
    n = 12

    for bank in lines:
        # we'll use "slice" to refer to the part of the battery bank we are interested in
        slice_start = 0
        bat_buffer = []

        # need to select n batteries
        for j in range(n):
            # start looking for a battery at the beginning of the slice
            curr_bat_idx = slice_start
            # for the jth battery, we can select anywhere from previous battery + 1 to to the -(j-1)th position
            # need to watch off-by-one errors...
            # for n=12, when j=0 (first check) we want to return len(bank)-11
            # for n=12, when j=11 (last check) we want to return len(bank)
            # aka formula is len(bank)-(n-j-1)
            for i in range(curr_bat_idx+1, len(bank)-(n-j-1)):
                if bank[i] > bank[curr_bat_idx]:
                    curr_bat_idx = i
            bat_buffer.append(bank[curr_bat_idx])
            # curr_bat_idx now has the highest eligible battery, so start next search from the next position to the right
            slice_start = curr_bat_idx + 1
        
        # increment solution
        combo = int("".join(bat_buffer))
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