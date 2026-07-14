from typing import Any

from solution import LineSolution


class Day01(LineSolution):
    year = 2025
    day = 1

    def perform_turns(self) -> list[int]:
        results: list[int] = []
        current_value: int = 0
        for line in self.input:
            if line.startswith("L"):
                current_value -= int(line[1:])
            elif line.startswith("R"):
                current_value += int(line[1:])
            results.append(current_value)
        return results

    def part1(self) -> Any:
        return sum([1 for value in self.perform_turns() if value == 0])

    def part2(self) -> Any:
        return None
