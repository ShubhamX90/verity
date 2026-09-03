# Citation verification workflow

**The single non-negotiable rule in this whole skill: never write a BibTeX entry from memory.** Peer-reviewed studies have measured LLM-generated academic citations as fabricated (referring to a paper that doesn't exist at all) at rates from roughly 18% up to 55%+ depending on the model, with additional real citations still carrying substantive metadata errors on top of that — see "Why this rule exists, with sources" below. A fabricated reference in a submitted paper can be a Code of Ethics matter at many venues, not a typo — check the active venue profile's AI-policy section (`venue-profile.md`) for the specific consequence language, if the venue has one. This rule has no exceptions and no autonomy tier discussion regardless of what a specific venue's policy says: it's not something that gets more permissive under Tier A.

### Why this rule exists, with sources

Rates vary by model, task, and domain — there is no single universal "AI citation error rate," and any claim stating one flat number should be treated skeptically (including a commonly-repeated "~40%" figure, which traces to real studies but is a rounded average across specific models/tasks, not a fixed constant):

- Walters & Wilder, *Scientific Reports* 13:14045 (2023) — 636 citations, 42 topics: **55% of GPT-3.5 citations fully fabricated vs. 18% of GPT-4 citations**; among the *real* (non-fabricated) citations, 43% (GPT-3.5) and 24% (GPT-4) still had substantive errors (wrong volume, issue, pages, authors).
- Chelli et al., *Journal of Medical Internet Research* (2024), systematic-review literature retrieval: **GPT-3.5 39.6% hallucinated, GPT-4 28.6%, Bard 91.4%**; precision (references that actually existed in the source material) as low as 9–13% for the weakest model.
- Cabezas-Clavijo & Sidorenko-Bautista (2025), arXiv:2505.18059, 8 chatbots (ChatGPT, Claude, Copilot, DeepSeek, Gemini, Grok, Le Chat, Perplexity), 400 references: 26.5% fully correct, 33.8% partially correct, **39.8% erroneous or fabricated** — this is the specific study a commonly-quoted "~40% of AI citations are wrong" figure traces back to.

The clear trend across all of these: newer/larger models fabricate less (GPT-3.5-era ~55% down to GPT-4-era ~18–29%), but the rate never reaches zero for any model measured, and even a *correctly-existing* citation still carries a meaningful chance of a wrong claim attribution or wrong bibliographic detail. That residual, non-zero rate at every model tier — not a specific number from a specific year — is the actual justification for treating every single citation as unverified until checked, regardless of which model produced it or how capable that model is generally.

## API stack (v1 — deliberately minimal)

- **Semantic Scholar API** — primary search and discovery. Good ML/AI coverage, citation graph, ~free tier.
- **CrossRef** — the BibTeX-fetch authority for anything with a DOI, via content negotiation (no API key needed; use a `mailto` param for the polite pool).
- **arXiv** — native BibTeX export endpoint for preprints, preferred over parsing Semantic Scholar's arXiv metadata since it's the authoritative source for arXiv's own records.
- **Google Scholar**: discovery-only if you use it manually; no official API, not wired into any script (scraping violates ToS).

**Deliberately not included in v1**: DBLP and OpenAlex were considered in Phase 2 planning and set aside to keep the dependency surface small — noted here as the natural next addition if Semantic Scholar + CrossRef coverage proves insufficient for a specific reference (DBLP in particular has strong CS-conference coverage that Semantic Scholar sometimes misses). If you hit a paper that genuinely can't be verified through the current two sources, that's the signal to revisit this, not a reason to lower the verification bar.

## The workflow

1. **Identify**: DOI > arXiv ID > publisher landing page, in that priority order.
2. **Search**: Semantic Scholar API (`scripts/fetch_bibtex.sh` and manual WebSearch/WebFetch as needed).
3. **Cross-verify**: confirm the paper exists in **2 sources** — Semantic Scholar plus CrossRef (via the DOI, if there is one) or arXiv (if it's a preprint). One source alone is not enough to trust a bibliographic record.
4. **Fetch BibTeX programmatically** — never type it by hand from what a landing page shows:
   - DOI: `curl -sL -H "Accept: application/x-bibtex" "https://doi.org/<doi>"` (CrossRef content negotiation).
   - arXiv: `curl -sL "https://arxiv.org/bibtex/<arxiv_id>"` (arXiv's own BibTeX export, not a hand-built `@misc`).
   - Both wrapped in `scripts/fetch_bibtex.sh` — see that script's header for usage.
5. **Claim-level check**: if the citation supports a specific claim (not just general background), confirm the claim actually appears in the abstract or fetched text before treating it as verified. A paper existing is not the same as a paper supporting the specific thing you're citing it for.
6. **Add to `refs.bib`** only after steps 1–5 all succeed.

## When verification fails at any step

Never invent a similar-sounding paper, never guess a DOI, never fill in plausible-looking fields. Instead:

```latex
\cite{PLACEHOLDER_author_year}  % TODO verify — could not confirm via Semantic Scholar/CrossRef/arXiv
```

Tell the user explicitly how many placeholders exist and why each failed (not found / found but no DOI / found but claim doesn't match), in the same session — don't let this surface only at a later mechanical scan.

## Tier placement — where each step sits in the autonomy model

Per `SKILL.md`'s two-tier model:

| Action | Tier | Why |
|---|---|---|
| Search / verify / fetch BibTeX for a candidate citation | **A** — proactive, no pre-approval needed to run | Pure research; nothing in the paper changes yet |
| Normalize an *existing* `.bib` entry (key format, field completeness, sorting, adding a missing locator field to an entry already present) | **A** | Doesn't change what the paper claims or cites |
| **Inserting a *new* `\cite{}` into the paper text** | **B** — propose, wait for approval | Confirmed in Phase 2: even a fully-verified citation is a content decision once it's attached to a specific claim — it asserts that source backs that sentence. Surface the candidate (verified BibTeX + the sentence it would support + why) and wait, using the standard `Before / After / Why` format from `prose-editing-policy.md`. Before presenting, run it through `self-certification.md`'s fresh-context check — its question here is specifically whether the citation is being attached to the claim it actually supports, not a nearby-but-different claim the fresh check would catch precisely because it isn't carrying the reasoning that picked this citation in the first place |

## Mechanical post-hoc check (Tier A, always safe to run)

`scripts/check_citations.py` — static analysis only, never fetches or inserts anything:
- Every `\cite{key}` has a matching `.bib` entry (catches broken citations before they compile to `[?]`, which is exactly where a hallucinated reference would otherwise hide unnoticed).
- Every `.bib` entry is actually cited somewhere (dead weight, or a forgotten citation site).
- No duplicate `.bib` keys.
- Every `.bib` entry carries a locator (`doi`, `eprint`, `url`, or `isbn`) — an entry with none is exactly where a fabricated citation would be hardest to catch, since there's nothing to click through and check.

Run this after any citation work and before a pre-submission check (`pre-submission-checklist.md`).

## Finding candidate uncited claims (Tier A, scan-only)

`scripts/find_uncited_claims.py` flags sentences that look like they need a citation and don't have one nearby — related-work language ("recent work has shown..."), comparison claims ("outperforms X"), unattributed method/dataset proper nouns, unsupported numeric claims. This is a **scanner only** — it produces a list of candidate locations for you to look at, it never searches for or inserts a citation on its own. Turning a flagged location into an actual citation goes through the full six-step workflow above, ending at the Tier B approval gate.
