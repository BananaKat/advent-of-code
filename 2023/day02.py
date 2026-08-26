# Advent Of Code 2023 - Day 2
# Solving https://adventofcode.com/2023/day/2
import math


# Part 1
# Conditions: 12 Red, 13 Green, 14 Blue
def validate_game(cube_sets):
    max_red = 12
    max_green = 13
    max_blue = 14
    for cube_set in cube_sets:
        cube_counts = {
            'red': 0,
            'green': 0,
            'blue': 0
        }
        for cube in cube_set:
            cube = cube.split()
            count = int(cube[0])
            colour = cube[1]
            cube_counts[colour] += count
        if cube_counts['red'] > max_red or cube_counts['green'] > max_green or cube_counts['blue'] > max_blue:
            return False
    return True


def sum_possible_game_IDs(file):
    with open(file) as input_file:
        ID_sum = 0
        for line in input_file:
            line = line.rstrip().split(':')
            game_ID = int(line[0].removeprefix('Game '))
            cube_sets = [cube_set.split(',')
                         for cube_set in line[1].split(';')]
            valid_game = validate_game(cube_sets)
            if valid_game:
                ID_sum += game_ID
    print(f'Valid Game IDs Sum = {ID_sum}')
    return ID_sum


sum_possible_game_IDs("puzzle_input.txt")
# Answer: 2317


# Part 2
def find_minimum_valid_cube_set(cube_sets):
    max_cube_counts = {
        'red': 0,
        'green': 0,
        'blue': 0
    }
    for cube_set in cube_sets:
        cube_counts = {
            'red': 0,
            'green': 0,
            'blue': 0
        }
        for cube in cube_set:
            cube = cube.split()
            count = int(cube[0])
            colour = cube[1]
            cube_counts[colour] += count
        if cube_counts['red'] > max_cube_counts['red']:
            max_cube_counts['red'] = cube_counts['red']
        if cube_counts['green'] > max_cube_counts['green']:
            max_cube_counts['green'] = cube_counts['green']
        if cube_counts['blue'] > max_cube_counts['blue']:
            max_cube_counts['blue'] = cube_counts['blue']
    return max_cube_counts


def calculate_game_power(minimum_valid_cube_set):
    power = math.prod(minimum_valid_cube_set.values())
    return power


def sum_game_minimum_powers(file):
    with open(file) as input_file:
        power_sum = 0
        for line in input_file:
            line = line.rstrip().split(':')
            cube_sets = [cube_set.split(',')
                         for cube_set in line[1].split(';')]
            minimum_valid_cube_set = find_minimum_valid_cube_set(cube_sets)
            power = calculate_game_power(minimum_valid_cube_set)
            power_sum += power
    print(f'Minimum Power Sum = {power_sum}')
    return power_sum


sum_game_minimum_powers("puzzle_input.txt")
# Answer: 74804
