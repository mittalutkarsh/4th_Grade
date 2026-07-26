---
name: create-minesweeper-logic-tests
description: Create, vary, solve, validate, and explain original small-grid Minesweeper logic tests, worksheets, practice sets, answer keys, and interactive lessons for elementary learners. Use when a fourth- or fifth-grade activity needs number clues, diagonal neighbor counting, mine and safe-square deductions, mixed difficulty, unique solutions, printable output, or deterministic validation.
---

# Create Minesweeper Logic Tests

Create original Minesweeper deduction puzzles. A numbered clue equals the total mines in its surrounding horizontal, vertical, and diagonal neighbors.

## Use the COUNT method

Write child-facing explanations with this sequence:

1. **Circle** one useful clue.
2. **Outline** every neighboring non-clue square, including diagonals.
3. **Use** `clue - marked mines = mines still needed`.
4. **Name** forced squares as mine or safe.
5. **Test** every clue after the grid is filled.

## Generate a puzzle

1. Choose a small rectangular grid, normally 4x4 or 5x5.
2. Place a hidden mine set.
3. Choose safe squares to reveal as number clues.
4. Derive every displayed number from the hidden mine set.
5. Remove or add clues until exactly one mine arrangement remains.
6. Require at least one opening move from a local counting rule.
7. Validate the puzzle before writing its explanation.

Read [references/puzzle-spec.md](references/puzzle-spec.md) before constructing validator input.

Run:

```bash
python3 scripts/validate_minesweeper.py puzzle.json
```

Require `valid` and `unique` to be `true`, `solution_count` to equal `1`, and `intended_matches` to be `true`.

## Use the two core deductions

- **All mines:** if the clue still needs as many mines as it has unknown neighbors, mark every unknown neighbor as a mine.
- **All safe:** if the clue already touches its full number of marked mines, mark every other unknown neighbor safe.

For medium and challenge puzzles, let marks from one clue unlock a nearby clue. Do not require random guessing or probability.

## Control difficulty

- **Easy:** 4x4; one corner or edge clue immediately forces mines; 3-5 deductions.
- **Medium:** 4x4 or 5x5; overlap two or more clue neighborhoods.
- **Challenge:** 5x5; require comparing overlapping clue counts, while retaining a unique deterministic path.

## Explain the answer

For each deduction state:

1. the clue being used;
2. all of its relevant neighbors;
3. mines already marked;
4. mines still needed;
5. why each newly marked square is mine or safe;
6. which clue becomes useful next.

Never count the clue square itself. Never omit diagonal neighbors.

## Quality gate

- Confirm every displayed clue equals the adjacent intended mine count.
- Confirm clue squares are never mines.
- Confirm exactly one mine arrangement satisfies all clues.
- Confirm the explanation never uses an unrevealed answer early.
- Confirm every non-clue square is eventually classified.
- Confirm the final recount satisfies every clue.
- Confirm each puzzle is an original variation rather than a copied source item.

