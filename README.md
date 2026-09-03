<div align="center">

# Verity

**A venue-agnostic academic paper-writing skill for Claude Code.**

Citation integrity, prose discipline, and a two-tier autonomy model — built for git-tracked LaTeX repositories shared with co-authors, and portable across every CS/ML venue you'll ever submit to.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-5A45FF)](https://docs.claude.com/en/docs/claude-code)
[![Venue Agnostic](https://img.shields.io/badge/venues-ICLR%20%C2%B7%20NeurIPS%20%C2%B7%20ACL%20%C2%B7%20EMNLP%20%C2%B7%20%2B%20any-informational)](#venue-profiles)

</div>

---

## What this is

Verity is a [Claude Code Skill](https://docs.claude.com/en/docs/claude-code) — a structured extension that teaches Claude Code how to responsibly co-author an academic paper. It is not a paper generator. It is a set of rules, workflows, and scripts that govern how an AI assistant should behave inside a real, shared, version-controlled manuscript: when it may act on its own, when it must stop and ask, and how it verifies that what it's about to write is actually true.

It was built to solve a specific, narrow problem well, rather than a broad problem shallowly: **how does an AI assistant edit a paper you're going to put your name on, without fabricating a citation, silently rewording a hedged claim into an overclaim, or bulldozing a co-author's uncommitted work — while still being useful enough to actually save time?**

Every design decision in this repository traces back to that question.

## Table of contents

- [Why this exists](#why-this-exists)
- [Core design: the two-tier autonomy model](#core-design-the-two-tier-autonomy-model)
- [Feature overview](#feature-overview)
- [Venue profiles](#venue-profiles)
- [Installation](#installation)
- [Usage](#usage)
- [Repository layout](#repository-layout)
- [Design principles](#design-principles)
- [Provenance](#provenance)
- [Contributing](#contributing)
- [License](#license)

## Why this exists

Large language models writing academic prose have two well-documented failure modes that make them actively dangerous to use unsupervised on a real submission:

1. **Citation hallucination.** AI-generated citations carry a substantial fabrication rate — a plausible-looking author, year, and title that doesn't correspond to a real paper, or worse, one that does exist but doesn't say what it's being cited for. In a submitted paper this isn't a typo; at most venues it's explicitly a research-integrity violation.
2. **Self-certification.** An agent that drafts an edit and then evaluates its own edit has no independent signal that the edit preserved the original claim. This is a known failure mode in AI-assisted editing pipelines — the same context that wrote the rewording is the one checking whether the rewording is faithful, and it reliably rationalizes its own phrasing.

Verity is built around closing both gaps structurally, not just via a system prompt asking the model to "be careful." A citation is fetched and verified through independent bibliographic APIs before it is ever written to `.bib` — never typed from memory. A proposed content edit is checked by a fresh context with no visibility into why the edit was made before it is ever shown to you for approval. Neither of these is optional, and neither degrades under time pressure, because the skill is deliberately designed to have no concept of deadline urgency at all — see [Design principles](#design-principles).

## Core design: the two-tier autonomy model

Every action Verity can take falls into exactly one of two tiers. This is the single organizing principle underneath the entire skill.

| | **Tier A — Proactive** | **Tier B — Propose & Wait** |
|---|---|---|
| **What it covers** | Read-only diagnostics and mechanical fixes that cannot change what the paper *claims* — compile-error fixes, `.bib` entry normalization, table-syntax generation from already-verified numbers, latexdiff-based revision review | Anything that changes what the paper says — a reworded claim, a cut paragraph, a restructured section, a new citation attached to a sentence |
| **Approval required?** | No — runs and reports | Yes — every change is surfaced and held until explicitly accepted |
| **Output format** | A diagnostic report | A structured `Before / After / Why` block, most-severe first |
| **File mutation** | Individual `Read`/`Edit` calls only — **never** a script that bulk-rewrites a `.tex`/`.bib` file, even for a mechanical fix | Applied only after acceptance, and only after passing an independent self-certification pass |

The subtlety that makes both halves coexist without contradiction: **scanning is always Tier A**, even for something as content-adjacent as passive-voice detection or AI-flavored vocabulary — a scan that surfaces candidates changes nothing. It's only *acting* on a candidate — actually rewriting text — that crosses into Tier B. This is what lets the skill proactively fix a broken compile error while simultaneously never touching a sentence's meaning without asking.

## Feature overview

| Capability | What it does |
|---|---|
| **Citation verification** | Every citation is resolved via Semantic Scholar, CrossRef, and arXiv before it's written to `.bib`. Unverifiable → an explicit `PLACEHOLDER_` key and a disclosure to the user, never a fabricated entry. |
| **De-AI-slop detection** | A four-tier detection framework (lexical, structural, argument-level, heuristic) for AI-flavored prose — plus a *separate*, non-tiered discipline for how new text should be composed in the first place, so slop is avoided rather than generated-then-cleaned. |
| **Non-native English polish** | Grammar and register correction (hyphenation, tense-by-authorship, article/preposition usage, acronym handling) — a distinct failure mode from AI-slop, run as an independent pass. |
| **Writing craft** | Narrative-structure guidance synthesized from published advice (Gopen & Swan's reader-expectation principles, the five-sentence abstract formula, contribution-first introduction structure) for drafting new sections well from the outset. |
| **Compression toolkit** | Seven concrete, on-demand operations for cutting a paper down to a venue's page limit — invoked only when actually over budget, never as routine editing. |
| **Self-certification** | Every Tier B batch is checked by a fresh context with no memory of *why* the edit was proposed before it reaches you — a lightweight, always-on adversarial check against silent claim drift. |
| **Table & figure generation** | Booktabs-formatted LaTeX tables generated from JSON/CSV results with correct per-column best-value direction (accuracy ↑, latency ↓ — handled independently, not a single global flag). Figures validated against DPI, vector-format, and colorblind-accessibility norms. |
| **Backward traceability** | Every number in the paper can be hyperlinked back to the exact result artifact that produced it, with a mechanical check that distinguishes "verified clean" from "nothing was ever tagged" — a subtle but important distinction a naive implementation gets wrong. |
| **Git-safe editing** | No script ever bulk-mutates a shared `.tex`/`.bib` file. Dirty-working-tree detection, staleness checks against a co-author's unpulled commits, and an explicit refusal to auto-resolve merge conflicts (they are inherently a Tier B content decision). |
| **Mock review** | A formal per-venue reviewer simulation (distinct score schemas for ICLR, NeurIPS, ICML, ACL, AAAI, ICCV, CVPR) and a separate "constructive advisor" mode that produces a prioritized revision checklist instead of an accept/reject verdict. |
| **Reproducibility audit** | Scores a project against seed control, dependency pinning, data hashing, git-state cleanliness, and environment documentation — feeding directly into a venue's reproducibility statement. |

## Venue profiles

Verity makes no assumptions about which conference or workshop a paper targets. Every venue- and year-specific fact — page limits, anonymization policy, AI-disclosure requirements, reviewing obligations, desk-rejection triggers — lives in a **venue profile**: a single Markdown file under `venues/`, fetched from the venue's own live policy pages and loaded per session.

```
venues/
├── iclr2027.md      # populated, live-verified
├── neurips2026.md   # populated, live-verified
├── icml2026.md      # populated, live-verified
├── colm2026.md      # populated, live-verified
├── acl2026.md       # populated, live-verified
├── emnlp2026.md     # populated, live-verified
├── naacl2027.md     # populated, live-verified
├── aaai2027.md      # populated, live-verified
└── <venue><year>.md # add as needed, same method
```

Building a new profile follows the same method used to build the first one: locate the venue's official call-for-papers and author-guidelines pages, fetch them directly, and populate the profile — never reconstruct policy from memory or a prior year's cached understanding. The full mechanism is documented in [`references/venue-profile.md`](references/venue-profile.md).

Deliberately **excluded** from the profile schema: submission deadlines. Verity's own behavior never depends on how close a deadline is — no urgency-driven shortcuts, no "skip verification because time is short." A paper-writing tool has no reason to track a calendar.

## Installation

Verity is a [Claude Code Skill](https://docs.claude.com/en/docs/claude-code/skills). Clone it into your skills directory:

```bash
git clone https://github.com/ShubhamX90/verity.git ~/.claude/skills/verity
```

Or, for project-scoped use, clone it into your paper's repository under `.claude/skills/`:

```bash
git clone https://github.com/ShubhamX90/verity.git .claude/skills/verity
```

Claude Code will pick up `SKILL.md`'s frontmatter automatically. No build step, no external dependencies beyond what's already on a typical LaTeX-authoring machine — see [Dependencies](#dependencies) below.

### Dependencies

All scripts are stdlib-only Python 3 or POSIX-portable Bash — no `pip install` required for the skill itself. Individual workflows expect the tools they wrap to be present:

| Tool | Used by | Required for |
|---|---|---|
| A LaTeX distribution (`pdflatex`/`xelatex`/`lualatex`, `bibtex`/`biber`) | `compile_check.sh` | Compiling the paper |
| `latexdiff` | `latex_diff.sh` | Reviewing a co-author's revision |
| `chktex` | `readiness_check.sh` | Style/lint checks |
| `kpsewhich` | `readiness_check.sh` | Package-availability checks |
| `detex` (optional) | `readiness_check.sh` | Word-count estimation (falls back to a cruder built-in method if absent) |
| `curl` | `fetch_bibtex.sh` | Citation fetching |

Every dependency degrades gracefully when absent — a missing tool produces a clearly labeled `SKIP`, never a silent gap presented as a pass.

## Usage

Once installed, describe what you need in plain language inside a Claude Code session working in your paper's repository:

```
> Check whether this citation is real before I add it.
> Run a pre-submission readiness check against the ICLR profile.
> This paragraph reads like it was written by an LLM — clean it up.
> I'm 1.5 pages over the limit — compress the related work section.
> What changed in main.tex since my co-author's last commit?
> Generate a results table from results/ablation.json.
```

Claude Code routes each request through `SKILL.md`'s task table to the relevant reference document and script. The first substantive action in any session is establishing the active venue profile — Verity will ask which venue and year you're targeting if it isn't already obvious from context, and will build a new profile from live sources if one doesn't exist yet for that venue-year.

## Repository layout

```
verity/
├── SKILL.md                    # Entry point: routing table, non-negotiable rules, the tier model
├── references/                 # One file per workflow — loaded on demand, not all at once
│   ├── venue-profile.md        #   The venue-profile mechanism itself
│   ├── citation-verification.md
│   ├── de-ai-slop.md
│   ├── polish.md
│   ├── writing-craft.md
│   ├── compression-toolkit.md
│   ├── self-certification.md
│   ├── git-and-latex-safety.md
│   ├── pre-submission-checklist.md
│   ├── figures-tables-diagrams.md
│   ├── reproducibility.md
│   ├── mock-review.md
│   ├── rebuttal.md             #   Stub — not built yet
│   └── prose-editing-policy.md
├── scripts/                    # 11 scripts, stdlib-only Python / portable Bash
├── venues/                     # 8 populated venue profiles: ICLR, NeurIPS, ICML, COLM, ACL, EMNLP, NAACL, AAAI
└── templates/                  # Official LaTeX kits, one directory per venue-year
```

## Design principles

**Never write a bibliographic entry from memory.** Every citation resolves through Semantic Scholar, CrossRef, or arXiv before it touches `.bib`. Failure to verify produces an explicit placeholder and a disclosure — never a plausible-looking invention.

**Never let a script mutate a shared source file directly.** Every diagnostic script is read-only by construction. Fixes are applied through individual, reviewable edits — never a batch find-and-replace across a document a co-author might be mid-edit on.

**Never let an edit check itself.** Every Tier B proposal passes through a self-certification step run with none of the context that produced the edit — an architectural answer to the well-documented failure mode of AI-assisted self-review.

**Never assume a venue's policy.** Page limits, disclosure rules, and reviewing obligations are loaded per session from a verified profile — never carried over from a different venue, a prior year, or general impression.

**Never let urgency change behavior.** No workflow in this skill is deadline-aware. Verification discipline does not relax as a deadline approaches, because the skill has no representation of deadlines at all.

## Provenance

Verity was synthesized from a structured audit of ten existing Claude Code skills spanning academic writing, LaTeX tooling, citation management, and peer review — auditing each for what to keep, what conflicted, and what didn't transfer, before any of this was written. Notable lineage:

- **[`SNL-UCSB/paper-writing-skill`](https://github.com/SNL-UCSB/paper-writing-skill)** — the compression-operation framework and the self-certification design rationale.
- **[`witold-andelie/claude-latex-paper-skill`](https://github.com/witold-andelie/claude-latex-paper-skill)** — the de-AI-slop modification threshold and rewrite safety zones.
- **[`ndpvt-web/latex-document-skill`](https://github.com/ndpvt-web/latex-document-skill)** — the latexdiff/git integration pattern.
- **[`MagicMonkey-XK/latex-precision-skill`](https://github.com/MagicMonkey-XK/latex-precision-skill)** — the no-bulk-regex editing constraint.
- **[`JeanDiable/academic-research-plugin`](https://github.com/JeanDiable/academic-research-plugin)** — the per-venue mock-review schemas.
- **[`minhuw/claude-writer`](https://github.com/minhuw/claude-writer)** (`polish` skill) — the non-native-English grammar/register rules.
- **davila7/claude-code-templates** (`ml-paper-writing`) — the citation-verification API workflow, writing-craft synthesis (Gopen & Swan, Farquhar, Lipton, Steinhardt), and the template-pitfalls checklist. Its per-venue table and citation-error-rate figure were unsourced starting points, not final content — both were independently re-derived from primary sources (live venue policy pages; peer-reviewed citation-fabrication studies) rather than copied.
- **`lingzhi227/agent-research-skills`** — figure/table generation and backward-traceability conventions.
- **`rzyu45/response-letter-bootstrap-skill`** and **`andikarachman/data-science-plugin`** (`reproducibility-checklist`) — informing the (respectively deferred and shipped) rebuttal and reproducibility-audit designs.

Every adaptation was fixed, tested against constructed edge cases, and — where the source made a claim about its own correctness — independently re-verified rather than trusted. Two independent audit passes were conducted against the finished skill before release, surfacing and closing gaps ranging from destructive file-overwrite bugs to a documentation/implementation mismatch in the reproducibility scoring rubric.

## Contributing

Issues and pull requests are welcome — particularly:
- A new populated venue profile under `venues/` for a venue not yet covered (CVPR, ICCV, KDD, AISTATS, etc.), or a re-verification pass on an existing one once its next cycle's CFP goes live (follow the schema in `references/venue-profile.md`)
- A verified per-venue mock-review schema for any venue currently unverified in `references/mock-review.md`
- Figure/diagram generation (currently checker-only, not generator — see `references/figures-tables-diagrams.md`)

Any script change should preserve the no-bulk-regex constraint and come with test evidence against constructed edge cases, not just a happy-path check.

## License

[MIT](LICENSE)
