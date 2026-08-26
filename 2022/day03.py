# Advent Of Code 2022 - Day 3
# Solving https://adventofcode.com/2022/day/3


def split_compartments(rucksack):
    half = len(rucksack) // 2
    first_compartment = rucksack[:half]
    second_compartment = rucksack[half:]
    return first_compartment, second_compartment


def find_common_item(first_compartment, second_compartment):
    first_compartment = set(first_compartment)
    second_compartment = set(second_compartment)
    for i in first_compartment:
        if i in second_compartment:
            return i


def convert_priority(string):
    ordinate = ord(string)
    if ordinate <= 90:  # ASCII codes A-Z are 65-90 inclusive
        priority = ordinate - 38
    else:
        priority = ordinate - 96
    return priority


# Solve Part 1


def find_item_priority_sum(file):
    with open(file) as input_file:
        item_priority_sum = 0
        for line in input_file:
            rucksack = line.rstrip()
            first_compartment, second_compartment = split_compartments(
                rucksack)
            common_char = find_common_item(
                first_compartment, second_compartment)
            priority = convert_priority(common_char)
            item_priority_sum += priority
    print(f'Item Priority Sum = {item_priority_sum}')
    return sum


find_item_priority_sum("puzzle_input.txt")


# Solve Part 2


def find_common_badge(rucksack_1: set, rucksack_2: set, rucksack_3: set):
    for i in rucksack_1:
        if i in rucksack_2 and i in rucksack_3:
            return i


def find_group_priority_sum(file):
    group_priority_sum = 0
    with open(file) as input_file:
        group = {
            1: "",
            2: "",
            3: "",
        }
        count = 0
        for line in input_file:
            rucksack = line.rstrip()
            if count < 3:
                count += 1
            else:
                count = 1

            group[count] = sorted(set(rucksack))

            if count == 3:
                common_badge = find_common_badge(group[1], group[2], group[3])
                badge_priority = convert_priority(common_badge)
                group_priority_sum += badge_priority
    print(f'Group Priority Sum = {group_priority_sum}')
    return find_group_priority_sum


find_group_priority_sum("puzzle_input.txt")


print("Day 3 now finished!")
