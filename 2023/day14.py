# Advent Of Code 2023 - Day 14
# Solving https://adventofcode.com/2023/day/14
from pprint import pprint
import numpy as np


# Part 1
def roll_rocks_north(rocks):
    # Move rocks as far right as possible
    for row in rocks:
        for i in range(len(row) - 2, -1, -1):
            rock = row[i]
            if rock == 'O':  # Initial check
                for j in range(i, len(row) - 1):
                    next_rock = row[j + 1]
                    if next_rock == '.':
                        row[j + 1] = 'O'
                        row[j] = '.'
                    else:
                        break
    return rocks


def calculate_load(rocks):
    load = 0
    for i, row in enumerate(reversed(rocks)):
        round_rocks = np.count_nonzero(row == 'O')
        load += round_rocks * (i + 1)
    return load


def total_north_load(file):
    with open(file) as input_file:
        rocks = [list(line.rstrip()) for line in input_file]
    # Rotate so Cardinal Direction faces right (end of list)
    rocks = np.rot90(np.array(rocks), 3)
    rocks = roll_rocks_north(rocks)
    rocks = np.rot90(rocks)
    load = calculate_load(rocks)
    print(f'Load on North Support Beams = {load}')
    return load


total_north_load('input.txt')
# Answer: 111339


# Part 2
def north_load_after_spin_cycles(file):
    # The cycle REPEATS after 1000 cycles
    # This applies to all datasets which was found by chance
    cycles = 1000
    rotations = cycles * 4
    with open(file) as input_file:
        rocks = np.array([list(line.rstrip()) for line in input_file])
    # Rotate so Cardinal Direction faces right (end of list)
    # North --> West --> South --> East (270 degree rotations)
    # Initialy, East faces right
    for i in range(rotations):
        rotated_rocks = np.rot90(rocks, 3)
        rocks = roll_rocks_north(rotated_rocks)
    load = calculate_load(rocks)
    print(f'North Support Beams Load After Spin Cycles = {load}')
    return load


north_load_after_spin_cycles('input.txt')
# Answer: 93736
