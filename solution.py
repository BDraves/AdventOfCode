from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, TypeVar

ROOT = Path(__file__).parent

InputT = TypeVar("InputT")


class Solution[InputT](ABC):
    year: int
    day: int
    raw_input: str
    input: InputT

    def __init__(self) -> None:
        self.raw_input = self.read_input()
        self.input = self.format_input(self.raw_input)

    @property
    def input_path(self) -> Path:
        input_dir = ROOT / "input" / str(self.year)
        padded_path = input_dir / f"{self.day:02}.txt"
        if padded_path.exists():
            return padded_path

        unpadded_path = input_dir / f"{self.day}.txt"
        if unpadded_path.exists():
            return unpadded_path

        return padded_path

    def get_url(self) -> str:
        return f"https://adventofcode.com/{self.year}/day/{self.day}"

    def read_input(self) -> str:
        return self.input_path.read_text()

    @abstractmethod
    def format_input(self, raw: str) -> InputT:
        ...

    @abstractmethod
    def part1(self) -> Any:
        ...

    @abstractmethod
    def part2(self) -> Any:
        ...


class LineSolution(Solution[list[str]], ABC):
    def format_input(self, raw: str) -> list[str]:
        return raw.splitlines()
