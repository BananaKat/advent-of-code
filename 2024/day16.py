# Written by Jason Phua
# on 16/12/2024
# Advent of Code 2024 - Day 16
# Solving https://adventofcode.com/2024/day/16
from typing import NamedTuple, TypeAlias
from collections import deque, defaultdict
from enum import Enum
import math
import heapq


# Define co-ordinates of a point on a grid
class Vertex(NamedTuple):
    x: int
    y: int


# Use trigonometric cardinal direction system
class Direction(Enum):
    NORTH = 90
    EAST = 0
    SOUTH = -90
    WEST = 180


# Map a direction to a vector (change in position)
DIRECTION_VECTOR_MAP = {
    Direction.NORTH: (0, -1),
    Direction.SOUTH: (0, 1),
    Direction.EAST: (1, 0),
    Direction.WEST: (-1, 0)
}
AdjacentTurn: TypeAlias = tuple[Direction | None, Direction | None]


# Maze properties
Maze: TypeAlias = list[str]
WALL = '#'
EMPTY = '.'
START = 'S'
END = 'E'

# Scoring parameters
MOVE_COST = 1
TURN_COST = 1000


# Parse input file, returning a 2D array of the Reindeer Maze
def parse_input(file: str) -> Maze:
    with open(file) as file:
        return [line.strip() for line in file.readlines()]


# Return the result requested in a problem part by solving the maze
# (finding lowest scored paths from Start to End nodes)
def solve_maze(maze: Maze, part: int) -> int:
    # Retrieve the start and end points of the maze
    def get_endpoints(maze: Maze) -> tuple[Vertex, Vertex]:
        for y, line in enumerate(maze):
            for x, char in enumerate(line):
                if char == START:
                    start = Vertex(x, y)
                if char == END:
                    end = Vertex(x, y)
        return start, end

    # Part 1
    # Return whether a given position is valid within map indexes and is empty (not wall)
    def valid_adj(maze: Maze, pos: Vertex) -> bool:
        map_height, map_width = len(maze), len(maze[0])
        in_bounds = pos.y >= 0 and pos.x >= 0 and pos.y < map_height and pos.x < map_width
        if not in_bounds:
            return False

        return maze[pos.y][pos.x] != WALL

    # Get the next vertex, given a direction
    def next_vertex(pos: Vertex, direction: Direction) -> Vertex:
        dx, dy = DIRECTION_VECTOR_MAP[direction]
        return Vertex(pos.x + dx, pos.y + dy)

    # Return adjacent vertices of a given position that are valid within the map
    # as a dictionary mapping from direction to next position
    def get_adjacent(maze: Maze, pos: Vertex) -> dict[Direction, Vertex]:
        return {dirn: adj for dirn in Direction if valid_adj(maze, adj := next_vertex(pos, dirn))}

    # Calculate a new score weight using the formula:
    # score = forward_cost + turn_cost * number_of_turns
    # Where forward_cost = 1, turn_cost = 1000, and a turn means changing direction by 90 degrees
    def calculate_score(prev_dir: Direction, next_dir: Direction) -> int:
        # Calculate the number of turns, taking the least turns
        TURN_DEGREE = 90
        num_turns = abs(next_dir.value - prev_dir.value) // TURN_DEGREE
        num_turns = num_turns % 2 if num_turns > 2 else num_turns
        return MOVE_COST + TURN_COST * num_turns

    # Dijkstra Single Source Shortest Path algorithm implementation with priority queue
    # Using a scoring function: timed_moved_forward + 1000 * number_of_turns
    def dijkstra_sssp(maze: Maze, start: Vertex, end: Vertex) -> int:
        scores = defaultdict(lambda: math.inf)
        scores[start] = 0

        # Priority Queue: (score, vertex, direction)
        pqueue = [(0, start, Direction.EAST)]
        while pqueue:
            score, vertex, direction = heapq.heappop(pqueue)

            for next_dir, adj in get_adjacent(maze, vertex).items():
                adj_score = scores[adj]
                next_score = score + calculate_score(direction, next_dir)

                if next_score < adj_score:
                    scores[adj] = next_score
                    heapq.heappush(pqueue, (next_score, adj, next_dir))

        return scores[end]

    # Part 2
    # Given a direction, return the two adjacent cardinal directions
    def turn_directions(maze: Maze, pos: Vertex, direction: Direction) -> AdjacentTurn:
        QUARTER_TURN = 90
        HALF_REVOLUTION = 180
        FULL_REVOLUTION = 360

        # Convert an angle in the range [-180, 180] to [0, 360]
        def normalise_angle(angle: int) -> int:
            return (angle + FULL_REVOLUTION) % FULL_REVOLUTION

        # Convert an angle in the range [0, 360] to [-90, 180]
        def denormalise_angle(angle: int) -> int:
            return angle if angle <= HALF_REVOLUTION else angle - FULL_REVOLUTION

        circ_clockwise = normalise_angle(direction.value - QUARTER_TURN)
        trig_clockwise = denormalise_angle(circ_clockwise)
        circ_anticlockwise = normalise_angle(direction.value + QUARTER_TURN)
        trig_anticlockwise = denormalise_angle(circ_anticlockwise)

        # Check if new direction faces a wall
        valid_dirn = get_adjacent(maze, pos).keys()
        adj_turns = [Direction(trig_anticlockwise), Direction(trig_clockwise)]
        return tuple(dirn if dirn in valid_dirn else None for dirn in adj_turns)

    # Use Breadth First Search to find all best paths, and store the best seats in a set
    def bfs_all_paths(maze: Maze, start: Vertex, end: Vertex) -> int:
        scores, best_score = defaultdict(lambda: math.inf), math.inf
        seats, path = {}, {start}

        # Queue: (score, vertex, direction, path)
        queue = deque()
        queue.append((0, start, Direction.EAST, path))
        while queue:
            score, vertex, dirn, path = queue.popleft()

            # Skip queue entry if an invalid direction is given, or the current
            # position already has a better score stored
            if dirn is None or score > scores[(vertex, dirn)] or score > best_score:
                continue
            scores[(vertex, dirn)] = score

            # Terminate paths that reach the END, and update best seats
            if maze[vertex.y][vertex.x] == END:
                if score < best_score:
                    best_score = score
                    seats = path
                elif score == best_score:
                    seats.update(path)
                continue

            # Move forward if valid tile (within map bounds and not a wall)
            next_pos = next_vertex(vertex, dirn)
            if valid_adj(maze, next_pos):
                new_path = path.copy()
                new_path.add(next_pos)
                queue.append((score + MOVE_COST, next_pos, dirn, new_path))

            # Turn left and right relatively on the spot and enqueue if not facing a wall
            left, right = turn_directions(maze, vertex, dirn)
            queue.append((score + TURN_COST, vertex, left, path.copy()))
            queue.append((score + TURN_COST, vertex, right, path.copy()))

        return len(seats)

    start, end = get_endpoints(maze)
    match part:
        case 1:
            return dijkstra_sssp(maze, start, end)
        case 2:
            return bfs_all_paths(maze, start, end)
        case _:
            raise Exception('Invalid problem part given.')


if __name__ == '__main__':
    maze = parse_input('puzzle_input.txt')

    lowest_score = solve_maze(maze, part=1)
    print(f'Part 1: {lowest_score}')

    num_seats = solve_maze(maze, part=2)
    print(f'Part 2: {num_seats}')
