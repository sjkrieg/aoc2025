# base cases
# - left -> subtraction
# - right -> addition
# - handle overflow to right
# - handle overflow to left
# - handle rotations greater than 100

# edge cases
# - last combo ends in 0

# approach
# - just use mod operator in Python, works on negative numbers too
# 78 -> R100 = 178 -> 178 % 100 = 78
# 78 -> L100 = -28 -> -28 % 100 = 78

solution = 0
dial = 50

with open("input.txt", "r") as inf:
    lines = [line.strip() for line in inf.readlines()]

print(f"Read {len(lines)} lines!")
for i, rotation in enumerate(lines):
    print(f"{i}: {dial} -> {rotation} = ", end="")
    if rotation[0] == "L":
        spin = -int(rotation[1:])
    elif rotation[0] == "R":
        spin = int(rotation[1:])
    else:
        raise ValueError(f"Invalid spin {spin} -- expected first char as 'L' or 'R'")
    
    # python mod works on negative numbers too
    dial = (dial + spin) % 100
    if not dial:
        solution += 1
    print(dial)

print(f"Solution: {solution}")