# Straightforward DFS problem
# We can also do some memoization though, since we would have repeated paths
# For example, in the test example "ccc" has 3 paths to out
# this means that any path leading to "ccc" can simply be multiplied by 3
# as long as there are no cycles this should be great

import argparse

TEST_SOLUTION = 5

def prep_input(lines: list[str]) -> dict[list[str]]:
    """Convert to adjacency list."""
    splits = [line.split(":") for line in lines]
    return {sp[0]: sp[1].split() for sp in splits}


def solve(adj: dict[list[str]]) -> int:
    # track all paths from i -> "out" so we don't duplicate dfs
    path_counts = {}
    
    def dfs(u):
        if u not in path_counts:
            # if there is an edge to out, 
            if "out" in adj[u]:
                path_counts[u] = 1
            else:
                # get sum of all paths going forward
                path_counts[u] = sum([dfs(v) for v in adj[u]])
        return path_counts[u]
    
    return dfs("you")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", action="store_true")
    args = parser.parse_args()

    if args.test:
        inf = "test1.txt"
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