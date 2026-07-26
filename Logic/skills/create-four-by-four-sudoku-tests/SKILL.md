---
name: create-four-by-four-sudoku-tests
description: Create, vary, solve, validate, and explain original 4x4 Sudoku tests, worksheets, practice sets, answer keys, and interactive lessons for elementary learners. Use when a fourth- or fifth-grade activity needs uniquely solvable 4x4 grids, 2x2 boxes, mixed difficulty, clue-by-clue reasoning, printable output, or deterministic solution validation.
---

# Create 4x4 Sudoku Tests

Create original 4x4 Sudoku puzzles in which every row, column, and 2x2 box contains 1, 2, 3, and 4 exactly once.

## Use the SCAN method

Write child-facing explanations with this sequence:

1. **Scan** the row, column, and box.
2. **Collect** the missing numbers.
3. **Ask** where each number can legally go.
4. **Note** a single only when one choice remains, then repeat.

Never describe a placement as a guess. Name the exact group that blocks each rejected candidate.

## Generate a puzzle

1. Generate or choose a valid completed 4x4 solution.
2. Remove entries while preserving exactly one solution.
3. Prefer puzzles that begin with at least one understandable single.
4. Vary rotations, reflections, digit permutations, and clue locations.
5. Keep the intended difficulty aligned with the number and depth of deductions.
6. Validate after every clue removal and again before publishing.

Read [references/puzzle-spec.md](references/puzzle-spec.md) before constructing validator input.

Run:

```bash
python3 scripts/validate_sudoku.py puzzle.json
```

Require `valid` and `unique` to be `true`, `solution_count` to equal `1`, and the returned solution to match the intended answer.

## Control difficulty

- **Easy:** 7-9 givens; several row, column, or box singles.
- **Medium:** 6-7 givens; require alternating between groups.
- **Challenge:** 5-6 givens; require candidate elimination, but avoid trial-and-error for the target grade.

Reject a puzzle if its first progress requires guessing between two equally possible candidates.

## Explain the answer

For every placement include:

1. the row, column, or box being scanned;
2. the missing number set;
3. the blocked candidate and where the blocking number appears;
4. the forced placement;
5. the new group unlocked by that placement.

Finish by checking all twelve groups: four rows, four columns, and four boxes.

## Quality gate

- Confirm all givens agree with the intended solution.
- Confirm the puzzle has exactly one solution.
- Confirm each explanation uses only information available at that step.
- Confirm no row, column, or box repeats a number.
- Confirm the worksheet and solution are visually distinguishable.
- Confirm every puzzle is an original variation rather than a copied source item.

