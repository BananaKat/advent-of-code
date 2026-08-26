# Written by Jason Phua
# on 29/01/2026
# Advent of Code 2025 - Day 6
# Solving https://adventofcode.com/2025/day/6
from functools import reduce
import operator
OPS = {
    '+': operator.add,
    '*': operator.mul,
}


# Parse input file and return a list of strings including all whitespace
def parse_input(filename: str) -> str:
    with open(filename) as file:
        return file.read().strip().split('\n')


# Part 1
# Transpose rows vertically and sum calculations
def total_vert_calc(lines: str) -> int:
    rows = [line.strip().split() for line in lines]
    return sum(
        reduce(OPS[col[-1]], map(int, col[:-1]))
        for col in zip(*rows)
    )


# Part 2
# Calculate each expression and sum
# Expressions are read vertically, right-to-left, by character
def vert_calc_by_col(lines: list[str]) -> int:
    # Convert groups of strings to integers, seperated by blank elements
    def split_on_empty(elements: list[str]) -> list[list[int]]:
        groups, current = [], []
        for elem in elements:
            if elem.strip() != '':
                current.append(int(elem))
                continue
            groups.append(current)
            current = []
        groups.append(current)
        return groups

    # Left justify lines, padding with spaces
    width = max(len(line) for line in lines)
    lines = [line.ljust(width, ' ') for line in lines]

    operands = lines[-1].split()
    vnums    = zip(*lines[:-1])
    ngroups  = split_on_empty([''.join(num) for num in vnums])
    assert len(operands) == len(ngroups)

    return sum(
        reduce(OPS[sym], nums)
        for nums, sym in zip(ngroups, operands)
    )


if __name__ == '__main__':
    lines = parse_input('puzzle_input.txt')

    print(f'Part 1: {total_vert_calc(lines)}')
    print(f'Part 2: {vert_calc_by_col(lines)}')
