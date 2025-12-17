import random
import math
from typing import List, Tuple, Set

# This is an nxm grid built using a matrix created by a vector of m inside a vector of m

class Grid:
    def __init__(self, rows: int = 10, cols: int = 10, obstacle_percent: float = 0.2):
        self.rows = rows
        self.cols = cols
        self.obstacle_percent = obstacle_percent
        self.grid = []
        self.start = None
        self.goal = None
        self.obstacles = set()

        self._generate_grid()
        self._place_start_goal()

    def _generate_grid(self) -> None:
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        # Calculate number of obstacles
        total_cells = self.rows * self.cols
        num_obstacles = int(total_cells * self.obstacle_percent)

        # Generate random obstacle positions
        all_positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        obstacle_positions = random.sample(all_positions, min(num_obstacles, total_cells))

        # Mark obstacles in grid
        for r, c in obstacle_positions:
            self.grid[r][c] = 1  # 1 represents obstacle
            self.obstacles.add((r, c))

    def _place_start_goal(self) -> None:
        # Get all free positions (non-obstacles)
        free_positions = [
            (r, c) for r in range(self.rows)
            for c in range(self.cols)
            if self.grid[r][c] == 0
        ]

        if len(free_positions) < 2:
            raise ValueError("Not enough free cells for start and goal positions")

        # Randomly select start and goal (different positions)
        self.start, self.goal = random.sample(free_positions, 2)

    def is_valid_position(self, position: Tuple[int, int]) -> bool:
        r, c = position
        return (0 <= r < self.rows and
                0 <= c < self.cols and
                self.grid[r][c] == 0)

    def get_neighbors(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        r, c = position
        neighbors = []

        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in moves:
            new_pos = (r + dr, c + dc)
            if self.is_valid_position(new_pos):
                neighbors.append(new_pos)

        return neighbors

    def euclidean_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def reset(self, rows: int = None, cols: int = None, obstacle_percent: float = None):
        if rows is not None:
            self.rows = rows
        if cols is not None:
            self.cols = cols
        if obstacle_percent is not None:
            self.obstacle_percent = obstacle_percent

        self.grid = []
        self.start = None
        self.goal = None
        self.obstacles.clear()
        self._generate_grid()
        self._place_start_goal()
