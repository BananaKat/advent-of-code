# Written by Jason Phua
# on 25/01/2026
# Advent of Code 2025 - Day 3
# Solving https://adventofcode.com/2025/day/3
'''
Part 1:
The highest joltage in a bank will always start with the highest start digit
E.g. 1, 2, 7, 9, 3, 4
The two highest numbers are 7 and 9, but 9X > 7X for any integer X.
So I can probably find the max by finding the largest non-tail value,
and then concatenating it with the largest value after the first digit.

Part 2:
Identical to part 1, but solving for 12 instead of just 2.
My solution solves for N amount of batteries using a greedy algorithm in O(n) time,
with a window with indexes bounded [head:tail], such that head < tail and
tail = battery_bank_length - remaining_battery_selections.
This ensures we always choose a max battery, such that there are enough
batteries left to make a total of exactly N selections.
'''


# Parse input file and return a list of battery banks as strings
def parse_input(filename: str) -> list:
    with open(filename) as file:
        return file.read().strip().split()

# Part 1
# Find max joltage where joltage is concatenation of two highest battery values
def find_total_joltage(bank: list) -> int:
    return sum(
        int(
            (max_non_tail := max(bank[:-1])) +
            max(bank[bank.index(max_non_tail) + 1:])
        )
        for bank in banks
    )

# Part 2
# Find max joltage where joltage is concatenation of twelve highest battery values
def find_total_overridden_joltage(bank: list) -> int:
    # Find the n-battery joltage of a single bank
    def joltage(bank: str, n: int) -> int:
        assert len(bank) >= n
        joltage = ''
        head = 0

        for remaining in reversed(range(0, n)):
            tail = len(bank) - remaining
            assert head < tail

            window = bank[head:tail]
            max_digit = max(window)
            head += (window.index(max_digit) + 1)

            joltage += max_digit

        return int(joltage)

    NUM_BATTERIES = 12
    return sum(joltage(bank, NUM_BATTERIES) for bank in banks)

if __name__ == '__main__':
    banks = parse_input('puzzle_input.txt')

    print(f'Part 1: {find_total_joltage(banks)}')
    print(f'Part 2: {find_total_overridden_joltage(banks)}')
