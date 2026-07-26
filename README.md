# Fourth Grade Learning Pages

An expandable collection of fourth-grade learning pages. The first subject area is **Logic**, beginning with an interactive Shapes lesson.

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
│   └── skills/
│       └── create-shape-number-card-tests/
│           ├── SKILL.md
│           ├── agents/openai.yaml
│           ├── references/puzzle-spec.md
│           └── scripts/validate_card_puzzle.py
└── .github/workflows/pages.yml
```

## Current learning page

The **Shapes** button on the Logic home page opens a complete lesson containing:

- an interactive clue-by-clue walkthrough;
- the SAME problem-solving method;
- a parent teaching script;
- four worked explanations;
- common mistakes and consistency checks.

## Add another Logic problem set

1. Add a new folder under `Logic/`, such as `Logic/patterns/`.
2. Put the new lesson in that folder as `index.html`.
3. Add a new topic card and button to the root `index.html`.
4. Push the changes to `main`; the Pages workflow will redeploy the site.

## Test-maker skill

`Logic/skills/create-shape-number-card-tests/` contains the reusable skill and deterministic validator for creating original shape-number-card tests with explained answer keys.
