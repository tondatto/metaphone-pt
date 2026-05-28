---
description: "Use when creating or editing Python code for the Metaphone PT-BR port to preserve parity with the legacy C# algorithm."
applyTo: "**/*.py"
---

# Python Port Instructions (Metaphone PT-BR)

Use these rules when implementing Python source files for this repository.

## Primary Reference

- Treat [AGENTS.md](AGENTS.md) as the top-level project policy.
- Treat [legacy/Metaphone.cs](legacy/Metaphone.cs) and [legacy/MetaphonePtBr.cs](legacy/MetaphonePtBr.cs) as behavior source of truth.

## Required Behavior Parity

- Preserve rule order from the C# algorithm exactly.
- Preserve cursor/consumption behavior from `Translate`, `Ignore`, `Keep`, and `IgnoreNoMatches`.
- Preserve input preprocessing semantics:
  - lowercase conversion
  - accent removal
  - duplicate-letter collapsing equivalent to legacy `RemoveMultiples`
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
