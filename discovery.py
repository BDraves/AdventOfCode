from collections.abc import Iterator
from dataclasses import dataclass
from importlib import import_module
from inspect import isclass
from pathlib import Path
from typing import Any

from solution import LineSolution, Solution

PROJECT_ROOT = Path(__file__).parent
SOLUTIONS_ROOT = PROJECT_ROOT / "solutions"


@dataclass(frozen=True, order=True)
class SolutionInfo:
    year: int
    day: int
    module_name: str
    class_name: str
    solution_type: type[Solution[Any]]

    def create(self) -> Solution[Any]:
        return self.solution_type()


def iter_solution_module_names(root: Path = SOLUTIONS_ROOT) -> Iterator[str]:
    for path in sorted(root.glob("y[0-9][0-9][0-9][0-9]/day[0-9][0-9].py")):
        relative_path = path.relative_to(PROJECT_ROOT).with_suffix("")
        yield ".".join(relative_path.parts)


def discover_solutions(root: Path = SOLUTIONS_ROOT) -> list[SolutionInfo]:
    solutions: list[SolutionInfo] = []
    for module_name in iter_solution_module_names(root):
        module = import_module(module_name)
        solutions.extend(_discover_module_solutions(module_name, module))

    return sorted(solutions)


def _discover_module_solutions(
    module_name: str, module: object
) -> Iterator[SolutionInfo]:
    for name, value in vars(module).items():
        if not isclass(value):
            continue
        if value in {Solution, LineSolution}:
            continue
        if value.__module__ != module_name:
            continue
        if not issubclass(value, Solution):
            continue

        year = value.year
        day = value.day
        yield SolutionInfo(
            year=year,
            day=day,
            module_name=module_name,
            class_name=name,
            solution_type=value,
        )
