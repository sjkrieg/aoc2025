# Straightforward DFS problem
# We can also do some memoization though, since we would have repeated paths
# For example, in the test example "ccc" has 3 paths to out
# this means that any path leading to "ccc" can simply be multiplied by 3
# as long as there are no cycles this should be great

import argparse

TEST_SOLUTION = 2
NODES_REQUIRED_VISIT = ["fft", "dac"]
# we will use a bit vector to track visits

def prep_input(lines: list[str]) -> dict[list[str]]:
    """Convert to adjacency list."""
    splits = [line.split(":") for line in lines]
    return {sp[0]: sp[1].split() for sp in splits}


def solve(adj: dict[list[str]]) -> int:
    # track all paths from (i, required_bits) -> "out" so we don't duplicate dfs
    path_counts = {}
    
    def dfs(u: str, required_visits=int):
        key = (u, required_visits)
        if key not in path_counts:
            if "out" in adj[u]: 
                # don't count this path if there are required visits remaining
                path_counts[key] = int(not required_visits)
            else:
                if u in NODES_REQUIRED_VISIT:
                    # flip the bit of the required_visits node
                    required_visits ^= (1 << NODES_REQUIRED_VISIT.index(u))
                path_counts[key] = sum([dfs(v, required_visits) for v in adj[u]])
        return path_counts[key]
    
    return dfs("svr", (1 << len(NODES_REQUIRED_VISIT)) - 1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", action="store_true")
    args = parser.parse_args()

    if args.test:
        inf = "test2.txt"
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