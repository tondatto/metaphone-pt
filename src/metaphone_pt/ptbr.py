from __future__ import annotations

from .engine import Metaphone


class MetaphonePtBr(Metaphone):
    def prepare(self) -> None:
        self.remove_multiples(
            " ",
            "b",
            "c",
            "g",
            "l",
            "t",
            "p",
            "d",
            "f",
            "j",
            "k",
            "m",
            "v",
            "n",
            "z",
        )

    def algorithm(self) -> None:
        self.translate("ph", "F")
        self.translate("th", "T")

        self.translate("lh", "1")
        self.ignore("(l)" + self.NON_VOWEL)
        self.translate("l", "L")

        self.translate("g[eiy]", "J")
        self.translate("g[ao]", "G")
        self.translate("gu[ei]", "G")
        self.translate("g", "G")

        self.translate("cao", "S")
        self.translate(r"l(chior)\s", "K2")
        self.translate("ch", "X")
        self.translate("ck", "K")
        self.translate("cq", "K")
        self.translate("c[eiy]", "S")
        self.translate("c[aou]", "K")
        self.translate("c", "K")
        self.translate("ç", "S")

        self.translate("rr", "2")
        self.translate(r"\s(r)", "2")
        self.translate(r"(r)\s", "2")
        self.translate("r", "R")

        self.translate(r"(z)\s", "S")
        self.translate("z", "Z")

        self.translate(r"(n)\s", "M")
        self.translate("nh", "3")
        self.translate("n", "N")

        self.translate("ss", "S")
        self.translate(r"\s(s)", "S")
        self.translate(r"(s)\s", "S")
        self.translate("sh", "X")
        self.translate(self.VOWEL + "(s)" + self.VOWEL, "Z")
        self.translate("sc[ei]", "S")
        self.translate("sc[aou]", "SC")
        self.translate("s", "S")

        self.translate("[ckglrxaeiou][aeiou](x)", "X")
        self.translate(r"\s(x)", "X")
        self.translate(r"x\s", "KS")
        self.translate("xc[ei]", "S")
        self.translate(r"\se(x)" + self.VOWEL, "Z")
        self.translate(r"\se(x)" + self.NON_VOWEL, "S")
        self.translate("x[ei]", "X")
        self.translate("x[aou]", "KS")
        self.translate("x", "KS")

        self.translate("q", "K")
        self.translate(r"\sh(" + self.VOWEL + ")", self.THE_MATCH)
        self.translate("w" + self.VOWEL, "V")
        self.ignore("h")

        self.keep("b", "t", "p", "d", "f", "j", "k", "m", "v")

        self.translate(r"\s(" + self.VOWEL + ")", self.THE_MATCH)

        self.ignore(self.VOWEL)


def metaphone_ptbr(text: str | None) -> str:
    return str(MetaphonePtBr(text))
