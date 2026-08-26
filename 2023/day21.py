# Advent Of Code 2023 - Day 21
# Solving https://adventofcode.com/2023/day/21
from pprint import pprint
import copy


# Part 1
def find_start(garden_map):
    for i, line in enumerate(garden_map):
        for j, item in enumerate(line):
            if item == 'S':
                return (i, j)


def isValidPos(row, col, row_size, col_size):
    if (row < 0 or col < 0 or row > row_size - 1 or col > col_size - 1):
        return False
    return True


def mark_next_positions(garden_map):
    next_garden_map = copy.deepcopy(garden_map)
    row_size = len(garden_map)
    for i, row in enumerate(garden_map):
        for j, item in enumerate(row):
            row = i
            col = j

            row_up = row - 1
            row_down = row + 1

            col_left = col - 1
            col_right = col + 1

            col_size = len(garden_map[i])
            row_above_col_size = len(garden_map[i - 1]) if i > 0 else 0
            row_below_col_size = len(
                garden_map[i + 1]) if i < row_size - 1 else 0

            if item == 'S' or item == 'O':
                next_garden_map[row][col] = '.'
                # Check surrounding values
                # North
                if isValidPos(row_up, col, row_size, row_above_col_size):
                    item = garden_map[row_up][col]
                    if item != '#':
                        next_garden_map[row_up][col] = 'O'
                # West
                if isValidPos(row, col_left, row_size, col_size):
                    item = garden_map[row][col_left]
                    if item != '#':
                        next_garden_map[row][col_left] = 'O'
                # East
                if isValidPos(row, col_right, row_size, col_size):
                    item = garden_map[row][col_right]
                    if item != '#':
                        next_garden_map[row][col_right] = 'O'
                # South
                if isValidPos(row_down, col, row_size, row_below_col_size):
                    item = garden_map[row_down][col]
                    if item != '#':
                        next_garden_map[row_down][col] = 'O'
    return next_garden_map


def count_reached_plots(garden_map):
    O_plots = 0
    for i, line in enumerate(garden_map):
        for j, item in enumerate(line):
            if item == 'O':
                O_plots += 1
    return O_plots


def plots_reached_in_steps(file):
    steps = 64
    with open(file) as input_file:
        garden_map = [list(line.rstrip()) for line in input_file.readlines()]
        start = find_start(garden_map)
    for i in range(steps):
        garden_map = mark_next_positions(garden_map)
    reached_plots = count_reached_plots(garden_map)
    print(f'Plots Reached in {steps} Steps = {reached_plots}')
    return reached_plots


plots_reached_in_steps("input.txt")
# Answer: 3853


# Part 2
"""
Advent of Code Subreddit suggests the answer is found
by doing Maths
There is a Quadratic Formula somewhere
"""
