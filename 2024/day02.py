# Written by Jason Phua
# on 02/12/2024
# Advent of Code 2024 - Day 2
# Solving https://adventofcode.com/2024/day/2


# Parse input file, returning a list of reports
# A report is a list of levels which are integers
def parse_input(file: str) -> list[list[int]]:
    with open(file) as file:
        reports = [list(map(int, report.strip().split()))
                   for report in file.readlines()]
    return reports


# Part 1
# Counts the number of safe reports: reports in which all levels are
# increasing or decreasing with a difference between 1 and 3 inclusive
def count_safe_reports_p1(reports: list[list[int]]) -> int:
    num_safe = 0

    for report in reports:
        is_safe = True
        if report[0] > report[1]:
            # Assume decreasing
            for i in range(len(report) - 1):
                if report[i] - report[i + 1] < 1 or report[i] - report[i + 1] > 3:
                    is_safe = False
        else:
            # Assume increasing
            for i in range(len(report) - 1):
                if report[i + 1] - report[i] < 1 or report[i + 1] - report[i] > 3:
                    is_safe = False

        if is_safe:
            num_safe += 1

    return num_safe


# Part 2
# Returns whether the difference between two adjacent levels is valid in
# the given slope direction
def valid_level_change(report: list[int], i: int, slope: str) -> bool:
    if slope == 'Increasing':
        return report[i + 1] - report[i] < 1 or report[i + 1] - report[i] > 3
    elif slope == 'Decreasing':
        return report[i] - report[i + 1] < 1 or report[i] - report[i + 1] > 3
    else:
        raise Exception('Invalid slope given')


# Returns whether the levels in a report are valid
def validate_report(report: list[int], slope: str, has_removed: bool) -> bool:
    for i in range(len(report) - 1):
        if valid_level_change(report, i, slope):
            return problem_dampener(report, i, slope) if not has_removed else False
    return True


# Attempts to validate a report by removing either the current level
# or the next level and returns whether it was successful
def problem_dampener(report: list[int], i: int, slope: str) -> bool:
    # Validate report with current level removed
    report_curr_removed = report[:i] + report[i + 1:]
    remove_curr = validate_report(report_curr_removed, slope, True)

    if i < len(report) - 2:
        # Validate report with next level removed
        report_next_removed = report[:i + 1] + report[i + 2:]
        remove_next = validate_report(report_next_removed, slope, True)
    else:
        # Validate report with last level removed
        report_next_removed = report[:-1]
        remove_next = validate_report(report_next_removed, slope, True)

    return remove_curr or remove_next


# Count the number of safe reports, validating with the problem dampener
# if necessary
def count_safe_reports_p2(reports: list[list[int]]) -> int:
    num_safe = 0

    for report in reports:
        is_safe_decreasing = validate_report(report, 'Decreasing', False)
        is_safe_increasing = validate_report(report, 'Increasing', False)

        if is_safe_increasing or is_safe_decreasing:
            num_safe += 1

    return num_safe


if __name__ == '__main__':
    reports = parse_input('puzzle_input.txt')

    num_safe = count_safe_reports_p1(reports)
    print(f'Part 1: {num_safe}')

    num_safe = count_safe_reports_p2(reports)
    print(f'Part 2: {num_safe}')
