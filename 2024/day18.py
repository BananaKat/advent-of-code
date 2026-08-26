# Written by Jason Phua
# on 24/12/2024
# Advent of Code 2024 - Day 18
# Solving https://adventofcode.com/2024/day/18
from typing import TypeAlias, NamedTuple
from collections import defaultdict
import heapq
import math


# Define co-ordinates of a point on a grid
class Vertex(NamedTuple):
    x: int
    y: int


Grid: TypeAlias = list[list[str]]
EMPTY, CORRUPTED = '.', '#'

Pred: TypeAlias = dict[Vertex, Vertex]


# Parse input file, returning a list of byte fall positions
def parse_input(file: str) -> list[Vertex]:
    def to_vertex(byte: str) -> Vertex:
        return Vertex(*map(int, byte.strip().split(',')))

    with open(file) as file:
        return list(map(to_vertex, file.read().strip().split('\n')))


# Modifies the grid in place
def place_bytes(_bytes: list[Vertex]) -> None:
    for byte in _bytes:
        grid[byte.y][byte.x] = CORRUPTED


# Find the shortest path solution to the given 2D grid maze
# Return both the solution's shortest distance and path taken
def solve_maze(grid: Grid) -> tuple[int, Pred]:
    start = Vertex(x=0, y=0)
    end = Vertex(x=COLS, y=ROWS)

    # Return whether a given position is valid within map indexes
    def valid_pos(grid: Grid, pos: Vertex) -> bool:
        in_bounds = 0 <= pos.y < ROWS + 1 and 0 <= pos.x < COLS + 1
        return in_bounds and grid[pos.y][pos.x] != CORRUPTED

    # Return adjacent vertices of a given position that are valid within the map
    # and are not a corrupted byte cell
    def get_adjacent(grid: Grid, pos: Vertex) -> list[Vertex]:
        adjacent = [Vertex(pos.x - 1, pos.y), Vertex(pos.x + 1, pos.y),
                    Vertex(pos.x, pos.y - 1), Vertex(pos.x, pos.y + 1)]
        return [adj for adj in adjacent if valid_pos(grid, adj)]

    # Dijkstra Single Source Shortest Path algorithm
    def dijkstra_sssp(grid: Grid, start: Vertex, end: Vertex) -> tuple[int, Pred]:
        dist, pred = defaultdict(lambda: math.inf), {}
        dist[start] = 0

        # Priority Queue: (dist, vertex)
        pqueue = [(0, start)]
        while pqueue:
            _, v = heapq.heappop(pqueue)

            for w in get_adjacent(grid, v):
                weight = 1
                if dist[v] + weight < dist[w]:
                    dist[w] = dist[v] + weight
                    pred[w] = v
                    heapq.heappush(pqueue, (dist[w], w))

        return dist[end], pred

    return dijkstra_sssp(grid, start, end)


# Find the first byte corruption that prevents the grid exit from being
# reachable from the start
def find_blocking_corruption(grid: Grid, pred: Pred, _bytes: list[Vertex]) -> Vertex:
    for byte in _bytes[KILOBYTE:]:
        grid[byte.y][byte.x] = CORRUPTED

        # Only resolve the grid if the byte corruption disturbs the best path
        if byte not in pred:
            continue

        # Attempt to resolve the maze
        min_steps, pred = solve_maze(grid)
        if min_steps == math.inf:
            return byte


if __name__ == '__main__':
    _bytes = parse_input('puzzle_input.txt')

    # Initialise the grid
    ROWS, COLS = 70, 70
    grid = [[EMPTY] * (COLS + 1) for _ in range(ROWS + 1)]

    # In Part 1, only the first kilobyte is simulated
    KILOBYTE = 1024
    place_bytes(_bytes[:KILOBYTE])
    min_steps, pred = solve_maze(grid)
    print(f'Part 1: {min_steps}')

    # Part 2: runs in ~23s
    cut_off_byte = find_blocking_corruption(grid, pred, _bytes)
    print(f'Part 2: {cut_off_byte.x},{cut_off_byte.y}')
