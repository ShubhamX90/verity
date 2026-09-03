#!/usr/bin/env python3
r"""style_scan.py — mechanical prose scan. Read-only, stdlib only, Tier A.

Reports two kinds of findings, clearly separated:

  HARD FAILURES — objectively broken, not judgment calls: leaked non-English
  characters, unresolved [CLAIM NEEDS EVIDENCE]/PLACEHOLDER_/TODO markers,
  \cite{} with no matching .bib entry (a lighter check than check_citations.py's;
  run that one too for the full picture), and leaked AI-tool-interface markup
  (contentReference/oaicite, turn0search-style tokens, [cite: N], grok_card,
  ppl-ai-file-upload) — see de-ai-slop.md 1b for the source list.

  FLAGGED SUGGESTIONS — soft, every one a candidate for a Tier B
  Before/After/Why proposal, never auto-applied, never a hard fail. This
  explicitly includes passive voice, per Phase 2's decision to drop the
  zero-tolerance passive-voice rule: ML methods/experiments sections
  routinely and correctly use it, so it's flagged like anything else, not
  banned. Word/phrase/pattern list substantially expanded from a dedicated
  research pass (peer-reviewed excess-vocabulary studies, current
  practitioner discourse, structural-pattern documentation) — see
  de-ai-slop.md's "Research basis and version awareness" section for full
  citations and confidence grading. Includes a whole-file sentence-length
  "burstiness" score (de-ai-slop.md 1d item 4) alongside the per-line
  pattern matches.

This script never rewrites anything. It only ever prints a report.

Usage: style_scan.py --tex main.tex [main2.tex ...]
       style_scan.py --tex-dir paper/ --bib refs.bib
Exit code: 1 if any HARD failure found, 0 otherwise. Flagged suggestions
never affect the exit code — they're not failures.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# ---- Hard failures -----------------------------------------------------

CJK_RE = re.compile(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]+")
MARKER_RE = re.compile(r"\[CLAIM NEEDS EVIDENCE\]|PLACEHOLDER_\w*|\bTODO\b|\bXXX\b")
# Literal markup accidentally left behind from copy-pasting out of an AI
# chat interface without stripping its internal citation/reference syntax.
# Not a judgment call like everything else in this script \u2014 an objectively
# broken paste artifact. Source: Wikipedia:Signs of AI writing, which
# documents the exact strings each major tool's interface leaves behind
# (de-ai-slop.md 1b).
AI_TOOL_ARTIFACT_RE = re.compile(
    r"contentReference|\boaicite\b|\bturn\d+[a-zA-Z]+\d+\b|"
    r"\[cite:\s*\d+\]|\[span_\d+\]|\bgrok_card\b|ppl-ai-file-upload"
)
# [Cc]ite (not full IGNORECASE) matches natbib's capitalized sentence-initial
# forms (\Citet, \Citep, \Citeauthor) as well as the lowercase forms —
# consistent with check_citations.py's equivalent pattern. Without this, a
# capitalized cite command was invisible here while check_citations.py
# caught it, so the two scripts disagreed on the same input.
CITE_RE = re.compile(r"\\(?:full|text|paren|auto|foot)?[Cc]ite[a-zA-Z]*\*?(?:\[[^\]]*\])*\{([^}]+)\}")
BIBKEY_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,")

# ---- Flagged suggestions (soft — every hit is a candidate, not a fail) --

# "---" (true em-dash) and the unicode em/en-dash characters are unambiguous.
# " -- " (double-hyphen WITH surrounding spaces) is also matched \u2014 that's
# the LaTeX en-dash ligature typed as a stand-in for a rhetorical dash-pause
# in running prose, confirmed missed in a dry run against a real excerpt.
# Deliberately NOT matching a bare "--" with no surrounding spaces, since
# that's the legitimate range idiom ("pages 10--20", "Jan--Feb"), not a
# dramatic pause.
EM_DASH_RE = re.compile(r"---|\u2014|\u2013|\s--\s")

AI_WORDS_RE = re.compile(
    r"\b(leverag(?:e|es|ed|ing)|delve[sd]?(?: into)?|pivotal|paramount|"
    r"underscor(?:e|es|ed|ing)|seamless(?:ly)?|holistic(?:ally)?|"
    r"cutting-edge|groundbreaking|paradigm|realm|landscape|burgeoning|"
    r"multifaceted|nuanced|unprecedented|showcas(?:e|es|ed|ing)|intricate|"
    r"synerg(?:y|istic|ies)|notably|"
    # Added from peer-reviewed excess-vocabulary research (Kobak et al.
    # Science Advances 2025; Juzek & Ward COLING 2025) — de-ai-slop.md 1a.
    r"elucidat(?:e|es|ed|ing)|encompass(?:es|ed|ing)?|streamlin(?:e|es|ed|ing)|"
    r"unveil(?:s|ed|ing)?|garner(?:s|ed|ing)?|boast(?:s|ed|ing)?|"
    r"commendabl[ey]|meticulous(?:ly)?|transformative|advancements)\b",
    re.IGNORECASE,
)

# Multi-word AI-flavored phrases — de-ai-slop.md Part 1a. Kept separate from
# AI_WORDS_RE since these are phrase-level, not single-token, matches.
AI_PHRASES_RE = re.compile(
    r"\bunlock(?:s|ed|ing)? the potential\b|\bpave(?:s|d)? the way\b|"
    r"\bshed(?:s)? light on\b|\bplays? a (?:crucial|pivotal) role\b|"
    r"\ba testament to\b|\bparadigm shift\b|\bevolving landscape\b|"
    r"\bit is (?:worth noting|important to note) that\b",
    re.IGNORECASE,
)

# Sentence-initial connective throat-clearing — de-ai-slop.md Part 1b.
# Anchored to line start (a real limitation: misses a mid-paragraph sentence
# start after a period on the same source line — see prose-editing-policy.md
# for the human-judgment fallback this doesn't replace).
THROAT_CLEARING_RE = re.compile(
    r"^(?:Moreover|Furthermore|Additionally|Notably|Importantly|Indeed|"
    r"Ultimately|Crucially|In turn|That said|First and foremost)\b",
    re.MULTILINE,
)

# Meta-announcement throat-clearing — sentences that announce what a
# section is about to do instead of doing it. de-ai-slop.md Part 1b.
META_ANNOUNCEMENT_RE = re.compile(
    r"This (?:section|paper|work) (?:provides an overview of|"
    r"is organized as follows|describes|discusses)\b|"
    r"\bIn this (?:section|paper|work),? we (?:describe|discuss|present|provide)\b",
    re.IGNORECASE,
)

# "It's/This isn't just X, it's Y" / "not only X but Y" antithesis
# construction. de-ai-slop.md Part 1b. Over-catches on purpose (a
# candidate list, not a precision detector) — many real hits are
# legitimate contrasts. Covers "it's"/"this is"/"that is" (and their
# negative contractions) as the subject — a dry run against a real
# excerpt found "This isn't just X, it's Y" was missed when only "it's"
# was recognized as the opening subject.
ANTITHESIS_RE = re.compile(
    r"\b(?:it|this|that)('s| is)? ?n[o']t (?:just|only)\b[^.!?]{0,80}\b(?:it'?s|but)\b|"
    r"\bnot only\b[^.!?]{0,80}\bbut\b",
    re.IGNORECASE,
)

# "significantly" not accompanied by a number nearby in the same sentence —
# de-ai-slop.md Part 1c/1a: a statistical-sounding word used without the
# statistic. Heuristic only: checks for a digit within ~120 chars after the
# match, not true sentence boundaries, so it can both over- and under-catch.
UNSUPPORTED_SIGNIFICANTLY_RE = re.compile(
    r"\bsignificantly\s+(?:outperform|improve|exceed|increase|decrease|reduce|"
    r"better|worse|higher|lower|faster|slower)\w*\b", re.IGNORECASE
)

# Bare "significant" (adjective, not "significantly...") paired with a
# results-shaped noun, unsupported by a nearby number — same digit-proximity
# check as above. Added because research (Geng & Trotta, arXiv:2502.09606)
# found "significant" specifically DIDN'T decline the way "delve" did after
# public callout, i.e. it's under-suspected precisely for sounding ordinary
# — de-ai-slop.md's opening note. Excludes "statistically/clinically
# significant", which is a real technical claim, not filler.
UNSUPPORTED_SIGNIFICANT_RE = re.compile(
    r"(?<!statistically )(?<!clinically )\bsignificant\s+"
    r"(?:improvement|increase|decrease|difference|effect|gain|reduction|boost)s?\b",
    re.IGNORECASE,
)

# The colon-reveal: a short setup, a colon, a punchy one-word/short-phrase
# "payoff" — manufactured suspense. de-ai-slop.md 1b. Deliberately narrow
# (targets the specific documented cliché nouns) rather than flagging every
# colon, since colons are common and legitimate in academic prose
# (definitions, enumerations, "Table 2: Results").
COLON_REVEAL_RE = re.compile(
    r"\b(?:[Tt]he result|[Tt]he answer|[Tt]he outcome|[Tt]he takeaway)[:?]\s*\S",
)

# "While X ... also/further-work-needed Y" forced/diplomatic balance —
# de-ai-slop.md 1b. Over-catches on purpose; "while" openers are common and
# often fine, this narrows to the specific hedge-closer combination that's
# actually the documented tell.
FALSE_BALANCE_RE = re.compile(
    r"\bwhile\b[^.!?]{5,150}\b(?:it may also|it also (?:faces|presents)|"
    r"further work is needed|remains to be (?:seen|fully understood))\b",
    re.IGNORECASE,
)

# Empty-opener clichés — scene-setting sentence openers that could introduce
# any paper in any field. de-ai-slop.md 1b. Anchored to line start, same
# limitation as THROAT_CLEARING_RE.
EMPTY_OPENER_RE = re.compile(
    r"^(?:In today's|As the field continues to|As \w+ continues? to evolve|"
    r"Picture this)\b",
    re.MULTILINE | re.IGNORECASE,
)

WORDINESS_RE = re.compile(
    r"\bin order to\b|\bthe fact that\b|\bdue to the fact that\b|"
    r"\bthe question as to whether\b|\bowing to the fact that\b",
    re.IGNORECASE,
)

WEAK_QUALIFIER_RE = re.compile(
    r"\b(rather|very|pretty|quite|somewhat|fairly|certainly)\b", re.IGNORECASE
)

# Deliberately over-broad — a candidate list for a human to triage, same
# spirit as paper-writing-skill's M11, minus the "zero exceptions" framing.
PASSIVE_VOICE_RE = re.compile(
    r"\b(is|are|was|were|be|been|being)\s+"
    r"([a-z]+ed|done|made|shown|given|taken|held|built|drawn|chosen|"
    r"written|known|found|seen|set|put|sent|kept|met|run|used|based)\b",
    re.IGNORECASE,
)

EMPHASIS_RE = re.compile(r"\\(?:textbf|emph|textit)\{")


def strip_tex_comments(text: str) -> str:
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in text.splitlines())


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")
MATH_MODE_RE = re.compile(r"\$[^$]*\$")
TEX_COMMAND_WITH_ARG_RE = re.compile(r"\\[a-zA-Z]+(\[[^\]]*\])?(\{[^}]*\})?")

# de-ai-slop.md 1d, item 4: human prose has irregular sentence-length rhythm
# (coefficient of variation, i.e. stdev/mean, typically 0.6-1.2); LLM text
# tends toward a narrower range (commonly cited ~0.2-0.4). This is a soft,
# whole-file signal, not a per-line one — report it once per file, not once
# per sentence, and treat it with real skepticism (see de-ai-slop.md's
# corrective on over-indexing on any single surface signal). Needs a
# minimum sentence count to be statistically meaningful at all.
BURSTINESS_MIN_SENTENCES = 10
BURSTINESS_LOW_THRESHOLD = 0.4


def compute_burstiness(text: str) -> tuple[float | None, int]:
    """Returns (coefficient of variation of sentence length in words, sentence
    count used). Returns (None, n) if there aren't enough sentences for the
    statistic to mean anything."""
    clean = MATH_MODE_RE.sub(" ", text)
    clean = TEX_COMMAND_WITH_ARG_RE.sub(" ", clean)
    sentences = SENTENCE_SPLIT_RE.split(clean)
    lengths = [len(s.split()) for s in sentences if len(s.split()) >= 3]
    if len(lengths) < BURSTINESS_MIN_SENTENCES:
        return None, len(lengths)
    mean = sum(lengths) / len(lengths)
    if mean == 0:
        return None, len(lengths)
    variance = sum((x - mean) ** 2 for x in lengths) / len(lengths)
    stdev = variance ** 0.5
    return stdev / mean, len(lengths)


def scan_file(path: Path, bib_keys: set[str]) -> tuple[list[str], list[str]]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    text = strip_tex_comments(raw)
    hard: list[str] = []
    soft: list[str] = []

    for m in CJK_RE.finditer(text):
        hard.append(f"{path}:{line_of(text, m.start())}: non-English characters: ...{m.group()[:20]}...")

    for m in MARKER_RE.finditer(text):
        hard.append(f"{path}:{line_of(text, m.start())}: unresolved marker: {m.group()}")

    for m in CITE_RE.finditer(text):
        for key in m.group(1).split(","):
            key = key.strip()
            if key and bib_keys and key not in bib_keys:
                hard.append(f"{path}:{line_of(text, m.start())}: \\cite{{{key}}} not found in supplied .bib file(s)")

    for m in AI_TOOL_ARTIFACT_RE.finditer(text):
        hard.append(f"{path}:{line_of(text, m.start())}: leaked AI-tool markup artifact: '{m.group()}' — text was pasted from a chat interface without stripping its internal syntax")

    for m in EM_DASH_RE.finditer(text):
        soft.append(f"{path}:{line_of(text, m.start())}: em-dash")

    for m in AI_WORDS_RE.finditer(text):
        soft.append(f"{path}:{line_of(text, m.start())}: AI-flavored word: '{m.group()}' — swap only if it carries no precise technical meaning here")

    for m in AI_PHRASES_RE.finditer(text):
        soft.append(f"{path}:{line_of(text, m.start())}: AI-flavored phrase (de-ai-slop.md 1a): '{m.group()}'")

    throat_clearing_lines: list[int] = []
    for m in THROAT_CLEARING_RE.finditer(text):
        ln = line_of(text, m.start())
        soft.append(f"{path}:{ln}: throat-clearing opener: '{m.group()}'")
        throat_clearing_lines.append(ln)
    # Stacking: two or more connective openers within 3 lines of each other
    # reads as consecutive sentences leaning on the same crutch in a row —
    # de-ai-slop.md 1b. Report once per adjacent pair, not every combination.
    for prev, cur in zip(throat_clearing_lines, throat_clearing_lines[1:]):
        if cur - prev <= 3:
            soft.append(f"{path}:{prev}-{cur}: throat-clearing openers stacked within {cur - prev} line(s) of each other")

    for m in META_ANNOUNCEMENT_RE.finditer(text):
        soft.append(f"{path}:{line_of(text, m.start())}: meta-announcement (de-ai-slop.md 1b): '{m.group()}' — states what the section will do instead of doing it")

    for m in ANTITHESIS_RE.finditer(text):
        soft.append(f"{path}:{line_of(text, m.start())}: antithesis construction (de-ai-slop.md 1b): '{m.group()[:60]}...'")

    for m in UNSUPPORTED_SIGNIFICANTLY_RE.finditer(text):
        window = text[m.end(): m.end() + 120]
        if not re.search(r"\d", window):
            soft.append(f"{path}:{line_of(text, m.start())}: 'significantly' with no number in the following ~120 characters — unsupported superlative (de-ai-slop.md 1c): '{m.group()}'")

    for m in UNSUPPORTED_SIGNIFICANT_RE.finditer(text):
        window = text[m.end(): m.end() + 120]
        if not re.search(r"\d", window):
            soft.append(f"{path}:{line_of(text, m.start())}: 'significant' with no number in the following ~120 characters — under-suspected filler (de-ai-slop.md intro note): '{m.group()}'")

    for m in COLON_REVEAL_RE.finditer(text):
        soft.append(f"{path}:{line_of(text, m.start())}: colon-reveal construction (de-ai-slop.md 1b): '{m.group()}'")

    for m in FALSE_BALANCE_RE.finditer(text):
        soft.append(f"{path}:{line_of(text, m.start())}: forced/diplomatic balance (de-ai-slop.md 1b): '{m.group()[:60]}...'")

    for m in EMPTY_OPENER_RE.finditer(text):
        soft.append(f"{path}:{line_of(text, m.start())}: empty-opener cliché (de-ai-slop.md 1b): '{m.group()}'")

    for m in WORDINESS_RE.finditer(text):
        soft.append(f"{path}:{line_of(text, m.start())}: wordy phrase: '{m.group()}'")

    for m in WEAK_QUALIFIER_RE.finditer(text):
        soft.append(f"{path}:{line_of(text, m.start())}: weak qualifier: '{m.group()}'")

    for m in PASSIVE_VOICE_RE.finditer(text):
        soft.append(f"{path}:{line_of(text, m.start())}: possible passive voice: '{m.group()}' — flag only, not an automatic rewrite; often correct in methods/experiments")

    n_emph = len(EMPHASIS_RE.findall(text))
    if n_emph > 3:
        soft.append(f"{path}: {n_emph} bold/italic emphasis commands in body text — consider whether sentence position could carry the emphasis instead")

    cv, n_sentences = compute_burstiness(text)
    if cv is not None and cv < BURSTINESS_LOW_THRESHOLD:
        soft.append(
            f"{path}: low sentence-length variation (coefficient of variation {cv:.2f} across "
            f"{n_sentences} sentences, human prose is typically 0.6-1.2 — de-ai-slop.md 1d item 4) "
            f"— a whole-file signal, treat with real skepticism, not evidence on its own"
        )

    return hard, soft


def collect_bib_keys(bib_files: list[Path]) -> set[str]:
    keys: set[str] = set()
    for f in bib_files:
        text = f.read_text(encoding="utf-8", errors="replace")
        keys.update(BIBKEY_RE.findall(text))
    return keys


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tex", nargs="*", default=[])
    ap.add_argument("--tex-dir")
    ap.add_argument("--bib", nargs="*", default=[], help="optional — enables the broken-\\cite hard-fail check")
    args = ap.parse_args()

    tex_files = [Path(p) for p in args.tex]
    if args.tex_dir:
        tex_files += sorted(Path(args.tex_dir).rglob("*.tex"))
    bib_files = [Path(p) for p in args.bib]

    missing = [p for p in tex_files + bib_files if not p.is_file()]
    if missing:
        print(f"error: file(s) not found: {', '.join(str(p) for p in missing)}", file=sys.stderr)
        return 2
    if not tex_files:
        print("error: no .tex files given (use --tex or --tex-dir)", file=sys.stderr)
        return 2

    bib_keys = collect_bib_keys(bib_files) if bib_files else set()

    all_hard: list[str] = []
    all_soft: list[str] = []
    for f in tex_files:
        hard, soft = scan_file(f, bib_keys)
        all_hard += hard
        all_soft += soft

    print(f"scanned {len(tex_files)} .tex file(s)")
    if all_hard:
        print(f"\n== HARD FAILURES ({len(all_hard)}) — objectively broken, fix directly ==")
        for h in all_hard:
            print(f"  {h}")
    if all_soft:
        print(f"\n== FLAGGED SUGGESTIONS ({len(all_soft)}) — each is a candidate for a Tier B "
              f"Before/After/Why proposal; none are auto-applied, none are hard bans ==")
        for s in all_soft:
            print(f"  {s}")
    if not all_hard and not all_soft:
        print("CLEAN")

    return 1 if all_hard else 0


if __name__ == "__main__":
    sys.exit(main())
