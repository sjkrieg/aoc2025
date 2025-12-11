# still a greedy alg
# this time we don't remove a choice unless pressing it again would ruin our solution
# we also can be more efficient by preferring to press the buttons that flip the most bits first
# that way we avoid trying a lot of combinations

import argparse

TEST_SOLUTION = 33

def prep_input(lines: list[str]):
    machines = []
    for line in lines:
        components = line.split()
        lights = [1 if ch == "#" else 0 for ch in components[0][1:-1]]
        buttons = [[int(ch) for ch in b[1:-1].split(",")] for b in components[1:-1]]
        joltage = [int(ch) for ch in components[-1][1:-1].split(",")]
        machines.append((lights, buttons, joltage))
    return machines

def solve(machines: list[tuple[list[int], list[list[int], list[int]]]]) -> int:
    solution = 0
    for lights, buttons, joltage in machines:
        buttons = sorted(buttons, key=len, reverse=True)
        print(f"Starting {joltage} with buttons {buttons}")
        solution += greedy_solve([0] * len(lights), joltage, buttons)
    return solution

def greedy_solve(curr_state, target_state, buttons):
    if curr_state == target_state:
        return 0
    if not buttons:
        return float("inf")
    # check for invalid state
    for i, j in zip(curr_state, target_state):
        if i > j:
            return float("inf")
        
    # try to keep pushing the highest value button
    result_push_first = 1 + greedy_solve(push(curr_state[:], buttons[0]), target_state, buttons)

    if result_push_first < float("inf"):
        return result_push_first

    # pushing the first button again didn't work, backtrack and try press next button
    return greedy_solve(curr_state[:], target_state, buttons[1:])

def push(state, button):
    for i in button:
        state[i] += 1
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