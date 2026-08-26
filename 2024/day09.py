# Written by Jason Phua
# on 09/12/2024
# Advent of Code 2024 - Day 9
# Solving https://adventofcode.com/2024/day/9
from copy import deepcopy


# Parse input file, returning a string with the newline removed
def parse_input(file: str) -> str:
    with open(file) as file:
        return file.read().strip()


# Separate the disk map "dense format", which is composed of file lengths and
# free space lengths in alternating order
def separate_format_components(disk_map: str) -> tuple[list[int], list[int]]:
    file_lengths = [int(digit) for digit in disk_map[::2]]
    free_spaces = [int(digit) for digit in disk_map[1::2]]
    return file_lengths, free_spaces


# Part 1
# Fragment the disk space such that the files make up a single continguous block
# Then return the "filesystem checksum": sum(position * file_index)
def calculate_checksum(file_lengths: list[int], free_spaces: list[int]) -> int:
    # Pointers
    file_index_forw = 0
    file_index_back = len(file_lengths) - 1
    free_index = 0

    checksum = 0
    position = 0
    is_free_space = False

    while sum(file_lengths) > 0:
        if not is_free_space:
            checksum += position * file_index_forw
            position += 1

            file_lengths[file_index_forw] -= 1

        if is_free_space and free_spaces[free_index] > 0:
            checksum += position * file_index_back
            position += 1

            file_lengths[file_index_back] -= 1
            free_spaces[free_index] -= 1

            if file_lengths[file_index_back] <= 0:
                file_index_back -= 1

        # Switch is_free_space state if current file_length item is empty
        if not is_free_space and file_lengths[file_index_forw] <= 0:
            file_index_forw += 1
            is_free_space = free_index < len(free_spaces)

        # Switch is_free_space state if current free_space item is empty
        if is_free_space and free_spaces[free_index] <= 0:
            free_index += 1
            is_free_space = False

    return checksum


# Part 2
# Compact the disk space such that empty space is filled without fragmenting the files
# Then calculate the filesystem checksum
def checksum_defragmented(file_lengths: list[int], free_spaces: list[int]) -> int:
    # In this part, any file may be moved, creating new free spaces
    # Use the original file lengths as a reference to increment the position if
    # a file is moved and then its space is encountered
    previous_filesystem = deepcopy(file_lengths)

    checksum = 0
    position = 0
    is_free_space = False

    file_index_forw = 0
    free_index = 0

    while sum(file_lengths) > 0:
        if not is_free_space:
            if file_lengths[file_index_forw] > 0:
                checksum += position * file_index_forw
                position += 1
                file_lengths[file_index_forw] -= 1
            else:
                # For an empty file_length space, increment the position by
                # the length of the file that used to be there
                position += previous_filesystem[file_index_forw]

        # For free spaces, find the first file that fits in the space in descending
        # order of IDs (check largest ID first)
        file_fits_span = True
        if is_free_space and free_spaces[free_index] > 0:

            # Find file that fits in span
            file_index_back = len(file_lengths) - 1
            file_length = file_lengths[file_index_back]
            free_span_size = free_spaces[free_index]
            while file_length <= 0 or file_length > free_span_size:
                file_index_back -= 1
                if file_index_back < 0:
                    file_fits_span = False
                    break
                file_length = file_lengths[file_index_back]

            # Move file and add to checksum
            while file_fits_span and file_lengths[file_index_back] > 0:
                checksum += position * file_index_back
                position += 1

                file_lengths[file_index_back] -= 1
                free_spaces[free_index] -= 1

        # Switch is_free_space state if current file_length item is empty
        if not is_free_space and file_lengths[file_index_forw] <= 0:
            file_index_forw += 1
            is_free_space = free_index < len(free_spaces)

        # Switch is_free_space state if current free_space item is empty
        # or if no file is able to fit the free space
        if is_free_space and (free_spaces[free_index] <= 0 or not file_fits_span):
            position += free_spaces[free_index]
            free_index += 1
            is_free_space = False

    return checksum


if __name__ == '__main__':
    disk_map = parse_input('puzzle_input.txt')

    file_lengths, free_spaces = separate_format_components(disk_map)
    filesystem_checksum = calculate_checksum(file_lengths, free_spaces)
    print(f'Part 1: {filesystem_checksum}')

    file_lengths, free_spaces = separate_format_components(disk_map)
    defragmented_checksum = checksum_defragmented(file_lengths, free_spaces)
    print(f'Part 2: {defragmented_checksum}')
