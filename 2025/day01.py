# Written by Jason Phua
# on 03/12/2025
# Advent of Code 2025 - Day 1
# Solving https://adventofcode.com/2025/day/1
from collections import defaultdict


# Parse input file and return seperated direction and distance
def parse_input(file: str) -> list[tuple[int, int]]:
    rotations = []
    with open(file) as file:
        for line in file:
            direction = -1 if line[0] == 'L' else 1
            distance = int(line[1:].strip())
            rotations.append((direction, distance))

    return rotations


# Part 1
# Count the number of rotations that move the dial past the "0" position
def count_point_zero(dial_pos: int, rotations: list[tuple[int, int]]) -> int:
    count = 0

    for direction, distance in rotations:
        dial_pos = (dial_pos + distance * direction) % 100
        count += 1 if dial_pos == 0 else 0

    return count


# Part 2
# Check if a turn passes zero, given that the distance is less than a full rotation
def passes_zero(direction: int, prev_pos: int, next_pos: int) -> bool:
    # If the dial starts at 0, it cannot pass 0
    if prev_pos == 0:
        return False
    # If the dial ends at 0, it always passes 0
    if next_pos == 0:
        return True
    if direction == -1:
        return next_pos > prev_pos
    else:
        return next_pos < prev_pos


# Count the number of rotations that cause the dial to pass "0"
def count_passes_zero(dial_pos: int, rotations: list[tuple[int, int]]) -> int:
    count = 0

    for direction, distance in rotations:
        full_rotations, bounded_distance = divmod(distance, 100)
        next_pos = (dial_pos + bounded_distance * direction) % 100
        count += full_rotations + passes_zero(direction, dial_pos, next_pos)
        dial_pos = next_pos

    return count


if __name__ == '__main__':
    rotations, init_dial_pos = parse_input('puzzle_input.txt'), 50

    print(f'Part 1: {count_point_zero(init_dial_pos, rotations)}')
    print(f'Part 2: {count_passes_zero(init_dial_pos, rotations)}')

