"""Experiment 6: minimax, alpha-beta pruning and tic-tac-toe AI."""
from __future__ import annotations

from math import inf


def minimax_tree(node: str, tree: dict[str, list[str] | int], maximizing: bool) -> int:
    if isinstance(tree[node], int): return tree[node]  # type: ignore[return-value]
    values = [minimax_tree(child, tree, not maximizing) for child in tree[node]]  # type: ignore[index]
    return max(values) if maximizing else min(values)


def alpha_beta(node: str, tree: dict[str, list[str] | int], maximizing: bool, alpha: float = -inf, beta: float = inf) -> int:
    if isinstance(tree[node], int): return tree[node]  # type: ignore[return-value]
    if maximizing:
        value = -inf
        for child in tree[node]:  # type: ignore[index]
            value = max(value, alpha_beta(child, tree, False, alpha, beta)); alpha = max(alpha, value)
            if alpha >= beta: break
        return int(value)
    value = inf
    for child in tree[node]:  # type: ignore[index]
        value = min(value, alpha_beta(child, tree, True, alpha, beta)); beta = min(beta, value)
        if alpha >= beta: break
    return int(value)


WINS = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
def winner(board: list[str]) -> str | None:
    for a,b,c in WINS:
        if board[a] != " " and board[a] == board[b] == board[c]: return board[a]
    return None

def ttt_score(board: list[str], turn: str) -> int:
    win = winner(board)
    if win == "X": return 1
    if win == "O": return -1
    if " " not in board: return 0
    scores = []
    for i, cell in enumerate(board):
        if cell == " ":
            copy = board.copy(); copy[i] = turn; scores.append(ttt_score(copy, "O" if turn == "X" else "X"))
    return max(scores) if turn == "X" else min(scores)

def best_ttt_move(board: list[str], player: str = "X") -> int:
    moves = [(ttt_score(board[:i] + [player] + board[i+1:], "O" if player == "X" else "X"), i) for i,x in enumerate(board) if x == " "]
    return (max if player == "X" else min)(moves)[1]


if __name__ == "__main__":
    tree = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F", "G"], "D": 3, "E": 5, "F": 2, "G": 9}
    print("Minimax value:", minimax_tree("A", tree, True))
    print("Alpha-beta value:", alpha_beta("A", tree, True))
    board = ["X", "O", "X", " ", "O", " ", " ", " ", " "]
    print("Tic-tac-toe board:", board, "best X move index:", best_ttt_move(board))
