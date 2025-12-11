# goal is to return the product of the size of the 3 largest circuit groups
# given n starting switches, we form a circuit by merging the two who are closest in 3d space
# continue until we have merged 1000 switches

# approach
# 1. compute distances between all pairs of switches - O(n^2), can't really avoid this
# 2. sort by smallest distance and build a graph where the 1000 smallest distances are edges
# 3. Perform BFS to merge groups
# 4. Get 3 smallest groups, multiply sizes and return result

# edge cases is dealing with self loops since those are included in the counts of the group sizes

import argparse
import math

TEST_SOLUTION = 40
N_LARGEST = 3

def prep_input(lines: list[str]) -> list[int]:
    return [list(map(int, line.split(","))) for line in lines]

def solve(coords: list[int], n_combine: int) -> int:
    solution = 0
    # distances - use dict instead of array for easier flattening
    d = {}
    # distance is symmetric so only populate d where i < j
    for j in range(1, len(coords)):
        for i in range(j):
            d[(i, j)] = get_dist(coords[i], coords[j])
    
    # find the N_COMBINE smallest pairs
    closest_pairs = sorted(d.items(), key=lambda x: x[1])[:n_combine]
    
    # build bi-directional adjacency list with set to prevent duplicates
    adj: dict[int, set[int]] = {i: {i} for i in range(len(coords))}
    for (i, j), _ in closest_pairs:
        adj[i].add(j)
        adj[j].add(i)

    # bfs to build groups
    groups: dict[int, set[int]] = {}
    for i in list(adj.keys()):
        print(f"Starting BFS for group {i}: {adj[i]}")
        # create a new group and perform BFS
        gid = len(groups)
        groups[gid] = adj[i]
        # don't run bfs on self
        bfs_queue = [u for u in adj[i] if i != u]
        adj[i] = {i}
        while bfs_queue:
            u = bfs_queue.pop()
            for v in list(adj[u]):
                # skip self loops
                if u == v:
                    continue
                # for each bfs neighbor at current stage,
                bfs_queue.append(v)
                groups[gid].add(v)
                adj[u].remove(v)

    largest_groups = sorted(map(len, groups.values()), reverse=True)[:N_LARGEST]
    # need to quickly look up what group a coordinate has been assigned to
    return math.prod(largest_groups)


# this would of course be faster with numpy but more fun to only use standard libraries
def get_dist(p: list[int], q: list[int]) -> int:
    return sum([(pi-qi)**2 for pi, qi in zip(p, q)])

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
    

    if args.test:
        solution = solve(prep_input(lines), 10)
        if solution == TEST_SOLUTION:
            print("Correct!")
        else:
            print(f"Incorrect! Expected {TEST_SOLUTION}")
    else:
        solution = solve(prep_input(lines), 1000)
    print(f"Output: {solution}")