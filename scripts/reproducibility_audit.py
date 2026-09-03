#!/usr/bin/env python3
"""reproducibility_audit.py — score a project against six reproducibility
categories (seeds, library versions, data version, code version,
environment, results determinism). Read-only, stdlib only, Tier A.

Venue-agnostic: feeds into whichever reproducibility statement the active
venue profile calls for (see references/venue-profile.md and
references/reproducibility.md) — run this before drafting that paragraph
rather than writing it from memory/impression.

IMPORTANT: the library-version check needs --requirements pointed at the
real project's requirements.txt/environment.yml/pyproject.toml. There is
no built-in default dependency list — without --requirements, that
category scores 0 with a note explaining why, rather than silently
checking for libraries the project may not even use.

Usage:
  reproducibility_audit.py --code-dir src/ --data-file data/train.csv \
      --requirements requirements.txt [--expected-hash <sha256>] \
      [--repo-dir .]
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

SEED_PATTERNS = re.compile(
    r"\b(random_state\s*=|np\.random\.seed|random\.seed|torch\.manual_seed|"
    r"tf\.random\.set_seed|seed\s*=)\b"
)


def check_seeds(code_dir: Path) -> tuple[int, list[str]]:
    if not code_dir.is_dir():
        return 0, [f"code directory not found: {code_dir}"]
    py_files = list(code_dir.rglob("*.py"))
    if not py_files:
        return 0, [f"no .py files found under {code_dir}"]
    hits = 0
    files_with_hits = []
    for f in py_files:
        text = f.read_text(encoding="utf-8", errors="replace")
        if SEED_PATTERNS.search(text):
            hits += 1
            files_with_hits.append(str(f))
    notes = [f"seed-setting calls found in {hits}/{len(py_files)} .py files"]
    if hits == 0:
        notes.append("no seed-setting calls found anywhere — this is the most common reproducibility gap")
    return (3 if hits >= len(py_files) * 0.5 else (1 if hits > 0 else 0)), notes


def check_library_versions(requirements_path: Path | None) -> tuple[int, list[str]]:
    if requirements_path is None:
        return 0, ["no --requirements file given — pass the real project's requirements.txt/"
                    "environment.yml/pyproject.toml; the built-in default list is a generic "
                    "placeholder, not project-specific"]
    if not requirements_path.is_file():
        return 0, [f"--requirements file not found: {requirements_path}"]
    text = requirements_path.read_text(encoding="utf-8", errors="replace")
    pinned = len(re.findall(r"^[\w.-]+\s*==\s*[\w.]+", text, re.MULTILINE))
    unpinned = len(re.findall(r"^[\w.-]+\s*$", text, re.MULTILINE))
    notes = [f"{requirements_path}: {pinned} pinned (==) entries, {unpinned} unpinned entries"]
    score = 2 if pinned > 0 and unpinned == 0 else (1 if pinned > 0 else 0)
    return score, notes


def check_data_version(data_file: Path | None, expected_hash: str | None) -> tuple[int, list[str]]:
    if data_file is None:
        return 0, ["no --data-file given — cannot compute a hash"]
    if not data_file.is_file():
        return 0, [f"--data-file not found: {data_file}"]
    h = hashlib.sha256()
    with data_file.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    digest = h.hexdigest()
    notes = [f"{data_file}: sha256={digest}"]
    score = 1
    if expected_hash:
        if expected_hash.lower() == digest.lower():
            notes.append("matches --expected-hash")
            score = 2
        else:
            notes.append(f"MISMATCH vs. --expected-hash ({expected_hash})")
            score = 0
    return score, notes


def check_code_version(repo_dir: Path) -> tuple[int, list[str]]:
    def run(args: list[str]) -> str | None:
        try:
            r = subprocess.run(["git", "-C", str(repo_dir)] + args, capture_output=True, text=True, timeout=10)
            return r.stdout.strip() if r.returncode == 0 else None
        except (OSError, subprocess.SubprocessError):
            return None

    sha = run(["rev-parse", "HEAD"])
    if sha is None:
        return 0, [f"{repo_dir} is not a git repository (or git is unavailable)"]
    status = run(["status", "--porcelain"])
    clean = status == ""
    notes = [f"HEAD={sha}", f"working tree clean={clean}"]
    if not clean:
        notes.append("uncommitted changes present — results produced now may not match a later checkout of HEAD")
    return (2 if clean else 1), notes


def check_environment(requirements_path: Path | None) -> tuple[int, list[str]]:
    if requirements_path is not None and requirements_path.is_file():
        return 1, [f"environment/lock file present: {requirements_path}"]
    return 0, ["no environment/lock file given (reuses --requirements) — hardware and compute-cost "
               "documentation can't be checked automatically; confirm by hand"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--code-dir", type=Path, default=Path("."))
    ap.add_argument("--data-file", type=Path)
    ap.add_argument("--expected-hash")
    ap.add_argument("--requirements", type=Path)
    ap.add_argument("--repo-dir", type=Path, default=Path("."))
    args = ap.parse_args()

    sections = {
        "1. Random seeds": check_seeds(args.code_dir),
        "2. Library versions": check_library_versions(args.requirements),
        "3. Data version": check_data_version(args.data_file, args.expected_hash),
        "4. Code version": check_code_version(args.repo_dir),
        "5. Environment": check_environment(args.requirements),
    }

    total = 0
    max_total = 0
    max_per_section = {"1. Random seeds": 3, "2. Library versions": 2, "3. Data version": 2,
                        "4. Code version": 2, "5. Environment": 1}

    for name, (score, notes) in sections.items():
        cap = max_per_section[name]
        total += score
        max_total += cap
        print(f"\n{name} [{score}/{cap}]")
        for n in notes:
            print(f"  - {n}")

    print("\n6. Results determinism [not automatically checkable]")
    print("  - re-run the pipeline with the same code/data/seed and confirm matching metrics by hand; "
          "document any known non-determinism (GPU ops, multi-threaded data loading)")

    pct = total / max_total if max_total else 0
    print(f"\n== Score: {total}/{max_total} automatable points ({pct:.0%}) — "
          f"category 6 is manual and not included in this number ==")
    if pct >= 0.85:
        rating = "Good — most of what's automatically checkable looks solid"
    elif pct >= 0.5:
        rating = "Fair — real gaps, worth closing before relying on this for the Reproducibility Statement"
    else:
        rating = "Poor — significant gaps"
    print(f"Rating: {rating}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
