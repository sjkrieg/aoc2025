# From part 1 we now have to filter out paths that do not travel through the required nodes
# This slightly complicates our DFS since now the count of valid paths from i -> out changes on its history
# The easiest way is to just copy a list/buffer and pop the node once we visit it
# But to be slightly more efficient (and to derust my bitwise operations) we'll use a bitvector instead
# Basically we start the DFS having visited none of the required nodes
# Whenever we visit a required node we xor it
# Then we include the bitvector as part of the key for path_counts hash table

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