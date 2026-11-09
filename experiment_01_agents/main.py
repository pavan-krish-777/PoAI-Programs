"""Experiment 1: four common intelligent-agent designs."""
from __future__ import annotations

from dataclasses import dataclass


class SimpleReflexVacuum:
    """Chooses solely from the current percept."""

    def act(self, location: str, status: str) -> str:
        if status == "Dirty":
            return "Suck"
        return "Right" if location == "A" else "Left"


class ModelBasedVacuum:
    """Remembers the last known condition of each square."""

    def __init__(self) -> None:
        self.model = {"A": "Unknown", "B": "Unknown"}

    def act(self, location: str, status: str) -> str:
        self.model[location] = status
        if status == "Dirty":
            return "Suck"
        other = "B" if location == "A" else "A"
        if self.model[other] != "Clean":
            return "Right" if location == "A" else "Left"
        return "NoOp"


class GoalBasedRouteAgent:
    def __init__(self, graph: dict[str, dict[str, int]], goal: str) -> None:
        self.graph, self.goal = graph, goal

    def act(self, current: str) -> str:
        # Select neighbour with the lowest direct cost to the goal in this tiny map.
        if current == self.goal:
            return "Arrived"
        return min(self.graph[current], key=self.graph[current].get)


class UtilityBasedRouteAgent:
    def __init__(self, choices: dict[str, tuple[int, int]]) -> None:
        self.choices = choices  # route -> (minutes, safety score)

    def utility(self, route: str) -> float:
        minutes, safety = self.choices[route]
        return safety * 10 - minutes  # prefer safety, then short travel time

    def act(self) -> str:
        return max(self.choices, key=self.utility)


def main() -> None:
    print("--- Simple reflex agent ---")
    reflex = SimpleReflexVacuum()
    for percept in [("A", "Dirty"), ("A", "Clean"), ("B", "Clean")]:
        print(percept, "=>", reflex.act(*percept))

    print("\n--- Model-based agent ---")
    model = ModelBasedVacuum()
    for percept in [("A", "Clean"), ("B", "Dirty"), ("B", "Clean")]:
        print(percept, "=>", model.act(*percept), "model:", model.model)

    print("\n--- Goal-based agent ---")
    roads = {"Home": {"Park": 2, "Market": 5}, "Park": {"College": 3}, "Market": {"College": 1}, "College": {}}
    print("From Home next move:", GoalBasedRouteAgent(roads, "College").act("Home"))

    print("\n--- Utility-based agent ---")
    utility = UtilityBasedRouteAgent({"highway": (20, 6), "scenic": (30, 9), "local": (25, 7)})
    print("Best route:", utility.act())


if __name__ == "__main__":
    main()
