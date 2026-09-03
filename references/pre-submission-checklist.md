# Pre-submission readiness check

A composite check assembled from four independent diagnostics — no single source shipped this as one unified tool, so this skill wraps them into one report via `scripts/readiness_check.sh`. Entirely **Tier A**: every check here is read-only and reports findings; nothing is auto-fixed by this workflow (some findings point back to Tier A fixes elsewhere — e.g. a missing package — and some point to Tier B content decisions — e.g. an ambiguous anonymization hit that needs a judgment call, not a mechanical rewrite).

Run this before submitting, and again after any late edit — a check run once at the start of a session is not a substitute for one run against the actual final file. **Requires the active venue profile** (`venue-profile.md`) to be loaded first for the anonymization-phrasing and page-limit checks to mean anything specific — the script itself takes the page limit as an explicit argument rather than assuming one (see `scripts/readiness_check.sh --help`).

## What it checks

1. **Packages** (`latex_package_check.sh` equivalent) — every `\usepackage{}`/`\documentclass{}` resolves via `kpsewhich`. Missing packages are reported with the `tlmgr install` command to fix them (Tier A fix — installing a package doesn't change the paper).

2. **Citations** — wraps `check_citations.py` (see `citation-verification.md`): every `\cite{}` resolves in `refs.bib`, no unused entries, no duplicate keys, every entry has a locator field.

3. **Style/lint** — `chktex` wrapper, reports warnings/errors with counts.

4. **Structure** (`latex_analyze.sh` equivalent) — word count and estimated page count (compare against the active venue profile's submission page limit), figure/table/equation counts, unused labels (defined but never `\ref`'d — note this catches *unused* labels, not the more common *broken* `\ref` case, which is instead caught at compile time by `compile_check.sh`'s log parsing), TODO/FIXME markers.

5. **Anonymization** (from `agent-research-skills`' `check_anonymization()`, the one genuinely automatable check in this list) — only meaningful if the active venue profile calls for double-blind submission; skip this section entirely for a non-anonymous venue. Flags:
   - a non-empty `\author{}` field not saying "anonymous"
   - self-citation phrasing ("our previous work," "we previously proposed" — most double-blind venues require third person instead; check the active profile for the exact rule)
   - GitHub/GitLab/institutional URLs (not anonymized)
   - an `\acknowledgment`/`\acknowledgement` section (should not exist in an anonymized submission)

   **This check is a scanner, not a verdict** — a flagged self-citation phrase might be a false positive, and a URL flagged as non-anonymous needs a human judgment call about whether it's actually identifying. Report hits; don't silently "fix" any of them.

6. **Page count vs. limit** — cross-references the estimated/actual page count against the active venue profile's submission and camera-ready limits. If over, this is the trigger for `compression-toolkit.md`, not something this check fixes itself.

## What it deliberately does not check

Account/logistics matters outside a repo-scoped tool's reach — profile-site completeness, reciprocal-reviewing registration, sanctioned-entity affiliation, or any other venue-specific submission-portal requirement not captured in the active venue profile's desk-rejection list. This checklist is a content/formatting safety net, not a substitute for reading the actual submission-portal requirements before you submit.

## Output format

One summary table, ✓/✗ per check, with file:line detail for every ✗ — modeled on `paper-writing-skill`'s pre-submission mechanical checklist format, since it was the clearest single-table presentation found across the audited sources.
