from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from solution import Solution


def is_pair(id: int) -> bool:
    # Cut the number in half
    length: int = len(id)
    first: str = str(id)[0:length//2]
    last: str = str(id)[(length//2)+1:]
    return first == last

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
        return sum([i for i in self.input if is_pair(i)])

    def part2(self) -> Any:
        raise NotImplementedError
