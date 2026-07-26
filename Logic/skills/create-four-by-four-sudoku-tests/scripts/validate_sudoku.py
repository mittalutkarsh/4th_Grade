#!/usr/bin/env python3
"""Validate a 4x4 Sudoku puzzle and confirm that it has one solution."""

from __future__ import annotations

import json
import sys
from pathlib import Path


SIZE = 4
DIGITS = {1, 2, 3, 4}


def valid_group(values: list[int]) -> bool:
    present = [value for value in values if value]
    return len(present) == len(set(present)) and all(value in DIGITS for value in present)


def valid_grid(grid: list[list[int]]) -> bool:
    if len(grid) != SIZE or any(len(row) != SIZE for row in grid):
        return False
    if any(not isinstance(value, int) or value < 0 or value > 4 for row in grid for value in row):
        return False
    for index in range(SIZE):
        if not valid_group(grid[index]):
            return False
        if not valid_group([grid[row][index] for row in range(SIZE)]):
            return False
    for box_row in (0, 2):
        for box_col in (0, 2):
            box = [
                grid[row][col]
                for row in range(box_row, box_row + 2)
                for col in range(box_col, box_col + 2)
            ]
            if not valid_group(box):
                return False
    return True


def candidates(grid: list[list[int]], row: int, col: int) -> list[int]:
    used = set(grid[row])
    used.update(grid[index][col] for index in range(SIZE))
    box_row = (row // 2) * 2
    box_col = (col // 2) * 2
    used.update(
        grid[r][c]
        for r in range(box_row, box_row + 2)
        for c in range(box_col, box_col + 2)
    )
    return sorted(DIGITS - used)


def solve(grid: list[list[int]], solutions: list[list[list[int]]], limit: int = 2) -> None:
    if len(solutions) >= limit:
        return
    best: tuple[int, int, list[int]] | None = None
    for row in range(SIZE):
        for col in range(SIZE):
            if grid[row][col] != 0:
                continue
            choices = candidates(grid, row, col)
            if not choices:
                return
            if best is None or len(choices) < len(best[2]):
                best = (row, col, choices)
    if best is None:
        solutions.append([row[:] for row in grid])
        return
    row, col, choices = best
    for value in choices:
        grid[row][col] = value
        solve(grid, solutions, limit)
        grid[row][col] = 0


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_sudoku.py puzzle.json", file=sys.stderr)
        return 2
    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    grid = payload.get("grid")
    if not isinstance(grid, list) or not valid_grid(grid):
        result = {"valid": False, "unique": False, "solution_count": 0, "error": "Invalid grid or givens"}
        print(json.dumps(result, indent=2))
        return 1
    solutions: list[list[list[int]]] = []
    solve([row[:] for row in grid], solutions)
    intended = payload.get("intended_solution")
    intended_matches = intended is None or (len(solutions) == 1 and solutions[0] == intended)
    result = {
        "valid": len(solutions) > 0 and intended_matches,
        "unique": len(solutions) == 1,
        "solution_count": len(solutions),
        "solution": solutions[0] if solutions else None,
        "intended_matches": intended_matches,
    }
    print(json.dumps(result, indent=2))
    return 0 if result["valid"] and result["unique"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
