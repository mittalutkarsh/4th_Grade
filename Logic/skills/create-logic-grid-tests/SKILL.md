---
name: create-logic-grid-tests
description: Create, vary, solve, validate, and explain original elementary logic-grid tests, worksheets, practice sets, answer keys, and interactive lessons that match equal-sized categories using clues, checkmarks, crosses, and ordering relationships. Use when a fourth- or fifth-grade activity needs three-category matching, direct and negative clues, before/after clues, unique solutions, mixed difficulty, printable output, or deterministic validation.
---

# Create Logic Grid Tests

Create original logic-grid puzzles that match one value from each equal-sized category. Use a checkmark for a confirmed match and a cross for an impossible match.

## Use the GRID method

Write child-facing explanations with this sequence:

1. **Group** the categories and verify that they have equal size.
2. **Record** each direct fact or impossibility.
3. **Infer** the forced crosses from each checkmark and combine related clues.
4. **Double-check** the completed matches against every clue.

## Generate a puzzle

1. Choose an anchor category, normally people or named characters.
2. Add two attribute categories, such as pet and order.
3. Choose a complete one-to-one solution.
4. Write a clue set using direct matches, non-matches, and at most one new relation type at a time.
5. Enumerate all category permutations and require exactly one solution.
6. Remove redundant clues when doing so preserves uniqueness and grade-appropriate reasoning.
7. Shuffle clue order so the final explanation still demonstrates a useful solving path.

Read [references/puzzle-spec.md](references/puzzle-spec.md) before constructing validator input.

Run:

```bash
python3 scripts/validate_logic_grid.py puzzle.json
```

Require `valid` and `unique` to be `true`, `solution_count` to equal `1`, and `intended_matches` to be `true`.

## Write fair clues

Use these clue forms:

- direct match: “Noah goes second”;
- direct non-match: “Maya does not bring the cat”;
- relative order: “The rabbit goes immediately before the dog”;
- earlier/later for medium or challenge puzzles.

Avoid pronoun ambiguity, hidden background knowledge, and wording tricks. Define whether “before” means anywhere earlier or immediately before.

## Control difficulty

- **Easy:** three categories of three; mostly direct matches and non-matches.
- **Medium:** three categories of three or four; include one ordering relation and a short contradiction branch.
- **Challenge:** three or four categories; combine two relations, but retain a clear deterministic path.

## Explain the answer

For every clue include:

1. the direct mark it creates;
2. the forced row and column crosses after a checkmark;
3. possibilities that must remain open;
4. the next clue that combines with the current marks;
5. any tested branch and the exact contradiction that rejects it.

Never fill an entire row without explaining the last remaining choice.

## Quality gate

- Confirm every category has the same number of values.
- Confirm each value appears exactly once in the intended solution.
- Confirm the clue set has exactly one solution.
- Confirm every clue is true in that solution.
- Confirm no explanation uses a later deduction early.
- Confirm grid labels are unambiguous and readable.
- Confirm each story and clue set is an original variation rather than a copied source item.

