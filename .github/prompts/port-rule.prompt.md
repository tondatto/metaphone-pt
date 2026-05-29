---
description: "Update one Metaphone PT-BR rule block in Python and generate regression tests."
---

# Update Rule Block With Regression Tests

Update one Metaphone PT-BR rule block in Python while preserving behavior exactly.

## Required Inputs

- Target rule snippet or behavior to change.
- Target Python file/module.
- Existing test file path.

## Procedure

1. Identify the exact current rule order around the target snippet.
2. Implement the smallest Python change that preserves cursor consumption and matching semantics.
3. Add regression tests for:
   - direct positive matches
   - near-miss cases that must not match
   - order-sensitive interactions with neighboring rules
4. Run tests and report results.

## Response Template

- Rule block updated: <short snippet summary>
- Python change: <what changed and why>
- Tests added: <test names and protected behavior>
- Validation: <commands run and pass/fail>
- Risk notes: <any remaining ambiguities>

Reference project policy in [AGENTS.md](AGENTS.md).
