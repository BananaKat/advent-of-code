# Written by Jason Phua
# on 24/12/2024
# Advent of Code 2024 - Day 20
# Solving https://adventofcode.com/2024/day/20
from typing import TypeAlias, NamedTuple
from collections import deque


# Define co-ordinates of a point on a grid
class Vertex(NamedTuple):
    x: int
    y: int


# Define data structures used for graph traversal
RaceTrack: TypeAlias = list[str]
Pred: TypeAlias = dict[Vertex, Vertex]
Dist: TypeAlias = dict[Vertex, int]
Path: TypeAlias = list[Vertex]

# Racetrack character components
EMPTY, WALL = '.', '#'
START, END = 'S', 'E'

# Minimum and maximum cheat durations
MIN_CHEAT = 2
MAX_CHEAT = 20

# Minimum time save for a cheat to be considered a 'best cheat'
BEST_CHEAT_COND = 100


# Parse input file, returning a 2D array of the race track
def parse_input(file: str) -> RaceTrack:
    with open(file) as file:
        return [line.strip() for line in file]


# Solve the 'Race Condition Festival' challenge by finding the list of cheats
# that save at least 100 picoseconds
def solve_race(racetrack: RaceTrack, part: int) -> int:
    # Find start and end points of the racetrack using generator expressions
    def get_endpoints() -> tuple[Vertex, Vertex]:
        start = next(Vertex(x, y) for y, line in enumerate(racetrack)
                     for x, char in enumerate(line) if char == START)
        end = next(Vertex(x, y) for y, line in enumerate(racetrack)
                   for x, char in enumerate(line) if char == END)
        return start, end

    # Return whether a given position is valid within map indexes and is empty (not a wall)
    def valid_pos(pos: Vertex) -> bool:
        map_height, map_width = len(racetrack), len(racetrack[0])
        in_bounds = 0 <= pos.y < map_height and 0 <= pos.x < map_width
        return in_bounds and racetrack[pos.y][pos.x] != WALL

    # Return adjacent vertices of a given position that are valid within the map
    def get_adjacent(pos: Vertex) -> list[Vertex]:
        adjacent = [Vertex(pos.x - 1, pos.y), Vertex(pos.x + 1, pos.y),
                    Vertex(pos.x, pos.y - 1), Vertex(pos.x, pos.y + 1)]
        return [adj for adj in adjacent if valid_pos(adj)]

    # Use the predecessor dictionary to reconstruct a list of vertices representing
    # the racetrack path in order from start to end
    def reconstruct_path(pred: Pred, pos: Vertex) -> Path:
        path = []
        while pos:
            path.append(pos)
            pos = pred[pos]
        return path

    # Use the Breadth First Search Flood Fill algorithm implementation to create a
    # dictionary of points on the track and their distance away from the end point,
    # and a list of vertices representing the track path
    def bfs_dist_flood_fill(start: Vertex, end: Vertex) -> tuple[Dist, Path]:
        end_dist = {end: 0}
        pred = {end: None}
        path = []

        queue = deque([end])
        while queue:
            v = queue.popleft()

            if v == start:
                path = reconstruct_path(pred, start)
                return end_dist, path

            for w in get_adjacent(v):
                if w not in end_dist:
                    end_dist[w] = end_dist[v] + 1
                    pred[w] = v
                    queue.append(w)

        return end_dist, path

    # Return a list of points that are a given Manhattan distance away from a point
    def manhattan_dist_points(pos: Vertex, distance: int) -> list[Vertex]:
        points = []

        for dx in range(-distance, distance + 1):
            dy = distance - abs(dx)
            points.append(Vertex(pos.x + dx, pos.y + dy))
            if dy != 0:
                points.append(Vertex(pos.x + dx, pos.y - dy))

        return [pos for pos in points if valid_pos(pos)]

    # Traverse the best path, for each point, find all cells that are a certain
    # Manhattan distance away and calculate the time saved by moving to that point;
    # Return the number of 'best cheats' (moves with at least a time save of 100)
    def count_best_cheats(end_dist: Dist, path: Path) -> int:
        max_cheat = MIN_CHEAT if part == 1 else MAX_CHEAT
        return len([
            v for v in path
            for cheat_dist in range(MIN_CHEAT, max_cheat + 1)
            for w in manhattan_dist_points(v, cheat_dist)
            if end_dist[v] - end_dist[w] - cheat_dist >= BEST_CHEAT_COND
        ])

    end_dist, path = bfs_dist_flood_fill(*get_endpoints())
    return count_best_cheats(end_dist, path)


if __name__ == '__main__':
    racetrack = parse_input('puzzle_input.txt')
    print(f'Part 1: {solve_race(racetrack, part=1)}')
    print(f'Part 2: {solve_race(racetrack, part=2)}')
