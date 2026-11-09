"""Experiment 4: BFS, DFS, DLS and bidirectional graph search."""
from __future__ import annotations

from collections import deque

Graph = dict[str, list[str]]
GRAPH: Graph = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"], "D": ["G"], "E": ["G"], "F": ["G"], "G": []}


def reconstruct(parent: dict[str, str | None], goal: str) -> list[str]:
    path = []
    while goal is not None:
        path.append(goal); goal = parent[goal]
    return path[::-1]


def bfs(graph: Graph, start: str, goal: str) -> list[str] | None:
    queue, parent = deque([start]), {start: None}
    while queue:
        node = queue.popleft()
        if node == goal: return reconstruct(parent, node)
        for child in graph[node]:
            if child not in parent: parent[child] = node; queue.append(child)
    return None


def dfs(graph: Graph, start: str, goal: str) -> list[str] | None:
    stack, parent = [start], {start: None}
    while stack:
        node = stack.pop()
        if node == goal: return reconstruct(parent, node)
        for child in reversed(graph[node]):
            if child not in parent: parent[child] = node; stack.append(child)
    return None


def depth_limited(graph: Graph, node: str, goal: str, limit: int, path: list[str] | None = None) -> list[str] | None:
    path = (path or []) + [node]
    if node == goal: return path
    if limit == 0: return None
    for child in graph[node]:
        if child not in path:
            result = depth_limited(graph, child, goal, limit - 1, path)
            if result: return result
    return None


def bidirectional(graph: Graph, start: str, goal: str) -> list[str] | None:
    reverse = {node: [] for node in graph}
    for node, children in graph.items():
        for child in children: reverse[child].append(node)
    front, back = {start}, {goal}; p1, p2 = {start: None}, {goal: None}
    while front and back:
        if len(front) <= len(back):
            frontier, adjacency, own, other = front, graph, p1, p2
            grow_front = True
        else:
            frontier, adjacency, own, other = back, reverse, p2, p1
            grow_front = False
        new = set()
        for node in frontier:
            for child in adjacency[node]:
                if child not in own: own[child] = node; new.add(child)
                if child in other:
                    meet = child
                    left = reconstruct(p1, meet)
                    right = [] ; cur = p2[meet]
                    while cur is not None: right.append(cur); cur = p2[cur]
                    return left + right
        if grow_front: front = new
        else: back = new
    return None


if __name__ == "__main__":
    print("BFS:", bfs(GRAPH, "A", "G"))
    print("DFS:", dfs(GRAPH, "A", "G"))
    print("DLS (limit 2):", depth_limited(GRAPH, "A", "G", 2))
    print("DLS (limit 3):", depth_limited(GRAPH, "A", "G", 3))
    print("Bidirectional:", bidirectional(GRAPH, "A", "G"))
