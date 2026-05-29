---
description: "Use when creating or editing Python code for the Metaphone PT-BR implementation to preserve current engine and rule semantics."
applyTo: "**/*.py"
---

# Python Implementation Instructions (Metaphone PT-BR)

Use these rules when implementing Python source files for this repository.

## Primary Reference

- Treat [AGENTS.md](AGENTS.md) as the top-level project policy.
- Treat [src/metaphone_pt/engine.py](src/metaphone_pt/engine.py), [src/metaphone_pt/ptbr.py](src/metaphone_pt/ptbr.py), and the regression tests under [tests](tests) as the behavior source of truth.

## Required Behavior

- Preserve rule order from the current implementation exactly.
- Preserve cursor/consumption behavior from `Translate`, `Ignore`, `Keep`, and `IgnoreNoMatches`.
- Preserve input preprocessing semantics:
  - lowercase conversion
  - accent removal
  - duplicate-letter collapsing equivalent to the configured `remove_multiples` calls
  - leading/trailing border spaces before iterative processing
- Preserve output formatting: uppercase code and trimmed final string.

## Implementation Constraints

- Keep a stateful engine abstraction and a PT-BR rule layer; do not flatten everything into a single function if it changes semantics.
- Prefer explicit regex anchors and deterministic matching over broad substitutions.
- Avoid refactors that alter matching granularity before parity tests pass.
- Avoid introducing SQL-specific concerns into Python algorithm logic.

## Test Expectations

- Add or update tests for every rule change.
- Prefer golden tests that capture known expected outputs.
- Include regression tests for edge classes: `r`, `s`, `z`, `x`, `ch`, `nh`, `lh`, `gu`, `sc`, `cao`, accents, and doubled letters.
