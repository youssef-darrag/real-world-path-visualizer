"""
Grid Environment Module
Handles grid creation, obstacle generation, and movement validation.
"""

import random
from typing import List, Tuple, Set, Optional

class Grid:
    """
    Represents a 2D grid environment for pathfinding.
    
    Attributes:
        rows (int): Number of rows in the grid
        cols (int): Number of columns in the grid
        grid (List[List[int]]): 2D matrix representing the grid
        start (Tuple[int, int]): Starting position (row, col)
        goal (Tuple[int, int]): Goal position (row, col)
        obstacles (Set[Tuple[int, int]]): Set of obstacle positions
    """
    
    def __init__(self, rows: int = 10, cols: int = 10, obstacle_percent: float = 0.2):
        """
        Initialize a grid with given dimensions and obstacle percentage.
        
        Args:
            rows: Number of rows (default: 10)
            cols: Number of columns (default: 10)
            obstacle_percent: Percentage of obstacles (0.0 to 1.0, default: 0.2)
        """
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
        """Generate the grid with random obstacles."""
        # Create empty grid
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
        """Place start and goal positions randomly on free cells."""
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
        
        # Mark start and goal in grid (optional - for visualization)
        # self.grid[self.start[0]][self.start[1]] = 2  # 2 for start
        # self.grid[self.goal[0]][self.goal[1]] = 3    # 3 for goal
    
    def is_valid_position(self, position: Tuple[int, int]) -> bool:
        """
        Check if a position is valid (within bounds and not obstacle).
        
        Args:
            position: (row, col) tuple
        
        Returns:
            True if position is valid, False otherwise
        """
        r, c = position
        return (0 <= r < self.rows and 
                0 <= c < self.cols and 
                self.grid[r][c] == 0)  # 0 represents free cell
    
    def get_neighbors(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Get all valid neighboring positions (4 directions).
        
        Args:
            position: Current (row, col) position
        
        Returns:
            List of valid neighboring positions
        """
        r, c = position
        neighbors = []
        
        # Define possible moves: up, down, left, right
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in moves:
            new_pos = (r + dr, c + dc)
            if self.is_valid_position(new_pos):
                neighbors.append(new_pos)
        
        return neighbors
    
    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """
        Calculate Manhattan distance between two positions.
        
        Args:
            pos1: First position (row, col)
            pos2: Second position (row, col)
        
        Returns:
            Manhattan distance (sum of absolute differences)
        """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def print_grid(self, path: List[Tuple[int, int]] = None) -> None:
        """
        Print the grid with start, goal, obstacles, and optional path.
        
        Args:
            path: List of positions representing the path (optional)
        """
        path_set = set(path) if path else set()
        
        print("\n" + "=" * (self.cols * 2 + 3))
        print("Grid Visualization:")
        print("=" * (self.cols * 2 + 3))
        
        for r in range(self.rows):
            row_str = "| "
            for c in range(self.cols):
                pos = (r, c)
                if pos == self.start:
                    row_str += "S "
                elif pos == self.goal:
                    row_str += "G "
                elif pos in self.obstacles:
                    row_str += "X "
                elif pos in path_set:
                    row_str += "* "
                else:
                    row_str += ". "
            row_str += "|"
            print(row_str)
        
        print("=" * (self.cols * 2 + 3))
        print(f"Start: {self.start}, Goal: {self.goal}")
        print(f"Obstacles: {len(self.obstacles)} ({self.obstacle_percent*100:.0f}% of grid)")
    
    def reset(self, rows: int = None, cols: int = None, obstacle_percent: float = None):
        """
        Reset the grid with new parameters.
        
        Args:
            rows: New number of rows (optional)
            cols: New number of columns (optional)
            obstacle_percent: New obstacle percentage (optional)
        """
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