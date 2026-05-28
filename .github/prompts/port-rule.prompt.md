---
description: "Port one Metaphone PT-BR rule block from legacy C# to Python and generate parity regression tests."
---

# Port Rule Block With Parity Tests

Port one rule block from legacy C# into Python while preserving behavior exactly.

## Required Inputs

- Legacy source file and rule snippet.
- Target Python file/module.
- Existing test file path.

## Procedure

1. Identify the exact legacy rule order around the target snippet.
2. Implement the smallest Python change that preserves cursor consumption and matching semantics.
3. Add regression tests for:
   - direct positive matches
   - near-miss cases that must not match
   - order-sensitive interactions with neighboring rules
4. Run tests and report results.

## Response Template

- Legacy rule mapped: <short snippet summary>
- Python change: <what changed and why>
- Tests added: <test names and protected behavior>
- Validation: <commands run and pass/fail>
- Risk notes: <any remaining ambiguities>

Reference project policy in [AGENTS.md](AGENTS.md).
