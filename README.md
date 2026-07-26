# Fourth Grade Learning Pages

An expandable collection of fourth-grade learning pages. The first subject area is **Logic**, with interactive lessons that teach a repeatable reasoning method for each puzzle family.

## Live site

Once GitHub Pages finishes deploying:

<https://mittalutkarsh.github.io/4th_Grade/>

## Repository structure

```text
.
├── index.html
├── Logic/
│   ├── shapes/
│   │   └── index.html
│   ├── sudoku/
│   │   └── index.html
│   ├── minesweeper/
│   │   └── index.html
│   ├── logic-grid/
│   │   └── index.html
│   └── skills/
│       ├── create-shape-number-card-tests/
│       ├── create-four-by-four-sudoku-tests/
│       ├── create-minesweeper-logic-tests/
│       └── create-logic-grid-tests/
└── .github/workflows/pages.yml
```

## Current learning pages

The Logic home page currently links to:

- **Shapes** - the SAME inventory-and-elimination method;
- **4x4 Sudoku** - the SCAN row-column-box method;
- **Minesweeper Logic** - the COUNT neighboring-mines method;
- **Logic Grids** - the GRID checkmark-and-cross method.

Each lesson includes clickable reasoning steps, parent prompts, a worked example, practice interaction, and consistency checks.

## Add another Logic problem set

1. Add a new folder under `Logic/`, such as `Logic/patterns/`.
2. Put the new lesson in that folder as `index.html`.
3. Add a new topic card and button to the root `index.html`.
4. Push the changes to `main`; the Pages workflow will redeploy the site.

## Test-maker skills

Each folder under `Logic/skills/` contains a reusable test-generation skill, a puzzle specification, and a deterministic validator. The validators reject ambiguous puzzles before they are added to a worksheet or lesson.
