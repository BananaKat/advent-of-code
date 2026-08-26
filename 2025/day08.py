# Written by Jason Phua
# on 31/01/2026
# Advent of Code 2025 - Day 8
# Solving https://adventofcode.com/2025/day/8
from collections import defaultdict, Counter
from dataclasses import dataclass
from warnings import deprecated
import itertools
import heapq
import math


@dataclass(frozen=True)
class JunctionBox:
    x: int
    y: int
    z: int

    # Return the straight line distance squared
    def sq_dist(self, other: JunctionBox) -> float:
        return ((self.x - other.x) ** 2 +
                (self.y - other.y) ** 2 +
                (self.z - other.z) ** 2)


# Parse input file and return a list of JunctionBox coordinates
def parse_input(filename: str) -> list[JunctionBox]:
    with open(filename) as file:
        return [JunctionBox(*map(int, line.strip().split(','))) for line in file]


# Disjoint-set/union-find data structure with Union by Rank and Path Compression
class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [1] * n

    # Find the representative/root node
    def find(self, i: int) -> int:
        # Path compression
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    # Combine two sets by combining the trees
    def union(self, x: int, y: int) -> None:
        s1 = self.find(x)
        s2 = self.find(y)
        if s1 == s2:
            return

        # Union by rank
        if self.rank[s1] < self.rank[s2]:
            self.parent[s1] = s2
        elif self.rank[s1] > self.rank[s2]:
            self.parent[s2] = s1
        else:
            self.parent[s2] = s1
            self.rank[s1] += 1

    # Convert tree structure to a nested list where each sublist is a disjoint set
    def to_list(self) -> list[list[int]]:
        sets_map = defaultdict(list)
        for i in self.parent:
            root = self.find(i)
            sets_map[root].append(i)
        return list(sets_map.values())


class Circuits:
    Pair = tuple[JunctionBox, JunctionBox]
    Edge = tuple[int, Pair]
    Connections = list[list[JunctionBox]]

    def __init__(self, junction_boxes: list[JunctionBox]):
        self.vertices = junction_boxes
        self.connections = list()
        self.last_connection = None

    # Produce a complete weighted undirected graph represented as an edge list
    # An edge is (weight, pair), where weight = distance, pair = (nodeA, nodeB)
    # Since the graph is dense, creating and sorting this edge list runs in O(V^2 log V^2)
    @staticmethod
    def _generate_complete_graph(junction_boxes: list[JunctionBox]) -> list[Edge]:
        pairs = itertools.combinations(junction_boxes, 2)
        return [(a.sq_dist(b), (a, b)) for a, b in pairs]

    @staticmethod
    @deprecated("Unused lazy generation")
    def _generate_complete_graph_DEP(junction_boxes: list[JunctionBox]) -> Edge:
        for a, b in itertools.combinations(junction_boxes, 2):
            yield a.sq_dist(b), (a, b)

    # Checks if the connections form a complete graph
    @staticmethod
    @deprecated("Helper for deprecated function")
    def _is_complete_DEP(conns: Connections, vertices: int) -> bool:
        if not conns:
            return False
        return len(conns[0]) == vertices

    # Add a junction box pair to the connections list
    @staticmethod
    @deprecated("Helper for deprecated function")
    def _connect_pair_DEP(conns: Connections, pair: Pair) -> Connections:
        NOT_FOUND = -1

        a, b = pair
        a_idx = next((i for i, c in enumerate(conns) if a in c), NOT_FOUND)
        b_idx = next((i for i, c in enumerate(conns) if b in c), NOT_FOUND)

        if a_idx == NOT_FOUND and b_idx == NOT_FOUND:
            conns.append([a, b])
        elif a_idx != NOT_FOUND and b_idx == NOT_FOUND:
            conns[a_idx].append(b)
        elif a_idx == NOT_FOUND and b_idx != NOT_FOUND:
            conns[b_idx].append(a)
        elif a_idx != b_idx:
            conns[a_idx].extend(conns[b_idx])
            del conns[b_idx]

        return conns

    # Connect n pairs of junction boxes in order of shortest distance
    # Sorting bounds this solution to O(V^2 log V^2)
    @deprecated("Replaced by faster solution")
    def connect_DEP(self, n: int = math.inf) -> None:
        edges = sorted(self._generate_complete_graph(junction_boxes))
        conns = list()
        count = 0

        for _, pair in edges:
            conns = Circuits._connect_pair(conns, pair)
            count += 1
            if count >= n or self._is_complete_DEP(conns, self.V):
                self.last_connection = pair
                break

        self.connections = conns

    # Kruskal's Algorithm modified for early termination
    # Let i be the number of edges traversed
    # Let count be the number of edges included in MST
    # We hold: i < N, count < V - 1
    '''
    Sorting bounds this solution to O(V^2 log V^2)
    Prim's algorithm may be faster as it runs in O((E + V) log V), and also
    does not require a sorted list of edges. However, it is not a valid solution as:
    - Part 1 requires selecting the N globally shortest edges to form incomplete MSTs
    - Part 2 requires selecting the K-th smallest edge on step K in strictly increasing order
    But Prim's algorithm does not maintain global edge order.
    '''
    def connect(self, n: int = None) -> None:
        # Only sort min(N, E) edges as i < N and on a complete MST, E = V(V - 1)/2
        V = len(self.vertices)
        edges = heapq.nsmallest(
            (n if n is not None else V * (V - 1) // 2),
            self._generate_complete_graph(self.vertices)
        )
        # Pre-map JunctionBox objects to integers to avoid hashing objects
        index = {v: i for i, v in enumerate(self.vertices)}
        dsu = DSU(V)
        count = 0

        for i, (dist, (a, b)) in enumerate(edges):
            if dsu.find(index[a]) != dsu.find(index[b]):
                dsu.union(index[a], index[b])
                count += 1
            if count == V - 1 or i == n:
                self.last_connection = (a, b)
                break

        self.connections = dsu.to_list()


    # Part 1
    @property
    def prod_len_largest_three(self) -> int:
        sorted_conn_lens = sorted(map(len, self.connections), reverse=True)
        return math.prod(sorted_conn_lens[:3])

    # Part 2
    @property
    def prod_last_connection_x(self) -> int:
        if self.last_connection is None:
            return None
        a, b = self.last_connection
        return a.x * b.x


if __name__ == '__main__':
    junction_boxes = parse_input('puzzle_input.txt')
    circuits = Circuits(junction_boxes)

    circuits.connect(1000)
    print(f'Part 1: {circuits.prod_len_largest_three}')
    circuits.connect()
    print(f'Part 2: {circuits.prod_last_connection_x}')
