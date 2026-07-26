# Minesweeper validator specification

Save one puzzle as JSON:

```json
{
  "grid": [
    [null, null, null, null],
    [3, null, 4, 2],
    [1, 1, 1, null],
    [null, null, null, null]
  ],
  "intended_mines": [[0, 0], [0, 1], [0, 2], [0, 3], [1, 1]]
}
```

- Use a nonnegative integer for a revealed clue.
- Use `null` for a square that must be classified as mine or safe.
- Keep the grid rectangular.
- Limit unknown squares to 20 for deterministic validation speed.
- List intended mine coordinates as zero-based `[row, column]` pairs.
- Accept a puzzle only when `solution_count` is `1`, `unique` is `true`, and `intended_matches` is `true`.

