# Advent Of Code 2023 - Day 19
# Solving https://adventofcode.com/2023/day/19
from pprint import pprint


# Part 1
def process_workflow(part_rating, part_rules):
    x, m, a, s = part_rating
    part = 'in'
    while part != 'A' and part != 'R':
        rules = part_rules[part]
        i = 0
        valid = False
        while i < len(rules) and not valid:
            cur_rule = rules[i]
            if ':' in cur_rule:
                expression, next_part = cur_rule.split(':')
                if eval(expression):
                    part = next_part
                    valid = True
            else:
                part = cur_rule
                valid = True
            i += 1
    return part


def sum_accepted_ratings(file):
    accepted_ratings_sum = 0
    part_rules = {}
    with open(file) as input_file:
        workflows, part_ratings = input_file.read().split('\n\n')
        workflows = [item[:-1].split('{') for item in workflows.split()]
        part_ratings = [item[1:-1].split(',') for item in part_ratings.split()]
    part_ratings = [[int(rating[2:]) for rating in part_rating]
                    for part_rating in part_ratings]
    for part, rules in workflows:
        part_rules[part] = rules.split(',')
    for part_rating in part_ratings:
        accepted = process_workflow(part_rating, part_rules)
        if accepted == 'A':
            accepted_ratings_sum += sum(part_rating)
    print(f'Accepted Parts Rating Sum = {accepted_ratings_sum}')
    return accepted_ratings_sum


sum_accepted_ratings("input.txt")
# Answer: 395382


# Part 2
def determine_ranges(rating, greater_than, value, ranges):
    new_ranges = []
    rating_index = 'xmas'.index(rating)
    for rng in ranges:
        rng = list(rng)
        low, high = rng[rating_index]
        if greater_than:
            low = max(low, value + 1)
        else:
            high = min(high, value - 1)
        rng[rating_index] = (low, high)
        new_ranges.append(tuple(rng))
    return new_ranges


def find_acceptable_combinations(part_rules, part, i):
    if part == 'R':
        return []
    if part == 'A':
        return [((1, 4000), (1, 4000), (1, 4000), (1, 4000))]
    rule = part_rules[part][i]
    if ':' not in rule:
        return find_acceptable_combinations(part_rules, rule, 0)
    condition, next_part = rule.split(':')
    greater_than = '>' in condition
    rating = condition[0]
    value = int(condition[2:])
    inverted_value = value + 1 if greater_than else value - 1
    # Find combinations when the condition is True
    if_condition_is_true = determine_ranges(
        rating, greater_than, value, find_acceptable_combinations(part_rules, next_part, 0))
    # Move to next part in the case where the condition is False
    i += 1
    if_condition_is_false = determine_ranges(
        rating, not greater_than, inverted_value, find_acceptable_combinations(part_rules, part, i))
    return if_condition_is_true + if_condition_is_false


def calculate_combinations(acceptable_ranges):
    total_combinations = 0
    for rng in acceptable_ranges:
        combinations = 1
        for low, high in rng:
            combinations *= high - low + 1
        total_combinations += combinations
    return total_combinations


def sum_acceptable_rating_combinations(file):
    part_rules = {}
    with open(file) as input_file:
        workflows = input_file.read().split('\n\n')[0]
        workflows = [item[:-1].split('{') for item in workflows.split()]
    for part, rules in workflows:
        part_rules[part] = rules.split(',')
    acceptable_ranges = find_acceptable_combinations(part_rules, 'in', 0)
    rating_combinations = calculate_combinations(acceptable_ranges)
    print(
        f'Number of Distinct Acceptable Rating Combinations = {rating_combinations}')
    return rating_combinations


sum_acceptable_rating_combinations("input.txt")
# Answer: 103557657654583
