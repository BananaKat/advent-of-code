# Written by Jason Phua
# on 05/12/2024
# Advent of Code 2024 - Day 5
# Solving https://adventofcode.com/2024/day/5


# Parse input file, returning both a rules list and an updates list
def parse_input(file: str) -> tuple[list[tuple[str, str]], list[list[str]]]:
    with open(file) as file:
        page_numbers, updates = file.read().strip().split('\n\n')
        rules = [(before, after) for before, after in
                 (pair.split('|') for pair in page_numbers.split())]
        updates = [update.split(',') for update in updates.split('\n')]

    return rules, updates


# Checks if a given update list follows the ordering specified by the page number rules
def is_ordered_update(rules: list[tuple[str, str]], update: list[str]) -> bool:
    for before, after in rules:
        if before not in update or after not in update:
            continue

        before_index = update.index(before)
        after_index = update.index(after)
        if before_index > after_index:
            return False

    return True


# Sum the middle values of every update that correctly follows the page number rules
def sum_middle_ordered_updates(rules: list[tuple[str, str]], updates: list[list[str]]) -> int:
    total = 0

    for update in updates:
        ordered = is_ordered_update(rules, update)
        total += int(update[len(update) // 2]) * ordered

    return total


# Part 2
# Swaps two array elements by index; Alters the list in place
def swap(lst: list[int], i: int, j: int) -> None:
    lst[i], lst[j] = lst[j], lst[i]


# Reorder an update such that it follows the page number rules by
# swapping invalidly ordered values
def reorder_update(rules: list[tuple[str, str]], update: list[str]) -> list[str]:
    while not is_ordered_update(rules, update):
        for before, after in rules:
            if before not in update or after not in update:
                continue

            before_index = update.index(before)
            after_index = update.index(after)
            if before_index > after_index:
                swap(update, before_index, after_index)

    return update


# Finds updates that do not follow the page rules and reorders it,
# then find the sum of the middle values of the reordered updates
def sum_middle_reordered_updates(rules: list[tuple[str, str]], updates: list[list[str]]) -> int:
    total = 0

    for update in updates:
        ordered = is_ordered_update(rules, update)
        if not ordered:
            update = reorder_update(rules, update)
            total += int(update[len(update) // 2])

    return total


if __name__ == '__main__':
    rules, updates = parse_input('puzzle_input.txt')

    middle_sum = sum_middle_ordered_updates(rules, updates)
    print(f'Part 1: {middle_sum}')

    reordered_middle_sum = sum_middle_reordered_updates(rules, updates)
    print(f'Part 2: {reordered_middle_sum}')
