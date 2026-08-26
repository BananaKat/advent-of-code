# Written by Jason Phua
# on 23/01/2026
# Advent of Code 2025 - Day 2
# Solving https://adventofcode.com/2025/day/2
'''
Part 1:
Lets list some invalid ids!
2-digits: 11, 22, 33, 44, 55, 66, 77, 88, 99
3-digits: 111, 222, 333, 444, 555, 666, 777, 888, 999
4-digits: 1010, 1111, 1212, 1313, 1414, ..., 1919,
          2020, 2121, 2222, 2323, 2424, ..., 2929,
          3030, 3131, 3232, 3333, 3434, ..., 3939,...
5-digits: 11111, 22222, 33333, 44444, 55555, 66666, 77777, 88888, 99999
I think:
Odd digits and less than 4 digits always have 9 invalid IDs
Even digits have some permutations amount of invalid IDs

Consider a 4-digit number with digits A, B, C, D:
A has 9 choices (1-9),
B has 10 choices (0-9),
C and D don't matter, as C=A and D=B.
Similarly with a 6-digit number ABCDEF:
A=9 choices, B=10 choices, C= 10 choices, disregard D, E, F.
So the total choices = 9 * 10 ^ (digits // 2 - 1)

For the range abcd-efgh, we want to find permutations of ABCD such that:
abcd < ABCD < efgh
E.g. 1234-8866, a valid choice would be 6767, but an invalid one is 1212 or 8787
For our choices, we only consider permuting A and B, so we have ranges:
max(a, e) <= A <= min(c, g) and max(b, f) <= B <= min(d, h)
which would give us choices:
A has min(c, g) - max(a, e) + 1 choices, where a>0, e>0
B has min(d, h) - max(b, f) + 1 choices

What happens if we have a range with different digits for each bound?
ab-cdef is the same as [ab-99] | [100-199] | [1000-cdef]
I think it would be worth it to pre-process our ranges such that bounds match digits...
'''

'''
It turns out I misunderstood the question for part 1.
I need to find and SUM all invalid IDs.
For this, a bruteforce solution works just fine.
Similarly, a bruteforce solution works fine for part 2.

A more complicated but faster solution would be to
'''


# Parse input file and return a list of ranges stored as tuples
def parse_input(filename: str) -> list:
    with open(filename) as file:
        ranges = [pair.split('-') for pair in file.read().strip().split(',')]
        return [tuple(map(int, pair)) for pair in ranges]


# Part 1
# Sum the invalid IDs within each range
# Invalid IDs are made only of a sequence of digits repeated twice
# e.g. 55, 6464, 123123
def sum_invalid_ids(ranges: list) -> int:
    def halves(n: str) -> tuple[str, str]:
        return n[:len(n) // 2], n[len(n) // 2:]

    def equal(a: str, b: str) -> bool:
        return a != '' and b != '' and a == b

    return sum(
        i for x, y in ranges
        for i in range(x, y + 1)
        if equal(*halves(str(i)))
    )

# Part 2
# Sum the repdigits within a range
# A repdigit is a natural number made up of repeated sequences of digits
def sum_repdigits(ranges: list) -> int:
    def split_chunks(s: str, l: int) -> list[str]:
        return [s[i:i+l] for i in range(0, len(s), l)]

    def is_repdigit(n: str) -> bool:
        for i in range(1, len(n)):
            if len(set(split_chunks(n, i))) == 1:
                return True
        return False

    return sum(
        i for x, y in ranges
        for i in range(x, y + 1)
        if is_repdigit(str(i))
    )


if __name__ == '__main__':
    ranges = parse_input('puzzle_input.txt')

    print(f'Part 1: {sum_invalid_ids(ranges)}')
    print(f'Part 2: {sum_repdigits(ranges)}')
