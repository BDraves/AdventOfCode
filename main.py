from discovery import discover_solutions


def main() -> None:
    for solution in discover_solutions():
        print(f"{solution.year} day {solution.day:02}: {solution.class_name}")


if __name__ == "__main__":
    main()
