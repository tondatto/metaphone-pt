from metaphone_pt.engine import Metaphone


class EchoEngine(Metaphone):
    def prepare(self) -> None:
        self.remove_multiples("a")

    def algorithm(self) -> None:
        self.translate(r"\s(a)", self.THE_MATCH)
        self.translate("b", "X")
        self.ignore(self.VOWEL)


def test_blank_none_returns_empty() -> None:
    assert str(EchoEngine(None)) == ""


def test_blank_empty_returns_empty() -> None:
    assert str(EchoEngine("")) == ""


def test_border_space_keeps_initial_vowel_capture() -> None:
    assert str(EchoEngine("ab")) == "AX"


def test_remove_multiples_runs_before_algorithm() -> None:
    assert str(EchoEngine("aaab")) == "AX"
