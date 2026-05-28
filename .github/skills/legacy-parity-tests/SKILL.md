---
name: legacy-parity-tests
description: "Use when creating or updating parity tests between Python implementation and legacy C# Metaphone PT-BR behavior."
---

# Legacy Parity Tests

## Purpose

Create and maintain deterministic tests that prevent behavior drift while porting legacy C# metaphone logic to Python.

## Inputs

- Python module(s) currently under test.
- Legacy behavior references in [legacy/Metaphone.cs](legacy/Metaphone.cs) and [legacy/MetaphonePtBr.cs](legacy/MetaphonePtBr.cs).
- Optional list of names/phrases to prioritize.

## Workflow

1. Inspect changed Python rules and map them to equivalent legacy rule blocks.
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

- Short summary of parity status.
- List of added/updated tests and what each protects.
- List of any unresolved divergences with likely source rule.

## Guardrails

- Do not approve behavior-changing refactors without test evidence.
- Keep tests deterministic and explicit; avoid fuzzy assertions.
- Prefer adding focused regression tests over broad snapshot churn.
