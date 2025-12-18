"""
Utility Functions Module
Contains helper functions, data structures, and common utilities.
"""

from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    """Enum for movement directions."""
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


@dataclass
class Node:
    """
    Represents a node in the search tree.

    Attributes:
        position: (row, col) coordinates
        parent: Parent node (for path reconstruction)
        action: Action taken to reach this node
        cost: Cost from start to this node (g(n))
        heuristic: Estimated cost to goal (h(n))
    """
    position: Tuple[int, int]
    parent: Optional['Node'] = None
    action: Optional[Direction] = None
    cost: float = 0.0
    heuristic: float = 0.0

    @property
    def total_cost(self) -> float:
        """Total estimated cost: f(n) = g(n) + h(n)."""
        return self.cost + self.heuristic

    def __lt__(self, other: 'Node') -> bool:
        """Comparison for priority queue (used in UCS and A*)."""
        return self.total_cost < other.total_cost


def reconstruct_path(node: Node) -> List[Tuple[int, int]]:
    """
    Reconstruct path from start to given node.

    Args:
        node: Goal node

    Returns:
        List of positions from start to goal
    """
    path = []
    current = node

    while current is not None:
        path.append(current.position)
        current = current.parent

    return path[::-1]  # Reverse to get start -> goal


def calculate_metrics(algorithm_name: str,
                     nodes_expanded: int,
                     max_nodes_in_memory: int,
                     path: List[Tuple[int, int]],
                     optimal_path_length: int) -> Dict[str, Any]:
    """
    Calculate and format performance metrics.

    Args:
        algorithm_name: Name of the algorithm
        nodes_expanded: Number of nodes expanded
        max_nodes_in_memory: Maximum nodes stored in memory
        path: Found path (list of positions)
        optimal_path_length: Length of optimal path (for comparison)

    Returns:
        Dictionary with all metrics
    """
    path_length = len(path) - 1 if path else 0  # Exclude start node
    is_optimal = path_length == optimal_path_length if path else False

    return {
        "algorithm": algorithm_name,
        "nodes_expanded": nodes_expanded,
        "max_nodes_in_memory": max_nodes_in_memory,
        "path_found": bool(path),
        "path_length": path_length,
        "is_optimal": is_optimal,
        "path": path
    }


def get_direction_name(action: Direction) -> str:
    """Get human-readable direction name."""
    direction_names = {
        Direction.UP: "Up",
        Direction.DOWN: "Down",
        Direction.LEFT: "Left",
        Direction.RIGHT: "Right"
    }
    return direction_names.get(action, "Unknown")
