# Written by Jason Phua
# on 15/12/2024
# Advent of Code 2024 - Day 14
# Solving https://adventofcode.com/2024/day/14
from typing import NamedTuple, TypeAlias
from enum import Enum
from re import findall
from collections import Counter
from os import getenv


# Puzzle input defined space sizes
WIDTH = 101
HEIGHT = 103


# Define possible quadrant areas
class Quadrant(Enum):
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_LEFT = 3
    BOTTOM_RIGHT = 4
    INVALID = -1


# Define magnitude components of a vector
class Vector(NamedTuple):
    x: int
    y: int


# Define co-ordinates of a point on a grid
class Point(NamedTuple):
    x: int
    y: int


# Define Robot type hint alias and set keys
Robot: TypeAlias = dict[str, Vector | Point]
POS = 'Position'
VEL = 'Velocity'

# ANSI colour escape codes
GREEN = '\033[32m'
RESET = '\033[0m'

# Refined estimated ranges for minimum safety factor time
LOWER_TIME = 7250
UPPER_TIME = 7750


# Parse input file, returning a list of robots with their position and velocity
def parse_input(file: str) -> list[Robot]:
    NUM_PATTERN = r'[+-]?\d+'

    def to_vector(info: str) -> Vector:
        return Vector(*map(int, findall(NUM_PATTERN, info)))

    def to_point(info: str) -> Point:
        return Point(*map(int, findall(NUM_PATTERN, info)))

    robots = []
    with open(file) as file:
        for line in file.readlines():
            point_info, velocity_info = line.strip().split(' ')
            point = to_point(point_info)
            velocity = to_vector(velocity_info)
            robot: Robot = {POS: point, VEL: velocity}
            robots.append(robot)

    return robots


# Get the position of a robot after a given number of seconds have elapsed
# Shift the robot's initial position by seconds multiplied by the velocity
# then wrap the position within the grid
def move_robot(robot: Robot, seconds: int) -> Point:
    # Perform vector scalar multiplication
    def scalar_multiplication(vector: Vector, scalar: int) -> Vector:
        return Vector(*map(lambda component: scalar * component, vector))

    # Translate a point by a vector
    def vector_transform(position: Point, vector: Vector) -> Point:
        return Point(position.x + vector.x, position.y + vector.y)

    # Wrap a robot's position around the edges of a defined map size
    # Given a positive size, will return a positive co-ordinate
    def wrap_position(position: Point) -> Point:
        return Point(position.x % WIDTH, position.y % HEIGHT)

    scaled_vector = scalar_multiplication(robot[VEL], seconds)
    transformed_pos = vector_transform(robot[POS], scaled_vector)
    final_pos = wrap_position(transformed_pos)
    return final_pos


# Part 1
# Calculates the 'safety factor', the product of the number of robots in each
# quadrant after a given number of seconds in which the robot moves along its velocity
def calculate_safety_factor(robots: list[Robot], seconds: int = 0) -> int:
    # Returns the quadrant a given position is in, or returns an invalid quadrant
    # for positions in middle rows or columns
    def find_quadrant(position: Point) -> Quadrant:
        mid_x = 1 if WIDTH % 2 == 0 else 0
        mid_y = 1 if WIDTH % 2 == 0 else 0

        if position.x < (WIDTH - mid_x) // 2 and position.y < (HEIGHT - mid_y) // 2:
            return Quadrant.TOP_LEFT
        if position.x > (WIDTH + mid_x) // 2 and position.y < (HEIGHT - mid_y) // 2:
            return Quadrant.TOP_RIGHT
        if position.x < (WIDTH - mid_x) // 2 and position.y > (HEIGHT + mid_y) // 2:
            return Quadrant.BOTTOM_LEFT
        if position.x > (WIDTH + mid_x) // 2 and position.y > (HEIGHT + mid_y) // 2:
            return Quadrant.BOTTOM_RIGHT

        return Quadrant.INVALID

    robot_quadrants = [find_quadrant(move_robot(robot, seconds))
                       for robot in robots]
    counts = Counter(robot_quadrants)
    return counts[Quadrant.TOP_LEFT] * counts[Quadrant.TOP_RIGHT] \
        * counts[Quadrant.BOTTOM_LEFT] * counts[Quadrant.BOTTOM_RIGHT]


# Part 2
# Finds an "Easter egg" arrangement of robots that form a Christmas tree
# Uses Part 1 as a clue to form the following heuristic:
# When the robots form an image, it is likely to have the lowest Safety Factor.
# This is because many of the robots will be either grouped into one quadrant, or
# near the centre, so will not be factored into the Safety Factor calculation
def find_easter_egg(robots: list[Robot]) -> int:
    # Checks whether the terminal being run supports colour
    def colour_supported() -> bool:
        term = getenv('TERM', '')
        colour_terminal_types = ['color', '256color', 'xterm', 'screen']
        return any(type in term for type in colour_terminal_types)

    # Prints out the arrangement of robots in a grid after a given number of
    # seconds of movement iterations have passed
    def print_robots(robots: list[Robot], seconds: int) -> None:
        grid = [['◻' for _ in range(WIDTH)] for _ in range(HEIGHT)]
        positions = set(move_robot(robot, seconds) for robot in robots)
        for x, y in positions:
            grid[y][x] = f'{GREEN}◼{RESET}' if colour_supported() else '◼'
        print('\n'.join(''.join(row) for row in grid))

    min_sf_time = LOWER_TIME
    min_safety_factor = calculate_safety_factor(robots)
    for i in range(LOWER_TIME, UPPER_TIME):
        safety_factor = calculate_safety_factor(robots, i)
        if safety_factor < min_safety_factor:
            min_safety_factor = safety_factor
            min_sf_time = i

    print_robots(robots, min_sf_time)
    print(f'Christmas tree displayed at {min_sf_time} seconds.')
    return min_sf_time


if __name__ == '__main__':
    robots = parse_input('puzzle_input.txt')

    safety_factor = calculate_safety_factor(robots, seconds=100)
    print(f'Part 1: {safety_factor}')

    easter_egg_time = find_easter_egg(robots)
    print(f'Part 2: {easter_egg_time}')
