# Advent Of Code 2023 - Day 18
# Solving https://adventofcode.com/2023/day/18
from pprint import pprint


# Part 1
"""
This problem uses the Trapezoid Formula from the Shoelace Algorithm:
https://en.wikipedia.org/wiki/Shoelace_formula#Trapezoid_formula

After the Trapezoid Formula, border_length must be added due to Pick's Theorem:
https://en.wikipedia.org/wiki/Pick's_theorem

Within the area counted by the Trapezoid Formula, only HALF of
the Trench (boundary) is counted
"""


def trapezium_formula(nodes, border_length):
    lava_area = 0
    for i, node in enumerate(nodes[:-1]):
        x_i, y_i = node
        next_x_i, next_y_i = nodes[i + 1]
        lava_area += (y_i + next_y_i) * (x_i - next_x_i)   # Trapezoid formula
        # lava_area += x_i * next_y_i - next_x_i * y_i     # Triangle form
    return (lava_area + border_length) // 2 + 1


def lava_area(file):
    border_length = 0
    # Positively oriented (Counter clock-wise) list of Vertices
    nodes = [(0, 0)]
    cur_node = [0, 0]
    # Store nodes in the form: [x, y]
    with open(file) as input_file:
        for line in input_file:
            # Parse input file line
            line = line.split()
            direction = line[0]
            distance = int(line[1])

            # Shift vector co-ords according to instructions
            if direction == 'R':
                cur_node[0] += distance
            if direction == 'L':
                cur_node[0] -= distance
            if direction == 'D':
                cur_node[1] -= distance
            if direction == 'U':
                cur_node[1] += distance

            border_length += distance
            # Prepend node to make vertice list positively oriented
            nodes.insert(0, tuple(cur_node))

    lava_area = trapezium_formula(nodes, border_length)
    print(f'Cubic Metres of Lava = {lava_area}')
    return lava_area


lava_area("input.txt")
# Answer: 52055


# Part 2
def convert_hex_codes(hex):
    direction_mapping = {
        '0': 'R',
        '1': 'D',
        '2': 'L',
        '3': 'U'
    }
    # Last digit indicates direction
    direction = direction_mapping[hex[-1]]
    # Convert Hex to Int
    distance = int(hex[:-1], 16)
    return direction, distance


def lava_area_from_hex_codes(file):
    border_length = 1
    # Positively oriented (Counter clock-wise) list of Vertices
    nodes = [(0, 0)]
    cur_node = [0, 0]
    # Store nodes in the form: [x, y]
    with open(file) as input_file:
        for line in input_file:
            hex_code = line.split()[2][2:-1]
            direction, distance = convert_hex_codes(hex_code)
            if direction == 'R':
                cur_node[0] += distance
            if direction == 'L':
                cur_node[0] -= distance
            if direction == 'D':
                cur_node[1] -= distance
            if direction == 'U':
                cur_node[1] += distance
            border_length += distance
            # Prepend node to make vertice list positively oriented
            nodes.insert(0, tuple(cur_node))
    lava_area = trapezium_formula(nodes, border_length)
    print(f'Cubic Metres of Lava From Hex Codes = {lava_area}')
    return lava_area


lava_area_from_hex_codes("input.txt")
# Answer: 67622758357096
