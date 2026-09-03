# Venue profiles

This skill is not specific to any one conference or workshop. It works the same way for ICLR, NeurIPS, ICML, ACL, EMNLP, NAACL, COLM, or any other CS/ML venue and any year — the paper-writing mechanics (citation verification, prose editing, compression, tables/figures, mock review, etc.) are entirely venue-independent. What *is* venue- and year-specific — page limits, anonymization rules, AI-use-disclosure policy, reviewing obligations, statement requirements, desk-rejection triggers, the LaTeX template — lives in a **venue profile**, a single file per venue-year, loaded on demand rather than hardcoded into the skill.

**Nothing in this skill assumes a specific venue by default.** Every other reference file that needs a policy fact (a page limit, an anonymization rule, an AI-disclosure requirement) says "consult the active venue profile," never a hardcoded number. If you're reading another reference file and it names a specific page limit or policy detail outside of a venue profile, that's a bug — file names, tables, everything policy-specific belongs here, not baked into the general mechanism docs.

## Where profiles live

`venues/<venue><year>.md`, lowercase, no separator — `venues/iclr2027.md`, `venues/acl2026.md`, `venues/emnlp2025.md`, `venues/colm2026.md`, `venues/naacl2026.md`. One file per venue-year; a venue you use across multiple years gets multiple files (policies change year to year — never assume last year's profile still applies).

## Establishing the active profile for a session

At the start of any work on a specific paper, establish which venue and year it targets — from the conversation, from the repo (a template folder name, a `.sty` file, existing front matter), or by asking directly if it's genuinely unclear. Then:

1. Check whether `venues/<venue><year>.md` already exists.
2. **If it exists**, load it and treat it as the source of truth for that venue's policy for the rest of the session. Don't re-derive page limits or anonymization rules from memory once a profile is loaded.
3. **If it doesn't exist**, build one (see below) before relying on any venue-specific fact — never guess a page limit or policy detail for a venue that has no profile yet.

## Building a new profile

Follow the same method used to build `venues/iclr2027.md`, the first populated profile:

1. Find the venue's official pages for the target year — a call-for-papers page, an author-guidelines page, and (if the venue has one) an AI-use-policy page. Search for them, or ask the user for the link if a web search doesn't surface the official page confidently.
2. Fetch each page directly and read its actual content — don't reconstruct policy from a prior year's memory or from general knowledge of "how these venues usually work." Venues change policy year to year, and two venues in the same subfield often differ in specifics (page limits, whether an AI-disclosure statement exists at all, anonymization strictness).
3. Write a new `venues/<venue><year>.md` following the section structure below.
4. If a page can't be found or fetched, say so explicitly and ask the user for the missing detail rather than fabricating a plausible-sounding policy. A venue profile is exactly the kind of factual claim this skill's own citation-verification discipline (`citation-verification.md`) applies to by extension: never invent what you can't verify.

## Profile file structure

Every venue profile follows this shape, so other reference files can point at "the active venue profile's page-limit section" etc. without knowing which specific venue is loaded:

```markdown
# <Venue> <Year> requirements

Verified against the live pages on <date verified — a plain fact about
the profile's own freshness, not a countdown to anything>. Sources:
- <CFP URL>
- <Author guidelines URL>
- <AI policy URL, if one exists>

## Page limits
- Submission: ...
- Camera-ready: ...
- What counts toward the limit and what doesn't (statements, references, appendix)

## Anonymization (or: this venue is not double-blind, if that's the case)
- ...

## AI use disclosure (if the venue has such a policy — many don't)
- Required vs. recommended disclosure, if the venue distinguishes them
- Where the statement goes and whether it counts toward the page limit

## Reviewing obligations (if the venue has a reciprocal/mandatory reviewing rule)
- ...

## Reproducibility / ethics statements (if the venue asks for them)
- ...

## Desk-rejection / rejection triggers
- Whatever is actually documented as an automatic rejection condition

## Template
- Where the official LaTeX/Word template lives, and whether this skill
  has a local copy under templates/<venue><year>/
```

Omit any section the venue doesn't have (not every venue requires an AI-use statement or has a reciprocal-reviewing obligation) rather than forcing empty sections to exist. A short profile is more honest than a padded one.

**Deliberately excluded from this schema: submission deadlines.** This skill's own behavior never depends on how close a deadline is, and a paper-writing tool has no reason to track a calendar. Where a venue's own policy mechanics reference a deadline as a concept (e.g. "reviewing eligibility is fixed as of the abstract-submission cutoff"), describe the *rule* without embedding the specific date — the current CFP is the authoritative source for the actual date, and this skill doesn't need to duplicate it. If you personally want to track your own deadline, that's outside this skill's scope, kept wherever you keep the rest of your project planning.

## Templates

`templates/<venue><year>/` mirrors the same per-venue-year pattern as profiles — fetch the official kit directly from its source repository (the way `templates/iclr2027/` was fetched from `github.com/ICLR/Master-Template`) rather than reconstructing it from memory. Not every venue profile needs a local template copy; some venues' templates are simple enough to reference by URL only in the profile's own "Template" section.

## Using an active profile elsewhere in this skill

Every other reference file that needs a venue-specific fact says "the active venue profile" rather than naming a venue — `pre-submission-checklist.md`'s page-count check, `citation-verification.md`'s AI-policy pointer, `reproducibility.md`'s statement-format pointer, `polish.md`'s conciseness note, all defer to whichever `venues/<venue><year>.md` is loaded for the current session. If no profile is loaded yet and a workflow needs a venue-specific fact, that's the signal to build one first (above), not to proceed on a guess.
