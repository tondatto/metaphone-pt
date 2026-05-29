# metaphone-pt

Phonetic encoding for Brazilian Portuguese names and words.

`metaphone-pt` converts text into a compact phonetic key. The goal is not to reproduce pronunciation exactly, but to group spellings that are likely to sound alike so they can be searched, compared, or deduplicated more effectively.

## What is Metaphone?

Metaphone is a family of phonetic algorithms introduced by Lawrence Philips. Instead of indexing a word by its exact spelling, Metaphone reduces it to a sound-oriented code. In practice, this makes fuzzy lookup much cheaper: many spelling variants collapse into the same key, and a second-pass similarity check can run on a much smaller candidate set.

This repository applies that idea to Brazilian Portuguese, where pronunciation rules differ substantially from the English-focused assumptions behind Soundex and standard Metaphone.

## Why a PT-BR variant?

**Soundex** was designed for English and performs poorly on Portuguese. It ignores important consonant clusters, handles accents badly, and tends to over-collapse names that are distinct in Brazilian Portuguese.

**Standard Metaphone (and Double Metaphone)** are also centered on English phonology. They do not model several common PT-BR sound patterns well, including:

- `lh`, a palatal lateral that is not the same as plain `l`
- `nh`, a palatal nasal similar to Spanish `ñ`
- `ch` and many `x` cases, which often map to a `sh`-like sound
- final reductions such as `ção`
- `r` at the beginning or end of a word
- spelling variants such as `ph → f`, `th → t`, and `y → i`

This implementation adds Portuguese-specific rules, accent normalization, and duplicate-letter collapsing so that names such as `Ayrton` and `Hairtom` can converge to the same phonetic key.

## Installation

```bash
python3 -m pip install metaphone-pt
```

For local development:

```bash
git clone https://github.com/tondatto/metaphone-pt.git
cd metaphone-pt
python3 -m pip install -e .[test]
```

## Usage

```python
from metaphone_pt import metaphone_ptbr

metaphone_ptbr("Xavier")
# "XV2"

metaphone_ptbr("AYRTON SENNA DA SILVA")
# "ARTM SN D SLV"

metaphone_ptbr("HAIRTOM CENA DA SYLWA")
# "ARTM SN D SLV"

metaphone_ptbr("Ação")
# "AS"

metaphone_ptbr("Queiroz")
# "KRS"
```

Input is normalized before processing, and the returned code is always uppercase.

## How the Algorithm Works

At a high level, each word goes through these steps:

1. Convert to lowercase.
2. Remove Portuguese accents.
3. Collapse configured duplicate letters such as `tt`, `zz`, or `ll`.
4. Add border spaces so start-of-word and end-of-word rules can be matched consistently.
5. Walk the text left to right, applying the first matching rule at each cursor position.
6. Emit a phonetic symbol, skip a symbol, or consume multiple characters depending on the matched rule.
7. Trim the result and return it in uppercase.

This is a rule-ordered algorithm. The same letter may produce different symbols depending on its neighbors and whether it appears at the beginning, middle, or end of a word.

## Rule Notation

When discussing rules, the following shorthand is useful:

| Notation | Meaning |
| --- | --- |
| `^` | Beginning of a word |
| `$` | End of a word |
| `V` | Any vowel |
| `C` | Any consonant |
| `[EIY]` | Any one of the listed letters |
| `->` | Produces the symbol on the right |
| `0` | Ignored, no output symbol is emitted |

These notations are conceptual. The actual implementation uses a cursor-driven engine with regex-like patterns.

## Output Symbols

The generated code uses both ordinary letters and a few symbolic placeholders to represent Portuguese-specific sounds:

| Symbol | Meaning | Typical examples |
| --- | --- | --- |
| `1` | `LH` sound | `filho`, `trabalho` |
| `2` | Strong or word-edge `R` | `Raul`, `amor` |
| `3` | `NH` sound | `nhoque`, `manhã` |
| `X` | `CH` / `SH` / soft `X` sound | `Chico`, `Xuxa` |
| `KS` | Explicit `ks` sound cluster | `Alex`, `sexo` |

These symbols are search conventions, not IPA transcription.

## Representative Rule Sketches

Some simplified examples of the transformations used by the algorithm:

| Rule sketch | Meaning |
| --- | --- |
| `^V -> V` | Keep an initial vowel |
| `PH -> F` | Treat archaic `ph` as `f` |
| `TH -> T` | Treat archaic `th` as `t` |
| `C[EIY] -> S` | Soft `c` before front vowels |
| `C[AOU] -> K` | Hard `c` before back vowels |
| `LH -> 1` | Encode palatal `lh` |
| `NH -> 3` | Encode palatal `nh` |
| `^R -> 2` | Encode initial `r` as strong `r` |
| `R$ -> 2` | Encode final `r` as strong `r` |
| `Z$ -> S` | Final `z` behaves like `s` |

The real implementation is more detailed and order-sensitive than this summary, especially for `x`, `s`, `r`, `sc`, and foreign-name spellings.

## Running the Tests

```bash
# Install with test dependencies
python3 -m pip install -e .[test]

# Run the full test suite
python3 -m pytest -q

# Run with verbose output
python3 -m pytest -v

# Run a specific test file
python3 -m pytest tests/test_ptbr_regression.py -q
python3 -m pytest tests/test_engine_semantics.py -q
```

The regression suite checks expected outputs for representative Portuguese names, accents, duplicated letters, and boundary-sensitive cases such as `r`, `s`, `z`, and `x`.

## Project Structure

```text
src/metaphone_pt/
    engine.py   # Cursor-driven rule engine
    ptbr.py     # Brazilian Portuguese rule set
tests/
    test_ptbr_regression.py   # Golden output tests
    test_engine_semantics.py  # Engine behavior tests
```
