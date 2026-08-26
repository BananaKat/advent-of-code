# Advent Of Code 2023 - Day 15
# Solving https://adventofcode.com/2023/day/15
from pprint import pprint


# Part 1
def HASH_algorithm(step):
    cur_val = 0
    for char in step:
        cur_val = ((cur_val + ord(char)) * 17) % 256
    return cur_val


def sum_HASH_values(file):
    result_sum = 0
    with open(file) as input_file:
        init_seq = input_file.readline().rstrip().split(',')
    for step in init_seq:
        result_sum += HASH_algorithm(step)
    print(f'Sum of Results = {result_sum}')
    return result_sum


sum_HASH_values("input.txt")
# Answer: 506269


# Part 2
def find_operation_and_lens(step):
    dash = '-'
    equals = '='
    if dash in step:
        lens = step.replace(dash, ' ')
        return dash, lens
    if equals in step:
        lens = step.replace(equals, ' ')
        return equals, lens


def calculate_focus_power(boxes):
    focus_power = 0
    for box_num, lenses in boxes.items():
        for slot, lens in enumerate(lenses):
            focal_length = int(lens.split()[1])
            focus_power += (box_num + 1) * (slot + 1) * focal_length
    return focus_power


def lens_focus_power(file):
    boxes = {i: [] for i in range(256)}
    with open(file) as input_file:
        init_seq = input_file.readline().rstrip().split(',')
    for step in init_seq:
        operation, lens = find_operation_and_lens(step)
        label = lens.split()[0]
        box = HASH_algorithm(label)
        if operation == '-':
            for item in boxes[box]:
                if label == item.split()[0]:
                    boxes[box].remove(item)
        elif operation == '=':
            replace = False
            for i, item in enumerate(boxes[box]):
                if label == item.split()[0]:
                    boxes[box][i] = lens
                    replace = True
            if replace is False:
                boxes[box].append(lens)
    focus_power = calculate_focus_power(boxes)
    print(f'Focus Power = {focus_power}')
    return focus_power


lens_focus_power("input.txt")
# Answer: 264021
