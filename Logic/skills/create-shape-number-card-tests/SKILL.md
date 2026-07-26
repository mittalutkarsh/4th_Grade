---
name: create-shape-number-card-tests
description: Create original elementary, fourth-grade, or fifth-grade shape-number card logic tests, worksheets, practice sets, and answer keys in which each double-sided card has one shape and one number, then cards are flipped and shuffled between two views. Use when generating, varying, validating, solving, or explaining these card-inventory puzzles; when a test needs diagrams, mixed difficulty, unique answers, or child-friendly step-by-step explanations; or when producing a printable HTML, PDF, DOCX, or presentation version.
---

# Create Shape-Number Card Tests

Create logically valid tests about the same physical double-sided cards shown in two shuffled arrangements. Make every answer uniquely deducible from the visible information.

## Apply the invariant

Treat each row as a photograph of the same card collection:

- Keep the number of physical cards constant.
- Give every card exactly one shape side and one number side.
- Allow cards to flip and move between views.
- Ignore left-to-right position after shuffling.
- Count duplicate symbols with multiplicity.
- Never assume matching visible symbols in two views belong to the same card.

Use the child-facing SAME method:

1. **Same cards** - count the physical cards.
2. **Arrange clues** - build shape and number inventories.
3. **Mark changes** - note disappearing, appearing, and simultaneous symbols.
4. **Eliminate** - cross out impossible sides, use the leftover, and check both views.

## Choose defaults

Honor the user's requested count, grade, difficulty, output format, and question types. If omitted, use:

- 10 questions
- Grade 5 language
- 3 or 4 cards per question
- Mixed difficulty
- Questions first and a separate answer key afterward
- Approximately 40% hidden-side inventory questions, 30% disappearing-symbol questions, and 30% number-property questions
- Shapes from triangle, square, circle, star, diamond, and heart
- Small positive whole numbers

Ask a clarifying question only when a missing choice would materially change the deliverable. Otherwise use these defaults.

## Generate each puzzle

1. Create the underlying physical cards as `(shape, number)` pairs.
2. Choose which side of each card is visible in view 1.
3. Flip zero or more cards for view 2, but require at least one useful change.
4. Shuffle the order independently in each view.
5. Select one question target:
   - hidden shape behind a visible number;
   - hidden number behind a visible shape;
   - count of odd, even, greater-than, less-than, or multiple-of number sides.
6. Derive the answer from the two visible views only.
7. Validate uniqueness before accepting the item.
8. Reject and regenerate an ambiguous, impossible, or accidentally under-specified item.

Use duplicate shapes or numbers only when they create an intentional reasoning step. Introduce duplicates mainly in medium and challenge questions.

## Validate every item

Read [references/puzzle-spec.md](references/puzzle-spec.md) when constructing validator input or diagnosing an ambiguous puzzle.

Run:

```bash
python3 scripts/validate_card_puzzle.py puzzle.json
```

Require all of the following:

- `valid_mapping_count` is greater than zero.
- `solvable` is `true`.
- `unknown_possible` is `false`.
- `unique_answers` contains exactly one answer.
- The unique answer equals the intended answer.

Do not publish a question that fails validation. Fix or regenerate it, then rerun the validator.

For a batch, validate every question rather than sampling.

## Control difficulty

### Easy

- Use 3 cards.
- Use distinct shapes and numbers.
- Make one symbol disappear and leave one obvious opposite-side candidate.
- Require one or two deductions.

### Medium

- Use 4 cards.
- Include one repeated shape or number.
- Require a complete inventory followed by elimination.
- Require two or three deductions.

### Challenge

- Use 4 or 5 cards.
- Include duplicates deliberately.
- Ask for a property count or require combining complementary groups across both views.
- Require three or four deductions, but keep the answer unique.

Do not create trick questions based on wording, visual position, or information unavailable to the learner.

## Draw the questions

Show each arrangement as a separate labeled row of equal-sized cards:

- `First arrangement`
- `Second arrangement - same cards, flipped and mixed`

Use large, unambiguous symbols and numbers. Keep the answer and hidden pairing out of the question section. If creating HTML, make it self-contained and printable. If creating DOCX or PDF, render and visually verify the final pages with the corresponding document skill.

## Write the answer key

For every question, include:

1. **Notice** - the exact visible evidence.
2. **Think** - the question the child should ask.
3. **Why** - the invariant or elimination rule.
4. **Eliminate** - which candidates cannot work.
5. **Answer** - the final response in a complete sentence.
6. **Check** - a short consistency check against both views.

Use grade-level language. Explain the logic rather than saying only that an item is “obvious” or “the only answer.”

## Quality gate

Before delivery:

- Confirm that both views contain the same number of cards.
- Confirm that each visible token is clearly a shape or a number.
- Confirm that no same physical card would require two different shapes or two different numbers.
- Confirm that duplicate symbols are counted correctly.
- Confirm that the explanation does not match cards by position.
- Confirm that the question text identifies the target unambiguously.
- Confirm that questions are original variations rather than copies of a supplied worksheet.
- Confirm that the answer key is separate from the student questions.
- Confirm that every accepted puzzle passed deterministic validation.
