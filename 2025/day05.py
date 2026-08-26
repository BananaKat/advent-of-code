# Written by Jason Phua
# on 27/01/2026
# Advent of Code 2025 - Day 5
# Solving https://adventofcode.com/2025/day/5
from dataclasses import dataclass
import bisect


'''
This exercise was pretty fun, but the main things I learnt here were actually
about Python classes and naming convention
_name -> indicates an interval/private identifier
name_ -> is a name avoiding a collision, e.g. id_ to avoid shadowing id()
@dataclass -> class primarily for storing data, automatically creates __init__, __repr__, __eq__
@property -> represents an attribute, without needing to make another getter
@staticmethod -> function belongs to class not an instance

Additionally I was reminded of the very simple optimisation of using binary search (BS).
I feel like I forget it all the time. Here we use the bisect module to perform BS for us!
bisect_left() finds the index to insert a number BEFORE existing values (i.e. arr[i] >= x)
bisect_right() finds the index to insert a number AFTER existing values (i.e. arr[i] > x)
We use bisect_right() as it returns the first index strictly greater-than x, and subtract 1
to find our candidate, whereas bisect_left() overshoot and point to an interval after x.
'''


@dataclass
class Interval:
    low: int
    high: int

    @property
    def size(self) -> int:
        return self.high - self.low + 1

    def includes(self, x: int) -> bool:
        return self.low <= x <= self.high


class IntervalSet:
    def __init__(self, intervals: list[Interval]):
        self.intervals = self._merge_overlapping(intervals)
        self.sorted_lows = [i.low for i in self.intervals]

    # Merge overlapping intervals leaving only disjointed ranges
    @staticmethod
    def _merge_overlapping(intervals: list[Interval]) -> list[Interval]:
        # Sorting by lower bounds gives invariant: prev.low <= next.low
        intervals.sort(key=lambda x: x.low)
        merged = [intervals[0]]
        for i in intervals[1:]:
            last = merged[-1]
            # [a, b] | [c, d] inclusive overlap if c <= b + 1
            if i.low <= last.high + 1:
                last.high = max(last.high, i.high)
            else:
                merged.append(i)
        return merged

    # Check membership with binary search over the merged intervals in O(log n)
    # Value x must belong to the interval with the greatest low <= x
    def contains(self, x: int) -> bool:
        idx = bisect.bisect_right(self.sorted_lows, x) - 1
        return idx >= 0 and self.intervals[idx].includes(x)

    # Sum interval sizes for Part 2
    def total_size(self) -> int:
        return sum(i.size for i in self.intervals)


# Parse input file and return a list of intervals, and a list of ids
def parse_input(filename: str) -> tuple[list[Interval], list[int]]:
    with open(filename) as file:
        intervals, ids = file.read().strip().split('\n\n')
        intervals = [map(int, i.split('-')) for i in intervals.split()]
        return [Interval(*i) for i in intervals], [int(id_) for id_ in ids.split()]


# Part 1
# Count number of 'fresh' ingredient IDs
# Fresh IDs fall into at least one given ID range
def count_fresh_ids(interval_set: IntervalSet, ids: list[int]) -> int:
    '''
    # Naive Solution: O(N * M) where N=len(ids), M=len(intervals)
    def is_fresh(intervals: list, value: int) -> bool:
        return any(i.includes(value) for i in intervals)
    return sum(is_fresh(intervals, i) for i in ids)
    '''
    return sum(interval_set.contains(id_) for id_ in ids)


# Part 2
# Find the total number of possible fresh IDs within the ID ranges
def total_fresh_ids(interval_set: IntervalSet) -> int:
    '''
    # Naive Solution: Gives MemoryError
    return len(set([r for i in intervals for r in range(i.low, i.high + 1)]))
    '''
    return interval_set.total_size()


if __name__ == '__main__':
    intervals, ids = parse_input('puzzle_input.txt')
    interval_set = IntervalSet(intervals)

    print(f'Part 1: {count_fresh_ids(interval_set, ids)}')
    print(f'Part 2: {total_fresh_ids(interval_set)}')
