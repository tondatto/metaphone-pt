# metaphone-pt

A phonetic algorithm for Brazilian Portuguese names and words.

## Why not Soundex or standard Metaphone?

**Soundex** was designed for English and performs poorly on Portuguese — it ignores many consonant clusters, treats cedillas and accented vowels inconsistently, and conflates phonetically distinct Brazilian names.

**Standard Metaphone (and Double Metaphone)** similarly target English phonology. They miss key PT-BR patterns such as:

- `lh` → palatal lateral (`LH` sound, not plain `L`)
- `nh` → palatal nasal (like Spanish `ñ`)
- `ch` / `x` → `X` (as in *Xavier*, *Chico*)
- `ção`, `são` ending reductions
- `r` at word boundaries (silent or strongly rolled)
- Archaic spellings: `ph` → `F`, `th` → `T`, `y` → `I`

**metaphone-pt** implements rules specifically tuned for Brazilian Portuguese, including accent normalization and duplicate-letter collapsing, making it suitable for fuzzy matching of Brazilian names in databases and search applications.

## Project Scope

This repository maintains the Python implementation directly. The current behavior is defined by the engine and PT-BR rule set in `src/metaphone_pt/`, with regression tests in `tests/` protecting expected outputs.

## Installation

```bash
pip install metaphone-pt
```

Or, for local development:

```bash
git clone https://github.com/tondatto/metaphone-pt.git
cd metaphone-pt
pip install -e .[test]
```

## Usage

```python
from metaphone_pt import metaphone_ptbr

metaphone_ptbr("Xavier")                  # "XV2"
metaphone_ptbr("AYRTON SENNA DA SILVA")   # "ARTM SN D SLV"
metaphone_ptbr("HAIRTOM CENA DA SYLWA")   # "ARTM SN D SLV"  (same as above)
metaphone_ptbr("Ação")                    # "AS"
metaphone_ptbr("Queiroz")                 # "KRS"
```

Accented input is normalized before processing, and the output is always uppercase.

## Running the Tests

```bash
# Install with test dependencies
pip install -e .[test]

# Run the full test suite
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/test_ptbr_regression.py
pytest tests/test_engine_semantics.py
```

The regression suite (`tests/test_ptbr_regression.py`) validates expected outputs across a range of Portuguese names, accented input, and edge cases.

## Algorithm Overview

Processing pipeline per word:

1. Lowercase and remove Unicode accents (NFD normalization).
2. Collapse consecutive duplicate letters (`otto` → `oto`, `rizzo` → `rizo`).
3. Pad with a leading and trailing space to enable boundary-aware rules.
4. Apply ordered substitution rules left-to-right with a moving cursor.
5. Trim and uppercase the result.

Key substitutions include `ph→F`, `th→T`, `lh→L`, `nh→N`, `ch→X`, `x→S/X`, `gu→G`, `sc→S`, and vowel reduction at word boundaries.

## Project Structure

```
src/metaphone_pt/
    engine.py   # Cursor-driven rule engine
    ptbr.py     # Brazilian Portuguese rules
tests/
    test_ptbr_regression.py   # Golden output tests
    test_engine_semantics.py  # Engine behavior tests
```

## License

See [LICENSE](LICENSE) for details.
