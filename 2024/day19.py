# Written by Jason Phua
# on 24/12/2024
# Advent of Code 2024 - Day 19
# Solving https://adventofcode.com/2024/day/19
from functools import lru_cache


# Parse input file, returning a list of patterns and a list of towel designs
def parse_input(file: str) -> tuple[list[str], list[str]]:
    with open(file) as file:
        block1, block2 = file.read().strip().split('\n\n')
        patterns = block1.split(', ')
        designs = [design.strip() for design in block2.split('\n')]
    return patterns, designs


def count_possible_designs(patterns: list[str], designs: list[str], part: int) -> int:
    # Part 1:
    # Use dynamic programming to check if a design is possible:
    # For each design, see if it starts with one of the available patterns,
    # then check the rest of the design recursively
    @lru_cache(maxsize=None)
    def is_possible(design: str) -> bool:
        if not design:
            return True

        for pattern in patterns:
            if not design.startswith(pattern):
                continue

            remaining_design = design[len(pattern):]
            if is_possible(remaining_design):
                return True

        return False

    # Part 2:
    # Use a similar approach to Part 1 to count valid arrangements of a design:
    # For each pattern, if the pattern is in the design, recursively count the
    # number of arrangements in the sub-design (the design after that starting pattern)
    @lru_cache(maxsize=None)
    def num_possible(design: str) -> int:
        # An empty design has exactly 1 arrangement
        if not design:
            return 1

        # Count arrangements
        count = 0
        for pattern in patterns:
            if not design.startswith(pattern):
                continue

            remaining_design = design[len(pattern):]
            count += num_possible(remaining_design)

        return count

    checker_func = is_possible if part == 1 else num_possible
    return sum(checker_func(design) for design in designs)


if __name__ == '__main__':
    patterns, designs = parse_input('puzzle_input.txt')

    possible_designs = count_possible_designs(patterns, designs, part=1)
    print(f'Part 1: {possible_designs}')

    num_designs = count_possible_designs(patterns, designs, part=2)
    print(f'Part 2: {num_designs}')
