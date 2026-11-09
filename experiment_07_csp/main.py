"""Experiment 7: CSP methods—backtracking, cryptarithmetic and min-conflicts."""
from __future__ import annotations

import random


def map_coloring() -> dict[str, str] | None:
    regions = {"WA": ["NT", "SA"], "NT": ["WA", "SA", "Q"], "SA": ["WA", "NT", "Q", "NSW", "V"], "Q": ["NT", "SA", "NSW"], "NSW": ["Q", "SA", "V"], "V": ["SA", "NSW"], "T": []}
    colors, assignment = ["red", "green", "blue"], {}
    def solve() -> bool:
        if len(assignment) == len(regions): return True
        area = next(x for x in regions if x not in assignment)
        for color in colors:
            if all(assignment.get(neighbour) != color for neighbour in regions[area]):
                assignment[area] = color
                if solve(): return True
                del assignment[area]
        return False
    return assignment if solve() else None


def cryptarithmetic_send_more_money() -> dict[str, int] | None:
    """Efficient column-wise backtracking for SEND + MORE = MONEY."""
    letters, used, result = "SENDMORY", set(), {}
    def assign(letter: str, digit: int) -> bool:
        if digit in used or (digit == 0 and letter in "SM"): return False
        result[letter] = digit; used.add(digit); return True
    def unassign(letter: str, digit: int) -> None: del result[letter]; used.remove(digit)
    # Column 1: D + E = Y + 10*c1
    for d in range(10):
      if assign("D", d):
       for e in range(10):
        if assign("E", e):
         y, c1 = (d + e) % 10, (d + e) // 10
         if assign("Y", y):
          for n in range(10):
           if assign("N", n):
            # Column 2 chooses R so N+R+c1 = E + 10*c2.
            for rr in range(10):
             if assign("R", rr):
              if (n + rr + c1) % 10 == e:
               carry_2 = (n + rr + c1) // 10
               # Column 3: E+O+c2=N+10*c3
               for o in range(10):
                if assign("O", o) and (e + o + carry_2) % 10 == n:
                 carry_3 = (e + o + carry_2) // 10
                 # Column 4: S+M+c3=O+10*c4; final carry means M=c4.
                 for s in range(1, 10):
                  if assign("S", s):
                   for m in range(1, 10):
                    if assign("M", m):
                     if (s + m + carry_3) % 10 == o and (s + m + carry_3) // 10 == m: return result.copy()
                     unassign("M", m)
                   unassign("S", s)
                 unassign("O", o)
                elif "O" in result: unassign("O", o)
              unassign("R", rr)
            unassign("N", n)
          unassign("Y", y)
         unassign("E", e)
       unassign("D", d)
    return None


def min_conflicts_queens(n: int = 8, limit: int = 1000) -> list[int] | None:
    board = [random.randrange(n) for _ in range(n)]
    def conflicts(col: int, row: int) -> int:
        return sum(row == board[c] or abs(row - board[c]) == abs(col - c) for c in range(n) if c != col)
    for _ in range(limit):
        bad = [c for c in range(n) if conflicts(c, board[c])]
        if not bad: return board
        col = random.choice(bad); values = [conflicts(col, row) for row in range(n)]
        board[col] = random.choice([r for r, value in enumerate(values) if value == min(values)])
    return None


if __name__ == "__main__":
    print("Map colouring:", map_coloring())
    solution = cryptarithmetic_send_more_money(); print("SEND + MORE = MONEY:", solution)
    print("Local-search 8 queens:", min_conflicts_queens())
