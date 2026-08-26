# Written by Jason Phua
# on 13/12/2024
# Advent of Code 2024 - Day 13
# Solving https://adventofcode.com/2024/day/13
from typing import NamedTuple, TypeAlias
from re import findall


# Token costs to use a button
A_COST = 3
B_COST = 1

# Part 2 measurement shift
CONVERSION_ERROR_SHIFT = 10_000_000_000_000


# Define components of a vector
class Vector(NamedTuple):
    x: int
    y: int


# Set type hint type aliases and corresponding keys
Machine: TypeAlias = dict[str, Vector]
BUTTON_A = 'Button_A'
BUTTON_B = 'Button_B'
PRIZE = 'Prize'

Combo: TypeAlias = tuple[int, int]


# Parse input file, returning a list of machines with corresponding properties
def parse_input(file: str) -> list[Machine]:
    def to_vector(info: str) -> Vector:
        # Use RegEx to parse vector components
        NUM_PATTERN = r'[+-]?\d+'
        return Vector(*map(int, findall(NUM_PATTERN, info)))

    claw_machines = []
    with open(file) as file:
        for info in file.read().strip().split('\n\n'):
            vec_a, vec_b, prize = map(to_vector, info.split('\n'))
            machine: Machine = {BUTTON_A: vec_a, BUTTON_B: vec_b, PRIZE: prize}
            claw_machines.append(machine)

    return claw_machines


# Part 1
# Calculates the fewest tokens required to win all available prizes from the arcade machines
# Applies a factoring method to find combinations and sums prices of the cheapest combinations
def least_win_cost_p1(machines: list[Machine]) -> int:
    # Factor integer p into multiples of integers a and b
    # Simple iterative method* with a linear search over number multiples
    # * Degrades significantly for large P or A due to the linear search,
    #   Possible improvement would be to solve a Diophantine equation instead
    #   using the Extended Euclidean Algorithm
    def factor_multiples(p: int, a: int, b: int) -> list[Combo]:
        res = []
        num_a_multiples = p // a + 1
        for n1 in range(num_a_multiples):
            remainder = p - n1 * a
            if remainder % b == 0:
                n2 = remainder // b
                res.append((n1, n2))
        return res

    # Finds all combinations of a and b that make p for each axis
    # Then returns all combinations that match both axes
    def winning_combinations(machine: Machine) -> list[Combo]:
        px, ax, bx = machine[PRIZE].x, machine[BUTTON_A].x, machine[BUTTON_B].x
        win_x_axis = factor_multiples(px, ax, bx)
        py, ay, by = machine[PRIZE].y, machine[BUTTON_A].y, machine[BUTTON_B].y
        win_y_axis = factor_multiples(py, ay, by)

        return [combo for combo in win_x_axis if combo in win_y_axis]

    # Finds the combination with the lowest cost and returns the cost
    # Default the cost of unwinnable machines to 0
    def minimum_cost_solution(machine: Machine) -> int:
        combos = winning_combinations(machine)
        return min([n1 * A_COST + n2 * B_COST for n1, n2 in combos], default=0)

    return sum(minimum_cost_solution(machine) for machine in machines)


# Part 2
# Add a 'conversion error' to the prize co-ordinates as stated by the problem
def correct_conversion_errors(machines: list[Machine]) -> list[Machine]:
    corrected_machines = []
    for machine in machines:
        corrected_prize = Vector(
            machine[PRIZE].x + CONVERSION_ERROR_SHIFT,
            machine[PRIZE].y + CONVERSION_ERROR_SHIFT
        )
        corrected_machine: Machine = {
            BUTTON_A: machine[BUTTON_A],
            BUTTON_B: machine[BUTTON_B],
            PRIZE: corrected_prize
        }
        corrected_machines.append(corrected_machine)
    return corrected_machines


# Calculates the fewest tokens required to win all available prizes from the arcade machines
# Applies Cramer's Rule to find the cheapest combination and sums the prices
def least_win_cost_p2(machines: list[Machine]) -> int:
    # Apply Cramer's Rule, an explicit formula to solve systems of linear equations.
    # For the system of linear equations:
    #   {
    #     px = i * ax + j * bx,
    #     py = i * ay + j * by
    #   }
    # Cramer's Rule applies determinants to find that:
    #   x = det(Ax) / det(A),
    #   y = det(Ay) / det(A)
    # Where det(A) > 0 and:
    #   det(Ax) = [[px, bx], [py, by]] = px * by - bx * py
    #   det(Ay) = [[ax, px], [ay, py]] = ax * py - px * ay
    #   det(A)  = [[ax, bx], [ay, by]] = ax * by - bx * ay
    # Cramer's Rule is only valid for systems with a single unique solution.
    #
    # This approach is valid because for a system of linear equations with two variables,
    # there are only three different types of solutions:
    # - Independent system (exactly 1 solution) -> lines only intersect at one point
    # - Inconsistent system (0 solutions) -> lines are parallel and never intersect
    # - Dependent system (infinitely many solutions) -> lines are coincident (are the same)
    # From this, if a valid solution is found, we assume it is the only valid solution,
    # because otherwise the lines must be coincident, and therefore the solution would be
    # to return the number of button B presses (since B_COST < A_COST)
    #
    # Default the winning combination of unwinnable machines to (0, 0) which will result in
    # a token cost of 0 (after all, the only way to win is not play!)
    def cramers_rule(machine: Machine) -> Combo:
        px, ax, bx = machine[PRIZE].x, machine[BUTTON_A].x, machine[BUTTON_B].x
        py, ay, by = machine[PRIZE].y, machine[BUTTON_A].y, machine[BUTTON_B].y

        det_Ax = px * by - bx * py
        det_Ay = ax * py - px * ay
        det_A = ax * by - bx * ay

        if det_A != 0:
            n1 = det_Ax / det_A
            n2 = det_Ay / det_A
            return (int(n1), int(n2)) if n1 == int(n1) and n2 == int(n2) else (0, 0)

        return (0, 0)

    # Finds the combination with the lowest cost
    def minimum_cost_solution(machine: Machine) -> int:
        n1, n2 = cramers_rule(machine)
        return n1 * A_COST + n2 * B_COST

    return sum(minimum_cost_solution(machine) for machine in machines)


if __name__ == '__main__':
    machines = parse_input('puzzle_input.txt')
    win_cost_p1 = least_win_cost_p1(machines)
    print(f'Part 1: {win_cost_p1}')

    corrected_machines = correct_conversion_errors(machines)
    win_cost_p2 = least_win_cost_p2(corrected_machines)
    print(f'Part 2: {win_cost_p2}')

    # My Cramer's Rule implementation for Part 2 was actually initially solved
    # by hand on pen and paper.
    # Referring to it as Cramer's Rule sounds way more interesting then "did some
    # basic linear algebra", and it was interesting to learn about the existence
    # of an explicit formula to solve systems of linear equations where:
    # - The number of equations, and the number of unknowns are equal
    # - Only a single unique solution exists
    #
    # An interesting note is that the naive implementation of Cramer's Rule is
    # computationally ineffecient for systems with more then 3 equations as for
    # each system with N equations and N unknowns, N + 1 determinant computations
    # are required (effecient determinant computations have a complexity of O(n^3)).
    # Gaussian Elimination is the much preferred method to solve linear systems
    # because it:
    # - Is more computationally effecient for large systems
    # - Is numerically stable (floatng-point calculation errors are minimised)
    # But Cramer's Rule is still useful for its ease of use for small systems.
