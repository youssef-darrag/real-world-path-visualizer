import time
from networkx import MultiDiGraph
from core.utils import reconstruct_path


def dfs(
    graph: MultiDiGraph,
    start: int,
    goal: int,
    callback=None,
    delay: float = 0.0,
):
    stack = [start]
    parent = {start: None}
    visited_set = set()

    while stack:
        current = stack.pop()

        if current in visited_set:
            continue

        visited_set.add(current)

        if callback:
            callback(current, visited_set.copy())

        if current == goal:
            break

        for neighbor in graph.neighbors(current):
            if neighbor not in parent:
                parent[neighbor] = current
                stack.append(neighbor)

    return reconstruct_path(parent, goal), len(parent)
