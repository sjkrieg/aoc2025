# this seems like a classic greedy choice algorithm
# each step we can choose to press or not press each of the combos
# we also know that each button would only be pressed once

import argparse

TEST_SOLUTION = 7

def prep_input(lines: list[str]):
    machines = []
    for line in lines:
        components = line.split()
        lights = [1 if ch == "#" else 0 for ch in components[0][1:-1]]
        buttons = [[int(ch) for ch in b[1:-1].split(",")] for b in components[1:-1]]
        joltage = []
        machines.append((lights, buttons, joltage))
    return machines

def solve(machines: list[tuple[list[int], list[list[int], list[int]]]]) -> int:
    solution = 0
    for lights, buttons, joltage in machines:
        print(f"Starting {lights}")
        solution += greedy_solve([0] * len(lights), lights, buttons)
    return solution

def greedy_solve(curr_state, target_state, buttons):
    if curr_state == target_state:
        return 0
    elif not buttons:
        # no choices left and we didn't get a match
        return float("inf")
    # either press the first button or don't
    return min(
        1 + greedy_solve(push(curr_state[:], buttons[0]), target_state, buttons[1:]),
        greedy_solve(curr_state, target_state, buttons[1:])
    )

def push(state, button):
    for i in button:
        state[i] ^= 1
    return state


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