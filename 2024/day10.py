# Written by Jason Phua
# on 10/12/2024
# Advent of Code 2024 - Day 10
# Solving https://adventofcode.com/2024/day/10
from typing import NamedTuple, TypeAlias


TopoMap: TypeAlias = list[list[int]]
VisitedMap: TypeAlias = list[list[bool]]


# Coordinate point on topographic map
class Point(NamedTuple):
    x: int
    y: int


# Topographic map heights
TRAIL_START = 0
TRAIL_END = 9
TRAIL_INVALID = -1


# Parse input file, returning a 2D array representing a topographic map
def parse_input(file: str) -> TopoMap:
    # Some test cases contain impassable tiles to simplify the example
    IMPASSABLE_CHAR = '.'

    def parse_char(char: str) -> int:
        return int(char) if char != IMPASSABLE_CHAR else TRAIL_INVALID

    with open(file) as file:
        return [[parse_char(char) for char in line.strip()] for line in file.readlines()]


# Return a list of coordinates of trailheads (trail starts)
def find_trailheads(topographic_map: TopoMap) -> list[Point]:
    trailheads = []

    for y, line in enumerate(topographic_map):
        for x, num in enumerate(line):
            if num == TRAIL_START:
                trailheads.append(Point(x, y))

    return trailheads


# Return whether a given position in valid within the map
def valid_pos(topographic_map: TopoMap, pos: Point) -> bool:
    map_height, map_width = len(topographic_map), len(topographic_map[0])
    return pos.y >= 0 and pos.x >= 0 and pos.y < map_height and pos.x < map_width


# Return adjacent vertices of a given position that are valid within the map
def adjacent_vertices(topographic_map: TopoMap, pos: Point) -> list[Point]:
    adjacent = [
        Point(pos.x - 1, pos.y),
        Point(pos.x + 1, pos.y),
        Point(pos.x, pos.y - 1),
        Point(pos.x, pos.y + 1)
    ]
    return [adj for adj in adjacent if valid_pos(topographic_map, adj)]


# Part 1
# Run standard depth first search recursively, with a visited array
# When a trail end (height 9) is encountered, append it to ends array
def dfs(topographic_map: TopoMap, visited: VisitedMap, pos: Point, score: list[int]) -> None:
    visited[pos.y][pos.x] = True

    if topographic_map[pos.y][pos.x] == TRAIL_END:
        score.append(1)
        return

    prev_height = topographic_map[pos.y][pos.x]
    for adj in adjacent_vertices(topographic_map, pos):
        next_height = topographic_map[adj.y][adj.x]

        if not visited[adj.y][adj.x] and next_height == prev_height + 1:
            dfs(topographic_map, visited, adj, score)


# Depth First Search driver function
# Return the number of 9 heights (end) encountered
def trail_score(topographic_map: TopoMap, trailhead: Point) -> int:
    map_height, map_width = len(topographic_map), len(topographic_map[0])
    visited = [[False] * map_width for i in range(map_height)]

    # Use a scores list instead of an integer so that it may be passed by reference
    score = []
    dfs(topographic_map, visited, trailhead, score)
    return sum(score)


# Part 2
# Modified Depth First Search
# Runs recursively but without a visited array as some distinct paths intersect
# Each time a search reaches a 9 height (end), append the trail route to the trails array
def dfs_unique_trails(topographic_map: TopoMap, pos: Point, rating: list[int]) -> None:
    prev_height = topographic_map[pos.y][pos.x]
    for adj in adjacent_vertices(topographic_map, pos):
        next_height = topographic_map[adj.y][adj.x]

        if next_height == prev_height + 1:
            if next_height == TRAIL_END:
                rating.append(1)
            dfs_unique_trails(topographic_map, adj, rating)


# Modified Depth First Search driver function
# Return the number of distinct trails that reach 9 heights (end)
def trail_rating(topographic_map: TopoMap, trailhead: Point) -> int:
    # Use a ratings list instead of an integer so that it may be passed by reference
    rating = []
    dfs_unique_trails(topographic_map, trailhead, rating)
    return sum(rating)


if __name__ == '__main__':
    topographic_map = parse_input('puzzle_input.txt')
    trailheads = find_trailheads(topographic_map)

    score_sum = sum(trail_score(topographic_map, trailhead)
                    for trailhead in trailheads)
    print(f'Part 1: {score_sum}')

    rating_sum = sum(trail_rating(topographic_map, trailhead)
                     for trailhead in trailheads)
    print(f'Part 2: {rating_sum}')
