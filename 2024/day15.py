# Written by Jason Phua
# on 15/12/2024
# Advent of Code 2024 - Day 15
# Solving https://adventofcode.com/2024/day/15
from typing import NamedTuple, TypeAlias
from copy import deepcopy
from collections import deque


# Define co-ordinates of a point on a grid
class Point(NamedTuple):
    x: int
    y: int


# Named tuple storing a box's new position and its original character
class BoxMove(NamedTuple):
    new_pos: Point
    box_side: str


# Grid aligned directions and their resulting position changes
MOVEMENT = {
    '^': lambda pos: Point(pos.x, pos.y - 1),
    'v': lambda pos: Point(pos.x, pos.y + 1),
    '<': lambda pos: Point(pos.x - 1, pos.y),
    '>': lambda pos: Point(pos.x + 1, pos.y)
}
LATERAL_MOVE = '<>'
VERTICAL_MOVE = '^v'


Warehouse: TypeAlias = list[list[str]]
# Unscaled warehouse characters
ROBOT = '@'
BOX = 'O'
WALL = '#'
EMPTY = '.'

# Scaled warehouse characters
SCALED_ROBOT = '@.'
SCALED_BOX = '[]'
SCALED_WALL = '##'
SCALED_EMPTY = '..'
BOX_LEFT = '['
BOX_RIGHT = ']'

# When scaling a warehouse grid, map the original character
# to its scaled character
SCALED_OBJECT = {
    ROBOT: SCALED_ROBOT,
    BOX: SCALED_BOX,
    WALL: SCALED_WALL,
    EMPTY: SCALED_EMPTY
}


# Parse input file, returning a 2D array of the warehouse, and the move instructions
def parse_input(file: str) -> tuple[Warehouse, str]:
    with open(file) as file:
        warehouse, moves = file.read().strip().split('\n\n')
        warehouse = [list(line) for line in warehouse.strip().split('\n')]
        moves = ''.join(moves.strip().split('\n'))

    return warehouse, moves


# Given a warehouse map and movement instructions, move a robot through the warehouse,
# interacting with boxes when possible
# Returns the changed warehouse grid
def simulate_warehouse_robot(warehouse: Warehouse, moves: str) -> Warehouse:
    # Retrieve the initial co-ordinates of the robot
    def get_start(warehouse: Warehouse) -> Point:
        for y, line in enumerate(warehouse):
            for x, char in enumerate(line):
                if char == ROBOT:
                    return Point(x, y)
        raise Exception('Error: Robot not found in map.')

    # Check whether the given warehouse is a scaled warehouse
    # I.e. contains double wide boxes
    def is_scaled(warehouse: Warehouse) -> bool:
        for line in warehouse:
            for char in line:
                if char in SCALED_BOX:
                    return True
        return False

    # Part 1
    # Recursive move function for a non-scaled warehouse
    def move_object(warehouse: Warehouse, pos: Point, move: str) -> Point:
        obj = warehouse[pos.y][pos.x]
        next_pos = MOVEMENT[move](pos)
        adj_object = warehouse[next_pos.y][next_pos.x]

        # If adjacent position is occupied by a wall, do nothing
        if adj_object == WALL:
            return pos

        # If next position moves a box, attempt move, then check if move was
        # successful by checking if the box's position changed
        if adj_object == BOX:
            if move_object(warehouse, next_pos, move) == next_pos:
                return pos

        warehouse[pos.y][pos.x] = EMPTY
        warehouse[next_pos.y][next_pos.x] = obj
        return next_pos

    # Part 2
    # Given a box side and position, return the position of its corresponding side
    def box_pair_coord(box: Point, side: str) -> Point:
        return Point(box.x + 1, box.y) if side == BOX_LEFT else Point(box.x - 1, box.y)

    # Run Breadth First Search in a single given direction to return the set of all
    # connected boxes that will be interacted with
    def bfs_connected_boxes(warehouse: Warehouse, box: Point, move: str) -> set[Point]:
        boxes = set()

        q = deque()
        q.append(box)
        q.append(box_pair_coord(box, warehouse[box.y][box.x]))
        while q:
            box_pos = q.popleft()
            boxes.add(box_pos)

            next_pos = MOVEMENT[move](box_pos)
            next_obj = warehouse[next_pos.y][next_pos.x]
            if next_obj in SCALED_BOX:
                q.append(next_pos)
                q.append(box_pair_coord(next_pos, next_obj))

        # print(boxes)
        return boxes

    # Given a set of box positions, move the box in that direction and store the new position
    # and corresponding box character in a set of tuples
    def valid_box_move(warehouse: Warehouse, box_set: set[Point], move: str) -> set[BoxMove]:
        moved_box_set = set()
        for box in box_set:
            box_side = warehouse[box.y][box.x]
            next_pos = MOVEMENT[move](box)
            next_obj = warehouse[next_pos.y][next_pos.x]
            if next_obj != WALL:
                moved_box_set.add(BoxMove(next_pos, box_side))
        return moved_box_set

    # Given previous and next positions and their corresponding character, erase objects
    # in the previous positions from the warehouse, and readd objects in their new positions
    def move_boxes(warehouse: Warehouse, prev: set[Point], next_move: set[BoxMove]) -> None:
        for prev_pos in prev:
            warehouse[prev_pos.y][prev_pos.x] = EMPTY
        for move in next_move:
            pos = move.new_pos
            box = move.box_side
            warehouse[pos.y][pos.x] = box

    # Part 2
    # Recursive move function for a scaled warehouse
    def move_scaled_object(warehouse: Warehouse, pos: Point, move: str) -> Point:
        obj = warehouse[pos.y][pos.x]
        next_pos = MOVEMENT[move](pos)
        adj_obj = warehouse[next_pos.y][next_pos.x]

        # If adjacent position is occupied by a wall, do nothing
        if adj_obj == WALL:
            return pos

        # If next position moves a scaled box laterally, move recursively, and check
        # if move was successful by checking if the scaled box's position changed
        if adj_obj in SCALED_BOX and move in LATERAL_MOVE:
            if move_scaled_object(warehouse, next_pos, move) == next_pos:
                return pos

        # If next position interacts with a scaled box vertically,
        # then find all connecting boxes, validate, then move all at once
        if adj_obj in SCALED_BOX and move in VERTICAL_MOVE:
            box_set = bfs_connected_boxes(warehouse, next_pos, move)
            moved_box_set = valid_box_move(warehouse, box_set, move)
            if len(box_set) != len(moved_box_set):
                return pos
            move_boxes(warehouse, box_set, moved_box_set)

        warehouse[pos.y][pos.x] = EMPTY
        warehouse[next_pos.y][next_pos.x] = obj
        return next_pos

    # Avoid changing original input
    warehouse = deepcopy(warehouse)
    move_func = move_scaled_object if is_scaled(warehouse) else move_object

    robot_pos = get_start(warehouse)
    for move in moves:
        robot_pos = move_func(warehouse, robot_pos, move)

    return warehouse


# Calculate the 'GPS co-ordinate' of a box following the formula:
# GPS_coord = y_coord * 100 + x_coord
# And return the sum of GPS co-ordinates of all boxes in a warehouse
def sum_box_gps_coords(warehouse: Warehouse) -> int:
    gps_sum = 0
    for y, line in enumerate(warehouse):
        for x, char in enumerate(line):
            if char == BOX or char == BOX_LEFT:
                gps_sum += y * 100 + x
    return gps_sum


# Double the size of a warehouse according to Part 2 instructions
def double_warehouse_size(warehouse: Warehouse) -> Warehouse:
    return [[scaled for obj in row for scaled in SCALED_OBJECT[obj]] for row in warehouse]


if __name__ == '__main__':
    warehouse, moves = parse_input('puzzle_input.txt')

    moved_warehouse = simulate_warehouse_robot(warehouse, moves)
    gps_sum_p1 = sum_box_gps_coords(moved_warehouse)
    print(f'Part 1: {gps_sum_p1}')

    scaled_warehouse = double_warehouse_size(warehouse)
    moved_scaled_warehouse = simulate_warehouse_robot(scaled_warehouse, moves)
    gps_sum_p2 = sum_box_gps_coords(moved_scaled_warehouse)
    print(f'Part 2: {gps_sum_p2}')
