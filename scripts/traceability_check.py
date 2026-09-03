#!/usr/bin/env python3
"""traceability_check.py — verify every \\hypertarget/\\hyperlink pair used to
trace numbers in the paper back to code/results output is internally
consistent. Read-only, stdlib only, Tier A.

Convention (from the backward-traceability workflow in
figures-tables-diagrams.md): a number produced by code/results is tagged
  \\hypertarget{LABEL}{VALUE}
and referenced in paper prose as
  \\hyperlink{LABEL}{VALUE}
so every number in the compiled PDF is one click away from the exact
output that produced it. This script does NOT do the tagging (that's a
manual/skill-driven step when drafting) — it only verifies that what's
already tagged is consistent: every hyperlink resolves to a target, every
target is actually used, and (optionally) tagged values match a
ground-truth code-output log. If nothing has been tagged at all, this
prints a distinct "NOTHING TO CHECK" message rather than "CLEAN" — zero
targets and zero links is not the same claim as "every number verified."

Usage:
  traceability_check.py --tex main.tex [main2.tex ...]
  traceability_check.py --tex main.tex --code-output results_log.txt
Exit code: 1 if any inconsistency found, 0 if clean.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HYPERTARGET_RE = re.compile(r"\\hypertarget\{([^}]+)\}\{([^}]*)\}")
HYPERLINK_RE = re.compile(r"\\hyperlink\{([^}]+)\}\{([^}]*)\}")


def strip_tex_comments(text: str) -> str:
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in text.splitlines())


def scan(tex_files: list[Path]) -> dict:
    targets: dict[str, tuple[str, Path]] = {}  # label -> (value, file)
    links: dict[str, list[tuple[str, Path]]] = {}  # label -> [(value, file), ...]
    duplicate_targets: list[str] = []

    for f in tex_files:
        text = strip_tex_comments(f.read_text(encoding="utf-8", errors="replace"))
        for m in HYPERTARGET_RE.finditer(text):
            label, value = m.group(1), m.group(2)
            if label in targets:
                duplicate_targets.append(f"{label} (in {targets[label][1]} and {f})")
            targets[label] = (value, f)
        for m in HYPERLINK_RE.finditer(text):
            label, value = m.group(1), m.group(2)
            links.setdefault(label, []).append((value, f))

    unresolved_links = sorted(set(links.keys()) - set(targets.keys()))
    unused_targets = sorted(set(targets.keys()) - set(links.keys()))
    value_mismatches = []
    for label, link_occurrences in links.items():
        if label not in targets:
            continue
        target_value = targets[label][0]
        for link_value, f in link_occurrences:
            if link_value != target_value:
                value_mismatches.append(
                    f"{label}: target says '{target_value}' but link in {f} says '{link_value}'"
                )

    return {
        "target_count": len(targets),
        "link_count": sum(len(v) for v in links.values()),
        "unresolved_links": unresolved_links,
        "unused_targets": unused_targets,
        "duplicate_targets": duplicate_targets,
        "value_mismatches": value_mismatches,
    }


def check_against_code_output(report: dict, targets_by_label: dict, code_output_path: Path) -> list[str]:
    """Cross-check tagged values against a raw code-output log containing
    its own \\hypertarget{label}{value} lines (or plain 'label: value' lines)."""
    raw = code_output_path.read_text(encoding="utf-8", errors="replace")
    code_values: dict[str, str] = {}
    for m in HYPERTARGET_RE.finditer(raw):
        code_values[m.group(1)] = m.group(2)
    for m in re.finditer(r"^([\w.-]+):\s*(.+)$", raw, re.MULTILINE):
        code_values.setdefault(m.group(1), m.group(2).strip())

    mismatches = []
    for label, (value, _f) in targets_by_label.items():
        if label in code_values and code_values[label] != value:
            mismatches.append(f"{label}: paper says '{value}' but code output says '{code_values[label]}'")
    return mismatches


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tex", nargs="+", required=True)
    ap.add_argument("--code-output", help="optional: a raw code-output log to cross-check tagged values against")
    args = ap.parse_args()

    tex_files = [Path(p) for p in args.tex]
    missing = [p for p in tex_files if not p.is_file()]
    if missing:
        print(f"error: file(s) not found: {', '.join(str(p) for p in missing)}", file=sys.stderr)
        return 2

    targets: dict[str, tuple[str, Path]] = {}
    for f in tex_files:
        text = strip_tex_comments(f.read_text(encoding="utf-8", errors="replace"))
        for m in HYPERTARGET_RE.finditer(text):
            targets[m.group(1)] = (m.group(2), f)

    report = scan(tex_files)
    print(f"scanned {len(tex_files)} .tex file(s): "
          f"{report['target_count']} hypertarget(s), {report['link_count']} hyperlink(s)")

    issues = 0
    if report["duplicate_targets"]:
        issues += len(report["duplicate_targets"])
        print(f"\n== duplicate hypertarget labels ({len(report['duplicate_targets'])}) ==")
        for d in report["duplicate_targets"]:
            print(f"  {d}")
    if report["unresolved_links"]:
        issues += len(report["unresolved_links"])
        print(f"\n== unresolved hyperlinks — no matching hypertarget ({len(report['unresolved_links'])}) ==")
        for label in report["unresolved_links"]:
            print(f"  {label}")
    if report["value_mismatches"]:
        issues += len(report["value_mismatches"])
        print(f"\n== value mismatches between target and link ({len(report['value_mismatches'])}) ==")
        for mm in report["value_mismatches"]:
            print(f"  {mm}")
    if report["unused_targets"]:
        print(f"\n== unused hypertargets — tagged but never referenced ({len(report['unused_targets'])}) — not an error, just worth a look ==")
        for label in report["unused_targets"]:
            print(f"  {label}")

    if args.code_output:
        code_path = Path(args.code_output)
        if not code_path.is_file():
            print(f"error: --code-output file not found: {code_path}", file=sys.stderr)
            return 2
        code_mismatches = check_against_code_output(report, targets, code_path)
        if code_mismatches:
            issues += len(code_mismatches)
            print(f"\n== mismatches vs. code output ({len(code_mismatches)}) ==")
            for mm in code_mismatches:
                print(f"  {mm}")

    if issues == 0:
        if report["target_count"] == 0 and report["link_count"] == 0:
            # Zero targets and zero links is not the same claim as "every
            # number verified" — it means the \hypertarget/\hyperlink
            # convention (see figures-tables-diagrams.md) hasn't been
            # adopted in these files at all, so there was nothing to check.
            # Reporting plain "CLEAN" here would be a false all-clear.
            print(
                "\nNOTHING TO CHECK — 0 \\hypertarget and 0 \\hyperlink found in the scanned "
                "file(s). This does NOT mean every number traces to an artifact; it means the "
                "tagging convention hasn't been applied yet. See figures-tables-diagrams.md "
                "for how to adopt it before relying on this script's output."
            )
        else:
            print("\nCLEAN — every traced number resolves and matches")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
