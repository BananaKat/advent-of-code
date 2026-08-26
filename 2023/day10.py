# Advent Of Code 2023 - Day 10
# Solving https://adventofcode.com/2023/day/10
from pprint import pprint
import copy


# Part 1
def find_S_pos(maze):
    for i in range(len(maze)):
        row = maze[i]
        for j in range(len(row)):
            pipe = maze[i][j]
            if pipe == 'S':
                return [i, j]


def find_next_valid_path(maze, pos, current_pipe, previous_pos):
    valid_up = '|7F'
    valid_down = '|LJ'
    valid_right = '-J7'
    valid_left = '-LF'
    can_go_up = 'S|LJ'
    can_go_right = 'S-LF'
    can_go_down = 'S|7F'
    can_go_left = 'S-J7'
    valid_directions = []
    y = pos[0]
    x = pos[1]
    # Check Up
    if y > 0 and current_pipe in can_go_up:
        adjacent_pipe = str(maze[y - 1][x])
        adjacent_pos = [y - 1, x]
        if adjacent_pipe in valid_up and adjacent_pos != previous_pos:
            valid_directions.append([y - 1, x])
    # Check Right
    if x < len(maze[y]) - 1 and current_pipe in can_go_right:
        adjacent_pipe = str(maze[y][x + 1])
        adjacent_pos = [y, x + 1]
        if adjacent_pipe in valid_right and adjacent_pos != previous_pos:
            valid_directions.append([y, x + 1])
    # Check Down
    if y < len(maze) - 1 and current_pipe in can_go_down:
        adjacent_pipe = str(maze[y + 1][x])
        adjacent_pos = [y + 1, x]
        if adjacent_pipe in valid_down and adjacent_pos != previous_pos:
            valid_directions.append([y + 1, x])
    # Check Left
    if x > 0 and current_pipe in can_go_left:
        adjacent_pipe = str(maze[y][x - 1])
        adjacent_pos = [y, x - 1]
        if adjacent_pipe in valid_left and adjacent_pos != previous_pos:
            valid_directions.append([y, x - 1])
    return valid_directions


def navigate_loop(maze, S_pos):
    maze[S_pos[0]][S_pos[1]] = 0  # Mark steps of initial pipe
    steps = 1
    valid_directions = find_next_valid_path(maze, S_pos, 'S', None)
    forwards = valid_directions[0]
    backwards = valid_directions[1]
    previous_forwards_pos = S_pos
    previous_backwards_pos = S_pos
    while forwards != backwards:
        # Go Forwards
        current_pipe = maze[forwards[0]][forwards[1]]
        maze[forwards[0]][forwards[1]] = steps
        temp = forwards
        forwards = find_next_valid_path(
            maze, forwards, current_pipe, previous_forwards_pos)[0]
        previous_forwards_pos = temp

        # Go Backwards
        temp = backwards
        current_pipe = maze[backwards[0]][backwards[1]]
        maze[backwards[0]][backwards[1]] = steps
        backwards = find_next_valid_path(
            maze, backwards, current_pipe, previous_backwards_pos)[0]
        previous_backwards_pos = temp
        steps += 1
    maze[forwards[0]][forwards[1]] = steps  # Mark steps of final pipe
    return steps


def find_furthest_point_in_loop(file):
    with open(file) as input_file:
        maze = [[*line][:-1] for line in input_file]
        S_pos = find_S_pos(maze)
        max_steps = navigate_loop(maze, S_pos)
    print(f'Furthest Point in Loop = {max_steps}')
    return max_steps


find_furthest_point_in_loop("puzzle_input.txt")
# Answer: 6690


# Part 2
def replace_S_in_maze(maze, S_pos):
    valid_directions = find_next_valid_path(maze, S_pos, 'S', None)
    directions = ''
    for direction in valid_directions:
        if direction[0] > S_pos[0]:
            directions += 'Down'
        if direction[0] < S_pos[0]:
            directions += 'Up'
        if direction[1] > S_pos[1]:
            directions += 'Right'
        if direction[1] < S_pos[1]:
            directions += 'Left'
    if 'Up' in directions:
        if 'Right' in directions:
            maze[S_pos[0]][S_pos[1]] = 'L'
        else:
            maze[S_pos[0]][S_pos[1]] = 'J'
    else:
        if 'Right' in directions:
            maze[S_pos[0]][S_pos[1]] = 'F'
        else:
            maze[S_pos[0]][S_pos[1]] = '7'
    return maze


def find_area(stepped_maze, maze):
    area = 0
    # FJ and L7 are essentially Vertical Bars
    directional_mapping = {
        'F': 'J',
        'L': '7',
        None: ''
    }
    for i in range(1, len(stepped_maze) - 1):
        row = stepped_maze[i]
        enclosed = 0
        previous_recorded = None
        for j in range(0, len(row)):
            pipe = row[j]
            # Use parity to determine direction of pipes
            # Only add Vertical Bars to parity counter
            #   - |, FJ, or L7
            # Odd = Enclosed
            # Even = Excluded
            if isinstance(pipe, int):
                if maze[i][j] == '|':
                    enclosed += 1
                elif maze[i][j] in 'J7':
                    if maze[i][j] in directional_mapping[previous_recorded]:
                        enclosed += 1
                if maze[i][j] in 'FL':
                    previous_recorded = maze[i][j]
            elif enclosed % 2 != 0:
                area += 1
    return area


def find_area_enclosed_by_loop(file):
    with open(file) as input_file:
        maze = [[*line][:-1] for line in input_file]
        stepped_maze = copy.deepcopy(maze)
        S_pos = find_S_pos(maze)
        # max_steps is never used but stores the return value
        # returned from reusing the navigate_loop function
        # from Part 1
        max_steps = navigate_loop(stepped_maze, S_pos)
        maze = replace_S_in_maze(maze, S_pos)
        area = find_area(stepped_maze, maze)
    print(f'Area Enclosed By Loop = {area}')
    return area


find_area_enclosed_by_loop("puzzle_input.txt")
# Answer: 525
