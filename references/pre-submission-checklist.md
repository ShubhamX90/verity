# Pre-submission readiness check

A composite check assembled from several independent diagnostics — no single source shipped this as one unified tool, so this skill wraps them into one report via `scripts/readiness_check.sh`. Entirely **Tier A**: every check here is read-only and reports findings; nothing is auto-fixed by this workflow (some findings point back to Tier A fixes elsewhere — e.g. a missing package — and some point to Tier B content decisions — e.g. an ambiguous anonymization hit that needs a judgment call, not a mechanical rewrite).

Run this before submitting, and again after any late edit — a check run once at the start of a session is not a substitute for one run against the actual final file. **Requires the active venue profile** (`venue-profile.md`) to be loaded first for the anonymization-phrasing and page-limit checks to mean anything specific — the script itself takes the page limit as an explicit argument rather than assuming one (see `scripts/readiness_check.sh --help`).

## What it checks

1. **Packages** (`latex_package_check.sh` equivalent) — every `\usepackage{}`/`\documentclass{}` resolves via `kpsewhich`. Missing packages are reported with the `tlmgr install` command to fix them (Tier A fix — installing a package doesn't change the paper).

2. **Citations** — wraps `check_citations.py` (see `citation-verification.md`): every `\cite{}` resolves in `refs.bib`, no unused entries, no duplicate keys, every entry has a locator field.

3. **Style/lint** — `chktex` wrapper, reports warnings/errors with counts.

4. **Structure** (`latex_analyze.sh` equivalent) — word count and estimated page count (compare against the active venue profile's submission page limit), figure/table/equation counts, TODO/FIXME markers.

5. **Figure/table/appendix cross-references** — every figure and table `\label` is referenced by at least one `\ref`/`\Cref`/`\cref`/`\autoref` in the body text, and (if the paper has an `\appendix`) the main text points to it at least once before that command. This is the mechanical form of "cite every figure, table, and the appendix at least once" — a candidate list, not a full parse (a label referenced only through a custom cross-reference macro this doesn't recognize is a false positive). Note this catches an *uncited* figure/table, not the more common *broken* `\ref` case (a `\ref` pointing at a `\label` that doesn't exist anywhere), which is instead caught at compile time by `compile_check.sh`'s log parsing as an undefined-reference warning.

6. **Anonymization** (from `agent-research-skills`' `check_anonymization()`, the one genuinely automatable check in this list) — only meaningful if the active venue profile calls for double-blind submission; skip this section entirely for a non-anonymous venue. Flags:
   - a non-empty `\author{}` field not saying "anonymous"
   - self-citation phrasing ("our previous work," "we previously proposed" — most double-blind venues require third person instead; check the active profile for the exact rule)
   - GitHub/GitLab/institutional URLs (not anonymized)
   - an `\acknowledgment`/`\acknowledgement` section (should not exist in an anonymized submission)

   **This check is a scanner, not a verdict** — a flagged self-citation phrase might be a false positive, and a URL flagged as non-anonymous needs a human judgment call about whether it's actually identifying. Report hits; don't silently "fix" any of them.

7. **Page count vs. limit** — cross-references the estimated/actual page count against the active venue profile's submission and camera-ready limits. If over, this is the trigger for `compression-toolkit.md`, not something this check fixes itself.

## Venue-specific formatting checker (not wrapped by this script — run separately)

For the ACL family (ACL, EMNLP, NAACL — the venues that share `templates/acl-style-files/`), run [aclpubcheck](https://github.com/acl-org/aclpubcheck) against the compiled PDF as a second, independent formatting check beyond what `readiness_check.sh` covers — margins, font embedding, and other camera-ready-specific rules a `.tex`-level check can't see. Run it twice: once about two days before the deadline, so a formatting problem doesn't surface for the first time at the last minute, and again immediately before the final submission, since a late edit can reintroduce a formatting issue a first pass already cleared. Other venues may have their own equivalent checker; check the active venue profile's Template section before assuming none exists.

## What it deliberately does not check

Account/logistics matters outside a repo-scoped tool's reach — profile-site completeness, reciprocal-reviewing registration, sanctioned-entity affiliation, or any other venue-specific submission-portal requirement not captured in the active venue profile's desk-rejection list. This checklist is a content/formatting safety net, not a substitute for reading the actual submission-portal requirements before you submit.

## Output format

One summary table, ✓/✗ per check, with file:line detail for every ✗ — modeled on `paper-writing-skill`'s pre-submission mechanical checklist format, since it was the clearest single-table presentation found across the audited sources.

## No automated check replaces a human read-through

Every check above is mechanical. None of them read the paper for whether a claim is actually true, a number actually matches its source, or a citation actually supports the sentence it's attached to. Before submitting, read the paper start to finish and manually verify every line, every number, and every citation yourself — say this explicitly when a readiness check comes back clean, since a clean mechanical report is not the same claim as "verified correct."
