# AGENTS.md

## Project Purpose

Build a Python library that converts input text to a phonetic code specialized for Brazilian Portuguese.

The current reference implementation is legacy C# code originally used as a SQL Server CLR function.

## Source Of Truth

- `legacy/Metaphone.cs`: abstract transformation engine (`Translate`, `Ignore`, `Keep`, cursor-based processing, regex matching, accent and duplicate handling).
- `legacy/MetaphonePtBr.cs`: Brazilian Portuguese phonetic rules and ordering.
- `legacy/MetaphoneSqlFunction.cs`: SQL wrapper only; not part of core algorithm behavior.

When behavior is ambiguous, preserve outputs produced by `MetaphonePtBr` + `Metaphone` core logic.

## Non-Negotiable Porting Rules

- Preserve rule order exactly. The algorithm is order-sensitive.
- Preserve cursor consumption semantics from `Translate` and `IgnoreNoMatches`.
- Preserve border-space behavior (`" " + transformed + " "`) before processing.
- Preserve uppercase output and final trim behavior.
- Preserve placeholder symbols used by the original algorithm (`1`, `2`, `3`, `X`, `KS`, etc.).
- Keep vowel/non-vowel classes behavior equivalent to the C# constants.

## Python Implementation Guidance

- Use `re` carefully to emulate C# `Regex.Match` + anchored look-ahead/look-behind checks used in `Translate`.
- Keep architecture split similar to legacy:
  - Base engine class (stateful, cursor-driven matching/consumption).
  - PT-BR rule class containing only rule setup and sequence.
- Normalize text before rules:
  - lowercase
  - remove accents
  - collapse repeated letters listed by the original `RemoveMultiples` call
- Avoid introducing language-specific shortcuts that change outputs, even if they look cleaner.

## Testing Strategy (Required)

- Create golden tests from representative Portuguese names and tricky edge cases seen in comments in `legacy/MetaphonePtBr.cs`.
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
- Do not treat SQL wrapper concerns as algorithm requirements.
- Be careful with character encoding when copying legacy accent patterns; prefer explicit Unicode-safe normalization in Python.

## Current Repository State

- No build/test tooling is defined yet.
- If adding tooling, prefer:
  - `pytest` for tests
  - minimal packaging (`pyproject.toml`)
  - deterministic tests focused on output parity with legacy behavior
