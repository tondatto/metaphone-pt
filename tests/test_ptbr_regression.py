import pytest

from metaphone_pt.ptbr import metaphone_ptbr


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (None, ""),
        ("", ""),
        ("Martha", "MRT"),
        ("Alphonso", "ANS"),
        ("Raul", "2"),
        ("Luiz", "LS"),
        ("Renan", "2NM"),
        ("Xavier", "XV2"),
        ("Alex", "ALX"),
        ("Queiroz", "KRS"),
        ("Ação", "AS"),
        ("AYRTON SENNA DA SILVA", "ARTM SN D SLV"),
        ("HAIRTOM CENA DA SYLWA", "ARTM SN D SLV"),
    ],
)
def test_regression_cases(text: str | None, expected: str) -> None:
    assert metaphone_ptbr(text) == expected
