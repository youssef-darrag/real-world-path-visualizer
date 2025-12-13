"""
Utility Functions Module
Contains helper functions, data structures, and common utilities.
"""

from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import heapq

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

def print_metrics(metrics: Dict[str, Any]) -> None:
    """
    Print performance metrics in a formatted table.
    
    Args:
        metrics: Dictionary containing algorithm metrics
    """
    print("\n" + "=" * 60)
    print(f"Algorithm: {metrics['algorithm']}")
    print("=" * 60)
    
    if not metrics['path_found']:
        print("❌ No path found!")
    else:
        print(f"✅ Path found: {metrics['path_length']} steps")
        print(f"📊 Nodes expanded: {metrics['nodes_expanded']}")
        print(f"💾 Max nodes in memory: {metrics['max_nodes_in_memory']}")
        print(f"🎯 Optimal path: {'Yes' if metrics['is_optimal'] else 'No'}")
    
    print("=" * 60)

def compare_algorithms(results: List[Dict[str, Any]]) -> None:
    """
    Compare multiple algorithms in a table format.
    
    Args:
        results: List of metrics dictionaries from different algorithms
    """
    print("\n" + "=" * 80)
    print("COMPARATIVE ANALYSIS")
    print("=" * 80)
    print(f"{'Algorithm':<20} {'Nodes Expanded':<15} {'Max Memory':<12} {'Path Length':<12} {'Optimal':<8}")
    print("-" * 80)
    
    for result in results:
        print(f"{result['algorithm']:<20} "
              f"{result['nodes_expanded']:<15} "
              f"{result['max_nodes_in_memory']:<12} "
              f"{result['path_length'] if result['path_found'] else 'N/A':<12} "
              f"{'Yes' if result['is_optimal'] else 'No':<8}")
    
    print("=" * 80)

class PriorityQueue:
    """
    Priority queue implementation for UCS and A* algorithms.
    Uses heapq for efficient minimum extraction.
    """
    
    def __init__(self):
        self.elements = []
    
    def empty(self) -> bool:
        return len(self.elements) == 0
    
    def put(self, item: Node, priority: float):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self) -> Node:
        return heapq.heappop(self.elements)[1]
    
    def __len__(self) -> int:
        return len(self.elements)

def get_direction_name(action: Direction) -> str:
    """Get human-readable direction name."""
    direction_names = {
        Direction.UP: "Up",
        Direction.DOWN: "Down",
        Direction.LEFT: "Left",
        Direction.RIGHT: "Right"
    }
    return direction_names.get(action, "Unknown")