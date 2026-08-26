# Written by Jason Phua
# on 01/12/2024
# Advent of Code 2024 - Day 1
# Solving https://adventofcode.com/2024/day/1
from collections import defaultdict


# Parse input file and return seperated left and right lists of integers
def parse_input(file: str) -> tuple[list[int], list[int]]:
    left_list, right_list = [], []

    with open(file) as file:
        for line in file:
            ids = [int(id) for id in line.strip().split()]
            left_list.append(ids[0])
            right_list.append(ids[1])

    return left_list, right_list


# Part 1
# Finds the minimum distance between two lists
# Will mutate the input lists
def find_minimum_distance(left_list: list[int], right_list: list[int]) -> int:
    total_distance = 0

    # A better method would be to sort the two lists first, and then
    # sum the pair-wise distances; This brute-force method is fast enough
    while len(left_list) > 0 and len(right_list) > 0:
        left_min, right_min = min(left_list), min(right_list)
        distance = abs(left_min - right_min)
        total_distance += distance

        left_list.remove(left_min)
        right_list.remove(right_min)

    return total_distance


# Part 2
# Calculates a similarity value which is the sum of the calculation
# (number * number of occurances in right list) for each value in the left list
def calculate_similarity(left_list: list[int], right_list: list[int]) -> int:
    right_occurances = defaultdict(int)
    for num in right_list:
        right_occurances[num] += 1

    similarity_score = 0
    for num in left_list:
        similarity_score += num * right_occurances[num]

    return similarity_score


# Succinct solution taken from online
# Solves both part 1 and 2
# An even more succinct solution can be done using Numpy
def succinct_solution(file: str) -> None:
    with open(file) as file:
        data = [int(i) for i in file.read().split()]
        A, B = sorted(data[0::2]), sorted(data[1::2])
    print(sum(map(lambda a, b: abs(a - b), A, B)),
          sum(a * B.count(a) for a in A))


if __name__ == '__main__':
    left_list, right_list = parse_input('puzzle_input.txt')
    total_distance = find_minimum_distance(left_list, right_list)
    print(f'Part 1: {total_distance}')

    left_list, right_list = parse_input('puzzle_input.txt')
    similarity_score = calculate_similarity(left_list, right_list)
    print(f'Part 2: {similarity_score}')
