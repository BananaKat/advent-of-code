# Written by Jason Phua
# on 05/02/2026
# Advent of Code 2025 - Day 11
# Solving https://adventofcode.com/2025/day/11
from collections import deque, defaultdict
from dataclasses import dataclass


Node = str
AdjList = dict[Node, list[Node]]
PathMap = dict[Node, int]


# Parse input file and return an adjacency list for a directed acyclic graph
def parse_input(filename: str) -> AdjList:
    adj_list = defaultdict(list)
    with open(filename) as file:
        for line in file:
            u, v_list = line.split(':')
            adj_list[u] = v_list.split()
        return adj_list


# Part 1
# Given an adjacency list, find the number of paths from 'you' to 'out'
# We can reuse the logic from AoC 2025 Day 7 Part 2, which uses DP over
# a topologically sorted list of vertices
def dag_num_paths(adj_list: AdjList, source: Node, sink: Node) -> int:
    # Topological sort with Kahn's Algorithm
    def topological_sort(adj_list: AdjList) -> list[Node]:
        # Calculate indegree for each node
        indegree = defaultdict(int)
        for u in adj_list:
            for v in adj_list[u]:
                indegree[v] += 1

        # Enqueue nodes of indegree 0
        queue = deque(u for u in adj_list if indegree[u] == 0)

        # Apply BFS, dequeue and decrement adjacent indegrees
        res = []
        while queue:
            top = queue.popleft()
            res.append(top)
            for next_node in adj_list[top]:
                indegree[next_node] -= 1
                if indegree[next_node] == 0:
                    queue.append(next_node)

        return res

    def generate_paths(adj_list: AdjList) -> PathMap:
        dp = defaultdict(int)
        for v in adj_list[source]:
            dp[v] += 1

        topo = topological_sort(adj_list)
        for u in topo:
            for v in adj_list[u]:
                dp[v] += dp[u]

        return dp

    paths = generate_paths(adj_list)
    return paths[sink]


# Part 2
# Given an adjacency list, find the number of paths from 'svr' to 'out', which
# also pass both the 'dac' and 'fft' nodes
# In a DAG, every path has a unique topological order, so required
# intermediate nodes will appear in a fixed sequence.
def dag_num_problematic_paths(adj_list: AdjList) -> int:
    svr_to_dac = dag_num_paths(adj_list, 'svr', 'dac')
    dac_to_fft = dag_num_paths(adj_list, 'dac', 'fft')
    fft_to_out = dag_num_paths(adj_list, 'fft', 'out')

    svr_to_fft = dag_num_paths(adj_list, 'svr', 'fft')
    fft_to_dac = dag_num_paths(adj_list, 'fft', 'dac')
    dac_to_out = dag_num_paths(adj_list, 'dac', 'out')

    return (
        svr_to_dac * dac_to_fft * fft_to_out +
        svr_to_fft * fft_to_dac * dac_to_out
    )


if __name__ == '__main__':
    adj_list = parse_input('puzzle_input.txt')

    print(f'Part 1: {dag_num_paths(adj_list, 'you', 'out')}')
    print(f'Part 2: {dag_num_problematic_paths(adj_list)}')
