from __future__ import annotations

from abc import ABC, abstractmethod
import re


class Metaphone(ABC):
    THE_MATCH = "$0"
    VOWEL = "[aeiouy]"
    NON_VOWEL = "[^aeiouy]"

    def __init__(self, text: str | None) -> None:
        self._original = text
        self._transformed = text
        self._result: list[str] = []
        self._current_position = 0
        self._had_matches = False
        self._current_match = ""

    @abstractmethod
    def prepare(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def algorithm(self) -> None:
        raise NotImplementedError

    def _calculate(self) -> None:
        if self._blank:
            return

        self._all_lower_case()
        self.remove_accents()
        self.prepare()
        self._add_space_to_borders()

        while self._not_fully_processed:
            self.keep(" ")
            self.algorithm()
            self._ignore_no_matches()

    @property
    def _fully_processed(self) -> bool:
        assert self._transformed is not None
        return self._current_position >= len(self._transformed)

    @property
    def _not_fully_processed(self) -> bool:
        return not self._fully_processed

    def _ignore_no_matches(self) -> None:
        if not self._had_matches:
            self._current_position += 1
        self._had_matches = False

    def translate(self, pattern: str, subst: str) -> None:
        if self._fully_processed or self._had_matches:
            return

        if re.search(r".+\(.*", pattern):
            split = pattern.index("(")
            self._look_behind(pattern[:split])
            if self._had_matches:
                self._look_ahead(pattern[split:])
        else:
            self._look_ahead(pattern)

        if not self._had_matches:
            return

        replacement = self._current_match if subst == self.THE_MATCH else subst
        self._consume(self._current_match)
        self._result.append(replacement.upper())

    def _consume(self, match: str) -> None:
        self._current_position += len(match)

    def ignore(self, pattern: str) -> None:
        self.translate(pattern, "")

    def keep(self, *patterns: str) -> None:
        self.translate(f"({'|'.join(patterns)})", self.THE_MATCH)

    def _matches(self, pattern: str, text: str) -> bool:
        match = re.search(pattern, text)
        self._had_matches = match is not None

        if self._had_matches:
            assert match is not None
            self._current_match = match.group(0)

        return self._had_matches

    def _look_ahead(self, pattern: str) -> None:
        self._matches("^" + pattern, self._ahead_string())

    def _look_behind(self, pattern: str) -> None:
        self._matches(pattern + "$", self._behind_string())

    def _ahead_string(self) -> str:
        assert self._transformed is not None
        return self._transformed[self._current_position :]

    def _behind_string(self) -> str:
        assert self._transformed is not None
        return self._transformed[: self._current_position]

    @property
    def _blank(self) -> bool:
        return self._transformed is None or len(self._transformed) == 0

    def remove_accents(self) -> None:
        assert self._transformed is not None
        substitutions = {
            "a": "[áàâãäå]",
            "e": "[éèêë]",
            "i": "[íìîï]",
            "o": "[óòôõö]",
            "u": "[úùûü]",
        }
        for replacement, pattern in substitutions.items():
            self._transformed = re.sub(pattern, replacement, self._transformed)

    def remove_multiples(self, *letters: str) -> None:
        assert self._transformed is not None
        for letter in letters:
            pattern = re.escape(letter) + r"{2,}"
            self._transformed = re.sub(pattern, letter, self._transformed, flags=re.IGNORECASE)

    def _add_space_to_borders(self) -> None:
        assert self._transformed is not None
        self._transformed = f" {self._transformed} "

    def _all_lower_case(self) -> None:
        assert self._transformed is not None
        self._transformed = self._transformed.lower()

    def __str__(self) -> str:
        self._calculate()
        return "".join(self._result).strip()
