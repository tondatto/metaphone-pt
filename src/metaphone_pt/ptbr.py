from __future__ import annotations

from .engine import Metaphone


class MetaphonePtBr(Metaphone):
    CONSONANT = "[bcdfghjklmnpqrstvwxyz]"

    def prepare(self) -> None:
        """Prepares the text for processing by the algorithm.
           This duplicated letters are just a headache. Before starting, we remove the excess.
           Otto, Rizzo, Millene, Riccardo
        """
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
        assert self._transformed is not None
        self._transformed = self._transformed.replace("y", "i")

    def algorithm(self) -> None:
        """The main algorithm of the Metaphone for Brazilian Portuguese."""

        # Older names
        self.translate("ph", "F") # Alphonso
        self.translate("th", "T") # Martha

        self.translate("lh", "1")
        self.translate("l[vw]", "LV") # Silva, Sylwa
        self.ignore("(l)" + self.NON_VOWEL) # Galdêncio or Gaudêncio? Discard the L in this case, but keep it in others, like "Luiz"
        self.translate("l", "L")

        self.translate("g[eiy]", "J")
        self.translate("g[ao]", "G")
        self.translate("gu[ei]", "G")
        self.translate("g", "G")
        
        # "ção" is a very common suffix in Portuguese, and it sounds like "são". So we translate it to "S". But we also have to take care of words like "coração", which should be translated to "KR2SÃO", not "KR2S". So we have to make sure that the "ção" is at the end of the word, or followed by a space.
        self.translate("cao", "S")

        self.translate(r"l(chior)\s", "K2") # Belchior (Belkior not Belxior). Melchior
        self.translate("ch", "X")
        self.translate("ck", "K") # Jackeline, Jackson
        self.translate("cq", "K") # Jacques, Jacquin
        self.translate("c[eiy]", "S")
        self.translate("c[aou]", "K")
        self.translate("c", "K")
        self.translate("ç", "S")

        self.translate("rr", "2")
        self.translate(self.WORD_START + "(r)", "2") # Raul, Régis
        self.translate("(r)(?=l)", "2")
        self.translate("(r)" + self.WORD_END, "2") # Adamastor, Maber
        self.translate("r", "R") # Maria, Marcelo

        self.translate("(z)" + self.WORD_END, "S") # Luiz, Tomaz
        self.translate("z", "Z")

        self.translate("(n)" + self.WORD_END, "M") # Renan
        self.translate("nh", "3")
        self.translate("n", "N")

        self.translate(self.WORD_START + "([ei]s)(?=" + self.CONSONANT + ")", "S")
        self.translate(self.VOWEL + "(s)" + self.VOWEL, "Z") # asa, Isabel
        self.translate("ss", "S")
        self.translate(self.WORD_START + "(s)", "S") # Sebastião, Sérgio
        self.translate("(s)" + self.WORD_END, "S") # Marcos
        self.translate("sh", "X") # Shakespeare, Shakira, but also "sheriff" and "shampoo", which are common words in Portuguese. So we translate "sh" to "X", but we also have to take care of words like "sheriff" and "shampoo", which should be translated to "XERIF" and "XAMPU", not "XERIF" and "XAMPU". So we have to make sure that the "sh" is at the beginning of the word, or followed by a space.
        self.translate("sc[ei]", "S") # Ascenso, Asceta
        self.translate("sc[aou]", "SC") # Mascarenhas
        self.translate("s", "S")

        # X is a very tricky letter in Portuguese. It can be pronounced as "s", "z", "ks", "ch", "sh", "j", "g", "x". So we have to take care of all the cases. And we also have to take care of words like "xará", which should be translated to "KSARÁ", not "KSAR". So we have to make sure that the "x" is at the end of the word, or followed by a space.

        # Some syllables like "ca", "ai" or "ei" before the "X" seam to make it sound like "KS", while others like "e" or "i" seam to make it sound like "S". So we have to take care of all the cases.
        self.translate("[ckglrxaeiou][aeiou](x)", "X") # Abacaxi, Aleixo, Alexandre
        self.translate(self.WORD_START + "(x)", "X") # Xavier, Xuxa
        self.translate("(x)" + self.WORD_END, "KS") # Félix, Max
        self.translate("xc[ei]", "S") # Excelsior, Exceção
        self.translate(self.WORD_START + "e(x)" + self.VOWEL, "Z") # Exemplo, Exame
        self.translate(self.WORD_START + "e(x)" + self.NON_VOWEL, "S") # Êxtase, Exposição
        self.translate("x[ei]", "X") 
        self.translate("x[aou]", "KS") # Sexo, Anexo
        self.translate("x", "KS") # all other cases

        self.translate("q", "K")
        self.translate(self.WORD_START + "h(" + self.VOWEL + ")", self.THE_MATCH)
        self.translate("w" + self.VOWEL, "V")
        self.ignore("h")

        # This consonants are pronounced as they are written, so we just keep them. 
        self.keep("b", "t", "p", "d", "f", "j", "k", "m", "v")

        # Vowels are only kept if they are at the beginning of the word
        self.translate(self.WORD_START + "(" + self.VOWEL + ")", self.THE_MATCH)

        self.ignore(self.VOWEL)


def metaphone_ptbr(text: str | None) -> str:
    return str(MetaphonePtBr(text))
