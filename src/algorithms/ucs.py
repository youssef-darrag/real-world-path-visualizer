import heapq
import time
from networkx import MultiDiGraph
from core.utils import reconstruct_path


def ucs(graph: MultiDiGraph, start: int, goal: int, callback=None, delay: float = 0.0):

    pq = [(0, start)]
    costs = {start: 0}
    parent = {start: None}
    visited = set()

    while pq:
        current_cost, current = heapq.heappop(pq)

        if current == goal:
            break

        if current in visited:
            continue

        visited.add(current)


        if callback:
            callback(current, visited.copy())

        for neighbor in graph.neighbors(current):
            edge_data = graph.get_edge_data(current, neighbor)[0]
            weight = edge_data.get("length", 1)

            new_cost = current_cost + weight

            if neighbor not in costs or new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(pq, (new_cost, neighbor))

    return reconstruct_path(parent, goal), len(visited)
