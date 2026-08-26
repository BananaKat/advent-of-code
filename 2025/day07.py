# Written by Jason Phua
# on 29/01/2026
# Advent of Code 2025 - Day 7
# Solving https://adventofcode.com/2025/day/7
from collections import deque, defaultdict
from dataclasses import dataclass
from warnings import deprecated
import bisect


# Parse input file and return a 2D grid
def parse_input(filename: str) -> Grid:
    with open(filename) as file:
        return [list(line.strip()) for line in file]


# Part 1: Naive solution
# Count the number of times a 'tachyon' beam is split, by simulating
# beam splitting row by row, and count splitters entered
# Warning: Alters grid input
def simulate_splits(grid: Grid) -> int:
    splits = 0
    prev = grid[0]
    prev[prev.index('S')] = '|'
    for curr in grid[1:]:
        beam_idxs = [i for i, x in enumerate(prev) if x == '|']
        for i in beam_idxs:
            if curr[i] == '^':
                # Splitters cannot be adjacent
                curr[i - 1] = '|'
                curr[i + 1] = '|'
                splits += 1
            if curr[i] == '.':
                curr[i] = '|'
        prev = curr

    return splits


@dataclass(frozen=True)
class Pos:
    row: int
    col: int

    def left(self, n: int = 1) -> Pos:
        return Pos(self.row, self.col - n)

    def right(self, n: int = 1) -> Pos:
        return Pos(self.row, self.col + n)


class Grid:
    START = 'S'
    EMPTY = '.'
    BEAM = '|'
    SPLITTER = '^'

    def __init__(self, grid: list[list[str]]):
        self.grid = grid
        self.max_rows = len(grid)
        self.max_cols = len(grid[0])
        self.start = Pos(0, grid[0].index(Grid.START))
        self.splitters = self._preprocess_splitters(grid)

    def _valid_pos(self, row: int, col: int) -> bool:
        return (0 <= row < self.max_rows and
                0 <= col < self.max_cols)

    def is_splitter(self, row: int, col: int) -> bool:
        assert self._valid_pos(row, col)
        return self.grid[row][col] == Grid.SPLITTER

    # Return map of splitters sorted by column
    def _preprocess_splitters(self, grid: Grid) -> dict[int, list]:
        return {
            col: [row for row in range(self.max_rows)
                  if self.is_splitter(row, col)]
            for col in range(self.max_cols)
        }


# Part 1 & 2 solution
# Part 2 asks for the number of possible 'timelines' where
# each timeline is a different path through the splitters
class TachyonManifold:
    Node = Pos | str
    AdjList = dict[Node, list[Node]]
    PathMap = dict[Node, int]
    SOURCE = "Source"
    SINK = "Sink"

    def __init__(self, grid: Grid):
        self.dag = TachyonManifold._generate_dag(grid)
        self.paths = TachyonManifold._generate_paths(self.dag)

    # Given a beam, find the next splitter or sink
    # Use precomputed splitter map with binary search for O(log V)
    @staticmethod
    def _next_splitter(grid: Grid, start: Pos) -> Pos:
        '''
        # By-row linear scan in O(V)
        next_row = start.row + 1
        for nr in range(next_row, grid.max_rows):
            if grid.is_splitter(nr, start.col):
                return Pos(nr, start.col)
        return TachyonManifold.SINK
        '''
        splitters = grid.splitters.get(start.col, [])
        idx = bisect.bisect_right(splitters, start.row)
        if idx < len(splitters):
            return Pos(splitters[idx], start.col)
        return TachyonManifold.SINK


    # Form a directed acyclic graph (DAG) where each
    # node is a splitter and each edge is a straight beam path
    # In future, using row-major BFS traversal would maintain topological order.
    @staticmethod
    def _generate_dag(grid: Grid) -> tuple[AdjList, int]:
        dag = defaultdict(list)
        visited = set()
        stack = list()

        start_node = TachyonManifold._next_splitter(grid, grid.start)
        dag[TachyonManifold.SOURCE].append(start_node)
        stack.append(start_node)

        # Depth-first-search traversal over splitter nodes
        while stack:
            node = stack.pop()

            if node not in visited:
                visited.add(node)

                # Duplicates must be kept as each split creates a separate timeline
                adj_nodes = [TachyonManifold._next_splitter(grid, node.left()),
                             TachyonManifold._next_splitter(grid, node.right())]
                dag[node].extend(adj_nodes)

                next_nodes = [node for node in adj_nodes if isinstance(node, Pos)]
                stack.extend(next_nodes)

        dag[TachyonManifold.SINK] = list()
        return dag

    # Part 1: splits = number of splitters in DAG
    @property
    def splits(self) -> int:
        # Exclude Source and Sink nodes
        exclude = [TachyonManifold.SOURCE, TachyonManifold.SINK]
        return sum(1 for u in self.dag if u not in exclude)

    @staticmethod
    @deprecated("Used only for old DP solution")
    def _reverse_adjacency_list_DEP(adj: AdjList) -> AdjList:
        parents = defaultdict(list)
        for u, vs in adj.items():
            for v in vs:
                parents[v].append(u)
        return parents

    '''
    First attempt:
    My algorithm here works by building up path lengths, and holding:
        Let Path(v, n) be the number of paths of length n from Source->v
        Base case: Path(v, 1) = 1 iff Source~v
        Path(v, n) = Sum(Path(u, n - 1)) for all u in V, where u->v
    However, in the worst case, this would run in O(V^3)...
    '''
    @staticmethod
    @deprecated("Suboptimal DP solution")
    def _generate_paths_DEP(grid: Grid, dag: AdjList) -> PathMap:
        paths = defaultdict(lambda: defaultdict(int))
        # Base case: 1-paths = 1 iff Source~v
        for v in dag[TachyonManifold.SOURCE]:
            paths[v][1] += 1

        # The range of distances is [1, N], where N = max_rows, as
        # paths can only move downwards, no cycles exist, and N <= V
        rev_adj = TachyonManifold._reverse_adjacency_list(dag)
        for i in range(1, grid.max_rows):
            for v in dag:
                for parent in rev_adj[v]:
                    paths[v][i] += paths[parent][i - 1]
        return paths

    # Sum of paths of all lengths to Sink
    @property
    @deprecated("Operates on old DP solution format")
    def timelines_DEP(self) -> int:
        return sum(self.paths[TachyonManifold.SINK].values())

    # Kahn's Algorithm which uses breadth-first-search (BFS -> O(V + E))
    # to find a linear ordering of vertices such that for every u->v
    # vertex u comes before vertex v.
    # https://www.geeksforgeeks.org/dsa/topological-sorting-indegree-based-solution/
    @staticmethod
    def _topological_sort(dag: AdjList) -> list[Pos]:
        # Calculate indegree for each node
        indegree = defaultdict(int)
        for u in dag:
            for v in dag[u]:
                indegree[v] += 1

        # Enqueue nodes of indegree 0
        queue = deque(u for u in dag if indegree[u] == 0)

        # Apply BFS, dequeue and decrement adjacent indegrees
        res = []
        while queue:
            top = queue.popleft()
            res.append(top)
            for next_node in dag[top]:
                indegree[next_node] -= 1
                if indegree[next_node] == 0:
                    queue.append(next_node)

        return res

    '''
    Final attempt:
    By taking advantage of a topological sort, it turns out we don't need
    to track path lengths at all. Instead we recognise that:
        Given Path(v) is the number of paths from Source->v
        Path(v) = Sum(Path(u)) for all u in V, where u->v
    Topological sort runs in O(V + E), and our DP now runs in O(E) as we
    now iterate over each edge once, giving a total complexity of O(V + E).
    '''
    @staticmethod
    def _generate_paths(dag: AdjList) -> PathMap:
        dp = defaultdict(int)
        for v in dag[TachyonManifold.SOURCE]:
            dp[v] += 1

        topo = TachyonManifold._topological_sort(dag)
        for u in topo:
            for v in dag[u]:
                dp[v] += dp[u]

        return dp

    @property
    def timelines(self) -> int:
        return self.paths[TachyonManifold.SINK]


if __name__ == '__main__':
    grid = parse_input('puzzle_input.txt')
    res = TachyonManifold(Grid(grid))

    print(f'Part 1: {res.splits}')
    print(f'Part 2: {res.timelines}')
