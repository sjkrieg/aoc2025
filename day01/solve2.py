# part 2 mods:
# for positive case, increment by quotient
# for negative case, increment by quotient +1

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
    
    # part 2 mod: use quotient to increment solution
    # also add absolute value to solution
    dial_overflow = dial + spin
    if dial_overflow > 0:
        n_passed_go = dial_overflow // 100
    else:
        n_passed_go = (-dial_overflow // 100)
        # add 1 for negative case, e.g. 1 -> R2 -> -1
        # but ONLY do this if we start from 0, e.g. 0 -> L1 -> 99 should NOT count
        if dial:
            n_passed_go += 1
    solution += n_passed_go
    dial = dial_overflow % 100
    print(f"{dial} (passed go {n_passed_go} times)")

print(f"Solution: {solution}")