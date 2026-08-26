# Written by Jason Phua
# on 09/12/2024
# Advent of Code 2024 - Day 8
# Solving https://adventofcode.com/2024/day/8
from collections import defaultdict


# Parse input file, returning a dictionary of coordinates of matching frequencies
def parse_input(file: str) -> list[str]:
    with open(file) as file:
        city_map = [line.strip() for line in file.readlines()]

    global MAP_HEIGHT, MAP_WIDTH
    MAP_HEIGHT = len(city_map)
    MAP_WIDTH = len(city_map[0])

    # Character representation for empty position
    EMPTY = '.'

    # Matching frequencies are represented by matching characters
    antennas = defaultdict(list)
    for y_pos, line in enumerate(city_map):
        for x_pos, char in enumerate(line):
            if char != EMPTY:
                antennas[char].append((x_pos, y_pos))

    return antennas


# Validates that a given position is within the bounds of the city
def valid_coord(coord: tuple[int, int]) -> bool:
    x, y = coord
    return y >= 0 and x >= 0 and y < MAP_HEIGHT and x < MAP_WIDTH


# Part 1
# Count the number of distinct antinode positions, given a dictionary of antennas
# An antinode is a grid position inline with two matching antenna, such that one
# antenna is twice the distance away as the other
def count_distinct_antinodes(antennas: dict[str, list[tuple[int, int]]]) -> int:
    antinodes = []

    for coords in antennas.values():
        for i, P in enumerate(coords):
            for Q in coords[i + 1:]:
                x_P, y_P = P
                x_Q, y_Q = Q
                vec_PQ_x, vec_PQ_y = x_Q - x_P, y_Q - y_P

                antinode_P = (x_P - vec_PQ_x, y_P - vec_PQ_y)
                if valid_coord(antinode_P):
                    antinodes.append(antinode_P)

                antinode_Q = (x_Q + vec_PQ_x, y_Q + vec_PQ_y)
                if valid_coord(antinode_Q):
                    antinodes.append(antinode_Q)

    return len(set(antinodes))


# Part 2
# Count the number of distinct antinode positions, given a dictionary of antennas
# Account for 'antenna resonance' where each antinode may occur at any grid position
# such that it is inline with two matching antenna, seperated by the same distance as
# the two matching antenna
def count_resonant_antinodes(antennas: dict[str, list[tuple[int, int]]]) -> int:
    antinodes = []

    for coords in antennas.values():
        for i, P in enumerate(coords):

            # Each antenna is considered an antinode
            antinodes.append(P)

            for Q in coords[i + 1:]:
                x_P, y_P = P
                x_Q, y_Q = Q
                vec_PQ_x, vec_PQ_y = x_Q - x_P, y_Q - y_P

                antinode_P = (x_P - vec_PQ_x, y_P - vec_PQ_y)
                while valid_coord(antinode_P):
                    antinodes.append(antinode_P)
                    prev_x, prev_y = antinode_P
                    antinode_P = (prev_x - vec_PQ_x, prev_y - vec_PQ_y)

                antinode_Q = (x_Q + vec_PQ_x, y_Q + vec_PQ_y)
                while valid_coord(antinode_Q):
                    antinodes.append(antinode_Q)
                    prev_x, prev_y = antinode_Q
                    antinode_Q = (prev_x + vec_PQ_x, prev_y + vec_PQ_y)

    return len(set(antinodes))


if __name__ == '__main__':
    antennas = parse_input('puzzle_input.txt')

    num_distinct_antinodes = count_distinct_antinodes(antennas)
    print(f'Part 1: {num_distinct_antinodes}')

    num_resonant_antinodes = count_resonant_antinodes(antennas)
    print(f'Part 2: {num_resonant_antinodes}')
