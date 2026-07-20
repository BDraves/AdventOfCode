from collections import defaultdict
from dataclasses import asdict

from flask import Flask, render_template_string

from discovery import discover_solutions
from results import DayResult, collect_day_results

HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Advent of Code Results</title>
  <style>
    :root {
      color-scheme: light dark;
      font-family: system-ui, sans-serif;
      line-height: 1.5;
    }

    body {
      margin: 0;
      padding: 2rem;
    }

    main {
      max-width: 72rem;
      margin: 0 auto;
    }

    h1 {
      margin-block: 0 1rem;
      font-size: 1.75rem;
    }

    h2 {
      margin-block: 2rem 0.75rem;
      font-size: 1.25rem;
    }

    .controls {
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem 1rem;
      align-items: end;
      margin-block: 0 1.5rem;
    }

    .view-toggle {
      display: inline-flex;
      gap: 0.25rem;
      padding: 0.25rem;
      border: 1px solid color-mix(in srgb, CanvasText 25%, transparent);
      border-radius: 0.5rem;
    }

    .view-toggle label {
      display: inline-flex;
      align-items: center;
      min-height: 2rem;
      padding-inline: 0.75rem;
      border-radius: 0.3125rem;
      cursor: pointer;
    }

    .view-toggle input {
      position: absolute;
      inline-size: 1px;
      block-size: 1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
    }

    .view-toggle label:has(input:checked) {
      background: CanvasText;
      color: Canvas;
    }

    .year-picker {
      display: inline-grid;
      gap: 0.25rem;
    }

    .year-picker[hidden] {
      display: none;
    }

    .year-picker label {
      font-size: 0.875rem;
      font-weight: 700;
    }

    select {
      min-height: 2.5rem;
      padding-inline: 0.625rem 2rem;
      border: 1px solid color-mix(in srgb, CanvasText 25%, transparent);
      border-radius: 0.375rem;
      background: Canvas;
      color: CanvasText;
      font: inherit;
    }

    .results-section[hidden] {
      display: none;
    }

    table {
      width: 100%;
      border-collapse: collapse;
    }

    caption {
      margin-block-end: 0.75rem;
      text-align: left;
      font-weight: 700;
    }

    th,
    td {
      padding: 0.5rem 0.625rem;
      border-block-end: 1px solid color-mix(in srgb, CanvasText 25%, transparent);
      text-align: left;
      vertical-align: top;
    }

    th {
      font-weight: 700;
    }

    .number {
      font-variant-numeric: tabular-nums;
      text-align: right;
      white-space: nowrap;
    }

    .status-error {
      color: light-dark(#9f1239, #fda4af);
      font-weight: 700;
    }

    .muted {
      color: color-mix(in srgb, CanvasText 65%, transparent);
    }
  </style>
</head>
<body>
  <main>
    <h1>Advent of Code Results</h1>

    {% macro results_table(year, year_results) %}
      <table data-year-table="{{ year }}">
        <caption>
          {{ year_results|length }} discovered
          solution{{ "" if year_results|length == 1 else "s" }}
        </caption>
        <thead>
          <tr>
            <th scope="col">Day</th>
            <th scope="col">Solution</th>
            <th scope="col">Part 1</th>
            <th scope="col">Part 1 time</th>
            <th scope="col">Part 2</th>
            <th scope="col">Part 2 time</th>
          </tr>
        </thead>
        <tbody>
          {% for result in year_results %}
            <tr>
              <th scope="row" class="number">
                <a href="{{ result.url }}">{{ "%02d"|format(result.day) }}</a>
              </th>
              <td>
                {{ result.title or result.class_name }}
                <div class="muted">{{ result.module_name }}</div>
              </td>
              <td
                {% if result.part1.status == "error" %}
                  class="status-error"
                {% endif %}
              >
                {% if result.part1.status == "error" %}
                  Error: {{ result.part1.error }}
                {% else %}
                  {{ result.part1.value }}
                {% endif %}
              </td>
              <td
                class="{{
                  "number" if result.part1.duration_ms is not none else "muted"
                }}"
              >
                {% if result.part1.duration_ms is not none %}
                  {{ "%.3f"|format(result.part1.duration_ms) }} ms
                {% else %}
                  Not run
                {% endif %}
              </td>
              <td
                {% if result.part2.status == "error" %}
                  class="status-error"
                {% endif %}
              >
                {% if result.part2.status == "error" %}
                  Error: {{ result.part2.error }}
                {% else %}
                  {{ result.part2.value }}
                {% endif %}
              </td>
              <td
                class="{{
                  "number" if result.part2.duration_ms is not none else "muted"
                }}"
              >
                {% if result.part2.duration_ms is not none %}
                  {{ "%.3f"|format(result.part2.duration_ms) }} ms
                {% else %}
                  Not run
                {% endif %}
              </td>
            </tr>
          {% endfor %}
        </tbody>
      </table>
    {% endmacro %}

    {% if results_by_year %}
      <div class="controls">
        <div class="view-toggle" role="group" aria-label="Results view">
          <label>
            <input type="radio" name="results-view" value="sections" checked>
            Year sections
          </label>
          <label>
            <input type="radio" name="results-view" value="picker">
            Pick a year
          </label>
        </div>

        <div class="year-picker" hidden>
          <label for="year-select">Year</label>
          <select id="year-select" disabled>
            {% for year in years %}
              <option value="{{ year }}">{{ year }}</option>
            {% endfor %}
          </select>
        </div>
      </div>

      <div id="results-sections">
        {% for year, year_results in results_by_year.items() %}
          <section class="results-section" data-year-section="{{ year }}">
            <h2>{{ year }}</h2>
            {{ results_table(year, year_results) }}
          </section>
        {% endfor %}
      </div>
    {% else %}
      <p>No solutions found.</p>
    {% endif %}
  </main>

  <script>
    const viewInputs = document.querySelectorAll('input[name="results-view"]');
    const yearPicker = document.querySelector(".year-picker");
    const yearSelect = document.querySelector("#year-select");
    const yearSections = document.querySelectorAll("[data-year-section]");

    function updateResultsView() {
      const selectedView = document.querySelector(
        'input[name="results-view"]:checked'
      )?.value ?? "sections";
      const selectedYear = yearSelect?.value;
      const pickerMode = selectedView === "picker";

      if (yearSelect) {
        yearSelect.disabled = !pickerMode;
      }
      if (yearPicker) {
        yearPicker.hidden = !pickerMode;
      }

      yearSections.forEach((section) => {
        section.hidden =
          pickerMode && section.dataset.yearSection !== selectedYear;
      });
    }

    viewInputs.forEach((input) => {
      input.addEventListener("change", updateResultsView);
    });
    yearSelect?.addEventListener("change", updateResultsView);
    updateResultsView();
  </script>
</body>
</html>
"""


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index() -> str:
        results = get_results()
        results_by_year = group_results_by_year(results)
        return render_template_string(
            HTML,
            results_by_year=results_by_year,
            years=list(results_by_year),
        )

    @app.get("/results.json")
    def results_json() -> list[dict[str, object]]:
        return [asdict(result) for result in get_results()]

    return app


def get_results() -> list[DayResult]:
    return collect_day_results(discover_solutions())


def group_results_by_year(results: list[DayResult]) -> dict[int, list[DayResult]]:
    grouped_results: defaultdict[int, list[DayResult]] = defaultdict(list)
    for result in results:
        grouped_results[result.year].append(result)

    return dict(grouped_results)


def main() -> None:
    create_app().run(debug=True)


if __name__ == "__main__":
    main()
