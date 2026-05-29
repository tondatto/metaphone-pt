# AGENTS.md

## Project Purpose

Build a Python library that converts input text to a phonetic code specialized for Brazilian Portuguese.

The repository maintains the Python implementation directly.

## Source Of Truth

- `src/metaphone_pt/engine.py`: transformation engine (`Translate`, `Ignore`, `Keep`, cursor-based processing, regex matching, accent handling, duplicate collapsing).
- `src/metaphone_pt/ptbr.py`: Brazilian Portuguese phonetic rules and ordering.
- `tests/test_engine_semantics.py`: engine behavior invariants.
- `tests/test_ptbr_regression.py`: golden outputs for names, phrases, accents, and edge cases.

When behavior is ambiguous, preserve outputs validated by the current engine, rule ordering, and regression tests.

## Non-Negotiable Algorithm Rules

- Preserve rule order exactly. The algorithm is order-sensitive.
- Preserve cursor consumption semantics from `Translate` and `IgnoreNoMatches`.
- Preserve border-space behavior (`" " + transformed + " "`) before processing.
- Preserve uppercase output and final trim behavior.
- Preserve placeholder symbols used by the algorithm (`1`, `2`, `3`, `X`, `KS`, etc.).
- Keep vowel/non-vowel classes behavior equivalent to the engine constants.

## Python Implementation Guidance

- Use `re` carefully to preserve the anchored look-ahead/look-behind checks used in `Translate`.
- Keep architecture split similar to the current implementation:
  - Base engine class (stateful, cursor-driven matching/consumption).
  - PT-BR rule class containing only rule setup and sequence.
- Normalize text before rules:
  - lowercase
  - remove accents
  - collapse repeated letters listed by `prepare()` / `remove_multiples()`
- Avoid introducing language-specific shortcuts that change outputs, even if they look cleaner.

## Testing Strategy (Required)

- Create golden tests from representative Portuguese names and tricky edge cases covered by current rules and comments.
- Add regression tests whenever a rule is changed.
- Verify edge behavior:
  - empty/null-ish input
  - names with accents
  - duplicated letters
  - start/end-of-word `r`, `s`, `z`, `x` handling
  - `ch`, `nh`, `lh`, `gu`, `sc`, and `cao` cases

## Common Pitfalls

- Do not simplify rule expressions before test parity is achieved.
- Do not convert the engine into token-based parsing that skips current cursor semantics.
- Be careful with character encoding during accent normalization; prefer explicit Unicode-safe normalization in Python.

## Current Repository State

- Test tooling is configured in `pyproject.toml`.
- Preferred validation commands:
  - `python3 -m pytest -q`
  - `python3 -m pytest tests/test_ptbr_regression.py -q`
  - `python3 -m pytest tests/test_engine_semantics.py -q`
