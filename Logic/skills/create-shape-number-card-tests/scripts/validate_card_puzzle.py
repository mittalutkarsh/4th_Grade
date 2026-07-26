#!/usr/bin/env python3
"""Validate whether a two-view shape-number card puzzle has a unique answer."""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Token:
    kind: str
    value: str


def parse_token(raw: str) -> Token:
    if not isinstance(raw, str) or ":" not in raw:
        raise ValueError(f"Invalid token {raw!r}; use S:name or N:number")
    prefix, value = raw.split(":", 1)
    if prefix not in {"S", "N"} or not value:
        raise ValueError(f"Invalid token {raw!r}; use S:name or N:number")
    if prefix == "N":
        float(value)
    return Token(prefix, value)


def compatible(a: Token, b: Token) -> bool:
    return a.kind != b.kind or a.value == b.value


def valid_mappings(view1: list[Token], view2: list[Token]):
    for permutation in itertools.permutations(range(len(view2))):
        if all(compatible(view1[index], view2[permutation[index]]) for index in range(len(view1))):
            yield permutation


def paired_token(
    view: int,
    position: int,
    view1: list[Token],
    view2: list[Token],
    permutation: tuple[int, ...],
) -> tuple[Token, Token]:
    if view == 1:
        return view1[position], view2[permutation[position]]
    inverse = {view2_index: view1_index for view1_index, view2_index in enumerate(permutation)}
    return view2[position], view1[inverse[position]]


def normalize_number(value: str) -> int | float:
    parsed = float(value)
    return int(parsed) if parsed.is_integer() else parsed


def hidden_side_answer(
    question: dict[str, Any],
    view1: list[Token],
    view2: list[Token],
    permutation: tuple[int, ...],
) -> str | None:
    target = question.get("target") or {}
    view = target.get("view")
    position = target.get("position")
    if view not in {1, 2} or not isinstance(position, int):
        raise ValueError("Hidden-side questions require target.view (1 or 2) and zero-based target.position")
    selected = view1 if view == 1 else view2
    if position < 0 or position >= len(selected):
        raise ValueError("target.position is outside the selected view")

    visible, paired = paired_token(view, position, view1, view2, permutation)
    question_type = question["type"]
    expected_visible_kind = "N" if question_type == "hidden_shape" else "S"
    expected_hidden_kind = "S" if question_type == "hidden_shape" else "N"

    if visible.kind != expected_visible_kind:
        raise ValueError(f"{question_type} target must visibly show kind {expected_visible_kind}")
    if paired.kind == expected_hidden_kind:
        return paired.value
    return None


def count_property_answer(
    question: dict[str, Any],
    view1: list[Token],
    view2: list[Token],
    permutation: tuple[int, ...],
) -> int | None:
    numbers: list[int | float] = []
    for index, other_index in enumerate(permutation):
        pair = (view1[index], view2[other_index])
        number_tokens = [token for token in pair if token.kind == "N"]
        if not number_tokens:
            return None
        numbers.append(normalize_number(number_tokens[0].value))

    property_name = question.get("property")
    threshold = question.get("threshold")
    if property_name == "odd":
        return sum(int(number) % 2 != 0 for number in numbers)
    if property_name == "even":
        return sum(int(number) % 2 == 0 for number in numbers)
    if property_name == "greater_than":
        if not isinstance(threshold, (int, float)):
            raise ValueError("greater_than requires numeric threshold")
        return sum(number > threshold for number in numbers)
    if property_name == "less_than":
        if not isinstance(threshold, (int, float)):
            raise ValueError("less_than requires numeric threshold")
        return sum(number < threshold for number in numbers)
    if property_name == "multiple_of":
        if not isinstance(threshold, (int, float)) or threshold == 0:
            raise ValueError("multiple_of requires a nonzero numeric threshold")
        return sum(number % threshold == 0 for number in numbers)
    raise ValueError(f"Unsupported count property {property_name!r}")


def analyze(spec: dict[str, Any]) -> dict[str, Any]:
    raw_view1 = spec.get("view1")
    raw_view2 = spec.get("view2")
    if not isinstance(raw_view1, list) or not isinstance(raw_view2, list):
        raise ValueError("view1 and view2 must be arrays")
    if len(raw_view1) != len(raw_view2) or not raw_view1:
        raise ValueError("view1 and view2 must contain the same positive number of cards")
    if len(raw_view1) > 8:
        raise ValueError("Validator supports at most 8 cards")

    view1 = [parse_token(token) for token in raw_view1]
    view2 = [parse_token(token) for token in raw_view2]
    question = spec.get("question")
    if not isinstance(question, dict):
        raise ValueError("question must be an object")

    question_type = question.get("type")
    mappings = list(valid_mappings(view1, view2))
    answers: set[str | int | float] = set()
    unknown_possible = False

    for mapping in mappings:
        if question_type in {"hidden_shape", "hidden_number"}:
            answer = hidden_side_answer(question, view1, view2, mapping)
        elif question_type == "count_property":
            answer = count_property_answer(question, view1, view2, mapping)
        else:
            raise ValueError(f"Unsupported question type {question_type!r}")
        if answer is None:
            unknown_possible = True
        else:
            answers.add(answer)

    sorted_answers = sorted(answers, key=lambda item: (str(type(item)), str(item)))
    solvable = bool(mappings) and not unknown_possible and len(sorted_answers) == 1
    result: dict[str, Any] = {
        "valid_mapping_count": len(mappings),
        "unknown_possible": unknown_possible,
        "unique_answers": sorted_answers,
        "solvable": solvable,
    }

    if "expected_answer" in spec:
        expected = spec["expected_answer"]
        result["expected_answer"] = expected
        result["matches_expected"] = solvable and sorted_answers[0] == expected
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, help="Path to a puzzle JSON file")
    args = parser.parse_args()

    try:
        with args.spec.open("r", encoding="utf-8") as stream:
            spec = json.load(stream)
        result = analyze(spec)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"error": str(error), "solvable": False}, indent=2))
        return 2

    print(json.dumps(result, indent=2))
    expected_ok = result.get("matches_expected", True)
    return 0 if result["solvable"] and expected_ok else 1


if __name__ == "__main__":
    sys.exit(main())
