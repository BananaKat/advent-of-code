# Advent Of Code 2023 - Day 17
# Solving https://adventofcode.com/2023/day/17
from pprint import pprint


# Part 1
def find_path(city):
    heat_loss = 0
    node = [0, 0]
    end = [len(city), len(city[0])]
    return heat_loss


def least_heat_loss(file):
    with open(file) as input_file:
        city = [[int(i) for i in list(line.rstrip())] for line in input_file]
    print(city[-1][-1])
    heat_loss = find_path(city)
    print(f'Least Heat Loss = {heat_loss}')
    return heat_loss


least_heat_loss("test.txt")

# This problem requires Dijkstra
