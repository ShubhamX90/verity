# Reference audit: a full retrospective check of every citation already in the paper

A distinct workflow from `citation-verification.md`, which governs verifying a citation *before* it's added to the paper, one at a time, while drafting. This file governs the opposite direction: taking a paper that already has a populated `.bib` file and checking every single entry in it against its real, canonical published record, all at once, as a pre-submission pass. Run both — they catch different failure windows. `check_citations.py` (also part of `citation-verification.md`) catches a third, narrower thing: internal `.tex`/`.bib` consistency (a `\cite{}` with no matching entry, a duplicate key) without ever checking whether an entry's claimed metadata is actually correct.

**Entirely Tier A: research and reporting only.** This workflow never edits `.bib` or `.tex` files itself. If it turns up a genuinely fabricated or badly wrong reference, removing or replacing the citation in the paper text is a content decision — route it through `citation-verification.md`'s existing Tier B insertion/normalization step (for a replacement) or surface it as an ordinary Tier B proposal (for a removal), the same as any other change to what the paper claims.

**Why this exists, briefly**: `citation-verification.md` already covers why a citation must never be written from memory and cites the underlying fabrication-rate studies (Walters & Wilder 2023, Chelli et al. 2024, Cabezas-Clavijo & Sidorenko-Bautista 2025) — read that file's "Why this rule exists" section rather than duplicating it here. What's added here is the retrospective audit *procedure*: given a paper that may already contain citations added at different times, by different authors, with different levels of care, verify every single one against its real source before submission, and produce a structured report of what was found.

## When to run this

Before submission, on a paper that's at or near its final reference list — not useful yet on a paper still actively adding citations, since it would just re-flag entries that are about to change anyway. Re-run it if the reference list changes materially after the first pass (a new co-author's edit added several citations, a revision added a new related-work paragraph).

## Phase 1 — Extract every reference

1. Read the paper's actual References/Bibliography section (or the `.bib` file that generates it) — not appendix headings, tables, or inline URLs in the body, which aren't bibliography entries.
2. For each entry, extract: `ref_key`, authors as written (including any "et al." or "and others" placeholder), title, venue, year, identifiers (DOI/arXiv ID/URL/ISBN), and the raw citation text.
3. Separately, note every in-text `\cite{}`/`\citep{}`/`\citet{}` key used in the body, for the cross-check in Phase 4.

## Phase 2 — Completeness and placeholder detection

A valid reference needs at least one author, a title, and a venue (exception: an informal, pre-1950 reference, where this is sometimes genuinely unavailable). Flag anything missing one of these as **INCOMPLETE**. Record any author-list placeholder ("et al.," "and others," "and N others," a trailing comma implying omitted authors) and how many authors are explicitly named, since Phase 3's truncation check needs this.

## Phase 3 — Verify existence and metadata

For each non-incomplete reference, using web search and page-reading against the paper's real, canonical source — never trusting a search-result snippet on its own:

1. Search the title in quotes plus the first author's last name.
2. If an arXiv ID or DOI is present, open it directly (`https://arxiv.org/abs/<id>` for arXiv) and confirm it's actually this work — don't just trust that the identifier string looks plausible.
3. Open the best candidate's canonical page — arXiv abstract page, ACL Anthology, publisher page, DOI record, dblp, or a library catalog for a book — and read the real title and full author list there.
4. If the reference cites only an arXiv preprint, check whether it has since been formally published (the arXiv page's "Journal reference"/"Comments" field, or one more search for the title plus "proceedings"/"ACL Anthology"/"dblp" — the same check `citation-verification.md`'s Step 1 now applies going forward). If nothing turns up, treat the arXiv version as the only known publication for this pass.
5. If two searches and an identifier lookup all fail, classify as **NOT FOUND**.

Compare these fields and record every discrepancy:

| Field | What counts as a mismatch |
|---|---|
| Title | A content-word mismatch, not just a casing/hyphenation difference |
| Authors | Any named author not on the real paper, or different lead authors |
| Truncation | A placeholder that materially understates the real author count (e.g. "and 1 others" after 6 named, but the real paper has 51) |
| Venue | A wrong conference/workshop, or a superseded arXiv preprint that's since been formally published — record the real venue so the citation can be corrected |
| Year | A mismatched publication year (the arXiv year is fine for a genuine, still-unpublished preprint) |
| Identifier | A DOI/arXiv ID that doesn't resolve to this exact work. Separately flag (for manual review, not an automatic fail) an arXiv ID whose encoded year/month is in the future |

Assign a **status**:
- **VERIFIED** — real record found, every field matches, no misleading truncation.
- **MALFORMED** — real record found, but at least one field is wrong; name the failing fields, e.g. "MALFORMED (title, authors)".
- **NOT FOUND** — no real record found after a title search, an author-plus-keyword search, and an identifier lookup. A flag for manual review, not proof of fabrication.
- **UNVERIFIABLE** — plausibly real but can't be confirmed online (an anonymized submission, an obscure regional book, a paywalled record). State why.

Assign a **confidence**: High (canonical record opened, fields compared directly), Medium (strong search evidence but the canonical page couldn't be fully opened), Low (weak or conflicting evidence — explain why).

## Phase 4 — Consistency checks

1. Flag any two entries referring to the same underlying work that disagree on year, venue, or edition.
2. Cross-check in-text citation keys against the bibliography: any in-text citation with no bibliography entry, and any bibliography entry never cited in the body. Both are advisory, not errors on their own — `check_citations.py` already catches the hard version of the first one (a genuinely broken `\cite{}`) mechanically; this phase is the softer, judgment-level version applied specifically while doing the audit read-through.

## Phase 5 (optional, best-effort) — Claim consistency

Pick up to five in-text citations that make a specific empirical or definitional claim. Open each cited work's abstract and judge whether the citing sentence is plausibly supported. Record **SUPPORTED**, **UNSUPPORTED**, or **UNCHECKED** with a one-line reason. Skip this phase if time is short — it's the most valuable phase per citation checked, but also the slowest, so it's the one to drop first under time pressure, not silently fold into a lower confidence rating elsewhere.

## Phase 6 — Write the report

Write the report in the same prose style this skill holds every other piece of writing to — see `writing-craft.md`'s register note and `de-ai-slop.md`'s punctuation guidance (no em/en dashes or semicolons as connectors, no colon-continuations, full sentences). Use this structure:

```markdown
# Reference Audit

## Summary
- Paper: {name}
- Total references extracted: N
- Verified: V
- Malformed (real work, wrong metadata): M
- Not found (possible fabrication): F
- Unverifiable: U
- Incomplete: W

## Detailed Results
A table with columns: # | Ref | Status | Confidence | Cited title | Issue(s) | Canonical source (URL).
Every row, including VERIFIED ones, carries a canonical source URL where one
exists, so each verdict is auditable.

## Malformed References
For each: raw citation, a field-by-field cited-vs-real comparison (title,
authors plus real author count, venue, year, identifier), the canonical
source URL, and, if it's a superseded-preprint case, the correct citation
to use instead.

## Not Found References
For each: raw citation, authors listed, search queries tried, outcome.

## Unverifiable References
For each: raw citation and the reason it can't be confirmed.

## Incomplete References
For each: ref_key, raw text (first 200 characters), missing fields.

## Consistency Issues
Duplicate-work clusters, orphan in-text cites, uncited bibliography
entries. Write "None found" if there are none.

## Claim Consistency
If Phase 5 was run, list the sampled claims and their verdicts. Otherwise
write "Not performed in this pass."

## Methodology Note
One paragraph explaining VERIFIED vs. MALFORMED vs. NOT FOUND vs.
UNVERIFIABLE, noting that NOT FOUND is a flag for manual review rather
than proof of fabrication, and that some genuine works (anonymized
submissions, obscure books, paywalled records) may be UNVERIFIABLE.
```

## After the report: routing findings back into the rest of this skill

- A **NOT FOUND** or badly **MALFORMED** entry that turns out to be genuinely fabricated: tell the user explicitly, the same disclosure discipline `citation-verification.md` requires when a *new* citation fails verification. Removing it, or replacing it with a `PLACEHOLDER_author_year` pending a real source, is a Tier B content change.
- A **MALFORMED** entry that's a real paper with wrong fields (a superseded arXiv preprint, a wrong year, a truncated author list): re-fetch the correct BibTeX per `citation-verification.md`'s workflow and propose the corrected entry — normalizing an *existing* entry to fix its own fields is Tier A (per `citation-verification.md`'s tier table), but if the correction changes which specific claim the citation is understood to support, treat it as Tier B instead.
- **Consistency issues** (orphan cites, uncited entries, duplicate-work clusters) feed into the ordinary pre-submission pass — see `pre-submission-checklist.md`.
