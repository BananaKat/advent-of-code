# Advent Of Code 2023 - Day 9
# Solving https://adventofcode.com/2023/day/9
from pprint import pprint


# Part 1
def find_sequences(history):
    differences = [history]
    additional_sequences = 0
    # Iterate while not all list items are equal
    while len(set(differences[additional_sequences])) > 1:
        sequence = differences[additional_sequences]
        next_sequence = [sequence[i] - sequence[i - 1]
                         for i in range(1, len(sequence))]
        differences.append(next_sequence)
        additional_sequences += 1
    return differences


def sum_next_extrapolated_histories(file):
    extrapolated_sum = 0
    with open(file) as input_file:
        for line in input_file:
            history = [int(i) for i in line.rstrip().split()]
            differences = find_sequences(history)
            extrapolated_sum += sum([sequence[-1] for sequence in differences])
    print(f'Extrapolated Next Histories Sum = {extrapolated_sum}')
    return extrapolated_sum


sum_next_extrapolated_histories("puzzle_input.txt")
# Answer: 2043183816


# Part 2
def extrapolate_previous_term(differences):
    previous_term = 0
    for sequence in reversed(differences):
        previous_term = sequence[0] - previous_term
    return previous_term


def sum_previous_extrapolated_histories(file):
    extrapolated_sum = 0
    with open(file) as input_file:
        for line in input_file:
            history = [int(i) for i in line.rstrip().split()]
            differences = find_sequences(history)
            previous_term = extrapolate_previous_term(differences)
            extrapolated_sum += previous_term
    print(f'Extrapolated Previous Histories Sum = {extrapolated_sum}')
    return extrapolated_sum


sum_previous_extrapolated_histories("puzzle_input.txt")
# Answer: 1118
