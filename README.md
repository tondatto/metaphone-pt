# metaphone-pt

Python port of a Brazilian Portuguese metaphone algorithm.

## Status

This repository is currently focused on parity with legacy C# behavior in `legacy/`.

## Quick Start

```bash
python -m pip install -e .[test]
pytest
```

## Usage

```python
from metaphone_pt import metaphone_ptbr

code = metaphone_ptbr("Xavier")
print(code)  # XV2
```
