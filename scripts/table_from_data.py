#!/usr/bin/env python3
"""table_from_data.py — JSON/CSV results -> booktabs LaTeX table.

Only ever formats numbers that are already in the input file — never
invents or estimates a value. If a number you want isn't in the results
file, that's a "go add it to the results file first" problem, not
something this script papers over.

Note: the source this was adapted from (agent-research-skills'
results_to_table.py) shipped a --significance flag that was parsed but
never implemented (confirmed dead code in the Phase 1 audit). It is not
carried over here — there is no significance-star support in this
version. Add it as real, tested functionality if you want it; don't
re-add a flag that silently does nothing.

A 0-byte or header-only CSV/JSON input produces a clean error, not a crash.
A CSV row with more values than the header defines drops the extra values
with a visible warning on stderr (never silently) — fix the source data or
the header if you see this, since it usually means a column is missing.

A single --bold-best direction is wrong for any table mixing higher-is-
better metrics (accuracy) with lower-is-better ones (latency, error rate)
in the same table — --bold-best max would otherwise bold the *worst*
latency as if it were best. Use --minimize-columns to override the
direction for specific columns.

Usage:
  table_from_data.py --input results.json --type comparison \
      --caption "Main results" --label tab:main --bold-best max

  table_from_data.py --input results.csv --type descriptive --output table.tex

  table_from_data.py --input results.json --bold-best max \
      --minimize-columns latency_ms,error_rate

--type: comparison (default) | ablation | descriptive
--bold-best: max (default) | min | none
--minimize-columns: comma-separated column names using the opposite
  direction from --bold-best
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

METHOD_KEYS = {"method", "model", "name", "variant"}


def parse_numeric(value) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str):
        return None
    s = value.strip()
    s = re.split(r"±|\+/-|\+-", s)[0].strip()
    try:
        return float(s)
    except ValueError:
        return None


def escape_latex(s: str) -> str:
    s = str(s)
    s = s.replace("\\", r"\textbackslash{}")
    for ch, esc in [("_", r"\_"), ("%", r"\%"), ("&", r"\&"), ("#", r"\#")]:
        s = s.replace(ch, esc)
    s = s.replace("±", r"$\pm$").replace("+/-", r"$\pm$").replace("+-", r"$\pm$")
    return s


def load_json(path: Path) -> tuple[list[str], list[dict]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        rows = data
        method_key = next((k for k in METHOD_KEYS if rows and k in rows[0]), None)
        if method_key is None:
            raise ValueError(
                f"could not find a method-name key in {list(rows[0].keys()) if rows else '[]'} "
                f"— expected one of {sorted(METHOD_KEYS)}"
            )
        columns = [k for k in rows[0].keys() if k != method_key]
        return columns, [{"__method__": r[method_key], **{c: r[c] for c in columns}} for r in rows]
    elif isinstance(data, dict):
        # {method: {metric: value}}
        all_cols: list[str] = []
        for metrics in data.values():
            for k in metrics.keys():
                if k not in all_cols:
                    all_cols.append(k)
        rows = [{"__method__": m, **{c: metrics.get(c) for c in all_cols}} for m, metrics in data.items()]
        return all_cols, rows
    raise ValueError("unrecognized JSON structure — expected a list of row-dicts or a {method: {metric: value}} dict")


def load_csv(path: Path) -> tuple[list[str], list[dict]]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            raise ValueError(f"{path} is empty — no header row to read") from None
        columns = header[1:]
        rows = []
        for line_no, row in enumerate(reader, start=2):
            if not row:
                continue
            values = row[1:]
            if len(values) > len(columns):
                dropped = values[len(columns):]
                print(
                    f"warning: {path}:{line_no} has {len(values)} value(s) but the header only "
                    f"defines {len(columns)} column(s) — dropping extra value(s): {dropped}",
                    file=sys.stderr,
                )
            rows.append({"__method__": row[0], **{c: v for c, v in zip(columns, values)}})
    return columns, rows


def find_best_indices(
    rows: list[dict], columns: list[str], mode: str, minimize_columns: set[str]
) -> dict[str, int]:
    """column -> row index of the best value in that column.

    A single global --bold-best direction is wrong for any table mixing
    higher-is-better metrics (accuracy) with lower-is-better ones (latency,
    error rate, loss) — applying "max" uniformly would bold the *worst*
    latency as if it were the best. minimize_columns lists the column
    names that should use the opposite direction from the global mode.
    """
    best: dict[str, int] = {}
    if mode == "none":
        return best
    for col in columns:
        values = [(i, parse_numeric(r.get(col))) for i, r in enumerate(rows)]
        values = [(i, v) for i, v in values if v is not None]
        if not values:
            continue
        col_mode = mode
        if col in minimize_columns:
            col_mode = "min" if mode == "max" else "max"
        if col_mode == "max":
            best[col] = max(values, key=lambda iv: iv[1])[0]
        else:
            best[col] = min(values, key=lambda iv: iv[1])[0]
    return best


def generate_table(columns: list[str], rows: list[dict], table_type: str,
                    caption: str, label: str, bold_best: dict[str, int], wide: bool) -> str:
    env = "table*" if wide else "table"
    col_spec = "l" + "c" * len(columns)
    lines = [
        f"\\begin{{{env}}}[t]",
        "  \\centering",
        f"  \\caption{{{caption}}}",
        f"  \\label{{{label}}}",
        f"  \\begin{{tabular}}{{{col_spec}}}",
        "    \\toprule",
        "    " + " & ".join(["Method"] + [escape_latex(c) for c in columns]) + r" \\",
        "    \\midrule",
    ]
    for i, row in enumerate(rows):
        cells = [escape_latex(row.get("__method__", ""))]
        for col in columns:
            raw = row.get(col)
            text = escape_latex(raw) if raw is not None else "--"
            if bold_best.get(col) == i:
                text = f"\\textbf{{{text}}}"
            cells.append(text)
        prefix = "    \\quad " if table_type == "ablation" and i > 0 else "    "
        lines.append(prefix + " & ".join(cells) + r" \\")
    lines += ["    \\bottomrule", "  \\end{tabular}", f"\\end{{{env}}}"]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True)
    ap.add_argument("--type", choices=["comparison", "ablation", "descriptive"], default="comparison")
    ap.add_argument("--caption", default="Results")
    ap.add_argument("--label", default="tab:results")
    ap.add_argument("--bold-best", choices=["max", "min", "none"], default="max")
    ap.add_argument(
        "--minimize-columns", default="",
        help="comma-separated column names that use the opposite direction from "
             "--bold-best (e.g. --bold-best max --minimize-columns latency_ms,error_rate "
             "for a table where accuracy is best-when-highest but latency is best-when-lowest)"
    )
    ap.add_argument("--wide", action="store_true", help="use table* (spans both columns)")
    ap.add_argument("--output")
    args = ap.parse_args()

    path = Path(args.input)
    if not path.is_file():
        print(f"error: input file not found: {path}", file=sys.stderr)
        return 2

    try:
        if path.suffix.lower() == ".json":
            columns, rows = load_json(path)
        elif path.suffix.lower() == ".csv":
            columns, rows = load_csv(path)
        else:
            print(f"error: unrecognized input extension '{path.suffix}' — expected .json or .csv", file=sys.stderr)
            return 2
    except (ValueError, json.JSONDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if not rows:
        print("error: no data rows found in input", file=sys.stderr)
        return 2

    minimize_columns = {c.strip() for c in args.minimize_columns.split(",") if c.strip()}
    bold_best = (
        {} if args.type == "descriptive"
        else find_best_indices(rows, columns, args.bold_best, minimize_columns)
    )
    tex = generate_table(columns, rows, args.type, args.caption, args.label, bold_best, args.wide)

    if args.output:
        Path(args.output).write_text(tex + "\n", encoding="utf-8")
        print(f"wrote {args.output} ({len(rows)} rows, {len(columns)} columns)", file=sys.stderr)
    else:
        print(tex)
    return 0


if __name__ == "__main__":
    sys.exit(main())
