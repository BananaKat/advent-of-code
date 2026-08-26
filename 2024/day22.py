# Written by Jason Phua
# on 25/12/2024
# Advent of Code 2024 - Day 22
# Solving https://adventofcode.com/2024/day/22
import numpy as np


# Parse input file, returning a list of initial secret numbers
def parse_input(file: str) -> list[int]:
    with open(file) as file:
        return [int(line.strip()) for line in file]


# Generate secret numbers after 2000 iterations and compute the sum
def secret_number_generation(initial_numbers: list[int]) -> int:
    # Mix secret number = given_value bitwise_XOR secret_number
    def mix(value: int, secret_number: int) -> int:
        return value ^ secret_number

    # Prune secret number = secret_number modulo 16777216
    # Note: x % 16777216 = x % (2**24) = x & ((1 << 24) - 1)
    def prune(value: int) -> int:
        mask = (1 << 24) - 1
        return value & mask

    # Determine the next secret number given the previous secret number
    def next_secret(secret_number: int) -> int:
        # secret_number * 64 = secret_number * (2**6) = secret_number << 6
        secret_number = prune(mix(secret_number << 6, secret_number))
        # secret_number // 32 = secret_number // (2**5) = secret_number >> 5
        secret_number = prune(mix(secret_number >> 5, secret_number))
        # secret_number * 2048 = secret_number * (2**11) = secret_number << 11
        secret_number = prune(mix(secret_number << 11, secret_number))
        return secret_number

    # Use Numpy Vectorisation to operate on entire array at once
    # Each operation, transform the secret numbers, then find the sum
    def vectorised_secret_sum(nums: list[int], iters: int) -> int:
        np_nums = np.array(nums, dtype=np.uint32)
        for _ in range(iters):
            np_nums = next_secret(np_nums)
        return np.sum(np_nums)

    return vectorised_secret_sum(initial_numbers, 2000)


if __name__ == '__main__':
    initial_numbers = parse_input('puzzle_input.txt')
    print(f'Part 1: {secret_number_generation(initial_numbers)}')
