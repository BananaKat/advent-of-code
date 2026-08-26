# Written by Jason Phua
# on 04/12/2024
# Advent of Code 2024 - Day 4
# Solving https://adventofcode.com/2024/day/4
import numpy as np
import re


# Parse input file, returning a list of each line as a string
def parse_input(file: str) -> list[str]:
    with open(file) as file:
        return file.read().strip().split('\n')


# Part 1
# Flips word search array horizontally (reverse each line)
def flip_horizontally(word_search: list[str]) -> list[str]:
    return [line[::-1] for line in word_search]


# Rotates a word search array 90 degrees anti-clockwise
def rotate_word_search(word_search: list[str]) -> list[str]:
    word_search = np.array([list(line) for line in word_search])
    backwards = np.rot90(word_search)
    return [''.join(line) for line in list(backwards)]


# Search all diagonals for a target word
def search_diagonally(word_search: list[str], target_word: str) -> int:
    length = len(word_search)
    word_search = np.array([list(line) for line in word_search])
    rotated = np.rot90(word_search)
    target_word_reversed = target_word[::-1]

    count = 0
    for k in range(-length + 3, length - 2):
        diag = ''.join(np.diag(word_search, k))
        rotated_diag = ''.join(np.diag(rotated, k))

        count += len(re.findall(target_word, diag))
        count += len(re.findall(target_word_reversed, diag))
        count += len(re.findall(target_word, rotated_diag))
        count += len(re.findall(target_word_reversed, rotated_diag))

    return count


# Count occurences of a word in a word search array
# Words may appear horizontal, vertical, diagonal,
# written backwards, or even overlapping other words
def count_in_word_search(word_search: list[str], target_word: str) -> int:
    count = 0

    # Search left to right
    count += sum([len(re.findall(target_word, line))
                  for line in word_search])

    # Search right to left
    backwards = flip_horizontally(word_search)
    count += sum([len(re.findall(target_word, line))
                  for line in backwards])

    # Search top to bottom
    rotated = rotate_word_search(word_search)
    count += sum([len(re.findall(target_word, line))
                  for line in rotated])

    # Search bottom to top
    rotated_reversed = flip_horizontally(rotated)
    count += sum([len(re.findall(target_word, line))
                  for line in rotated_reversed])

    # Search diagonals
    count += search_diagonally(word_search, target_word)

    return count


# Part 2
# Check if an X-MAS character cross can be made in the word search
# given a centre coordinate to check
# - Assumes the given (x, y) coordinate holds the character 'A'
# - Assumes the given (x, y) coordinate is 1 within the outer edge
#   as otherwise, an adjacent corner would exceed the bounds of the array
def check_x_mas(word_search: list[str], y: int, x: int) -> bool:
    opposing_corners = {'M': 'S', 'S': 'M'}

    top_left = word_search[y - 1][x - 1]
    bottom_right = word_search[y + 1][x + 1]
    if bottom_right != opposing_corners.get(top_left):
        return False

    top_right = word_search[y - 1][x + 1]
    bottom_left = word_search[y + 1][x - 1]
    if bottom_left != opposing_corners.get(top_right):
        return False

    return True


# Return a count of X-MAS character crosses found in a word search
def count_x_mas_in_word_search(word_search: list[str]) -> int:
    count = 0

    # Search for 'A' characters 1 within the outer edge
    for i, line in enumerate(word_search[1:-1], start=1):
        for j, char in enumerate(line[1:-1], start=1):
            if char == 'A':
                count += check_x_mas(word_search, i, j)

    return count


if __name__ == '__main__':
    word_search = parse_input('puzzle_input.txt')
    xmas_occurences = count_in_word_search(word_search, 'XMAS')
    print(f'Part 1: {xmas_occurences}')

    x_mas_occurences = count_x_mas_in_word_search(word_search)
    print(f'Part 2: {x_mas_occurences}')
