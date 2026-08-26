# Advent Of Code 2023 - Day 22
# Solving https://adventofcode.com/2023/day/22
from pprint import pprint


# Part 1
def format_coords(coord):
    coord = [int(i) for i in coord]
    return [coord[2]] + coord[:2]


def safely_disintegrable_bricks(file):
    safe_to_disintegrate_bricks = 0
    bricks = {}
    with open(file) as input_file:
        for i, line in enumerate(input_file):
            coord1, coord2 = [format_coords(coord.split(','))
                              for coord in line.rstrip().split('~')]
            bricks[i] = [coord1, coord2]
    pprint(bricks)
    # Sort bricks by lowest Z coord
    # Drop brick
    print(f'Safely Disintegrable Bricks = {safe_to_disintegrate_bricks}')
    return safe_to_disintegrate_bricks


safely_disintegrable_bricks("test.txt")
