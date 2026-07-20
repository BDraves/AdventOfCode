from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from solution import Solution

def is_pair(number: int) -> bool:
    text = str(number)

    if len(text) % 2 != 0:
        return False

    middle = len(text) // 2
    return text[:middle] == text[middle:]

def has_any_repeated_pairs(number: int) -> bool:
    text = str(number)

    for pattern_length in range(1, len(text) // 2 + 1):
        if len(text) % pattern_length != 0:
            continue

        pattern = text[:pattern_length]
        repetitions = len(text) // pattern_length

        if pattern * repetitions == text:
            return True

    return False

@dataclass(frozen=True)
class Range:
    start: int
    end: int

    @classmethod
    def from_string(cls, s: str) -> Range:
        start, end = map(int, s.split("-"))
        return cls(start, end)

class Day02(Solution):
    year = 2025
    day = 2

    def format_input(self, raw: str) -> list[Range]:
        return [Range.from_string(line) for line in raw.split(",")]

    def part1(self) -> Any:
        return sum(
            number
            for interval in self.input
            for number in range(interval.start, interval.end + 1)
            if is_pair(number)
        )

    def part2(self) -> Any:
        return sum(
            number
            for interval in self.input
            for number in range(interval.start, interval.end + 1)
            if has_any_repeated_pairs(number)
        )
