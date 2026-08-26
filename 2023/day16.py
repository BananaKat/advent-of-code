# Advent Of Code 2023 - Day 16
# Solving https://adventofcode.com/2023/day/16
from pprint import pprint
import numpy as np
import copy


# Part 1
def parse_input(file):
    with open(file) as input_file:
        layout = np.array([list(line.rstrip())
                           for line in input_file.readlines()])
        # Note that '\\' is the same as '\' from the input
        pprint(layout)
    return layout


def project_light(layout, loc, angle, energised_layout):
    splitters = '|-'
    print(loc)
    print(angle)
    if loc[0] < 0 or loc[0] >= len(layout):
        return None

    if angle > 0:
        layout = np.rot90(layout, (360 - angle) // 90)
        energised_layout = np.rot90(energised_layout, (360 - angle) // 90)

    angle_interactions = {
        0: '|',
        90: '-',
        180: '|',
        270: '-'
    }

    cur_row = layout[loc[0]]
    i = loc[1]
    while i >= 0 and i < len(cur_row):
        loc[1] = i
        cur = cur_row[i]
        print(cur)
        energised_layout[loc[0]][loc[1]] = '#'

        # Check mirrors
        if cur == '/':
            layout = np.rot90(layout, 1)
            energised_layout = np.rot90(energised_layout, 1)
            loc[1] = loc[0]  # Switch X and Y coords
            loc[0] = i
            cur_row = layout[loc[0]]
            i = loc[1]
            angle = (angle + 90) % 360
        elif cur == '\\':
            layout = np.rot90(layout, 3)
            energised_layout = np.rot90(energised_layout, 3)
            loc[1] = loc[0]
            loc[0] = len(cur_row) - i - 1
            cur_row = layout[loc[0]]
            i = loc[1]
            angle = (angle + 270) % 360

        # Check splitters
        if cur == angle_interactions[angle]:
            angle_1 = (angle + 90) % 360
            angle_2 = (angle + 270) % 360
            loc_1 = copy.deepcopy(loc)
            loc_2 = copy.deepcopy(loc)
            if cur == '|':
                loc_1[0] -= 1  # Above '|' Splitter
                loc_2[0] += 1  # Below '|' Splitter
            elif cur == '-':
                loc_1[1] += 1  # Right of '-' Splitter
                loc_2[1] -= 1  # Left of '-' Splitter
            project_light(layout, loc_1, angle_1, energised_layout)
            project_light(layout, loc_2, angle_2, energised_layout)
            break

        print(energised_layout)
        i += 1
    return None


def energised_tiles(layout):
    energised = 0
    start = [0, 0]
    initial_direction = 0
    project_light(layout, start, initial_direction, energised_layout)
    print(f'Amount of Energised Tiles = {energised}')
    return energised


layout = parse_input("test.txt")
energised_layout = copy.deepcopy(layout)
energised_tiles(layout)
for line in energised_layout:
    print(''.join(line))

# Problem can use A*, Dijkstra, Depth First Search (DFS) or Breadth First Search (BFS)
# Most people recommend BFS (the simplest approach)

# Basic Pseudocode:

# expand_node(node, visited, energized):
    # bail if we left grid
    # bail if we already visited this node
    # add location to energized
    # add node to visited
    # return any continuations in the form of nodes

# make energized, visited, queue
# add starting node to queue
# while queue isn't empty
    # new_nodes = expand_node(node in queue)
    # remove the node we just expanded from the queue
    # add new_nodes to queue

# Rewrite this code but without Numpy
