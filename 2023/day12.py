# Advent Of Code 2023 - Day 12
# Solving https://adventofcode.com/2023/day/12
# My solutions were made with extensive help from YouTube video:
# https://www.youtube.com/watch?v=WiNz_zBhGIM
from pprint import pprint


# Part 1
def check_group_can_be_placed(springs, spring_index, record_size):
    if spring_index + record_size >= len(springs):
        return False
    # Check that a group of record_size can be placed
    # 1. Check that no dots are in the group
    # 2. Check that the element after the group is NOT a '#'
    springs_group = springs[spring_index:spring_index + record_size]
    element_after_group = springs[spring_index + record_size]
    return '.' not in springs_group and element_after_group != '#'


# Brute force recursion
# Increase indexes instead of actually placing springs
def spring_arrangement(springs, records, spring_index, record_index):
    # Base case: No records left
    if record_index >= len(records):
        # Check that there are no unchecked groups in springs
        if spring_index < len(springs) and '#' in springs[spring_index:]:
            return 0  # Invalid solution
        return 1
    # Base case: No springs left but unfinished groups
    if spring_index >= len(springs):
        return 0

    record_size = records[record_index]
    current_spring = springs[spring_index]

    # Check if the current spring is a '?'
    # If so, the current group may or may not be placed here
    if current_spring == '?':
        if check_group_can_be_placed(springs, spring_index, record_size):
            # Find arrangements after placing group here
            group_here = spring_arrangement(
                springs, records, spring_index + record_size + 1, record_index + 1)
            # Place '.' and then attempt to place group
            next_group_here = spring_arrangement(
                springs, records, spring_index + 1, record_index)
            # Sum arrangements
            result = group_here + next_group_here
        else:
            # Place '.' and then attempt to place group
            result = spring_arrangement(
                springs, records, spring_index + 1, record_index)

    # Check if current spring is a '#'
    # If so, the current group must be placed here
    elif current_spring == '#':
        if check_group_can_be_placed(springs, spring_index, record_size):
            result = spring_arrangement(
                springs, records, spring_index + record_size + 1, record_index + 1)
        else:
            return 0  # Invalid group placement

    # Check if current spring is a '.'
    # If so, the current group can only be placed after
    elif current_spring == '.':
        result = spring_arrangement(
            springs, records, spring_index + 1, record_index)

    return result


def sum_arrangements_of_springs(file):
    arrangement_sum = 0
    with open(file) as input_file:
        for line in input_file:
            line = line.rstrip().split()
            # Add '.' to the end of springs
            # This is done because spring groups can only be terminated by a dot or the end of the springs
            # But checking the end of the springs is not in the check_group_can_be_placed() function for simplicity
            springs = list(line[0]) + ['.']
            records = [int(i) for i in line[1].split(',')]
            arrangement_sum += spring_arrangement(springs, records, 0, 0)
    print(f'Arrangements of Springs Sum = {arrangement_sum}')
    return arrangement_sum


sum_arrangements_of_springs("puzzle_input.txt")
# Answer: 7916


# Part 2
# Dynamic Programming
global MEMO
MEMO = {}


def spring_arrangement_with_MEMO(springs, records, spring_index, record_index):
    # Base case: No records left
    if record_index >= len(records):
        # Check that there are no unchecked groups in springs
        if spring_index < len(springs) and '#' in springs[spring_index:]:
            return 0  # Invalid solution
        return 1
    # Base case: No springs left but unfinished groups
    if spring_index >= len(springs):
        return 0

    # Memoization: Check MEMO dictionary
    if (spring_index, record_index) in MEMO:
        return MEMO[(spring_index, record_index)]

    record_size = records[record_index]
    current_spring = springs[spring_index]

    # Check if the current spring is a '?'
    # If so, the current group may or may not be placed here
    if current_spring == '?':
        if check_group_can_be_placed(springs, spring_index, record_size):
            # Find arrangements after placing group here
            group_here = spring_arrangement_with_MEMO(
                springs, records, spring_index + record_size + 1, record_index + 1)
            # Place '.' and then attempt to place group
            next_group_here = spring_arrangement_with_MEMO(
                springs, records, spring_index + 1, record_index)
            # Sum arrangements
            result = group_here + next_group_here
        else:
            # Place '.' and then attempt to place group
            result = spring_arrangement_with_MEMO(
                springs, records, spring_index + 1, record_index)

    # Check if current spring is a '#'
    # If so, the current group must be placed here
    elif current_spring == '#':
        if check_group_can_be_placed(springs, spring_index, record_size):
            result = spring_arrangement_with_MEMO(
                springs, records, spring_index + record_size + 1, record_index + 1)
        else:
            return 0  # Invalid group placement

    # Check if current spring is a '.'
    # If so, the current group can only be placed after
    elif current_spring == '.':
        result = spring_arrangement_with_MEMO(
            springs, records, spring_index + 1, record_index)

    MEMO[(spring_index, record_index)] = result
    return result


def sum_arrangements_of_folded_springs(file):
    arrangement_sum = 0
    with open(file) as input_file:
        for line in input_file:
            line = line.rstrip().split()
            # Add '.' to the end of springs
            # This is done because spring groups can only be terminated by a dot or the end of the springs
            # But checking the end of the springs is not in the check_group_can_be_placed() function for simplicity
            springs = list('?'.join([line[0]] * 5)) + ['.']
            records = [int(i) for i in line[1].split(',')] * 5
            # Clear MEMO dictionary
            # This is because MEMO does not store the springs and records
            # and assumes that it is being used for the current line
            global MEMO
            MEMO = {}
            arrangement_sum += spring_arrangement_with_MEMO(
                springs, records, 0, 0)
    print(f'Arrangements of Folded Springs Sum = {arrangement_sum}')
    return arrangement_sum


sum_arrangements_of_folded_springs("puzzle_input.txt")
# Answer: 37366887898686
