# Written by Jason Phua
# on 25/12/2024
# Advent of Code 2024 - Day 21
# Solving https://adventofcode.com/2024/day/21
from typing import TypeAlias


Keypad: TypeAlias = dict[str | None, tuple[int, int]]

# Define keypad layouts as a 2D list
numeric_layout = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    [None, '0', 'A']
]
directional_layout = [
    [None, '^', 'A'],
    ['<', 'v', '>']
]

# Generate coordinate mappings
numeric_keypad = {
    key: (x, y)
    for y, row in enumerate(numeric_layout)
    for x, key in enumerate(row)
}
directional_keypad = {
    key: (x, y)
    for y, row in enumerate(directional_layout)
    for x, key in enumerate(row)
}


# Parse input file, returning a list of code strings
def parse_input(file: str) -> list[str]:
    with open(file) as file:
        return [line.strip() for line in file]


# Find the shortest button sequences and return the code complexity sum
def shortest_button_sequence(codes: list[str]) -> int:
    # Move horizontally then vertically and check if the gap (None key) is moved over
    def intercepts_gap(x1: int, y1: int, x2: int, y2: int, keypad: Keypad) -> bool:
        layout = numeric_layout if keypad == numeric_keypad else directional_layout
        # Horizontal movement
        if x1 < x2:  # Move right
            for x in range(x1 + 1, x2 + 1):
                if layout[y1][x] is None:
                    return True
        elif x1 > x2:  # Move left
            for x in range(x1 - 1, x2 - 1, -1):
                if layout[y1][x] is None:
                    return True
        # Vertical movement
        if y1 < y2:  # Move down
            for y in range(y1 + 1, y2 + 1):
                if layout[y][x2] is None:
                    return True
        elif y1 > y2:  # Move up
            for y in range(y1 - 1, y2 - 1, -1):
                if layout[y][x2] is None:
                    return True
        return False

    # Determine the movement sequence from one key to another
    def determine_sequence(dx: int, dy: int, vertical_priority: bool) -> str:
        y_button = {(dy > 0): 'v', (dy < 0): '^'}.get(True, '')
        x_button = {(dx > 0): '>', (dx < 0): '<'}.get(True, '')
        if vertical_priority:
            # Compute the vertical first only if moving horizontally hovers over the gap
            return y_button * abs(dy) + x_button * abs(dx) + 'A'
        # # Default to computing horizontal movement first
        # return x_button * abs(dx) + y_button * abs(dy) + 'A'
        if dx < 0:
            return x_button * abs(dx) + y_button * abs(dy) + 'A'
        return y_button * abs(dy) + x_button * abs(dx) + 'A'

    # Generate the button press sequence required to input the given code with the keypad
    def generate_sequence(code: str, keypad: Keypad) -> str:
        sequence = ''
        point = keypad['A']
        for char in code:
            x1, y1 = point
            point = keypad[char]
            x2, y2 = point
            dx, dy = x2 - x1, y2 - y1
            vertical_priority = intercepts_gap(x1, y1, x2, y2, keypad)
            sequence += determine_sequence(dx, dy, vertical_priority)
        return sequence

    # Code complexity = shortest_sequence_length * numeric_code_component
    def calculate_complexity(code: str, sequence: str) -> int:
        return len(sequence) * int(code[:-1])

    '''
    Issue:
    if you want to press "2" you have 2 options: "^<A" and "<^A" (same length)
    with 1 layer you still have 2 sequence of same length

           ^<A : <Av<A>>^A
           <^A : v<<A>^A>A

    but with 2 layers the sequences are:

           ^<A : v<<A>>^A<vA<A>>^AvAA^<A>A
           <^A : <vA<AA>>^AvA^<A>AvA^A

    it's like if with the 2nd option you need less moves to return the robot to "A"

    I need to find a way to preference < over ^
    '''
    code = '179A'
    num_seq = generate_sequence(code, numeric_keypad)
    print(num_seq)
    dir_seq1 = generate_sequence(num_seq, directional_keypad)
    print(dir_seq1)
    dir_seq2 = generate_sequence(dir_seq1, directional_keypad)
    print(dir_seq2)
    print(len(dir_seq2))
    print(calculate_complexity(code, dir_seq2))
    total_complexity = 0
    for code in codes:
        num_seq = generate_sequence(code, numeric_keypad)
        dir_seq1 = generate_sequence(num_seq, directional_keypad)
        dir_seq2 = generate_sequence(dir_seq1, directional_keypad)
        total_complexity += calculate_complexity(code, dir_seq2)
    return total_complexity


if __name__ == '__main__':
    codes = parse_input('puzzle_input.txt')
    print(codes)
    print(f'Part 1: {shortest_button_sequence(codes)}')
    # 148734 is too high
    # 142222 is too high
    # 141026 is just wrong
    # 135030 is also wrong
    # 137870 is the answer

# Solution by https://www.reddit.com/r/adventofcode/comments/1hj2odw/comment/m3ilhmj
# from collections import defaultdict


# def process_input(filename):
#     """Acquire input data"""
#     with open(filename) as file:
#         input = file.read().splitlines()
#     return input


# def enter_codes():
#     global button_presses
#     complexity_sum = 0
#     for code in codes:
#         # A "button press" is a sequence of ending in A
#         button_presses = defaultdict(int)

#         # First count button presses on the numeric keypad
#         move_numeric_keypad(code)

#         # Count all the button presses on the directional keypads
#         for n in range(robot_dir_keypads):
#             count_dir_keypad_presses()

#         complexity = 0
#         for button_press, count in button_presses.items():
#             complexity += len(button_press) * count
#         complexity_sum += complexity * int(code[:3])
#     return complexity_sum


# def move_numeric_keypad(code):
#     from_button = 'A'
#     for button in code:
#         directions = move_to_button(from_button, button)
#         from_button = button
#         directions += 'A'
#         button_presses[directions] += 1
#     return


# def move_to_button(from_button, to_button):
#     """If moving in the preferred direction would eventually move to the
#     missing button, then move all the way in the 90° direction. """
#     keypad = {'7': (0, 0), '8': (1, 0), '9': (2, 0),
#               '4': (0, 1), '5': (1, 1), '6': (2, 1),
#               '1': (0, 2), '2': (1, 2), '3': (2, 2),
#               'x': (0, 3), '0': (1, 3), 'A': (2, 3)}

#     x1, y1 = keypad[from_button]
#     x2, y2 = keypad[to_button]
#     nx, ny = keypad['x']    # missing button
#     directions = ''
#     while (x1, y1) != (x2, y2):
#         if x2 < x1:             # highest priority is left
#             if (y1 == ny) and (x2 == nx):    # if would move to missing button
#                 directions += '^' * (y1 - y2)   # move up instead
#                 y1 = y2
#             else:
#                 directions += '<'
#                 x1 -= 1
#         elif y2 < y1:           # move up
#             directions += '^'
#             y1 -= 1
#         elif y2 > y1:
#             if (x1 == nx) and (y2 == ny):    # if would move to missing button
#                 directions += '>' * (x2 - x1)   # move right instead
#                 x1 = x2
#             else:
#                 directions += 'v'   # move down
#                 y1 += 1
#         elif x2 > x1:        # lowest priority is right
#             directions += '>'
#             x1 += 1
#     return directions


# def count_dir_keypad_presses():
#     iterate_button_presses = dict(button_presses)
#     for button_press, count in iterate_button_presses.items():
#         move_dir_keypad(button_press, count)
#         button_presses[button_press] -= count
#     return


# def move_dir_keypad(code, count):
#     dir_keypad_moves = dict([(('A', '^'), '<A'),
#                              (('A', '>'), 'vA'),
#                              (('A', 'v'), '<vA'),
#                              (('A', '<'), 'v<<A'),
#                              (('^', 'A'), '>A'),
#                              (('^', '>'), 'v>A'),
#                              (('^', '<'), 'v<A'),
#                              (('^', 'v'), 'vA'),
#                              (('v', 'A'), '^>A'),
#                              (('v', '>'), '>A'),
#                              (('v', '<'), '<A'),
#                              (('v', '^'), '^A'),
#                              (('>', 'A'), '^A'),
#                              (('>', '^'), '<^A'),
#                              (('>', 'v'), '<A'),
#                              (('>', '<'), '<<A'),
#                              (('<', 'A'), '>>^A'),
#                              (('<', '^'), '>^A'),
#                              (('<', 'v'), '>A'),
#                              (('<', '>'), '>>A')])

#     from_button = 'A'
#     for button in code:
#         if from_button == button:
#             directions = 'A'
#         else:
#             directions = dir_keypad_moves[(from_button, button)]
#         from_button = button
#         button_presses[directions] += count
#     return

# #-----------------------------------------------------------------------------------------


# filename = 'puzzle_input.txt'
# robot_dir_keypads = 2
# #filename = 'sample.txt'; robot_dir_keypads = 2

# codes = process_input(filename)

# complexity_sum = enter_codes()

# print()
# print('Sum =', complexity_sum)
