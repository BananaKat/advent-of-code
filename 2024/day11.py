# Written by Jason Phua
# on 11/12/2024
# Advent of Code 2024 - Day 11
# Solving https://adventofcode.com/2024/day/11
from functools import lru_cache
from math import floor, log10
import concurrent.futures


P1_BLINK_ITERS = 25
P2_BLINK_ITERS = 75


# Parse input file, returning a list of integers representing a line of stones
def parse_input(file: str) -> list[int]:
    with open(file) as file:
        return [int(stone) for stone in file.read().strip().split()]


# Returns whether a stone engraving consists of an even amount of digits
@lru_cache(maxsize=None)
def is_even_digits(stone: int) -> bool:
    return len(str(stone)) % 2 == 0


# Multiplies a stone engraving by a given factor
@lru_cache(maxsize=None)
def multiply_stone(num: int, factor: int = 2024) -> int:
    return num * factor


# Returns the result of splitting a stone in two
# Asssumes that the stone consists of an even amount of digits
@lru_cache(maxsize=None)
def split_stone(num: int) -> tuple[int, int]:
    # Messy back and forth integer to string conversions to string split
    # return int(str(num)[:len(str(num)) // 2]), int(str(num)[len(str(num)) // 2:])

    # Instead you can actually seperate the two halves mathematically:
    length = floor(log10(num)) + 1
    left = num // 10**(length // 2)
    right = num % 10**(length // 2)
    return left, right


# Simulate the resulting stone changes after blinking:
# - Stones engraved with 0 turn into 1
# - Stones engraved with numbers with an even amount of digits split into two stones
# - All other stones have their engravings multiplied by 2024
# Alters the stones list in place
def simulate_blink(stones: list[int]) -> list[int]:
    i = 0
    while i < len(stones):
        num = stones[i]
        if num == 0:
            stones[i] = 1
        elif is_even_digits(num):
            left_half, right_half = split_stone(num)
            stones[i] = left_half
            stones.insert(i + 1, right_half)
            i += 1
        else:
            stones[i] = multiply_stone(num, 2024)
        i += 1

    return stones


def multithread_simulation(stones: list[int], num_threads: int = 1) -> list[int]:
    chunk_size = len(stones) // num_threads
    chunks = [stones[i:i + chunk_size]
              for i in range(0, len(stones), chunk_size)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = list(executor.map(simulate_blink, chunks))

    # Flatten the list of results
    return [stone for chunk in results for stone in chunk]


# Use memoization
# Key: Tuple(stone, number of blinks completed on stone)
# Value: Resulting number of stones after that amount of blinks
memo = {}


# Recursively calculate the number of stones resulting from blinking a single stone
# Store and retrieve results from a memoization dictionary. This works because:
# - The number of stones resulting from a specific number of blinks
#   always remains the same
# - The result of each stone blinking is always independent from other stones
# It would be more succinct to remove all the memoization lines and simply add
# @lru_cache(maxsize=None)   -   But I chose to implement it myself
def stone_count(stone: int, blink: int, blink_total: int) -> int:
    if blink == blink_total:
        return 1

    # Check memoization dictionary
    key = (stone, blink)
    if key in memo:
        return memo[key]

    if stone == 0:
        zero_count = stone_count(1, blink + 1, blink_total)
        memo[(1, blink + 1)] = zero_count
        return zero_count

    if is_even_digits(stone):
        left_half, right_half = split_stone(stone)

        left_count = stone_count(left_half, blink + 1, blink_total)
        memo[(left_half, blink + 1)] = left_count

        right_count = stone_count(right_half, blink + 1, blink_total)
        memo[(right_half, blink + 1)] = right_count

        return left_count + right_count

    stone_multiple = multiply_stone(stone, 2024)
    mult_count = stone_count(stone_multiple, blink + 1, blink_total)
    memo[(stone_multiple, blink + 1)] = mult_count
    return mult_count


if __name__ == '__main__':
    # Part 1: Brute force blink simulation with pre-computed input and multithreading
    stones, cached_iters = parse_input('puzzle_input_iter_10_cached.txt'), 10
    for _ in range(P1_BLINK_ITERS - cached_iters):
        stones = multithread_simulation(stones, num_threads=len(stones))
    print(f'Part 1: {len(stones)}')

    # Part 2
    stones, count = parse_input('puzzle_input.txt'), 0
    for stone in stones:
        count += stone_count(stone, blink=0, blink_total=P2_BLINK_ITERS)
    print(f'Part 2: {count}')
