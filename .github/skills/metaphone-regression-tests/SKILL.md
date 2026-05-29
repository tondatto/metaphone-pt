---
name: metaphone-regression-tests
description: "Use when creating or updating deterministic regression tests for Metaphone PT-BR behavior."
---

# Metaphone Regression Tests

## Purpose

Create and maintain deterministic tests that prevent behavior drift in the Python Metaphone PT-BR implementation.

## Inputs

- Python module(s) currently under test.
- Rule definitions in [src/metaphone_pt/engine.py](src/metaphone_pt/engine.py) and [src/metaphone_pt/ptbr.py](src/metaphone_pt/ptbr.py).
- Existing regression tests in [tests/test_engine_semantics.py](tests/test_engine_semantics.py) and [tests/test_ptbr_regression.py](tests/test_ptbr_regression.py).
- Optional list of names/phrases to prioritize.

## Workflow

1. Inspect changed Python rules and map them to the affected engine and PT-BR rule blocks.
2. Build or update a compact golden-case table:
   - normal names
   - accented names
   - duplicated letters
   - start/end-sensitive consonant cases (`r`, `s`, `z`, `x`)
   - digraph clusters (`ch`, `nh`, `lh`, `gu`, `sc`)
3. Add or update unit tests that assert exact code outputs.
4. Run tests and report mismatches grouped by likely rule family.
5. If mismatches are found, propose minimal rule-order-preserving fixes.

## Output Format

- Short summary of regression status.
- List of added/updated tests and what each protects.
- List of any unresolved divergences with likely source rule.

## Guardrails

- Do not approve behavior-changing refactors without test evidence.
- Keep tests deterministic and explicit; avoid fuzzy assertions.
- Prefer adding focused regression tests over broad snapshot churn.
