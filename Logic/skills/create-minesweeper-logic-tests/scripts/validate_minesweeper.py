#!/usr/bin/env python3
"""Validate a small Minesweeper logic puzzle by enumerating mine assignments."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def neighbors(row: int, col: int, rows: int, cols: int) -> list[tuple[int, int]]:
    result = []
    for row_change in (-1, 0, 1):
        for col_change in (-1, 0, 1):
            if row_change == 0 and col_change == 0:
                continue
            next_row = row + row_change
            next_col = col + col_change
            if 0 <= next_row < rows and 0 <= next_col < cols:
                result.append((next_row, next_col))
    return result


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_minesweeper.py puzzle.json", file=sys.stderr)
        return 2
    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    grid = payload.get("grid")
    if not isinstance(grid, list) or not grid or not all(isinstance(row, list) for row in grid):
        print(json.dumps({"valid": False, "error": "grid must be a nonempty matrix"}, indent=2))
        return 1
    rows = len(grid)
    cols = len(grid[0])
    if cols == 0 or any(len(row) != cols for row in grid):
        print(json.dumps({"valid": False, "error": "grid must be rectangular"}, indent=2))
        return 1
    unknowns = []
    clues = []
    for row in range(rows):
        for col in range(cols):
            value = grid[row][col]
            if value is None:
                unknowns.append((row, col))
            elif isinstance(value, int) and 0 <= value <= 8:
                clues.append((row, col, value))
            else:
                print(json.dumps({"valid": False, "error": "cells must be null or integers 0-8"}, indent=2))
                return 1
    if len(unknowns) > 20:
        print(json.dumps({"valid": False, "error": "validator limit is 20 unknown squares"}, indent=2))
        return 1

    unknown_index = {cell: index for index, cell in enumerate(unknowns)}
    clue_unknowns = []
    for row, col, value in clues:
        adjacent = [unknown_index[cell] for cell in neighbors(row, col, rows, cols) if cell in unknown_index]
        if value > len(adjacent):
            print(json.dumps({"valid": False, "error": f"clue at {row},{col} exceeds its unknown neighbors"}, indent=2))
            return 1
        clue_unknowns.append((value, adjacent))

    solutions: list[set[tuple[int, int]]] = []
    assignment = [False] * len(unknowns)

    def possible(depth: int) -> bool:
        for value, indices in clue_unknowns:
            assigned_indices = [index for index in indices if index < depth]
            marked = sum(1 for index in assigned_indices if assignment[index])
            remaining = sum(1 for index in indices if index >= depth)
            if marked > value or marked + remaining < value:
                return False
        return True

    def search(depth: int) -> None:
        if len(solutions) >= 2:
            return
        if depth == len(unknowns):
            if all(sum(1 for index in indices if assignment[index]) == value for value, indices in clue_unknowns):
                solutions.append({unknowns[index] for index, is_mine in enumerate(assignment) if is_mine})
            return
        assignment[depth] = False
        if possible(depth + 1):
            search(depth + 1)
        assignment[depth] = True
        if possible(depth + 1):
            search(depth + 1)
        assignment[depth] = False

    search(0)
    intended = {tuple(pair) for pair in payload.get("intended_mines", [])}
    intended_matches = not payload.get("intended_mines") or (len(solutions) == 1 and solutions[0] == intended)
    result = {
        "valid": len(solutions) > 0 and intended_matches,
        "unique": len(solutions) == 1,
        "solution_count": len(solutions),
        "mines": sorted([list(cell) for cell in solutions[0]]) if solutions else None,
        "intended_matches": intended_matches,
    }
    print(json.dumps(result, indent=2))
    return 0 if result["valid"] and result["unique"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
