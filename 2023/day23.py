# Advent Of Code 2023 - Day 23
# Solving https://adventofcode.com/2023/day/23
from pprint import pprint
import copy
import sys


sys.setrecursionlimit(100_000)


# Part 1
def isValidPos(row, col, row_size, col_size):
    if (row < 0 or col < 0 or row > row_size - 1 or col > col_size - 1):
        return False
    return True


def find_neighbours(hike_map, node):
    valid_neighbours = []
    row, col = node

    above_row = row - 1
    below_row = row + 1

    left_col = col - 1
    right_col = col + 1

    row_size = len(hike_map)
    col_size = len(hike_map[row])

    # Consider slopes: (>, V, <, ^)
    tile = hike_map[row][col]
    slopes = {
        '>': (row, right_col),
        'V': (below_row, col),
        '<': (row, left_col),
        '^': (above_row, col)
    }
    if tile in '>V<^':
        return [slopes[tile]]

    # Check surrounding values
    # North
    if isValidPos(above_row, col, row_size, col_size):
        item = hike_map[above_row][col]
        if item != '#':
            valid_neighbours.append((above_row, col))
    # West
    if isValidPos(row, left_col, row_size, col_size):
        item = hike_map[row][left_col]
        if item != '#':
            valid_neighbours.append((row, left_col))
    # East
    if isValidPos(row, right_col, row_size, col_size):
        item = hike_map[row][right_col]
        if item != '#':
            valid_neighbours.append((row, right_col))
    # South
    if isValidPos(below_row, col, row_size, col_size):
        item = hike_map[below_row][col]
        if item != '#':
            valid_neighbours.append((below_row, col))
    return valid_neighbours


# Global list of path
record = []
visited_record = {}


def depth_first_search(hike_map, visited, node, cur_steps):
    if node[0] == len(hike_map) - 1:
        record.append(cur_steps)
    path = cur_steps
    if node not in visited:
        visited.add(node)
        visited_record[node] = copy.deepcopy(visited)
        cur_steps += 1
        adjacent_nodes = find_neighbours(hike_map, node)
        for neighbour in adjacent_nodes:
            visited = visited_record[node]
            path = depth_first_search(
                hike_map, visited, neighbour, cur_steps)
    return max(path, cur_steps)
    # Problem with visited: when it backtracks, visited is not reset


def find_steps_of_longest_hike(file):
    steps = 0
    visited = set()
    with open(file) as input_file:
        hike_map = [list(line.rstrip()) for line in input_file]
    start_node = (0, 1)
    depth_first_search(hike_map, visited, start_node, steps)
    print(record)
    print(f'Steps in Longest Hike = {max(record)}')
    return steps


find_steps_of_longest_hike("test.txt")
