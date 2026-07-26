#!/usr/bin/env python3
"""Enumerate small category matchings and validate a logic-grid clue set."""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path
from typing import Any


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_logic_grid.py puzzle.json", file=sys.stderr)
        return 2
    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    categories = payload.get("categories")
    anchor_name = payload.get("anchor")
    ordered_name = payload.get("ordered_category")
    clues = payload.get("clues", [])
    if not isinstance(categories, dict) or anchor_name not in categories or ordered_name not in categories:
        print(json.dumps({"valid": False, "error": "Missing categories, anchor, or ordered_category"}, indent=2))
        return 1
    anchors = categories[anchor_name]
    size = len(anchors)
    if size == 0 or size > 5 or any(not isinstance(values, list) or len(values) != size for values in categories.values()):
        print(json.dumps({"valid": False, "error": "All categories must have the same size from 1 through 5"}, indent=2))
        return 1
    if any(len(values) != len(set(values)) for values in categories.values()):
        print(json.dumps({"valid": False, "error": "Category values must be distinct"}, indent=2))
        return 1

    attribute_names = [name for name in categories if name != anchor_name]
    order_values = categories[ordered_name]

    def validate_ref(ref: dict[str, Any]) -> bool:
        return (
            isinstance(ref, dict)
            and ref.get("category") in categories
            and ref.get("value") in categories[ref["category"]]
        )

    for clue in clues:
        if clue.get("type") not in {"match", "not_match", "before", "immediately_before"}:
            print(json.dumps({"valid": False, "error": "Unsupported clue type"}, indent=2))
            return 1
        if not validate_ref(clue.get("a")) or not validate_ref(clue.get("b")):
            print(json.dumps({"valid": False, "error": "Invalid clue reference"}, indent=2))
            return 1

    solutions = []
    permutation_sets = [list(itertools.permutations(categories[name])) for name in attribute_names]
    for combined in itertools.product(*permutation_sets):
        assignment = {
            anchor: {name: combined[index][anchor_index] for index, name in enumerate(attribute_names)}
            for anchor_index, anchor in enumerate(anchors)
        }

        def owner(ref: dict[str, str]) -> str:
            if ref["category"] == anchor_name:
                return ref["value"]
            return next(anchor for anchor in anchors if assignment[anchor][ref["category"]] == ref["value"])

        def order_index(ref: dict[str, str]) -> int:
            anchor = owner(ref)
            order_value = assignment[anchor][ordered_name]
            return order_values.index(order_value)

        satisfies = True
        for clue in clues:
            clue_type = clue["type"]
            left = clue["a"]
            right = clue["b"]
            if clue_type == "match":
                satisfies = owner(left) == owner(right)
            elif clue_type == "not_match":
                satisfies = owner(left) != owner(right)
            elif clue_type == "before":
                satisfies = order_index(left) < order_index(right)
            else:
                satisfies = order_index(left) + 1 == order_index(right)
            if not satisfies:
                break
        if satisfies:
            solutions.append(assignment)
            if len(solutions) >= 2:
                break

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
