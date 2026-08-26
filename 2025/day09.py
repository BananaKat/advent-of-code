# Written by Jason Phua
# on 01/02/2026
# Advent of Code 2025 - Day 9
# Solving https://adventofcode.com/2025/day/9
from shapely.geometry import Polygon
from shapely.prepared import prep
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from warnings import warn


# Frozen = Immutable
# Order automatically adds comparison
# Slots stores attributes in fixed offsets (like C structs)
# removes __dict__, and forbids new attributes
@dataclass(frozen=True, order=True, slots=True)
class Vertex:
    x: int
    y: int

    # Given opposite point, calculate rectilinear area
    def rect_area(self, other: Vertex) -> int:
        length = abs(self.x - other.x) + 1
        width = abs(self.y - other.y) + 1
        return length * width


# Parse input file and return a list red tile coordinates
def parse_input(filename: str) -> list[Vertex]:
    with open(filename) as file:
        return [Vertex(*map(int, line.strip().split(','))) for line in file]


# Part 1
# Return the max area of a rectangle whose corners are two red tiles
def largest_rectangle(red_tiles: list[Vertex]) -> int:
    # Find the areas for every combination of tiles
    areas = [a.rect_area(b) for a, b in combinations(red_tiles, 2)]
    return max(areas)


# Part 2
# Find the area of the largest inscribed rectangle within the composite
# shape with points defined by the red tiles
# It is not guaranteed that the shape is convex
'''
Included are two different solutions:
* Use Python's Shapely library (~3.5s)
    Switching from Geometry.within to PreparedGeometry.contains
    speeds us up to ~1.8s
* Check point inclusion with Ray Casting algorithm and no
  orthogonal intersection between rectangle and polygon (~14.1s)
    By bucketing edges by y-value, we significantly reduce the edges
    checked by the ray casting algorithm, down to an incredible ~526ms

I also tried using a Maximal rectangle in histogram algorithm,
since the polygon is orthogonal and hole-free, then for any row y,
the inside of the polygon is a union of disjoint x-intervals.
Then we find the largest axis-aligned rectangle fully contained in
a set of per-row x-intervals.
However, after coding the whole thing up, it finds the largest rectangle,
but does not respect the fact that our rectangle must select two points
from the list as opposite corners.
Also without x-coordinate compression, the unit-based array is massive.
'''
# Solution 1 with Python libraries
Area = tuple[int, Vertex, Vertex]
def largest_rect_in_poly(areas: list[Area], red_tiles: list[Vertex]) -> int:
    poly = prep(Polygon(shell=[(r.x, r.y) for r in red_tiles]))
    for area, u, v in sorted(areas, reverse=True):
        a, c = (u.x, u.y), (v.x, v.y)
        b, d = (u.x, v.y), (v.x, u.y)
        rect = Polygon(shell=[a, b, c, d])
        if (poly.contains(rect)):
            return area
    return 0

# Solution 2 with ray casting
Edge = tuple[Vertex, Vertex]
class PolygonIntersect:
    YBuckets = dict[int, list[Edge]]
    def __init__(self, edges: list[Edge]):
        self.edges = edges
        yb_h, yb_v = self._build_y_buckets(edges)
        self.horizontal_by_y = yb_h
        self.vertical_by_y = yb_v

    # Precompute edges that scan across y-value for ray casting
    # As a point can only intersect an edge that shares its y-value
    @staticmethod
    def _build_y_buckets(edges: list[Edge]) -> (YBuckets, YBuckets):
        horizontal_by_y = defaultdict(list)
        vertical_by_y = defaultdict(list)
        for u, v in edges:
            if u.y == v.y:
                # Horizontals edges only span a single y-value
                horizontal_by_y[u.y].append((u, v))
                continue
            # Keep half-open rule consistent: Include start, exclude end
            y1, y2 = sorted((u.y, v.y))
            for y in range(y1, y2):
                vertical_by_y[y].append((u, v))
        return horizontal_by_y, vertical_by_y

    # Check if a point lies inside an edge
    @staticmethod
    def _in_edge(edge: Edge, point: Vertex) -> bool:
        u, v = edge
        if u.y == v.y == point.y:
            return min(u.x, v.x) <= point.x <= max(u.x, v.x)
        if u.x == v.x == point.x:
            return min(u.y, v.y) <= point.y <= max(u.y, v.y)
        return False

    # Check if a ray projected right from a point intersects with edge
    @staticmethod
    def _intersects_edge(edge: Edge, point: Vertex) -> bool:
        u, v = edge
        # Edges are either horizontal or vertical, discard horizontal
        if u.y == v.y:
            return False
        # Half-open rule: Include the start, exclude the end
        if not (min(u.y, v.y) <= point.y < max(u.y, v.y)):
            return False
        # Ray cast check
        return point.x < max(u.x, v.x)

    # Ray Casting algorithm to check if point exists in composite shape
    # If intersections are odd, then the point is inside the shape
    def _includes_point(self, point: Vertex) -> bool:
        # Check edge membership in horizontal edges
        for hori in self.horizontal_by_y.get(point.y, ()):
            if self._in_edge(hori, point):
                return True
        # Check edge membership and apply ray casting for verticals
        intersections = 0
        for vert in self.vertical_by_y.get(point.y, ()):
            if self._in_edge(vert, point):
                return True
            # Only keep intersection parity
            intersections ^= self._intersects_edge(vert, point)
        return intersections % 2 != 0

    # Check if two edges orthogonally intersect
    # Overlaps are strictly interior (boundary contact is not an intersection)
    @staticmethod
    def _orthogonal_intersect(x: Edge, y: Edge) -> bool:
        (a, b), (c, d) = x, y
        # x vertical, y horizontal
        if a.x == b.x and c.y == d.y:
            return (
                min(c.x, d.x) < a.x < max(c.x, d.x) and
                min(a.y, b.y) < c.y < max(a.y, b.y)
            )
        # x horizontal, y vertical
        if a.y == b.y and c.x == d.x:
            return (
                min(a.x, b.x) < c.x < max(a.x, b.x) and
                min(c.y, d.y) < a.y < max(c.y, d.y)
            )
        return False

    # Given opposite corners of a rectangle, check if its within a polygon
    def rect_within_poly(self, a: Vertex, c: Vertex) -> bool:
        # Given (x1, y1) and (x2, y2), swap to find the
        # other two corners: (x1, y2) and (x2, y1)
        b, d = Vertex(a.x, c.y), Vertex(c.x, a.y)
        for p in (a, b, c, d):
            if not self._includes_point(p):
                return False

        rect_edges = [(a, b), (b, c), (c, d), (d, a)]
        for re in rect_edges:
            # Since edges can span large intervals, it's faster to check
            # each edge, rather than filtering by value or direction
            for pe in self.edges:
                if self._orthogonal_intersect(re, pe):
                    return False

        return True


# Attempted solution 3
# 1. Compute intervals per row
# 2. Convert rows into column heights
# 3. Run largest rectangle in histogram per row
class IntervalHistogram:
    Interval = tuple[int, int]
    PerRowIntervals = dict[int, Interval]

    def __init__(self, vertices: list[Vertex], edges: list[Edge]):
        warn("Invalid algorithm")
        self.vertices = vertices
        self.intervals = self._compute_per_row_interval(edges)

    @staticmethod
    def _compute_per_row_interval(edges: list[Edge]) -> PerRowIntervals:
        rows = defaultdict(list)
        for (u, v) in edges:
            # Discard non-vertical edges
            if u.x != v.x:
                continue
            y1, y2 = sorted([u.y, v.y])
            for y in range(y1, y2 + 1):
                rows[y].append(u.x)

        intervals = dict()
        for y, xs in rows.items():
            xs.sort()
            intervals[y] = (xs[0], xs[-1])
        return intervals

    # Given n non-negative integers representing a histogram's bar height,
    # where each bar width is 1, find the largest area
    # - https://www.youtube.com/watch?v=zx5Sw9130L0
    @staticmethod
    def _largest_rectangle_histogram(heights: list[int]) -> int:
        stack = []
        best = 0

        for i, h in enumerate(heights):
            start = i
            while stack and stack[-1][1] > h:
                idx, height = stack.pop()
                best = max(best, height * (i - idx))
                start = idx
            stack.append((start, h))

        for i, h in stack:
            best = max(best, h * (len(heights) - i))
        return best

    def max_rectangle(self) -> int:
        warn("Massive unit-spaced array")
        best = 0
        cols = max([i[1] for i in self.intervals.values()]) + 1
        heights = [0] * cols

        for y in sorted(self.intervals):
            # Determine which columns are inside current histogram
            inside = [False] * cols
            x1, x2 = self.intervals[y]
            for i in range(x1, x2 + 1):
                inside[i] = True

            for i in range(cols):
                if inside[i]:
                    heights[i] += 1
                else:
                    heights[i] = 0
            best = max(best, self._largest_rectangle_histogram(heights))
        return best


# Part 2 driver
def largest_inscribed_rectangle(red_tiles: list[Vertex]) -> int:
    areas = [(u.rect_area(v), u, v) for u, v in combinations(red_tiles, 2)]

    # Sol 1
    # return largest_rect_in_poly(areas, red_tiles)

    # Sol 2
    shifted_red_tiles = red_tiles[1:] + red_tiles[:1]
    edges = [(u, v) for u, v in zip(red_tiles, shifted_red_tiles)]
    poly = PolygonIntersect(edges)
    for area, a, c in sorted(areas, reverse=True):
        if poly.rect_within_poly(a, c):
            return area

    return 0


if __name__ == '__main__':
    red_tiles = parse_input('puzzle_input.txt')

    print(f'Part 1: {largest_rectangle(red_tiles)}')
    print(f'Part 2: {largest_inscribed_rectangle(red_tiles)}')
