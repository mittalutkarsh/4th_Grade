# Puzzle validator specification

Use this format with `scripts/validate_card_puzzle.py`.

## Token format

- Shape: `S:triangle`, `S:square`, `S:circle`, `S:star`
- Number: `N:4`, `N:12`

Tokens are case-sensitive after the prefix only for display. Prefer lowercase shape names.

## Hidden-side example

```json
{
  "view1": ["N:4", "S:triangle", "S:square"],
  "view2": ["S:triangle", "N:2", "S:circle"],
  "question": {
    "type": "hidden_shape",
    "target": {"view": 1, "position": 0}
  },
  "expected_answer": "circle"
}
```

`view` is 1 or 2. `position` is zero-based and refers to the target card's visible position in that view.

Use `hidden_number` for the number behind a visible shape.

## Property-count example

```json
{
  "view1": ["S:square", "S:triangle", "N:3", "N:1"],
  "view2": ["N:2", "S:circle", "S:star", "N:1"],
  "question": {
    "type": "count_property",
    "property": "odd"
  },
  "expected_answer": 3
}
```

Supported properties:

- `odd`
- `even`
- `greater_than` with numeric `threshold`
- `less_than` with numeric `threshold`
- `multiple_of` with nonzero numeric `threshold`

## Result interpretation

The script enumerates every possible way the cards in view 1 could correspond to the cards in view 2.

- `valid_mapping_count: 0` means the views cannot come from the same physical cards.
- `unknown_possible: true` means at least one valid interpretation leaves the requested fact hidden.
- More than one value in `unique_answers` means the problem is ambiguous.
- `solvable: true` means every valid interpretation gives the same known answer.
- `matches_expected: false` means the intended answer is wrong even if the puzzle is solvable.

Accept an item only when `solvable` and `matches_expected` are both true.
