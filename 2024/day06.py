# Written by Jason Phua
# on 07/12/2024
# Advent of Code 2024 - Day 6
# Solving https://adventofcode.com/2024/day/6
from enum import Enum
from time import perf_counter


# Available guard directions
class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


CARDINALITY = len(Direction)

# Lab map elements
START = '^'
EMPTY = '.'
OBSTACLE = '#'
TRAVERSED = 'X'

# Steps for traversal to be considered a loop
# Hard coded value may not work for more complex inputs
MAX_STEPS = 7000

# Global set of coordinates traversed by guard path
# Filled in Part 1 for reuse in Part 2
traversed = set()


# Decorator to calculate duration taken by a function
def calculate_time(func):
    def inner1(*args, **kwargs):
        begin = perf_counter()
        res = func(*args, **kwargs)
        end = perf_counter()
        print(f"Function {func.__name__} took: {end - begin} seconds.")
        return res
    return inner1


# Parse input file, returning a 2D array representing the lab map
# Sets global variables for the max width and max height of the map
def parse_input(file: str) -> list[list[str]]:
    with open(file) as file:
        lab_map = [list(line.strip()) for line in file.readlines()]

    global MAP_HEIGHT
    global MAP_WIDTH
    MAP_HEIGHT = len(lab_map)
    MAP_WIDTH = len(lab_map[0])

    return lab_map


# Part 1
# Validates that a given position is within the bounds of the lab map
def valid_pos(lab_map: list[list[str]], y: int, x: int) -> bool:
    if not lab_map:
        return False

    return y >= 0 and x >= 0 and y < MAP_HEIGHT and x < MAP_WIDTH


# Returns the coordinates of the next position given the current position and direction
def get_next_pos(y: int, x: int, direction: Direction) -> tuple[int, int]:
    match direction:
        case Direction.NORTH:
            return y - 1, x
        case Direction.EAST:
            return y, x + 1
        case Direction.SOUTH:
            return y + 1, x
        case Direction.WEST:
            return y, x - 1
        case _:
            raise Exception('Direction not found')


# Returns the coordinates of the next position and next direction given the current
# position and direction, ensuring that the next position is not an obstacle
# Guard pathing turns 90 degrees clockwise when an obstacle is encountered
def update_pos(
    lab_map: list[list[str]],
    y: int,
    x: int,
    direction: Direction
) -> tuple[int, int, str]:
    next_y, next_x = get_next_pos(y, x, direction)
    if not valid_pos(lab_map, next_y, next_x):
        return next_y, next_x, direction

    while lab_map[next_y][next_x] == OBSTACLE:
        DIRECTIONS = list(Direction)
        direction = DIRECTIONS[(DIRECTIONS.index(direction) + 1) % CARDINALITY]
        next_y, next_x = get_next_pos(y, x, direction)
    return next_y, next_x, direction


# Find the starting position and direction of the guard in the lab map
def get_start(lab_map: list[list[str]]) -> tuple[int, int, str]:
    for i, line in enumerate(lab_map):
        for j, char in enumerate(line):
            if char == START:
                return i, j, Direction.NORTH

    raise Exception('No guard starting position found')


# Count the number of distinct positions traversed by a lab guard
@calculate_time
def count_distinct_steps(lab_map: list[list[str]]) -> int:
    y, x, direction = get_start(lab_map)

    while valid_pos(lab_map, y, x):
        traversed.add((y, x))
        y, x, direction = update_pos(lab_map, y, x, direction)

    return len(traversed)


# Part 2
# Checks if a guard traversing the given map encounters a loop
def has_loop(lab_map: list[list[str]]) -> bool:
    y, x, direction = get_start(lab_map)

    steps = 0
    while valid_pos(lab_map, y, x):
        y, x, direction = update_pos(lab_map, y, x, direction)
        steps += 1

        if steps > MAX_STEPS:
            return True

    return False


# Returns the number of positions where placing an obstacle would put the
# guard into a loop
# Brute forces the solution by trial and erroring obstacle placement locations
# Optimisations:
# - Temporarily mutates the lab map instead of deep copying it <Saves ~100s>
# - Only place obstacles along the original path <Saves ~60s>
@calculate_time
def find_path_loops(lab_map: list[list[str]]) -> int:
    valid_obstacles = 0

    for coords in traversed:
        y, x = coords
        if lab_map[y][x] != EMPTY:
            continue

        lab_map[y][x] = OBSTACLE
        if has_loop(lab_map):
            valid_obstacles += 1
        lab_map[y][x] = EMPTY

    return valid_obstacles


if __name__ == '__main__':
    lab_map = parse_input('puzzle_input.txt')

    num_distinct_pos = count_distinct_steps(lab_map)
    print(f'Part 1: {num_distinct_pos}')

    num_obstacles = find_path_loops(lab_map)
    print(f'Part 2: {num_obstacles}')
