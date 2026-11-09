"""Experiment 8: facts, Horn rules, forward chaining and backward chaining."""
from __future__ import annotations

from dataclasses import dataclass

Fact = str
@dataclass(frozen=True)
class Rule:
    premises: tuple[Fact, ...]
    conclusion: Fact

class KnowledgeBase:
    def __init__(self, facts: set[Fact], rules: list[Rule]) -> None: self.facts, self.rules = facts, rules
    def forward_chain(self) -> set[Fact]:
        known = self.facts.copy(); changed = True
        while changed:
            changed = False
            for rule in self.rules:
                if set(rule.premises) <= known and rule.conclusion not in known:
                    known.add(rule.conclusion); changed = True
        return known
    def backward_chain(self, query: Fact, seen: set[Fact] | None = None) -> bool:
        seen = seen or set()
        if query in self.facts: return True
        if query in seen: return False
        return any(rule.conclusion == query and all(self.backward_chain(p, seen | {query}) for p in rule.premises) for rule in self.rules)


def example(name: str, facts: set[Fact], rules: list[Rule], query: Fact) -> None:
    kb = KnowledgeBase(facts, rules)
    print(f"\n{name}")
    print("Forward chaining derives:", sorted(kb.forward_chain()))
    print(f"Backward chaining: {query}?", kb.backward_chain(query))


if __name__ == "__main__":
    example("Medical diagnosis", {"fever", "cough"}, [Rule(("fever", "cough"), "flu"), Rule(("flu",), "rest_required")], "rest_required")
    example("Autonomous vehicle", {"obstacle_detected", "red_light"}, [Rule(("obstacle_detected",), "brake"), Rule(("red_light",), "stop")], "stop")
    example("Industrial manufacturing", {"high_temperature", "vibration"}, [Rule(("high_temperature", "vibration"), "machine_fault"), Rule(("machine_fault",), "schedule_maintenance")], "schedule_maintenance")
