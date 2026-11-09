"""Experiment 5: Greedy BFS, A*, AO* and a memory-bounded search example."""
from __future__ import annotations

import heapq
from itertools import count

WEIGHTED = {"S": {"A": 1, "B": 4}, "A": {"C": 2, "D": 5}, "B": {"D": 1}, "C": {"G": 5}, "D": {"G": 2}, "G": {}}
H = {"S": 7, "A": 6, "B": 3, "C": 5, "D": 2, "G": 0}


def best_first(start: str, goal: str) -> list[str]:
    queue, parent, seen = [(H[start], start)], {start: None}, set()
    while queue:
        _, node = heapq.heappop(queue)
        if node in seen: continue
        seen.add(node)
        if node == goal: return path(parent, node)
        for child in WEIGHTED[node]:
            if child not in parent: parent[child] = node; heapq.heappush(queue, (H[child], child))
    return []


def a_star(start: str, goal: str) -> tuple[list[str], int]:
    order = count(); queue = [(H[start], next(order), 0, start)]; parent = {start: None}; cost = {start: 0}
    while queue:
        _, _, g, node = heapq.heappop(queue)
        if node == goal: return path(parent, node), g
        if g != cost[node]: continue
        for child, edge in WEIGHTED[node].items():
            new_g = g + edge
            if new_g < cost.get(child, float("inf")):
                cost[child], parent[child] = new_g, node
                heapq.heappush(queue, (new_g + H[child], next(order), new_g, child))
    return [], -1


def path(parent: dict[str, str | None], node: str) -> list[str]:
    result = []
    while node is not None: result.append(node); node = parent[node]
    return result[::-1]


def ao_star(node: str, graph: dict[str, list[list[tuple[str, int]]]], memo: dict[str, tuple[int, list]] | None = None) -> tuple[int, list]:
    """Returns cheapest solution cost and selected AND/OR decomposition."""
    memo = memo if memo is not None else {}
    if node in memo: return memo[node]
    if node not in graph: return (0, [node])
    alternatives = []
    for and_set in graph[node]:
        cost, solution = 0, []
        for child, edge_cost in and_set:
            child_cost, child_solution = ao_star(child, graph, memo)
            cost += edge_cost + child_cost; solution.append(child_solution)
        alternatives.append((cost, solution))
    memo[node] = min(alternatives, key=lambda item: item[0]); return memo[node]


def memory_bounded_best_first(limit: int = 3) -> list[str]:
    """Keeps only `limit` most promising frontier states (a simple beam variant)."""
    frontier, parents = [(H["S"], "S")], {"S": None}
    while frontier:
        frontier.sort(); _, node = frontier.pop(0)
        if node == "G": return path(parents, node)
        for child in WEIGHTED[node]:
            if child not in parents: parents[child] = node; frontier.append((H[child], child))
        frontier = sorted(frontier)[:limit]
    return []


if __name__ == "__main__":
    print("Greedy best-first:", best_first("S", "G"))
    print("A*:", a_star("S", "G"))
    and_or = {"S": [[("A", 1), ("B", 1)], [("C", 2)]], "A": [[("G", 3)]], "B": [[("G", 1)]], "C": [[("G", 5)]]}
    print("AO* cost, plan:", ao_star("S", and_or))
    print("Memory-bounded best-first:", memory_bounded_best_first())
