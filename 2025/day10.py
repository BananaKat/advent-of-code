# Written by Jason Phua
# on 04/02/2026
# Advent of Code 2025 - Day 10
# Solving https://adventofcode.com/2025/day/10
from functools import cache
import itertools
import z3


# Parse input file and return a list of machine manuals
def parse_input(filename: str) -> list[Machine]:
    machines = []
    with open(filename) as file:
        for line in file:
            raw_lights, *raw_buttons, raw_joltages = (
                part[1:-1] for part in line.split()
            )
            INDICATOR_ON = '#'
            light_req = [1 if l == INDICATOR_ON else 0 for l in raw_lights]
            buttons = [list(map(int, b.split(','))) for b in raw_buttons]
            joltage_req = list(map(int, raw_joltages.split(',')))

            machines.append(Machine(light_req, buttons, joltage_req))
        return machines


class Machine:
    # Linear objective function: Z = c1 * x1 + c2 * x2 + c3 * x3 ...
    # where index = x = which button, value = c = whether button toggles.
    '''
        Given: [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1)
        Button1 = 0 + 0x + 0x^2 + 1x^3
        Button2 = 0 + 1x + 0x^2 + 1x^3
        Button3 = 0 + 0x + 1x^2 + 0x^3
        Button4 = 0 + 0x + 1x^2 + 1x^3
        Button5 = 1 + 0x + 1x^2 + 0x^3
        Button6 = 1 + 1x + 0x^2 + 0x^3
        Target  = 0 + 1x + 1x^2 + 0x^3
    '''
    Vector = list[int]
    Matrix = list[Vector]

    def __init__(self, light_req: str, buttons: list[list[int]], joltage_req: list[int]):
        self.lights = light_req
        self.joltages = joltage_req
        assert len(self.lights) == len(self.joltages)
        self.buttons = self._to_matrix(buttons, len(self.lights))

    @staticmethod
    def _to_matrix(buttons: list[list[int]], n: int) -> Matrix:
        button_functions = []
        for button in buttons:
            b_fn = [0] * n
            for i in button:
                b_fn[i] = 1
            button_functions.append(b_fn)
        return button_functions

    # Part 1 driver
    # Given a series of lights, and buttons which toggle specified lights, count the
    # fewest button presses requried to turn the lights into the specified configuration
    @property
    def min_light_buttons(self) -> int:
        sols = gaussian_elimination_GF2(self.buttons, self.lights)
        return min(sum(s) for s in sols)

    # Part 2 driver
    @property
    def min_joltage_buttons(self) -> int:
        # return min_presses_z3(self.buttons, self.joltages)
        return min_presses_bifurcate(self.buttons, self.joltages)

    def __repr__(self):
        val1 = f'lights={self.lights}'
        val2 = f'buttons={self.buttons}'
        val3 = f'joltages={self.joltages}'
        return f'Machine({val1}, {val2}, {val3})'


# Part 1
# Gaussian elimination (row reduction) over GF(2), or Galois Field 2
# As our light/button states are represented as boolean states, we
# operate over the finite field of two elements (0 and 1)
def gaussian_elimination_GF2(buttons: Matrix, target: Vector) -> list[int]:
    # We convert our matrix rows to bitsets for bitwise row operations
    Bitset = int
    CoefficientMatrix = list[list[int]]
    ConstantVector = list[int]
    AugmentedMatrix = list[Bitset]

    # Cast a list of binary digits to an integer bitset
    def to_bitset(bin_int: Vector) -> Bitset:
        bin_str = ''.join(str(bit) for bit in bin_int)
        return int(bin_str, 2)

    # Given a matrix row, check if the k-th value is not zero
    def non_zero_kth(val: Bitset, nc: int, k: int) -> bool:
        if k + 1 > nc:
            return False
        return (val >> nc - (k + 1)) & 1 != 0

    # Given a matrix row, find the pivot column (first non-zero entry)
    def get_pivot_col(row: Bitset, nc: int) -> int:
        for c in range(nc - 1):
            if non_zero_kth(row, nc, c):
                return c
        return -1

    # Swap current row if it is non-leading
    # Return whether the given row is leading
    def swap_rows(A: list[Bitset], nr: int, nc: int, r: int, c: int) -> bool:
        if non_zero_kth(A[r], nc, c):
            # Current row is already a pivot
            return True

        for i in range(r + 1, nr):
            if non_zero_kth(A[i], nc, c):
                # Perform swap
                A[r], A[i] = A[i], A[r]
                return True
        # No pivot for column
        return False

    # Perform forward elimination from leading row, eliminating all
    # rows below pivot row r using pivot column c
    def forward_elimination(A: list[Bitset], nr: int, nc: int, r: int, c: int) -> None:
        for i in range(r + 1, nr):
            if non_zero_kth(A[i], nc, c):
                A[i] ^= A[r]

    # Check that the matrix is consistent (i.e. has a solution)
    # No solution exists if all coefficients in A are zero, but the corresponding
    # entry in b is non-zero
    def is_inconsistent(A: list[Bitset]) -> bool:
        # Since we store the augmented row in the form:
        # [a1 a2 a3 ... ak | b] as a Bitset, a row is inconsistent
        # if the row is [0 0 0 ... 0 | 1] = 1
        return any(row == 1 for row in A)

    # Solve for non-free variables for reduced-row-echelon form (RREF)
    def back_substitute(A: list[Bitset], free_map: dict[int, int], nc: int) -> list[int]:
        sol = [0] * (nc - 1)
        for fv_idx, val in free_map.items():
            sol[fv_idx] = val

        # Back-substitute from bottom row up
        for row in reversed(A):
            pivot = get_pivot_col(row, nc)
             # Discard rows of zeros
            if pivot == -1:
                continue

            # Pivot + sum(other_bits) = Target
            target = row & 1
            current_sum = 0
            for c in range(pivot + 1, nc - 1):
                if non_zero_kth(row, nc, c):
                    current_sum ^= sol[c]

            sol[pivot] = target ^ current_sum
        return sol

    def get_solutions(A: list[Bitset], nc: int) -> list[list[int]]:
        if is_inconsistent(A):
            return []

        # Determine free variables (columns with no pivots)
        pivot_cols = [get_pivot_col(row, nc) for row in A]
        free_vars = [c for c in range(nc - 1) if c not in pivot_cols]

        # Back substitute all combinations of free variable values
        solutions = []
        for choices in itertools.product([0, 1], repeat=len(free_vars)):
            free_map = dict(zip(free_vars, choices))
            solutions.append(back_substitute(A, free_map, nc))
        return solutions

    # Given the linear system with zero initial state, v_i = 0:
    #   v_i + sum_j(A_ij * x_j) = target_state (mod 2) => Ax = b (mod 2)
    # solve for x using Gaussian elimination.
    # Since we are in Base 2, we can pivot and eliminate with XOR
    def solve_system(A: CoefficientMatrix, b: ConstantVector) -> list[int]:
        # Convert linear problem: Ax = b, to augmented matrix
        aug: AugmentedMatrix = [to_bitset(i + [j]) for i, j in zip(A, b)]
        nr, nc = len(b), len(A[0]) + 1
        # Transform augmented matrix to row echelon form
        r = 0
        for c in range(nc - 1):
            if r >= nr:
                break
            # Attempt to place pivot into row r at column c
            if not swap_rows(aug, nr, nc, r, c):
                # No pivot for column
                continue
            # Eliminate all rows below pivot and advance to next row
            forward_elimination(aug, nr, nc, r, c)
            r += 1

        # Determine solutions with back substitution to RREF
        return get_solutions(aug, nc)

    b: ConstantVector = target
    A: CoefficientMatrix = [list(item) for item in zip(*buttons)]
    return solve_system(A, b)


# Part 2
# Given each button increments a specified 'joltage' counter, find
# the minimum button presses to reach the joltages requirement
'''
Similar to Part 1, we are essentially solving a linear system, this
time over the integer field, with the constraint of only integer solutions.

Some possible solutions would be to apply Integer Linear Programming (ILP)
or to write a modified Simplex solver (which typically operates on a set
of inequations) to work on a system of equations. These would both be
highly complicated though.

A simpler solution could be to reapply my Gaussian Elimination above, but
enumerate over every possible integer choice for each free variable. However,
since I wrote my Gaussian Elimination to only operate over GF(2), it would
need a significant rewrite, and I'm not bothered.

One ingenius method suggested on the AdventOfCode Reddit, suggests using
a recursive strategy with the solution for the parity of each counter
being already solvable with the Part 1 solution. This solution is cool,
and I'll probably have a go making it too.

The sledgehammer solution would be to just abuse the Z3 solver Python library.
'''

'''
For the solution below, we apply the Z3 satisfiability solver library.
To use it, we give it variables and constraints, then invoke the Optimization
module to find the minimum solution to the satisfiability problem.
The decision variables are the buttons:
    x_j = number of times button j is pressed,
    where x_j is a non-negative integer
We have the constraint:
    For each counter i, sum_j( A[i][j]x_j = b[i] ),
    where A is the matrix of bit-vectors for
    A[j][i] == 1 if button j affects counter i,
    and b is the target vector
And the optimisation objective:
    min( sum_j( x_j ) )

For an introduction to using Z3, check:
- https://theory.stanford.edu/~nikolaj/programmingz3.html
'''
def min_presses_z3(buttons: Matrix, joltages: Vector) -> int:
    A, n = buttons, len(buttons)
    b, m = joltages, len(joltages)
    opt = z3.Optimize()

    # Decision variables: x[j]: Int >= 0
    x = [z3.Int(f'x{j}') for j in range(n)]
    opt.add([x[j] >= 0 for j in range(n)])
    # Constraint: counter must reach joltages exactly
    opt.add(
        z3.Sum(A[j][i] * x[j] for j in range(n)) == b[i]
        for i in range(m)
    )
    # Objective: minimise sum of button presses
    opt.minimize(z3.Sum(x))

    # Solve and verify verdict sat (satisfying assignment exists)
    assert opt.check() == z3.sat

    model = opt.model()
    return sum(model[x[j]].as_long() for j in range(n))

'''
For the solution below, we use a recursive bifurcation strategy and,
we represent each counter by their parity (e.g. {3, 5, 4, 7} = [##.#]) to
reduce the Part 2 problem to a Part 1 analogy.
We also note the following observations from Part 1:
- Button press order doesn't matter (XOR is commutative).
- Pressing a button twice does nothing, so an optimal solution consists of
  pressing a button either 1 or 0 times, for each button.

Let f(w, x, y, z) be the button presses to reach joltages {w, x, y, z}.

Consider the example problem: (3) (1,3) (2) (2,3) (0,2) (0,1) {3, 5, 4, 7}
- We reduce our counters to parities (odd=1 and even=0), because subtracting
   the parity from the counters gives us only even joltage values.
   So reaching f(3, 5, 4, 7) = f(2, 4, 4, 6) + f(1, 1, 0, 1)
- The solution to f(2, 4, 4, 6) can be reduced to to: 2 * f(1, 2, 2, 3), as we can
   just press all buttons in the f(1, 2, 2, 3) solution twice.
   Note that this does not mean: f(2, 4, 4, 6) = 2 * f(1, 2, 2, 3), as there may
   exist a more optimal solution for f(2, 4, 4, 6).
   For example, consider the counter example: (0,1) (0,2) (1,2) {2,2,2}
   Which has optimal solution [1, 1, 1], whereas the halve {1, 1, 1} is an
   impossible configuration. Therefore, f(2, 2, 2) != 2 * f(1, 1, 1)
- Then we can repeat our method for the halved joltage path, separating both the
   parity target and the only-even target:
   f(1, 2, 2, 3) = f(0, 2, 2, 2) + f(1, 0, 0, 1) = 2 * f(0, 1, 1, 1) + f(1, 0, 0, 1)

Each time we calculate a solution to a parity problem, we need to subtract the button
presses from the total counter. For example, the solutions to f(1, 1, 0, 1) are:
(3) + (0, 1), (1, 3) + (2) + (0, 2), (2) + (2, 3) + (0, 1), (3) + (1, 3) + (2, 3) + (0, 2)
- Pressing (3) + (0, 1) => f(2, 4, 4, 6) + 2 = 2 * f(1, 2, 2, 3) + 2
- Pressing (1, 3) + (2) + (0, 2) => f(2, 4, 2, 6) = 2 * f(1, 2, 1, 3) + 3
And so on.

Essentially we are recursively brute forcing combinations of buttons, and applying
bifurcation (splitting into two subproblems) to cut down on the problem space.

Reference:
- - https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/
'''
def min_presses_bifurcate(buttons: Matrix, joltages: Vector) -> int:
    # Use immutable vector references for memoization
    IVector = tuple[int, ...]

    # Return the parity of counter vector, e.g. [3, 5, 4, 7] => [1, 1, 0, 1]
    def counter_parity(counter: IVector) -> IVector:
        return tuple([int(j % 2 != 0) for j in counter])

    # Given which buttons were pressed, return the reduced counter
    def map_presses(counter: IVector, presses: Vector) -> Vector:
        # Avoid repeated list comprehensions as they reallocate the list
        counter = list(counter)
        for i, press in enumerate(presses):
            if not press:
                continue
            row = buttons[i]
            for j in range(len(counter)):
                counter[j] -= row[j]
        return tuple(counter)

    # Halve the values of a counter
    def halve_counter(counter: IVector) -> IVector:
        return tuple([x // 2 for x in counter])

    # Wrap expensive call for caching
    @cache
    def get_candidates(parity: IVector) -> list[Vector]:
        return gaussian_elimination_GF2(buttons, parity)

    MAX = 1000000
    @cache
    def bifurcate(counter: IVector) -> int:
        # Base case: f(0, 0, 0, ...) = 0
        if all(x == 0 for x in counter):
            return 0

        parity = counter_parity(counter)
        candidates = get_candidates(parity)

        # Discard impossible configurations
        if any(x < 0 for x in counter) or not candidates:
            return MAX

        best = MAX
        for cand in candidates:
            next_counter = halve_counter(map_presses(counter, cand))
            best = min(best, 2 * bifurcate(next_counter) + sum(cand))
        return best

    counter = tuple(joltages)
    return bifurcate(counter)

if __name__ == '__main__':
    machines = parse_input('puzzle_input.txt')

    print(f'Part 1: {sum(m.min_light_buttons for m in machines)}')
    print(f'Part 2: {sum(m.min_joltage_buttons for m in machines)}')
