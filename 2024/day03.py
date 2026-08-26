# Written by Jason Phua
# on 03/12/2024
# Advent of Code 2024 - Day 3
# Solving https://adventofcode.com/2024/day/3
import re


# Parses the input file and returns a single string of instructions
def parse_input(file: str) -> str:
    with open(file) as file:
        return file.read()


# Part 1
# Find all valid multiplication commands
def find_mult_commands(memory: str) -> list[str]:
    MULT_PATTERN = r"mul\([0-9]{1,3},[0-9]{1,3}\)"
    return re.findall(MULT_PATTERN, memory)


# Runs a multiplication command
# First checks that command is valid to run, returns 0 if not
def mult(instruction: str, enabled=True) -> int:
    if not enabled or 'mul' not in instruction:
        return 0

    NUMBER_PATTERN = r"([0-9]{1,3}),([0-9]{1,3})"
    numbers = re.search(NUMBER_PATTERN, instruction)
    num1, num2 = int(numbers.group(1)), int(numbers.group(2))
    return num1 * num2


# Run all valid multiplication commands and return the product sum
def run_mult_commands(mult_commands: list[str]) -> int:
    product_sum = 0
    for command in mult_commands:
        product_sum += mult(command)
    return product_sum


# Part 2
# Find valid multiplication, do and don't commands
def find_commands(memory: str) -> list[str]:
    INSTRUCTION_PATTERN = r"mul\([0-9]{1,3},[0-9]{1,3}\)|do\(\)|don\'t\(\)"
    return re.findall(INSTRUCTION_PATTERN, memory)


# Run all valid instructions and return the product sum
# Halt and resume calculations for don't() and do() respectively
def run_instructions(mult_commands: list[str]) -> int:
    product_sum = 0
    enabled = True
    CONDITIONALS = {'don\'t()': False, 'do()': True}

    for command in mult_commands:
        enabled = CONDITIONALS.get(command, enabled)
        product_sum += mult(command, enabled)

    return product_sum


if __name__ == '__main__':
    memory = parse_input('puzzle_input.txt')

    mult_commands = find_mult_commands(memory)
    product_sum = run_mult_commands(mult_commands)
    print(f'Part 1: {product_sum}')

    commands = find_commands(memory)
    product_sum = run_instructions(commands)
    print(f'Part 2: {product_sum}')
