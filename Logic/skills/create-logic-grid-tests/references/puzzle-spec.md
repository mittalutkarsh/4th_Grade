# Logic-grid validator specification

Represent each clue as a relationship between category values:

```json
{
  "anchor": "people",
  "ordered_category": "order",
  "categories": {
    "people": ["Maya", "Noah", "Priya"],
    "pets": ["Cat", "Dog", "Rabbit"],
    "order": ["First", "Second", "Third"]
  },
  "clues": [
    {
      "type": "match",
      "a": {"category": "people", "value": "Noah"},
      "b": {"category": "order", "value": "Second"}
    },
    {
      "type": "immediately_before",
      "a": {"category": "pets", "value": "Rabbit"},
      "b": {"category": "pets", "value": "Dog"}
    },
    {
      "type": "not_match",
      "a": {"category": "people", "value": "Maya"},
      "b": {"category": "pets", "value": "Cat"}
    }
  ],
  "intended_solution": {
    "Maya": {"pets": "Rabbit", "order": "First"},
    "Noah": {"pets": "Dog", "order": "Second"},
    "Priya": {"pets": "Cat", "order": "Third"}
  }
}
```

- Keep all categories the same size.
- Order values in `ordered_category` from earliest to latest.
- Supported clue types: `match`, `not_match`, `before`, and `immediately_before`.
- Each `a` and `b` reference must name a category and one of its values.
- Limit the anchor category to five values for practical enumeration.
- Include `intended_solution` for generated tests.

