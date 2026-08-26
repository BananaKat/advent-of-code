# Advent Of Code 2023 - Day 13
# Solving https://adventofcode.com/2023/day/13
from pprint import pprint


# Part 1
# LoR stands for Line of Reflection
def find_symmetrical_LoR(lines):
    last = len(lines)
    for n, _ in enumerate(lines[:-1]):
        symmetrical = True
        i = n
        j = n + 1
        while i >= 0 and j < last:
            if lines[i] != lines[j]:
                symmetrical = False
            i -= 1
            j += 1
        if symmetrical is True:
            return n + 1
    return 0


def summarise_reflection_lines(file):
    summary = 0
    with open(file) as input_file:
        patterns = input_file.read().rstrip().split('\n\n')
    for pattern in patterns:
        rows = [tuple(row) for row in pattern.split('\n')]
        cols = list(zip(*rows))
        vertical_LoR = find_symmetrical_LoR(cols)
        horizontal_LoR = find_symmetrical_LoR(rows)
        summary += vertical_LoR + horizontal_LoR * 100
    print(f'Reflection Lines Sum = {summary}')
    return summary


summarise_reflection_lines("input.txt")
# Answer: 30575


# Part 2
# A smudge is found if exactly ONE difference is found
def find_smudged_symmetrical_LoR(lines):
    last = len(lines)
    for n, _ in enumerate(lines[:-1]):
        differences = 0
        i = n
        j = n + 1
        while i >= 0 and j < last:
            for char_1, char_2 in zip(lines[i], lines[j]):
                if char_1 != char_2:
                    differences += 1
            i -= 1
            j += 1
        if differences == 1:
            return n + 1
    return 0


def summarise_smudged_reflection_lines(file):
    summary = 0
    with open(file) as input_file:
        patterns = input_file.read().rstrip().split('\n\n')
    for pattern in patterns:
        rows = [list(row) for row in pattern.split('\n')]
        cols = [list(col) for col in list(zip(*rows))]
        vertical_LoR = find_smudged_symmetrical_LoR(cols)
        horizontal_LoR = find_smudged_symmetrical_LoR(rows)
        summary += vertical_LoR + horizontal_LoR * 100
    print(f'Reflection Lines Sum = {summary}')
    return summary


summarise_smudged_reflection_lines("input.txt")
# Answer: 37478
