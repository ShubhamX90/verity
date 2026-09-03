#!/usr/bin/env python3
"""check_citations.py — static citation integrity check. Read-only, stdlib only.

Never fetches or inserts anything (that's fetch_bibtex.sh + the Tier B
insertion workflow in citation-verification.md). This script only checks
that what's already in the document is internally consistent:

  1. Every \\cite{key} has a matching entry in the .bib file(s).
  2. Every .bib entry is cited somewhere (dead weight, or a forgotten site).
  3. No duplicate .bib keys.
  4. Every .bib entry carries a locator (doi/url/eprint/isbn) — an entry
     with none is exactly where a fabricated citation would be hardest to
     catch, since there's nothing to click through and verify. Checked
     anywhere in the entry, not just at line start, so a compact
     single-line entry isn't false-flagged.
  5. Malformed .bib entries: keyless entries (previously silently dropped
     from every report rather than flagged), unbalanced braces, and a
     conservative missing-comma-between-fields heuristic. None of this is
     a full BibTeX parser — it's a candidate list for entries worth a
     second look, same spirit as the mechanical style scan elsewhere in
     this skill.

Recognizes capitalized natbib commands (\\Citet, \\Citep, etc.) and
\\nocite{} alongside the lowercase \\cite family.

Usage: check_citations.py --tex main.tex [main2.tex ...] --bib refs.bib [refs2.bib ...]
       check_citations.py --tex-dir paper/ --bib-dir paper/
Exit code: 1 if any hard issue found (missing cite, duplicate key, malformed
entry), 0 otherwise. Unused entries and missing locators are reported but do
not affect exit code (they're not broken, just worth a look).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CITE_RE = re.compile(
    r"\\(?:full|text|paren|auto|foot|no)?[Cc]ite[a-zA-Z]*\*?(?:\[[^\]]*\])*\{([^}]+)\}"
)
# Loose "this block looks like an attempted entry" detector — used to catch
# keyless entries (@article{,) that BIBENTRY_RE's required-key group would
# otherwise cause it to skip silently rather than flag.
BIBSTART_RE = re.compile(r"^\s*@(\w+)\s*\{", re.IGNORECASE)
BIBENTRY_RE = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", re.IGNORECASE)
# No longer anchored to line start (^) — a compact, valid, single-line entry
# like "@article{k, title={x}, doi={1}}" has its doi= mid-line, not
# line-initial, and the anchored version missed it, producing a false
# "no locator" on a perfectly fine entry.
LOCATOR_RE = re.compile(r"(?im)\b(doi|url|eprint|isbn|howpublished)\s*=")
# Field-assignment lines, for the missing-comma heuristic below. Matches a
# line that looks like "key = {...}" or "key = "..."" ending the visible
# value on that same line (does not handle a value that itself spans
# multiple lines — over-catches on purpose, like the mechanical style
# scan; a candidate list for a human to check, not a full BibTeX parser).
FIELD_LINE_RE = re.compile(r"^\s*[\w-]+\s*=")


def strip_tex_comments(text: str) -> str:
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in text.splitlines())


def collect_cited_keys(tex_files: list[Path]) -> set[str]:
    keys: set[str] = set()
    for f in tex_files:
        text = strip_tex_comments(f.read_text(encoding="utf-8", errors="replace"))
        for m in CITE_RE.finditer(text):
            for k in m.group(1).split(","):
                k = k.strip()
                if k:
                    keys.add(k)
    return keys


def collect_bib_entries(
    bib_files: list[Path],
) -> tuple[dict[str, list[Path]], list[str], list[str]]:
    """Returns (key -> list of files it appears in [for duplicate detection],
    list of "file:key" strings for entries with no locator field,
    list of malformed-entry descriptions [keyless / unbalanced braces /
    likely missing comma between fields])."""
    key_to_files: dict[str, list[Path]] = {}
    no_locator: list[str] = []
    malformed: list[str] = []
    for f in bib_files:
        raw = f.read_text(encoding="utf-8", errors="replace")
        for block in re.split(r"(?m)^(?=@)", raw):
            start_m = BIBSTART_RE.match(block)
            if not start_m:
                continue  # not an entry at all (blank chunk, leading comments)

            m = BIBENTRY_RE.search(block)
            if not m:
                # Looks like an attempted entry (@type{...) but no key
                # before the first comma — previously silently dropped
                # from every report; now flagged instead.
                snippet = block.strip().splitlines()[0][:60] if block.strip() else "(empty)"
                malformed.append(f"{f}: keyless or malformed entry near: {snippet}")
                continue

            key = m.group(2).strip()
            key_to_files.setdefault(key, []).append(f)
            if not LOCATOR_RE.search(block):
                no_locator.append(f"{f}:{key}")

            n_open = block.count("{")
            n_close = block.count("}")
            if n_open != n_close:
                malformed.append(
                    f"{f}:{key}: unbalanced braces ({n_open} '{{' vs {n_close} '}}') — "
                    f"a missing closing brace can silently swallow the rest of the file"
                )

            # Missing-comma heuristic: a field-assignment line not ending in
            # ',' immediately followed by another field-assignment line, in
            # the same entry. Deliberately conservative (checked line pairs
            # only, not the general case of a value spanning multiple
            # lines) — a candidate to inspect, not a certain diagnosis.
            lines = block.splitlines()
            for i in range(len(lines) - 1):
                if FIELD_LINE_RE.match(lines[i]) and FIELD_LINE_RE.match(lines[i + 1]):
                    if not lines[i].rstrip().endswith(","):
                        malformed.append(
                            f"{f}:{key}: line {i+1} of this entry doesn't end with ',' and the "
                            f"next line also looks like a field — possible missing comma"
                        )
    return key_to_files, no_locator, malformed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tex", nargs="*", default=[], help="one or more .tex files")
    ap.add_argument("--bib", nargs="*", default=[], help="one or more .bib files")
    ap.add_argument("--tex-dir", help="directory to search for .tex files (recursive)")
    ap.add_argument("--bib-dir", help="directory to search for .bib files (recursive)")
    args = ap.parse_args()

    tex_files = [Path(p) for p in args.tex]
    bib_files = [Path(p) for p in args.bib]
    if args.tex_dir:
        tex_files += sorted(Path(args.tex_dir).rglob("*.tex"))
    if args.bib_dir:
        bib_files += sorted(Path(args.bib_dir).rglob("*.bib"))

    missing = [p for p in tex_files if not p.is_file()]
    missing += [p for p in bib_files if not p.is_file()]
    if missing:
        print(f"error: file(s) not found: {', '.join(str(p) for p in missing)}", file=sys.stderr)
        return 2
    if not tex_files:
        print("error: no .tex files given (use --tex or --tex-dir)", file=sys.stderr)
        return 2
    if not bib_files:
        print("error: no .bib files given (use --bib or --bib-dir)", file=sys.stderr)
        return 2

    cited = collect_cited_keys(tex_files)
    key_to_files, no_locator, malformed = collect_bib_entries(bib_files)
    bib_keys = set(key_to_files.keys())

    hard_issues: list[str] = []
    soft_issues: list[str] = []

    for key in sorted(cited - bib_keys):
        hard_issues.append(f"\\cite{{{key}}} has no matching entry in any .bib file")

    for key, files in sorted(key_to_files.items()):
        if len(files) > 1:
            hard_issues.append(f"duplicate .bib key '{key}' in: {', '.join(str(f) for f in files)}")

    # Malformed entries (keyless, unbalanced braces, likely missing comma)
    # are objectively broken states, not judgment calls, so they're hard
    # issues — same treatment as a broken \cite key.
    hard_issues.extend(sorted(malformed))

    for key in sorted(bib_keys - cited):
        soft_issues.append(f"'{key}' is defined in .bib but never cited")

    for entry in sorted(no_locator):
        soft_issues.append(f"{entry} has no locator field (doi/url/eprint/isbn)")

    print(f"scanned {len(tex_files)} .tex file(s), {len(bib_files)} .bib file(s)")
    print(f"{len(cited)} unique \\cite key(s) used, {len(bib_keys)} unique .bib entries found")

    if hard_issues:
        print(f"\n== HARD ISSUES ({len(hard_issues)}) ==")
        for i in hard_issues:
            print(f"  - {i}")
    if soft_issues:
        print(f"\n== worth a look ({len(soft_issues)}) ==")
        for i in soft_issues:
            print(f"  - {i}")
    if not hard_issues and not soft_issues:
        print("\nCLEAN")

    return 1 if hard_issues else 0


if __name__ == "__main__":
    sys.exit(main())
