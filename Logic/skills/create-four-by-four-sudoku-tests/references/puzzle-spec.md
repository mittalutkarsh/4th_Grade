# 4x4 Sudoku validator specification

Save one puzzle as JSON:

```json
{
  "grid": [
    [0, 2, 0, 4],
    [3, 0, 0, 0],
    [0, 0, 4, 0],
    [4, 0, 0, 1]
  ],
  "intended_solution": [
    [1, 2, 3, 4],
    [3, 4, 1, 2],
    [2, 1, 4, 3],
    [4, 3, 2, 1]
  ]
}
```

- Use `0` for an empty square.
- Use only integers from `0` through `4`.
- Provide exactly four rows of four entries.
- `intended_solution` is optional, but include it for generated tests.
- Accept a puzzle only when `solution_count` is `1` and `unique` is `true`.

