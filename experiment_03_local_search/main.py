"""Experiment 3: local search optimization using the 8-queens problem."""
from __future__ import annotations

import math
import random


def conflicts(state: list[int]) -> int:
    return sum(1 for c1 in range(len(state)) for c2 in range(c1 + 1, len(state))
               if state[c1] == state[c2] or abs(state[c1] - state[c2]) == abs(c1 - c2))


def neighbours(state: list[int]):
    for col in range(len(state)):
        for row in range(len(state)):
            if row != state[col]:
                candidate = state.copy(); candidate[col] = row
                yield candidate


def hill_climb(start: list[int]) -> list[int]:
    current = start
    while True:
        best = min(neighbours(current), key=conflicts)
        if conflicts(best) >= conflicts(current):
            return current
        current = best


def simulated_annealing(start: list[int], temperature: float = 20.0) -> list[int]:
    current = start.copy()
    while temperature > 0.05 and conflicts(current):
        candidate = random.choice(list(neighbours(current)))
        delta = conflicts(current) - conflicts(candidate)
        if delta > 0 or random.random() < math.exp(delta / temperature):
            current = candidate
        temperature *= 0.96
    return current


def local_beam_search(k: int = 4, steps: int = 100) -> list[int]:
    beam = [[random.randrange(8) for _ in range(8)] for _ in range(k)]
    for _ in range(steps):
        all_candidates = [n for state in beam for n in neighbours(state)]
        beam = sorted(all_candidates, key=conflicts)[:k]
        if conflicts(beam[0]) == 0:
            break
    return beam[0]


def report(name: str, state: list[int]) -> None:
    print(f"{name}: {state}; attacking pairs = {conflicts(state)}")


if __name__ == "__main__":
    random.seed(7)
    start = [random.randrange(8) for _ in range(8)]
    report("Start", start)
    report("Hill climbing", hill_climb(start))
    report("Simulated annealing", simulated_annealing(start))
    report("Local beam", local_beam_search())
