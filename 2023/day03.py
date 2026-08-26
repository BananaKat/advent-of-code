# Advent Of Code 2023 - Day 3
# Solving https://adventofcode.com/2023/day/3


# Part 1
def find_special_chars(input_2D_array):
    found_special_chars_list = []
    special_characters = "!@#$%^&*()-+?_=,<>/"
    row_size = len(input_2D_array)
    for row in range(row_size):
        col_size = len(input_2D_array[row])
        for col in range(col_size):
            char = input_2D_array[row][col]
            if char in special_characters:
                coords = (row, col)
                found_special_chars_list.append(coords)
    return found_special_chars_list


# Reused function in Part 2
def isValidPos(row, col, row_size, col_size):
    if (row < 0 or col < 0 or row > row_size - 1 or col > col_size - 1):
        return False
    return True


def replace_adjacent_instances_in_row(col, col_size, current_row):
    current_value = current_row[col]
    current_row[col] = '.'
    adjacent = True
    forward_index = col + 1
    while adjacent and forward_index <= col_size - 1:
        if current_row[forward_index] == current_value:
            current_row[forward_index] = '.'
        else:
            adjacent = False
        forward_index += 1
    adjacent = True
    backwards_index = col - 1
    while adjacent and backwards_index >= 0:
        if current_row[backwards_index] == current_value:
            current_row[backwards_index] = '.'
        else:
            adjacent = False
        backwards_index -= 1
    return current_row


def sum_surrounding_values(coord_list, input_2D_array):
    value_sum = 0
    row_size = len(input_2D_array)
    for coord in coord_list:
        row = coord[0]
        row_up = row - 1
        row_down = row + 1
        col = coord[1]
        col_left = col - 1
        col_right = col + 1
        col_size = len(input_2D_array[row])
        row_above_col_size = len(input_2D_array[row - 1]) if row > 0 else 0
        row_below_col_size = len(
            input_2D_array[row + 1]) if row < row_size - 1 else 0

        # Check surrounding values
        if isValidPos(row_up, col_left, row_size, row_above_col_size):  # Top Left
            item = input_2D_array[row_up][col_left]
            if item.isdigit():
                value_sum += int(item)
                input_2D_array[row_up] = replace_adjacent_instances_in_row(
                    col_left, row_above_col_size, input_2D_array[row_up])
        if isValidPos(row_up, col, row_size, row_above_col_size):  # Top Middle
            item = input_2D_array[row_up][col]
            if item.isdigit():
                value_sum += int(item)
                input_2D_array[row_up] = replace_adjacent_instances_in_row(
                    col, row_above_col_size, input_2D_array[row_up])
        if isValidPos(row_up, col_right, row_size, row_above_col_size):  # Top Right
            item = input_2D_array[row_up][col_right]
            if item.isdigit():
                value_sum += int(item)
                input_2D_array[row_up] = replace_adjacent_instances_in_row(
                    col_right, row_above_col_size, input_2D_array[row_up])

        if isValidPos(row, col_left, row_size, col_size):  # Middle Left
            item = input_2D_array[row][col_left]
            if item.isdigit():
                value_sum += int(item)
                input_2D_array[row] = replace_adjacent_instances_in_row(
                    col_left, col_size, input_2D_array[row])
        if isValidPos(row, col_right, row_size, col_size):  # Middle Right
            item = input_2D_array[row][col_right]
            if item.isdigit():
                value_sum += int(item)
                input_2D_array[row] = replace_adjacent_instances_in_row(
                    col_right, col_size, input_2D_array[row])

        if isValidPos(row_down, col_left, row_size, row_below_col_size):  # Bottom Left
            item = input_2D_array[row_down][col_left]
            if item.isdigit():
                value_sum += int(item)
                input_2D_array[row_down] = replace_adjacent_instances_in_row(
                    col_left, row_below_col_size, input_2D_array[row_down])
        if isValidPos(row_down, col, row_size, row_below_col_size):  # Bottom Middle
            item = input_2D_array[row_down][col]
            if item.isdigit():
                value_sum += int(item)
                input_2D_array[row_down] = replace_adjacent_instances_in_row(
                    col, row_below_col_size, input_2D_array[row_down])
        if isValidPos(row_down, col_right, row_size, row_below_col_size):  # Bottom Right
            item = input_2D_array[row_down][col_right]
            if item.isdigit():
                value_sum += int(item)
                input_2D_array[row_down] = replace_adjacent_instances_in_row(
                    col_right, row_below_col_size, input_2D_array[row_down])

    return value_sum


def sum_part_numbers(file):
    with open(file) as input_file:
        part_number_sum = 0
        input_2D_array = []
        for line in input_file:
            input_row = []
            line = line.rstrip()
            start, end = 0, 1
            for i in range(len(line)):
                current = line[start:end]
                if not current.isdigit():
                    if len(current) > 1:
                        for i in range(len(current) - 1):
                            input_row.append(current[:-1])
                    input_row.append(line[end - 1])
                    start = end
                if end == len(line):  # Check end of line
                    input_row.append(current)
                end += 1
            input_2D_array.append(input_row)

        found_special_chars_list = find_special_chars(input_2D_array)
        part_number_sum = sum_surrounding_values(
            found_special_chars_list, input_2D_array)
    print(f'Part Number Sum = {part_number_sum}')
    return part_number_sum


sum_part_numbers("puzzle_input.txt")
# Answer: 550064


# Part 2
def find_potential_gears(input_2D_array):
    found_potential_gears_list = []
    potential_gear = "*"
    row_size = len(input_2D_array)
    for row in range(row_size):
        col_size = len(input_2D_array[row])
        for col in range(col_size):
            char = input_2D_array[row][col]
            if char == potential_gear:
                coords = (row, col)
                found_potential_gears_list.append(coords)
    return found_potential_gears_list


def find_surrounding_values(coord_list, input_2D_array):
    all_values = []
    row_size = len(input_2D_array)
    for coord in coord_list:
        adjacent_values = set()
        row = coord[0]
        row_up = row - 1
        row_down = row + 1
        col = coord[1]
        col_left = col - 1
        col_right = col + 1
        col_size = len(input_2D_array[row])
        row_above_col_size = len(input_2D_array[row - 1]) if row > 0 else 0
        row_below_col_size = len(
            input_2D_array[row + 1]) if row < row_size - 1 else 0

        # Check surrounding values
        if isValidPos(row_up, col_left, row_size, row_above_col_size):  # Top Left
            item = input_2D_array[row_up][col_left]
            if item.isdigit():
                adjacent_values.add(int(item))
        if isValidPos(row_up, col, row_size, row_above_col_size):  # Top Middle
            item = input_2D_array[row_up][col]
            if item.isdigit():
                adjacent_values.add(int(item))
        if isValidPos(row_up, col_right, row_size, row_above_col_size):  # Top Right
            item = input_2D_array[row_up][col_right]
            if item.isdigit():
                adjacent_values.add(int(item))

        if isValidPos(row, col_left, row_size, col_size):  # Middle Left
            item = input_2D_array[row][col_left]
            if item.isdigit():
                adjacent_values.add(int(item))
        if isValidPos(row, col_right, row_size, col_size):  # Middle Right
            item = input_2D_array[row][col_right]
            if item.isdigit():
                adjacent_values.add(int(item))

        if isValidPos(row_down, col_left, row_size, row_below_col_size):  # Bottom Left
            item = input_2D_array[row_down][col_left]
            if item.isdigit():
                adjacent_values.add(int(item))
        if isValidPos(row_down, col, row_size, row_below_col_size):  # Bottom Middle
            item = input_2D_array[row_down][col]
            if item.isdigit():
                adjacent_values.add(int(item))
        if isValidPos(row_down, col_right, row_size, row_below_col_size):  # Bottom Right
            item = input_2D_array[row_down][col_right]
            if item.isdigit():
                adjacent_values.add(int(item))
        all_values.append(list(adjacent_values))
    return all_values


def calculate_gear_ratio_sum(value_list):
    gear_ratio_sum = 0
    for surrounding_values in value_list:
        if len(surrounding_values) == 2:
            gear_ratio = surrounding_values[0] * surrounding_values[1]
            gear_ratio_sum += gear_ratio
    return gear_ratio_sum


def sum_gear_ratios(file):
    with open(file) as input_file:
        input_2D_array = []
        for line in input_file:
            input_row = []
            line = line.rstrip()
            start, end = 0, 1
            for i in range(len(line)):
                current = line[start:end]
                if not current.isdigit():
                    if len(current) > 1:
                        for i in range(len(current) - 1):
                            input_row.append(current[:-1])
                    input_row.append(line[end - 1])
                    start = end
                if end == len(line):  # Check end of line
                    input_row.append(current)
                end += 1
            input_2D_array.append(input_row)

        potential_gears_list = find_potential_gears(input_2D_array)
        surrounding_values = find_surrounding_values(
            potential_gears_list, input_2D_array)
        gear_ratio_sum = calculate_gear_ratio_sum(surrounding_values)
    print(f'Gear Ratio Sum = {gear_ratio_sum}')
    return gear_ratio_sum


sum_gear_ratios("puzzle_input.txt")
# Answer: 85010461
