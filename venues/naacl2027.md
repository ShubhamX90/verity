# NAACL 2027 requirements

Verified against the live pages on 2026-09-03. Re-verify against these sources directly before relying on anything here for a final submission decision — policy pages can be revised after a CFP goes out:
- https://2027.naacl.org/calls/main_conference_papers/
- https://www.aclweb.org/portal/content/call-main-conference-papers-naacl-2027
- https://aclrollingreview.org/cfp
- https://aclrollingreview.org/authors
- https://aclrollingreview.org/authorchecklist
- https://aclrollingreview.org/responsibleNLPresearch/
- https://aclrollingreview.org/dates
- https://github.com/acl-org/acl-style-files

**Naming note — read this before assuming a typo**: this file is `naacl2027.md`, not `naacl2026.md`, because ACL's own numbering calls this conference "NAACL 2027" (held in San Francisco), even though the ARR cycle that feeds it is the **October 2026** cycle. There is no separate "NAACL 2026" main-conference CFP — NAACL isn't held every calendar year, and the ACL portal's own most recent NAACL main-conference call is explicitly titled "NAACL 2027." Use the venue's own self-declared year, not the ARR cycle's calendar year, when naming a profile like this.

NAACL runs on **ACL Rolling Review (ARR)**, the same shared reviewing system as ACL and EMNLP — see `venues/acl2026.md` for the fuller explanation of the mechanism. This file restates the shared rules in full (so it works standalone) and flags what's NAACL-specific. NAACL 2027 shares its ARR cycle (October 2026) with **COLING 2027**; at commitment time, authors must designate one of the two as their primary conference — a binding choice, not a hedge across both.

## Page limits

- **Long papers**: up to 8 pages of content; references unlimited and uncounted; the mandatory Limitations section (below) also uncounted.
- **Short papers**: up to 4 pages of content, same carve-outs.
- **Camera-ready**: accepted long papers get one additional content page (up to 9); accepted short papers get one additional content page (up to 5).

## Anonymization (double-blind)

- Standard ARR-wide double-blind policy: no author names, affiliations, or identifying self-references in the main text or supplementary material; self-citation in third person.
- The CFP's own phrasing is explicit that this extends past reviewers: "Reviewers will not see authors, nor will authors see reviewers **and reviews on ARR will not be made publicly visible**" — a slightly stronger visibility statement than ACL's or EMNLP's own CFP pages used, though it describes the same underlying ARR anonymity system, not a NAACL-specific extra rule.
- No anonymity-period restriction on preprints, per the shared ARR policy (in force since February 2024).

## AI use disclosure

NAACL's own CFP page doesn't restate an AI-use policy beyond pointing at ARR's shared requirements — it is silent on the topic in the specific page fetched for this profile. Treat the shared ARR mechanism as authoritative here: the mandatory Responsible NLP Research Checklist's question E1 (AI-assistant use disclosure, tied to the ACL Publication Ethics Policy's authorship rules) applies to NAACL submissions exactly as it does to ACL and EMNLP ones. See `venues/acl2026.md`'s AI-use-disclosure section for the full mechanics.

## Reviewing obligations

- Same ARR-wide rule: all submitting authors must register as reviewers for the October 2026 ARR cycle. NAACL's own CFP names this "Reviewer registration deadline for **ALL** authors" (its emphasis) — worth flagging because it's phrased more absolutely than the generic ARR language, though it describes the same one-registration-per-submitting-author requirement, not a stricter NAACL-only rule. Check the live ARR cycle page for the exact date rather than relying on any date recorded here.
- Non-compliance carries the standard ARR penalty (ineligibility to (re)submit or commit during the current and next ARR cycle) unless NAACL's own page says otherwise — it didn't, as fetched.

## Reproducibility / ethics — the Limitations section

- Mandatory Limitations section, uncounted toward the page limit, same placement and content guidance as the rest of the ARR family.
- Submissions must comply with "ACL's Publication Ethics Policy, and ARR's Ethics Policy including the responsible NLP research checklist" — NAACL's CFP states this almost verbatim from the shared ARR requirement, without adding NAACL-specific ethics review machinery beyond it.

## Desk-rejection triggers

NAACL's own CFP, as fetched, does not enumerate its own separate list of desk-rejection triggers the way EMNLP's does (no NAACL-specific callouts like EMNLP's "hallucinated citations" language, and no ACL-2026-style "unregistered presenting author" clause were found on the page). Treat the shared ARR-wide list as authoritative for NAACL: page-limit violations, anonymity violations, dual/parallel submission, missing or misplaced Limitations section, an incomplete or misleading Responsible NLP Research Checklist, not using the official style template, and prompt-injection attempts against automated screening — see `venues/acl2026.md`'s Desk-rejection triggers section for the full list with its ARR sourcing. Re-check NAACL's own CFP page directly for any NAACL-added condition before submitting, since this profile can't rule out that one exists and simply wasn't surfaced by the fetch used to build it.

- One NAACL-stated mechanical rule that functions as a hard constraint rather than a "trigger": author-list changes are not permitted at ARR-to-NAACL commitment time; only author-order changes are.

## Template

`templates/acl-style-files/` — same shared *ACL family package used for ACL, EMNLP, and NAACL, fetched from `github.com/acl-org/acl-style-files` (master branch) on 2026-09-03. See `venues/acl2026.md`'s Template section for the file list; nothing NAACL-specific here — copy the whole directory when starting a new paper.
