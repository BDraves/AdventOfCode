from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from time import perf_counter
from typing import Any, Literal

from discovery import SolutionInfo

ResultStatus = Literal["ok", "error", "missing"]


@dataclass(frozen=True)
class PartResult:
    value: str
    duration_ms: float | None = None
    status: ResultStatus = "ok"
    error: str | None = None

    @classmethod
    def ok(cls, value: object, duration_ms: float) -> PartResult:
        return cls(value=str(value), duration_ms=duration_ms)

    @classmethod
    def error_result(cls, error: Exception) -> PartResult:
        return cls(value="", status="error", error=str(error))


@dataclass(frozen=True)
class DayResult:
    year: int
    day: int
    title: str | None
    url: str
    module_name: str
    class_name: str
    part1: PartResult
    part2: PartResult


def collect_day_results(solutions: list[SolutionInfo]) -> list[DayResult]:
    return [solve_day(solution_info) for solution_info in solutions]


def solve_day(solution_info: SolutionInfo) -> DayResult:
    url = f"https://adventofcode.com/{solution_info.year}/day/{solution_info.day}"

    try:
        solution = solution_info.create()
    except Exception as error:
        load_error = PartResult.error_result(error)
        return DayResult(
            year=solution_info.year,
            day=solution_info.day,
            title=None,
            url=url,
            module_name=solution_info.module_name,
            class_name=solution_info.class_name,
            part1=load_error,
            part2=load_error,
        )

    title = getattr(solution, "title", None)
    return DayResult(
        year=solution_info.year,
        day=solution_info.day,
        title=title if isinstance(title, str) else None,
        url=solution.get_url(),
        module_name=solution_info.module_name,
        class_name=solution_info.class_name,
        part1=solve_part(solution.part1),
        part2=solve_part(solution.part2),
    )


def solve_part(part: Callable[[], Any]) -> PartResult:
    started_at = perf_counter()
    try:
        value = part()
    except Exception as error:
        return PartResult.error_result(error)

    return PartResult.ok(value, (perf_counter() - started_at) * 1000)
