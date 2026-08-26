# Written by Jason Phua
# on 17/12/2024
# Advent of Code 2024 - Day 17
# Solving https://adventofcode.com/2024/day/17
from typing import TypeAlias
from re import findall

Program: TypeAlias = list[int]
Registers: TypeAlias = dict[str, int]

# Instruction pointer:
# init = 0
# increase by 2 in each iteration
# halt program if IP >= len(program)
A = 'Register A'
B = 'Register B'
C = 'Register C'
IP = 'Instruction Pointer'
registers = {
    IP: 0,
    A: 0,
    B: 0,
    C: 0
}
IP_INCR = 2
# The computer is a 3-bit system which corresponds to octal numbers
OCTAL = 8

# Literal operands = itself
# Combo Operands:
# Combo operands 0 through 3 represent literal values 0 through 3.
# Combo operand 4 represents the value of register A.
# Combo operand 5 represents the value of register B.
# Combo operand 6 represents the value of register C.
# Combo operand 7 is reserved and will not appear in valid programs.
combo_operands = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: registers[A],
    5: registers[B],
    6: registers[C],
    7: None
}

# Instructions:
# adv (opcode 0) -> A division: A_register = A_register // (2 ^ combo_operand)
# bxl (opcode 1) -> B bitwise XOR: B_register = B_register XOR literal_operand
# bst (opcode 2) -> B mod 8: B_register = combo_operand % 8 (i.e. keep only lowest 3 bits)
# jnz (opcode 3) -> jump if not 0: if A_register == 0, do nothing, else jump (set instruction_ptr = lieral_operand, do not increment IP)
# bxc (opcode 4) -> legacy B bitwise XOR: B_register = B_register XOR C_register (read but ignore operand)
# out (opcode 5) -> output mod 8: print(combo_operand % 8)
# bdv (opcode 6) -> B division: B_register = A_register // (2 ^ combo_operand)
# cdv (opcode 7) -> C division: C_register = A_register // (2 ^ combo_operand)
print_args = []
instructions = {
    0: lambda op: registers.__setitem__(A, registers[A] // (2 ** combo_operands[op])),
    1: lambda op: registers.__setitem__(B, registers[B] ^ op),
    2: lambda op: registers.__setitem__(B, combo_operands[op] % 8),
    3: lambda op: registers.__setitem__(IP, op - IP_INCR) if registers[A] != 0 else None,
    4: lambda op: registers.__setitem__(B, registers[B] ^ registers[C]),
    5: lambda op: print_args.append(combo_operands[op] % 8),
    6: lambda op: registers.__setitem__(B, registers[A] // (2 ** combo_operands[op])),
    7: lambda op: registers.__setitem__(C, registers[A] // (2 ** combo_operands[op])),
}


# Batch execute output print
def output(print_args: list[int]) -> None:
    print(','.join(map(str, print_args)))


# Parse input file, modifying computer's registers returning program instructions
def parse_input(file: str) -> tuple[Registers, Program]:
    # Use RegEx to parse numerical values, given a string
    def get_num(info: str) -> int:
        NUM_PATTERN = r'[+-]?\d+'
        return int(*findall(NUM_PATTERN, info))

    with open(file) as file:
        register_info, program_info = file.read().strip().split('\n\n')
        reg_a, reg_b, reg_c = map(get_num, register_info.split('\n'))
        registers[A], registers[B], registers[C] = reg_a, reg_b, reg_c
        program = list(map(get_num, program_info.split(',')))

    return program


# After updating registers, update combo_operands to mirror its values
def update_combo_operands() -> None:
    combo_operands[4] = registers[A]
    combo_operands[5] = registers[B]
    combo_operands[6] = registers[C]


# Part 1
# Run the 3-bit computer with specified instructions
def run_program(program: Program) -> None:
    # Initialise combo_operands with initial register values
    update_combo_operands()

    # Halt condition: Computer attempts to read past program
    while registers[IP] < len(program) - 1:
        # Read program
        opcode = program[registers[IP]]
        operand = program[registers[IP] + 1]

        # Execute instruction
        instruction = instructions[opcode]
        instruction(operand)

        # Update instruction pointer and combo_operand values
        update_combo_operands()
        registers[IP] += IP_INCR


# Manually reverse engineered program
# Used to help determine a formula to validate quines
def reverse_engineered_program(a: int = 21539243, b: int = 0, c: int = 0) -> list[int]:
    out = []                        # Store output
    while a != 0:
        b = a % 8                   # bst 4
        b = b ^ 3                   # bxl 3
        c = a // (2 ** b)           # cdv 5
        b = b ^ 5                   # bxl 5
        a = a // 8                  # adv 3
        b = b ^ c                   # bxc 1
        out.append(b % 8)           # out 5
        continue                    # jnz 0
    output(out)
    return out


# Given a possible value, A, return the B value that would be printed out.
# We can write B as a function of A, where B is a 3-bit integer:
#
# B = A % 8 = A & 0b111,
# C = A >> (B ^ 3) = A >> ((A & 0b111) ^ 0b011)
# B = B ^ 5
# B = B ^ C
# B = B % 8 = B & 0b111
#
# So:
# B = ((A & 8) ^ 3 ^ C ^ 5)) & 8
#   = ((A & 0b111) ^ 0b011 ^ (A >> ((A & 0b111) ^ 0b011)) ^ 0b101) & 0b111
#
# Let, Factor = (A & 0b111) ^ 0b011
# Therefore, B = (Partial ^ (A >> Partial) ^ 0b101) & 0b111
def calculate_B(A: int) -> int:
    Factor = (A & 0b111) ^ 0b011
    return (Factor ^ (A >> Factor) ^ 0b101) & 0b111


# Given a possible value A, update A such that it can be calculated into B
# using the formula determined above
# Test A with the next 3 bits of A in the range [0, 7] (octal base)
# Update A by left bitshifting it by 3, then adding 3 potential new LSBs
def build_quines(previous_A: int, B: int) -> set[int]:
    valid_quines = set()
    for i in range(OCTAL):
        possible_A = (previous_A << 3) + i
        if calculate_B(possible_A) == B:
            valid_quines.add(possible_A)
    return valid_quines


# Part 2
# Find Quine (computer code that produces itself)
# Return the lowest positive value of A such that the program prints out itself
def find_quine(program: list[int]) -> int:
    quines = {0}
    for num in reversed(program):
        new_quines = set()
        for previous_A in quines:
            new_quines = new_quines.union(build_quines(previous_A, num))
        quines = new_quines

    return min(quines)


if __name__ == '__main__':
    program = parse_input('puzzle_input.txt')

    run_program(program)
    print('Part 1: ', end='')
    output(print_args)

    min_A_quine = find_quine(program)
    assert(program == reverse_engineered_program(a=min_A_quine))
    print(f'Part 2: {min_A_quine}')
