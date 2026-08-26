# Advent Of Code 2023 - Day 1
# Solving https://adventofcode.com/2023/day/1


# Part 1
def find_value(string):
    value = ['0', '0']
    front_pointer = 0
    first_digit_found = False
    back_pointer = len(string) - 1
    second_digit_found = False
    while first_digit_found is False or second_digit_found is False:
        if first_digit_found is False and string[front_pointer].isdigit():
            value[0] = string[front_pointer]
            first_digit_found = True
        if second_digit_found is False and string[back_pointer].isdigit():
            value[1] = string[back_pointer]
            second_digit_found = True
        front_pointer += 1
        back_pointer -= 1
    # print(int("".join(value)))
    return int("".join(value))


def sum_calibration_values(file):
    with open(file) as input_file:
        calibration_sum = 0
        for line in input_file:
            value = find_value(line.rstrip())
            calibration_sum += value
    print(f'Calibration Values Sum = {calibration_sum}')
    return calibration_sum


sum_calibration_values("puzzle_input.txt")
# Answer: 55712


# Part 2
def test_func(string):
    letter_digits = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
    }
    alpha_digits = ['one', 'two', 'three', 'four',
                    'five', 'six', 'seven', 'eight', 'nine']
    numerical_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    found = False
    counter = 0
    while found is False and counter < 9:
        if alpha_digits[counter] in string:
            print(letter_digits[alpha_digits[counter]])
            found = True
        if numerical_digits[counter] in string:
            print(numerical_digits[counter])
            found = True
        counter += 1
    if found is False:
        print(False)


# test_func("abconee")


def find_new_value(string):
    letter_digits = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
    }
    alpha_digits = ['zero', 'one', 'two', 'three', 'four',
                    'five', 'six', 'seven', 'eight', 'nine']
    numerical_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    value = ['0', '0']
    front_pointer = 1
    first_digit_found = False
    back_pointer = len(string) - 1
    second_digit_found = False

    while first_digit_found is False or second_digit_found is False:
        front_window = string[:front_pointer]
        back_window = string[back_pointer:]

        counter = 0
        while first_digit_found is False and counter <= 9:
            if alpha_digits[counter] in front_window:
                value[0] = letter_digits[alpha_digits[counter]]
                first_digit_found = True
            if numerical_digits[counter] in front_window:
                value[0] = numerical_digits[counter]
                first_digit_found = True
            counter += 1

        counter = 0
        while second_digit_found is False and counter <= 9:
            if alpha_digits[counter] in back_window:
                value[1] = letter_digits[alpha_digits[counter]]
                second_digit_found = True
            if numerical_digits[counter] in back_window:
                value[1] = numerical_digits[counter]
                second_digit_found = True
            counter += 1

        front_pointer += 1
        back_pointer -= 1

    # print(int("".join(value)))
    return int("".join(value))


def sum_new_calibration_values(file):
    with open(file) as input_file:
        new_calibration_sum = 0
        for line in input_file:
            value = find_new_value(line.rstrip())
            new_calibration_sum += value
    print(f'New Calibration Values Sum = {new_calibration_sum}')
    return new_calibration_sum


sum_new_calibration_values("puzzle_input.txt")
# Answer: 55413
