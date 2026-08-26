# Advent Of Code 2023 - Day 8
# Solving https://adventofcode.com/2023/day/8
from pprint import pprint
from math import lcm


# Part 1
def map_steps(file):
    steps = 0
    nodes_map = {}
    with open(file) as input_file:
        desert_map = input_file.read().splitlines()
        instructions = desert_map[0].replace('R', '1').replace('L', '0')
        for i in range(2, len(desert_map)):
            nodes = desert_map[i].split(' = ')
            node_start = nodes[0]
            node_paths = filter(lambda x: x.isalpha() or x.isspace(), nodes[1])
            nodes_map[node_start] = ''.join(node_paths).split()
        current_node = 'AAA'
        i = 0
        while current_node != 'ZZZ':
            direction = int(instructions[i])
            current_node = nodes_map[current_node][direction]
            steps += 1
            i = i + 1 if i < len(instructions) - 1 else 0
    print(f'Total Steps = {steps}')
    return steps


map_steps("puzzle_input.txt")
# Answer: 15517


# Part 2

"""
Calculate the number of steps by finding the LCM of the
steps needed for each node ending with A to get to its
corresponding node ending with Z

A brute force method is ineffective as the answer is
almost 15 trillion
My brute force method completes about 450,000 steps per second
At that rate, it would take over 384 days to complete
"""


def ghost_map_steps(file):
    steps = []
    nodes_map = {}
    with open(file) as input_file:
        desert_map = input_file.read().splitlines()
        instructions = desert_map[0].replace('R', '1').replace('L', '0')
        for i in range(2, len(desert_map)):
            nodes = desert_map[i].split(' = ')
            node_start = nodes[0]
            node_paths = nodes[1][1:-1].replace(',', '')
            nodes_map[node_start] = ''.join(node_paths).split()
        starting_nodes = [node for node in nodes_map.keys() if node[2] == 'A']
        for node in starting_nodes:
            path_length = 0
            i = 0
            while not node.endswith('Z'):
                direction = int(instructions[i])
                node = nodes_map[node][direction]
                path_length += 1
                i = i + 1 if i < len(instructions) - 1 else 0
            steps.append(path_length)
        total_steps = lcm(*steps)
    print(f'Total Steps = {total_steps}')
    return total_steps


ghost_map_steps("puzzle_input.txt")
# Answer: 14935034899483
