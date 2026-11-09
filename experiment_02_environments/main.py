"""Experiment 2: agent behavior under environment characteristics."""
from __future__ import annotations

import random


def classify_environment(**properties: bool) -> str:
    return ", ".join(name.replace("_", " ") for name, value in properties.items() if value)


def demo() -> None:
    scenarios = {
        "Chess": dict(fully_observable=True, deterministic=True, sequential=True, static=True),
        "Taxi driving": dict(partially_observable=True, stochastic=True, sequential=True, dynamic=True),
        "Image classification": dict(fully_observable=True, deterministic=True, episodic=True, static=True),
    }
    for name, attributes in scenarios.items():
        print(f"{name}: {classify_environment(**attributes)}")

    print("\nPartially observable robot: sensor may hide an obstacle")
    actual_obstacle = random.choice([True, False])
    sensor_reports = actual_obstacle if random.random() > 0.25 else not actual_obstacle
    print("Sensor sees obstacle:", sensor_reports, "-> action:", "turn" if sensor_reports else "move forward")
    print("(Actual state is", actual_obstacle, ")")


if __name__ == "__main__":
    demo()
