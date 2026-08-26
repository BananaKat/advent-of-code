# Written by Jason Phua
# on 08/12/2024
# Advent of Code 2024 - Day 7
# Solving https://adventofcode.com/2024/day/7


operations = {}


# Parse input file, returning a list of dictionaries, each containing a
# target number, and a list of equation numbers
def parse_input(file: str) -> list[dict[str, int | list[int]]]:
    with open(file) as file:
        return [
            {
                'target': int(target),
                'numbers': [int(num) for num in numbers.strip().split()]
            } for target, numbers in (line.split(':') for line in file.readlines())
        ]


# Combines the given numbers to using the given operations and then is called
# recursively with the used numbers removed until either the target is reached,
# or the given numbers are exhausted
def can_make_target(target: int, res: int, numbers: list[int]) -> bool:
    if res == target and len(numbers) == 0:
        return True
    if len(numbers) == 0 or res > target:
        return False

    next_num = numbers[0]
    for func in operations.values():
        next_res = func(res, next_num)
        if can_make_target(target, next_res, numbers[1:]):
            return True

    return False


# Find the total calibration result: the sum of equation target numbers that can be made
# using the list of numbers and the given operators
# Evaluate left-to-right and ignore precedence rules
#
# Warning: Alters the equations list
def sum_calibration_results(equations: list[dict[str, int | list[int]]]) -> int:
    total = 0

    for eq in equations:
        start = eq['numbers'].pop(0)
        if can_make_target(eq['target'], start, eq['numbers']):
            total += eq['target']

    return total


if __name__ == '__main__':
    # Part 1: '+' & '*' operations
    equations = parse_input('puzzle_input.txt')
    operations = {
        '+': lambda x, y: x + y,
        '*': lambda x, y: x * y
    }
    p1_calibration_result = sum_calibration_results(equations)
    print(f'Part 1: {p1_calibration_result}')

    # Part 2: '+', '*', & '||' operations
    equations = parse_input('puzzle_input.txt')
    operations = {
        '+': lambda x, y: x + y,
        '*': lambda x, y: x * y,
        '||': lambda x, y: int(str(x) + str(y))
    }
    p2_calibration_result = sum_calibration_results(equations)
    print(f'Part 2: {p2_calibration_result}')
