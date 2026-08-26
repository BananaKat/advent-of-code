# Written by Jason Phua
# on 12/12/2024
# Advent of Code 2024 - Day 12
# Solving https://adventofcode.com/2024/day/12
from typing import NamedTuple, TypeAlias
from collections import deque


GardenPlot: TypeAlias = list[list[str]]
VisitedMap: TypeAlias = list[list[bool]]


# Coordinate point on map
class Point(NamedTuple):
    x: float
    y: float


class Edge(NamedTuple):
    p1: Point
    p2: Point


# Parse input file, returning a 2D array representing a garden plot
def parse_input(file: str) -> GardenPlot:
    with open(file) as file:
        garden = [list(line.strip()) for line in file.readlines()]

    assert(len(garden) > 0)
    assert(len(garden[0]) > 0)

    return garden


# Return whether a given position in valid within the map
def valid_pos(garden: GardenPlot, pos: Point) -> bool:
    map_height, map_width = len(garden), len(garden[0])
    return pos.y >= 0 and pos.x >= 0 and pos.y < map_height and pos.x < map_width


# Return whether a given position is a valid adjacent plot in the garden:
# - Is within bounds of the map
# - Adjacent plot is the same character type as the given previous char
# - Plot is not already marked as visited
def valid_adj(garden: GardenPlot, visited: VisitedMap, prev_char: str, pos: Point) -> bool:
    if valid_pos(garden, pos):
        matching_char = garden[pos.y][pos.x] == prev_char
        marked_visited = visited[pos.y][pos.x]

        return matching_char and not marked_visited

    return False


# Return adjacent vertices of a given position that are valid within the map
def unvisited_adjacent(
    garden: GardenPlot,
    visited: VisitedMap,
    prev_char: str,
    pos: Point
) -> list[Point]:
    adjacent = [
        Point(pos.x - 1, pos.y),
        Point(pos.x + 1, pos.y),
        Point(pos.x, pos.y - 1),
        Point(pos.x, pos.y + 1)
    ]
    return [adj for adj in adjacent if valid_adj(garden, visited, prev_char, adj)]


# Part 1
# Returns the external edges surrounding a given point
# An external edge is an adjacent point that is outside the map, or is not a matching character
def find_edges(garden: GardenPlot, pos: Point, prev_char: str) -> int:
    def is_external(garden: GardenPlot, adj: Point, prev_char: str) -> bool:
        return not valid_pos(garden, adj) or garden[adj.y][adj.x] != prev_char

    adjacent = [
        Point(pos.x - 1, pos.y), Point(pos.x + 1, pos.y),
        Point(pos.x, pos.y - 1), Point(pos.x, pos.y + 1)
    ]
    return [Edge(pos, adj) for adj in adjacent if is_external(garden, adj, prev_char)]


# Part 2
# Converts each edge in an edges list into an edge that bisects it orthogonally
# Each edge given in the input is from the inner point to the outer point,
# but we want the points of the actual external edge with the points along the perimeter
def normalise_edges(edges: list[Edge]) -> list[Edge]:
    normals = []
    for edge in edges:
        midpoint = Point((edge.p1.x + edge.p2.x) / 2,
                         (edge.p1.y + edge.p2.y) / 2)
        mid_dist = 0.5
        if edge.p2.x == edge.p1.x:
            new_p1 = Point(midpoint.x - mid_dist, midpoint.y)
            new_p2 = Point(midpoint.x + mid_dist, midpoint.y)
        elif edge.p2.y == edge.p1.y:
            new_p1 = Point(midpoint.x, midpoint.y - mid_dist)
            new_p2 = Point(midpoint.x, midpoint.y + mid_dist)
        else:
            raise Exception('Given edge is neither vertical nor horizontal')
        normals.append(Edge(new_p1, new_p2))

    return normals


# Given a list of edges, for each edge, combine each edge that shares a point
# and direction into a single edge
def flatten_edges(edges: list[Edge]) -> None:
    # Returns whether two edges share a point
    def edges_connect(edge1: Edge, edge2: Edge) -> bool:
        return edge1.p2 == edge2.p1

    # Verifies that two edges share the same direction (either horizontal or vertical)
    def same_direction(edge1: Edge, edge2: Edge) -> bool:
        edge1_horizontal = edge1.p2.x == edge1.p1.x
        edge2_horizontal = edge2.p2.x == edge2.p1.x
        edge1_vertical = edge1.p2.y == edge1.p1.y
        edge2_vertical = edge2.p2.y == edge2.p1.y
        return (edge1_horizontal and edge2_horizontal) or (edge1_vertical and edge2_vertical)

    # Assume the two given edges have a shared point and find two other edges which
    # also share this point - Handle edge case from test_case_4.txt
    def is_inner_corner(edges: list[Edge], edge1: Edge, edge2: Edge) -> bool:
        shared_point = edge1.p2 if edge1.p2 == edge2.p1 else edge2.p2
        num_intersect = 0
        for edge in edges:
            if edge == edge1 or edge == edge2:
                continue
            if edge.p1 == shared_point or edge.p2 == shared_point:
                num_intersect += 1
        return num_intersect >= 2

    # Connects two edges by removing them and then appending a new edge of its endpoints
    # Returns whether an edge combination was made
    def connect_edge(edges: list[Edge]) -> bool:
        for i, edge1 in enumerate(edges):
            for j, edge2 in enumerate(edges):
                if i == j or not same_direction(edge1, edge2) or is_inner_corner(edges, edge1, edge2):
                    continue
                if edges_connect(edge1, edge2):
                    edges.pop(i)
                    edges.pop(j - (j > i))
                    edges.append(Edge(edge1.p1, edge2.p2))
                    return True
        return False

    combined = connect_edge(edges)
    while combined:
        combined = connect_edge(edges)
    return edges


# Runs the Breadth First Search implementation of flood fill and returns two cost parameters
# For Part 1, the cost parameters are: (area, perimeter)
# For Part 2, the cost parameters are: (area, number_of_edges)
def bfs_flood_fill(
    garden: GardenPlot,
    visited: VisitedMap,
    start: Point,
    part: int
) -> tuple[int, int]:
    area = 0
    prev_char = garden[start.y][start.x]
    visited[start.y][start.x] = True
    edges = find_edges(garden, start, prev_char)

    q = deque()
    q.append(start)
    while q:
        pos: Point = q.popleft()
        area += 1

        for adj in unvisited_adjacent(garden, visited, prev_char, pos):
            edges += find_edges(garden, adj, prev_char)
            visited[adj.y][adj.x] = True
            q.append(adj)

    if part == 2:
        edges = normalise_edges(edges)
        edges = flatten_edges(edges)
    return area, len(edges)


# Calculates the total cost of fencing, given which question part is being solved
# Driver function to run BFS Flood Fill for each region (represented by a char)
def total_fencing_cost(garden: GardenPlot, part: int) -> int:
    rows, cols = len(garden), len(garden[0])
    visited = [[False] * cols for i in range(rows)]

    fencing_cost = 0
    for y, line in enumerate(garden):
        for x, char in enumerate(line):
            if visited[y][x]:
                continue

            cost1, cost2 = bfs_flood_fill(garden, visited, Point(x, y), part)
            fencing_cost += cost1 * cost2

    return fencing_cost


if __name__ == '__main__':
    garden = parse_input('puzzle_input.txt')
    total_fencing_price_p1 = total_fencing_cost(garden, part=1)
    print(f'Part 1: {total_fencing_price_p1}')

    total_fencing_price_p2 = total_fencing_cost(garden, part=2)
    print(f'Part 2: {total_fencing_price_p2}')
