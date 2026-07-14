from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from solution import Solution

DIAL_SIZE = 100
START_POSITION = 50


@dataclass(frozen=True)
class Turn:
    direction: str
    distance: int

    @classmethod
    def parse(cls, line: str) -> Turn:
        return cls(direction=line[0], distance=int(line[1:]))

    def apply(self, position: int) -> int:
        if self.direction == "L":
            return (position - self.distance) % DIAL_SIZE
        return (position + self.distance) % DIAL_SIZE

    def zero_crossings_from(self, position: int) -> int:
        first_zero = position if self.direction == "L" else -position % DIAL_SIZE
        if first_zero == 0:
            first_zero = DIAL_SIZE

        if self.distance < first_zero:
            return 0

        return 1 + (self.distance - first_zero) // DIAL_SIZE


class Day01(Solution[list[Turn]]):
    year = 2025
    day = 1

    def format_input(self, raw: str) -> list[Turn]:
        return [Turn.parse(line) for line in raw.splitlines()]

    def end_positions(self) -> list[int]:
        positions: list[int] = []
        position = START_POSITION
        for turn in self.input:
            position = turn.apply(position)
            positions.append(position)

        return positions

    def part1(self) -> Any:
        return sum(position == 0 for position in self.end_positions())

    def part2(self) -> Any:
        total = 0
        position = START_POSITION

        for turn in self.input:
            total += turn.zero_crossings_from(position)
            position = turn.apply(position)

        return total
