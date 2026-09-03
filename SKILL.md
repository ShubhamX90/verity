---
name: verity
description: Write, edit, and prepare an academic paper submission (ICLR, NeurIPS, ICML, ACL, EMNLP, NAACL, COLM, or any other CS/ML venue) in a git-tracked LaTeX repo shared with co-authors. Use when the user asks to draft or revise a section, check compression against a page limit, verify or add a citation, generate a table or figure, review a co-author's diff, run a pre-submission or reproducibility check, or produce a mock review. Venue- and year-specific policy (page limits, anonymization, AI-disclosure rules, etc.) comes from a venue profile loaded per session, not hardcoded here — see references/venue-profile.md. Not for general LaTeX questions unrelated to a paper submission, and not for the rebuttal stage (not built yet — see references/rebuttal.md).
---

# Verity

A venue-agnostic academic paper-writing skill for Claude Code. The mechanics here (citation verification, prose editing, compression, tables/figures, mock review, pre-submission checks) apply the same way regardless of which conference or workshop a paper targets. What varies by venue and year — page limits, anonymization rules, AI-disclosure policy, reviewing obligations — lives in a **venue profile** (`references/venue-profile.md`), loaded per session rather than built into this file.

## First: establish the active venue profile

Before relying on any page limit, anonymization rule, or disclosure policy, establish which venue and year the paper targets, and load (or build) its profile — see `references/venue-profile.md` for the full mechanism. Don't assume a venue's rules from a different venue, a different year of the same venue, or general memory of "how these things usually work." A wrong assumption here (a page limit off by one, an anonymization rule that doesn't apply) is exactly the kind of error the rest of this skill's discipline exists to prevent, so it's worth getting right before anything else.

## Core philosophy: the two-tier autonomy model

Every action this skill takes falls into exactly one of two tiers. This is the single organizing principle underneath everything else in this file and in `references/`.

**Tier A — proactive.** Runs and reports, no pre-approval needed to act. Covers: read-only diagnostics (compile errors, citation integrity, anonymization scan, reproducibility audit, mock review) and mechanical fixes that cannot change what the paper claims (compile-error fixes, `.bib` entry formatting/normalization, table-syntax conversion from already-verified numbers, latexdiff-based revision review). When Tier A work writes to a shared `.tex`/`.bib` file, it always does so through individual `Read`/`Edit` calls at the specific flagged location — **never** a script that bulk-rewrites the file (see `references/git-and-latex-safety.md`).

**Tier B — propose and wait.** Anything that changes what the paper says: cutting a paragraph, rewording a claim, restructuring a section, any compression-toolkit operation, any de-AI vocabulary swap, and inserting a **new** `\cite{}` into the paper text (even once the citation itself is fully verified — attaching a source to a claim is a content decision). Always surfaced as:
```
<file>:<line>  [Critical | Major | Minor]
Before: <current text>
After:  <proposed text>
Why:    <the rule or reason>
```
grouped, most-severe first, applied only after per-item approval, then re-verified. Before any Tier B batch is presented, it runs through the fresh-context check in `references/self-certification.md` — a lightweight, non-self-certifying pass that checks the proposed rewrite still says what the paper actually claims, without carrying the reasoning that produced the edit.

**The subtlety that makes both halves coexist**: *scanning* is always Tier A, even for content-adjacent things like passive voice or AI-slop vocabulary — running a scanner and showing you the hits changes nothing. It's only *acting* on a hit — rewriting the text — that's Tier B. This is why "proactively fix compile errors" and "flag passive voice, never auto-rewrite it" are both true at once.

## Non-negotiable rules (no tier discussion — these have no permissive mode)

1. **Never write a BibTeX entry from memory.** Verify via Semantic Scholar + CrossRef/arXiv before adding anything to `refs.bib`; unverifiable → `\cite{PLACEHOLDER_author_year}` + tell the user how many and why. See `references/citation-verification.md`.
2. **Never bulk-regex a `.tex`/`.bib` file.** Scripts read and report; edits are applied manually, one location at a time. See `references/git-and-latex-safety.md`.
3. **Never auto-apply a content-level edit.** Every Tier B change waits for explicit per-item approval, regardless of how confident the proposed fix is, and no Tier B batch skips the self-certification check (`references/self-certification.md`) before it's presented.
4. **Always compile before judging layout.** Never assess figure placement, page count, or spacing from raw `.tex` source.
5. **Never invent a number.** Every quantitative claim traces to a file in the results/data folder, never to conversational memory. See `references/reproducibility.md` and `references/figures-tables-diagrams.md`.
6. **Never commit or push without an explicit request.** Git operations are the user's call.
7. **Never draft persuasive rebuttal prose.** Not built yet regardless (`references/rebuttal.md`), but recorded here because it's a standing rule for whenever it is built.
8. **Never invent or assume a venue's policy.** Page limits, anonymization rules, disclosure requirements, and reviewing obligations come from a loaded venue profile (`references/venue-profile.md`), never from memory of a different venue or a prior year.

## Routing table

| Task | Reference | Script(s) | Tier |
|---|---|---|---|
| Establish/build the active venue profile | `venue-profile.md` | — | — |
| Add/verify a citation | `citation-verification.md` | `fetch_bibtex.sh`, `check_citations.py` | A (verify/fetch/normalize) → B (insert into text) |
| Find candidate uncited claims | `citation-verification.md` | `find_uncited_claims.py` | A (scan only) |
| Polish prose / check for AI-slop | `prose-editing-policy.md` + `de-ai-slop.md` | `style_scan.py` | A (scan) → B (any rewrite) |
| Fix non-native-English grammar/register (hyphen use, tense-by-authorship, articles/prepositions, acronyms) | `polish.md` | — (read-through, not scripted — see file for why) | A (scan) → B (any rewrite) |
| Draft brand-new paper text | `de-ai-slop.md` (Part 2) | — | not tiered — a standing constraint on composition itself |
| Structure a paper/section/abstract (narrative, argument, sentence-level clarity) | `writing-craft.md` | — | Part 1 not tiered (composing); Part 2 is Tier A (judgment review) |
| Fresh-context check before presenting any Tier B batch | `self-certification.md` | — | runs as part of every Tier B workflow below, not a standalone task |
| Compress a section (only when over the active profile's page limit) | `compression-toolkit.md` | `style_scan.py` (re-verify after) | B throughout |
| Review a co-author's changes | `git-and-latex-safety.md` | `latex_diff.sh` | A |
| Compile / diagnose build errors | `git-and-latex-safety.md` | `compile_check.sh` | A |
| Generate a table from results | `figures-tables-diagrams.md` | `table_from_data.py` | A (format) / B (choosing what to show) |
| Check a figure against publication-quality norms | `figures-tables-diagrams.md` | `figure_check.py` | A |
| Verify every number traces to an artifact | `figures-tables-diagrams.md` | `traceability_check.py` | A |
| Pre-submission readiness check | `pre-submission-checklist.md` | `readiness_check.sh` | A |
| Reproducibility audit | `reproducibility.md` | `reproducibility_audit.py` | A |
| Mock review / revision checklist | `mock-review.md` | — (direct analysis) | A |
| Venue/year policy questions (page limits, anonymization, AI disclosure, reviewing obligations) | `venue-profile.md` + the active `venues/<venue><year>.md` | — | — |
| Rebuttal | `rebuttal.md` | — (stub, not built) | — |

## Workflows

**Starting work on a paper.** Establish the active venue profile first (above) before anything else that depends on venue-specific facts.

**Adding a citation.** Search and verify (Tier A) through the full workflow in `citation-verification.md`, ending with a proposed `\cite{}` insertion at a specific location (Tier B) — surface the verified BibTeX and the sentence it would support together, and wait.

**A normal editing pass.** Default posture is "leave it if it's already natural" (`prose-editing-policy.md`) — there's no mandatory per-edit audit. Run `style_scan.py` when useful; treat every hit, including passive voice, as a flagged suggestion, not an automatic fix. `de-ai-slop.md` has the full detection reference (lexical, structural, and argument-level tells, plus judgment heuristics beyond what any script catches) and, separately, the standing composition-time constraints that apply whenever new text is being drafted rather than edited. `polish.md` is a separate, independent pass for genuine grammar/register errors (as opposed to AI-flavored prose) — run it separately, not merged into the same batch, since the two have different "why"s and you may want to accept one kind of fix without the other.

**Drafting or restructuring a section, abstract, or introduction.** `writing-craft.md` — the narrative principle, the 5-sentence abstract formula, Gopen & Swan's sentence-level reader-expectation principles, and word-choice precision guidance. This is a composing-time discipline (Part 1, not tiered) plus a judgment-based review pass (Part 2, Tier A) — distinct from `de-ai-slop.md`, which is about removing AI-flavored filler, not about structuring the argument in the first place. A paragraph can need both, either, or neither.

**Approaching the page limit.** Only then, invoke the compression toolkit (`compression-toolkit.md`) explicitly, against the limit given in the active venue profile — it's on-demand, not something that runs as part of routine editing. Prefer moving non-essential content to the appendix over deleting it outright, per the user's own stated habit.

**Reviewing a co-author's diff.** `latex_diff.sh` against a specific commit/branch/tag, or the current working copy — true two-revision (`rev` vs. `rev`) diffing isn't supported; do it in two manual `git show` steps if genuinely needed (see `git-and-latex-safety.md`).

**Before submitting.** Run `readiness_check.sh` (pre-submission checklist) against the active venue profile's page limit, and re-verify the profile itself against its live source pages if it's been a while since it was last checked — policy pages get revised.

**Getting feedback before anyone else sees the paper.** Mock review (`mock-review.md`) — Mode 1 for a realistic accept/reject read, Mode 2 for a prioritized fix-it list. Both are safe to run anytime, don't modify the paper.

## Script provenance

Every script under `scripts/` is adapted from source material, not copied verbatim — each one had a specific bug fixed or was rebuilt around the no-bulk-regex constraint before being included here (see the README's design notes for the fuller history). If you find another bug in one of these scripts, fix it or rewrite it — the same rule that got them here in the first place applies to anything found later.

## Templates

`templates/<venue><year>/` — one directory per venue-year, mirroring the `venues/` profile structure, each fetched directly from its official source repository: `templates/iclr2027/` (`github.com/ICLR/Master-Template`), `templates/neurips2026/`, `templates/icml2026/`, `templates/colm2026/`, `templates/aaai2027/`. ACL, EMNLP, and NAACL share one official style-file package rather than each getting a duplicate copy — `templates/acl-style-files/` (`github.com/acl-org/acl-style-files`) — since the venue profiles for that family (`venues/acl2026.md`, `venues/emnlp2026.md`, `venues/naacl2027.md`) confirmed the underlying kit really is identical across all three. Copy the whole relevant directory when starting a new paper from a template; never edit the `.sty`/`.bst` files directly, and never work from just the `.tex` file with the style files elsewhere. Adding a new venue's template follows the same method: fetch it from its official source repository, don't reconstruct it from memory.

## Figures/tables/diagrams subfolder mapping

**Placeholder — not yet filled in.** `references/figures-tables-diagrams.md` has the mapping table; it needs the real repo's actual folder names before it's accurate. Fill it in the first time this skill is pointed at the real paper repo.
