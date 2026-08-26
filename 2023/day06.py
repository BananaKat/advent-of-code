# Advent Of Code 2023 - Day 6
# Solving https://adventofcode.com/2023/day/6


# Part 1
# millimetres_travelled() is reused in Part 2
def millimetres_travelled(race_duration, charge_held):
    distance = (race_duration - charge_held) * charge_held
    return distance


def multiply_winning_scenarios(file):
    with open(file) as input_file:
        multiplied_total = 1
        race_info = input_file.read().splitlines()
        race_durations = [int(i) for i in race_info[0].split()[1:]]
        max_distances = [int(i) for i in race_info[1].split()[1:]]
        # Iterate through races
        for i in range(len(race_durations)):
            winning_cases = 0
            # Iterate through options
            for j in range(race_durations[i]):
                distance = millimetres_travelled(race_durations[i], j)
                if distance > max_distances[i]:
                    winning_cases += 1
            multiplied_total *= winning_cases
    print(f'Multiplied Total of No. of Winning Cases = {multiplied_total}')
    return multiplied_total


multiply_winning_scenarios("puzzle_input.txt")
# Answer: 4811940


# Part 2
def find_winning_scenarios(file):
    with open(file) as input_file:
        winning_cases = 0
        race_info = input_file.read().splitlines()
        race_duration = int("".join(race_info[0].split()[1:]))
        distance_to_beat = int("".join(race_info[1].split()[1:]))
        for i in range(race_duration):
            distance = millimetres_travelled(race_duration, i)
            if distance > distance_to_beat:
                winning_cases += 1
    print(f'Total Amount of Winning Cases = {winning_cases}')
    return winning_cases


find_winning_scenarios("puzzle_input.txt")
# Answer: 30077773


# Mathematical Solution
"""
 The equation:
 distance = (race_duration - charge_held) * charge_held
 Is a QUADRATIC and can therefore be solved as such.
 Sample solution sourced from:
   https://www.reddit.com/r/adventofcode/comments/18bwe6t/comment/kc71csv/

 Notes:
   - zip() creates an iterator of tuples that pairs each item of the
     lists supplied in the arguments
   - The "*" operator unpacks a list and applies it to a function
   - So zip(*l) unpacks the list, l, and then zips them
   - E.g: zip(l) = zip([[1, 2, 3], [3, 4, 5]])
   - But: zip(*l) = zip([1, 2, 3], [3, 4, 5])
"""
import math


part_1_l = [[int(i) for i in l.strip().split()[1:]]
            for l in open("puzzle_input.txt").readlines()]
part_2_l = [[int("".join(l.strip().split()[1:]))]
            for l in open("puzzle_input.txt").readlines()]


def algebraically_evaluate_wins(l):
    w = 1
    for t, d in zip(*l):
        lf = (-t + (t * t - 4 * d) ** 0.5) / -2
        hf = (-t - (t * t - 4 * d) ** 0.5) / -2
        li = math.ceil(lf)
        hi = math.floor(hf)
        w *= hi - li + 1 - (lf == li) - (hf == hi)
    print(w)


algebraically_evaluate_wins(part_1_l)
algebraically_evaluate_wins(part_2_l)
