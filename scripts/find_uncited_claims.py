#!/usr/bin/env python3
"""find_uncited_claims.py — scan-only. Flags sentences that look like they
need a citation and don't have one nearby. Never searches for, fetches, or
inserts a citation itself — turning a flagged location into an actual
citation goes through the full workflow in citation-verification.md,
ending at a Tier B approval gate. This script's only job is to produce a
list of candidate locations for a human (or the assistant, proposing to
the human) to look at.

Usage: find_uncited_claims.py --tex main.tex [main2.tex ...]
       find_uncited_claims.py --tex-dir paper/
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Sentence-level patterns suggesting an unsupported claim. Deliberately
# broad (over-catches on purpose, like the mechanical style scan) — this
# is a candidate list for a human to triage, not a precision detector.
CLAIM_PATTERNS = [
    (r"\b(recent work|prior (?:work|studies)|previous (?:work|research)|"
     r"earlier work|it has been shown|other approaches)\b", "related-work indicator"),
    (r"\b(outperforms?|surpasses?|superior to|more effective than|"
     r"compared to (?:existing|previous|prior))\b", "comparison claim"),
    (r"\b\d+(?:\.\d+)?\s?\\?%[\s~]+(?:accuracy|improvement|reduction|faster|"
     r"better|higher|lower)\b", "unattributed numeric claim"),
    (r"\b(transformers?|attention mechanisms?|deep learning|neural networks?)\s+"
     r"(?:have|has|enable[sd]?|is known to)\b", "background assertion"),
]

# Skip a flagged sentence if it already has a \cite within this many
# characters on either side — approximates "within ~2 sentences."
# [Cc]ite, consistent with check_citations.py and style_scan.py, so a
# capitalized \Citet{}/\Citep{} counts as a nearby citation for suppression
# purposes — without this, an adequately-cited claim using natbib's
# sentence-initial capitalized form was false-flagged as needing a citation.
CITE_NEARBY_RE = re.compile(r"\\(?:full|text|paren|auto|foot)?[Cc]ite[a-zA-Z]*\*?(?:\[[^\]]*\])*\{")
CITE_PROXIMITY_CHARS = 200

SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")


def strip_tex(text: str) -> str:
    text = re.sub(r"(?<!\\)%.*$", "", text, flags=re.MULTILINE)
    # Drop math mode contents so patterns don't fire inside equations.
    text = re.sub(r"\$[^$]*\$", " ", text)
    return text


def has_nearby_cite(text: str, start: int, end: int) -> bool:
    window = text[max(0, start - CITE_PROXIMITY_CHARS): end + CITE_PROXIMITY_CHARS]
    return bool(CITE_NEARBY_RE.search(window))


def scan_file(path: Path) -> list[tuple[int, str, str]]:
    """Returns list of (line_number, matched_text, reason)."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    text = strip_tex(raw)
    findings = []
    for pattern, reason in CLAIM_PATTERNS:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            if has_nearby_cite(text, m.start(), m.end()):
                continue
            line_no = text.count("\n", 0, m.start()) + 1
            snippet = text[max(0, m.start() - 30): m.end() + 30].strip().replace("\n", " ")
            findings.append((line_no, snippet, reason))
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tex", nargs="*", default=[])
    ap.add_argument("--tex-dir")
    args = ap.parse_args()

    tex_files = [Path(p) for p in args.tex]
    if args.tex_dir:
        tex_files += sorted(Path(args.tex_dir).rglob("*.tex"))

    missing = [p for p in tex_files if not p.is_file()]
    if missing:
        print(f"error: file(s) not found: {', '.join(str(p) for p in missing)}", file=sys.stderr)
        return 2
    if not tex_files:
        print("error: no .tex files given (use --tex or --tex-dir)", file=sys.stderr)
        return 2

    total = 0
    for f in tex_files:
        findings = scan_file(f)
        if not findings:
            continue
        print(f"\n{f} ({len(findings)} candidate(s)):")
        for line_no, snippet, reason in findings:
            print(f"  line {line_no} [{reason}]: ...{snippet}...")
        total += len(findings)

    print(f"\n{total} candidate location(s) across {len(tex_files)} file(s) — "
          f"none inserted, none searched. Review each; verify via "
          f"citation-verification.md before adding anything.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
