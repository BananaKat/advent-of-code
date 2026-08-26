# Advent Of Code 2023 - Day 4
# Solving https://adventofcode.com/2023/day/4
from collections import defaultdict


# Part 1
def match_lists(winning_list, owned_list):
    matching = 0
    for num in owned_list:
        if num in winning_list:
            matching += 1
    return matching


def calculate_points(matching):
    if matching == 0:
        return 0
    return 2**(matching - 1)


def total_points(file):
    with open(file) as input_file:
        total_points = 0
        game_number = 1
        for line in input_file:
            line = line.rstrip().removeprefix(
                f'Card {game_number}: ').split('|')
            winning_list = line[0].split()
            owned_list = line[1].split()
            matching = match_lists(winning_list, owned_list)
            total_points += calculate_points(matching)
            game_number += 1
    print(f'Total Points = {total_points}')
    return total_points


total_points("puzzle_input.txt")
# Answer: 15205


# Part 2
def find_won_cards(game_number, winning_list, owned_list):
    won_cards = []
    matching = 1
    for num in owned_list:
        if num in winning_list:
            won_cards.append(str(matching + game_number))
            matching += 1
    return won_cards


def total_scratchcards(file):
    with open(file) as input_file:
        game_number = 1
        scratchcards = {}
        card_copies = defaultdict(lambda: 1)
        for line in input_file:
            line = line.rstrip().removeprefix(
                f'Card {game_number}: ').split('|')
            card_copies[str(game_number)] += 0
            winning_list = line[0].split()
            owned_list = line[1].split()
            won_cards = find_won_cards(game_number, winning_list, owned_list)
            scratchcards[str(game_number)] = won_cards
            for card in won_cards:
                card_copies[card] += 1 * card_copies[str(game_number)]
            game_number += 1
        total_scratchcards = sum(card_copies.values())
    print(f'Total Scratchcards = {total_scratchcards}')
    return total_scratchcards


total_scratchcards("puzzle_input.txt")
# Answer: 6189740


# 'ALLEZ CUISINE' Challenge: Code Golf (Shortest Code)

# Part 1 Only
"""
print(sum(round(2**(len([i for i in l.rstrip().split('|')[1].split() if i in l.rstrip().split('|')[0].split()]) - 1)) for l in open('puzzle_input.txt')))
"""

# Part 2 Only
"""
def f(k,i):s[str(int(k)+i)][1]+=1*s[k][1]
s={l.split(':')[0].split()[1]:[len([i for i in l.rstrip().split('|')[1].split() if i in l.rstrip().split('|')[0].split()]),1] for l in open("puzzle_input.txt")}
[[f(k,i) for i in range(1, s[k][0]+1)] for k in s.keys()]
print(sum(i[1] for i in s.values()))
"""

# One-line solution to both Part 1 and Part 2
# The exec() function calls the above code but uses '\n' to make next line
exec("print(sum(round(2**(len([i for i in l.rstrip().split('|')[1].split() if i in l.rstrip().split('|')[0].split()])-1)) for l in open('puzzle_input.txt')))\ndef f(k,i):s[str(int(k)+i)][1]+=1*s[k][1]\ns={l.split(':')[0].split()[1]:[len([i for i in l.rstrip().split('|')[1].split() if i in l.rstrip().split('|')[0].split()]),1] for l in open('puzzle_input.txt')}\n[[f(k,i) for i in range(1,s[k][0]+1)] for k in s.keys()]\nprint(sum(i[1] for i in s.values()))\n")
