"""Experiment 9: Bayesian diagnosis and a compact Mamdani-style fuzzy system."""
from __future__ import annotations


def bayes_disease_given_positive(prevalence: float, sensitivity: float, specificity: float) -> float:
    """P(disease | positive test), from Bayes' theorem."""
    return sensitivity * prevalence / (sensitivity * prevalence + (1 - specificity) * (1 - prevalence))


def triangle(x: float, left: float, peak: float, right: float) -> float:
    if x <= left or x >= right: return 0.0
    return 1.0 if x == peak else (x-left)/(peak-left) if x < peak else (right-x)/(right-peak)


def fuzzy_fan_speed(temperature: float, humidity: float) -> float:
    """Returns 0..100 fan speed using min for AND and weighted-centroid defuzzification."""
    cool = triangle(temperature, 0, 15, 25); warm = triangle(temperature, 18, 27, 36); hot = triangle(temperature, 28, 40, 50)
    dry = triangle(humidity, 0, 20, 55); humid = triangle(humidity, 40, 70, 100)
    rules = [(min(cool, dry), 20), (warm, 55), (max(hot, humid), 90)]
    total = sum(strength for strength, _ in rules)
    return sum(strength * output for strength, output in rules) / total if total else 0.0


if __name__ == "__main__":
    probability = bayes_disease_given_positive(prevalence=0.01, sensitivity=0.95, specificity=0.90)
    print(f"P(disease | positive test) = {probability:.2%}")
    for temp, humidity in [(20, 30), (29, 55), (39, 80)]:
        print(f"Temperature {temp} C, humidity {humidity}% -> fan {fuzzy_fan_speed(temp, humidity):.1f}%")
