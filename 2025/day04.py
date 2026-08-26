# Written by Jason Phua
# on 25/01/2026
# Advent of Code 2025 - Day 4
# Solving https://adventofcode.com/2025/day/4


# Parse input file and return a mutable 2D array of a grid
def parse_input(filename: str) -> list:
    with open(filename) as file:
        return [list(line) for line in file.read().strip().split()]


class Grid:
    PAPER_ROLL = '@'
    EMPTY = '.'

    def __init__(self, layout):
        self.layout = layout
        self.max_row = len(layout)
        self.max_col = len(layout[0])

    @staticmethod
    def is_paper_roll(element: str) -> bool:
        return element == Grid.PAPER_ROLL

    def valid_pos(self, row: int, col: int) -> bool:
        return 0 <= row < self.max_row and 0 <= col < self.max_col

    def is_accessible(self, row: int, col: int) -> bool:
        MAX_ADJ = 4
        adj_rolls = sum(
            Grid.is_paper_roll(self.layout[i][j])
            for i in range(row - 1, row + 2)
            for j in range(col - 1, col + 2)
            if not (i == row and j == col) and self.valid_pos(i, j)
        )
        return adj_rolls < MAX_ADJ

    def remove_roll(self, row: int, col: int) -> bool:
        if self.layout[row][col] == Grid.EMPTY:
            return False

        self.layout[row][col] = Grid.EMPTY
        return True


# Part 1
# Find number of accessible rolls, which are '@' characters surrounded
# by fewer than 4 adjacent '@' rolls
def num_accessible_rolls(grid: Grid) -> int:
    return sum(
        grid.is_paper_roll(col) and grid.is_accessible(i, j)
        for i, row in enumerate(grid.layout)
        for j, col in enumerate(row)
    )


# Part 2
# Count and remove accessible rolls until no more can be removed
def count_removeable_rolls(grid: Grid) -> int:
    def remove_accessible_rolls() -> int:
        return sum(
            grid.remove_roll(i, j)
            for i, row in enumerate(grid.layout)
            for j, col in enumerate(row)
            if grid.is_paper_roll(col) and grid.is_accessible(i, j)
        )

    count = 0
    while True:
        count += (removed := remove_accessible_rolls())
        if removed == 0:
            break
    return count


if __name__ == '__main__':
    grid = Grid(parse_input('puzzle_input.txt'))

    print(f'Part 1: {num_accessible_rolls(grid)}')
    print(f'Part 2: {count_removeable_rolls(grid)}')
