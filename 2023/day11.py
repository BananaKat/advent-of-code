# Advent Of Code 2023 - Day 11
# Solving https://adventofcode.com/2023/day/11
from pprint import pprint


# Part 1
def expand_galaxy(rows, columns):
    # Expand vertically, stepping backwards to avoid interfering
    # with counter
    empty_vertical_space = '.'
    i = len(columns) - 1
    while i > 0:
        # Find empty columns
        if '#' not in columns[i]:
            # Insert '.' into every row
            for row in rows:
                row.insert(i, empty_vertical_space)
        i -= 1
    # Expand horizontally
    empty_horizontal_space = ['.'] * len(rows[0])
    j = 0
    while j < len(rows):
        # Find empty rows
        if '#' not in rows[j]:
            rows.insert(j, empty_horizontal_space)
            j += 2
        else:
            j += 1
    return rows


def locate_galaxies(expanded_galaxy):
    counter = 1
    galaxy_locations = {}
    for i in range(len(expanded_galaxy)):
        row = expanded_galaxy[i]
        for j in range(len(row)):
            if expanded_galaxy[i][j] == '#':
                galaxy_locations[counter] = [i, j]
                counter += 1
    return galaxy_locations


def sum_galaxy_distances(locations):
    # 5: [6, 1]
    # 9: [11, 5]
    # Distance = (11-6) + (5-1)
    distances = 0
    last_key = max(locations)
    for i in locations:
        for j in range(i + 1, last_key + 1):
            galaxy_1 = locations[i]
            galaxy_2 = locations[j]
            distances += abs(galaxy_2[0] - galaxy_1[0]) + \
                abs(galaxy_2[1] - galaxy_1[1])
    return distances


def sum_of_expanding_galaxy_paths(file):
    with open(file) as input_file:
        rows = [[*line][:-1] for line in input_file]
        columns = list(zip(*rows))
        expanded_galaxy = expand_galaxy(rows, columns)
        galaxy_locations = locate_galaxies(expanded_galaxy)
        distance_sum = sum_galaxy_distances(galaxy_locations)
    print(f'Sum of Expanding Galaxy Paths = {distance_sum}')
    return distance_sum


sum_of_expanding_galaxy_paths("puzzle_input.txt")
# Answer: 10885634


# Part 2
def locate_empty_rows_and_cols(rows, columns):
    empty_cols = []
    for i in range(len(columns)):
        col = columns[i]
        if '#' not in col:
            empty_cols.append(i)
    empty_rows = []
    for j in range(len(rows)):
        row = rows[j]
        if '#' not in row:
            empty_rows.append(j)
    return empty_rows, empty_cols


def expand_locations(galaxy_locations, empty_rows, empty_cols):
    expansion_constant = 999_999
    # Expand horizontally
    row_shift = 0  # Account for shifting due to expansion
    for row in empty_rows:
        row += row_shift
        for galaxy in galaxy_locations:
            galaxy_row = galaxy_locations[galaxy][0]
            if galaxy_row > row:
                galaxy_locations[galaxy][0] += expansion_constant
        row_shift += expansion_constant
    col_shift = 0  # Account for shifting due to expansion
    for col in empty_cols:
        col += col_shift
        for galaxy in galaxy_locations:
            galaxy_col = galaxy_locations[galaxy][1]
            if galaxy_col > col:
                galaxy_locations[galaxy][1] += expansion_constant
        col_shift += expansion_constant
    return galaxy_locations


def sum_of_million_expanding_galaxy_paths(file):
    with open(file) as input_file:
        rows = [[*line][:-1] for line in input_file]
        columns = list(zip(*rows))
        galaxy_locations = locate_galaxies(rows)
        empty_rows, empty_cols = locate_empty_rows_and_cols(rows, columns)
        expanded_galaxy_locations = expand_locations(
            galaxy_locations, empty_rows, empty_cols)
        distance_sum = sum_galaxy_distances(expanded_galaxy_locations)
    print(f'Sum of Paths of a Million Expanded Galaxy = {distance_sum}')
    return distance_sum


sum_of_million_expanding_galaxy_paths("puzzle_input.txt")
# Answer: 707505470642
