# EMNLP 2026 requirements

Verified against the live pages on 2026-09-03. Re-verify against these sources directly before relying on anything here for a final submission decision — policy pages can be revised after a CFP goes out:
- https://2026.emnlp.org/calls/main_conference_papers/
- https://aclrollingreview.org/cfp
- https://aclrollingreview.org/authors
- https://aclrollingreview.org/authorchecklist
- https://aclrollingreview.org/responsibleNLPresearch/
- https://2023.aclweb.org/blog/ACL-2023-policy/ (origin of the AI-writing-assistance checklist question, still in force)
- https://github.com/acl-org/acl-style-files

EMNLP 2026 is a hybrid conference in Budapest, Hungary — the currently-active, most-recently-completed EMNLP cycle as of this verification date. It runs on **ACL Rolling Review (ARR)**, the same shared reviewing system as ACL and NAACL. See `venues/acl2026.md` for the fuller explanation of the ARR mechanism; this file restates the shared rules in full (so it works standalone) and flags what's EMNLP-specific.

## Page limits

- **Long papers**: up to 8 pages of content; references unlimited and uncounted; the mandatory Limitations section (below) also uncounted.
- **Short papers**: up to 4 pages of content, same carve-outs.
- **Camera-ready**: accepted long papers get one additional content page (up to 9); accepted short papers get one additional content page (up to 5).
- Appendices unlimited but must match the main paper's double-column format; reviewers aren't obligated to read them.

## Anonymization (double-blind)

- Same ARR-wide double-blind policy as ACL: no author names, affiliations, or identifying self-references anywhere in the submission or supplementary material; self-citation phrased in third person.
- **Reviews remain double-blind throughout**: "Reviewers will not see authors, nor will authors see reviewers." No anonymity-period restriction on preprints — ARR's February 2024 policy change (no embargo on posting/discussing a non-anonymous preprint of a submitted paper) applies here too.
- Supplementary material must be anonymized; non-anonymous or tracking-enabled links are a listed problem.

## AI use disclosure

EMNLP's own CFP explicitly notes that AI writing assistance is permitted, pointing back to the ACL 2023 policy (see `venues/acl2026.md`'s AI-use-disclosure section for the exact checklist mechanics — same Responsible NLP Research Checklist, same question E1 on AI-assistant use, same "not for automatic desk rejection but for reviewer visibility and research-norms" framing). What's specific to EMNLP is a **stronger, explicitly named set of AI-related concerns in its own desk-rejection language** (below) — EMNLP's CFP calls out hallucinated citations and fully AI-generated papers by name in a way ACL's page didn't, which reads as a direct response to the recent wave of AI-assisted-submission problems in the field. Treat any output from this skill's own drafting/citation workflows accordingly: verify every citation is real (this skill's citation-verification discipline exists for exactly this reason) before submission, and keep the running note of what the skill touched, as recommended in the ACL profile.

## Reviewing obligations

- Same ARR-wide rule: all submitting authors are expected to sign up to review, or — EMNLP's own phrasing adds this explicitly — to serve as an Area Chair or Senior Area Chair, for the ARR cycle they submit to. Registration is due within 48 hours of that cycle's submission deadline; check the live ARR cycle page for the exact date.
- Non-compliance can carry a harsher consequence at EMNLP specifically: the CFP states ineligibility can extend to **both EMNLP 2026 and EMNLP 2027** for authors who don't meet their reviewing obligation, not just "the current and next ARR cycle" as the generic ARR language states — a two-conference-cycle penalty rather than a two-ARR-cycle one.

## Reproducibility / ethics — the Limitations section

- Mandatory Limitations section, placed after content and before references, uncounted toward the page limit — same requirement and same guidance (methodological caveats and confounders, not a "future work" section) as the rest of the ARR family.
- Papers must also follow ACL's Publication Ethics Policy and ARR's own Ethics Policy, including the mandatory Responsible NLP Research Checklist (limitations/risks, scientific-artifact licensing and documentation, computational-experiment reporting, human-subjects/annotator handling, AI-assistant use — see `venues/acl2026.md` for the full five-section breakdown).

## Desk-rejection triggers

- Page-limit violations; anonymity violations (identity, non-anonymized supplementary material, identifying links); dual/parallel submission to another archival venue during ARR review.
- **EMNLP-specific, explicitly named in its own CFP**: "hallucinated citations," "entirely AI-generated papers," and "thinly sliced contributions" — these three are called out by name as targets for desk rejection and for the extended EMNLP-2026-and-2027 ineligibility penalty described above, distinct from the more generic ARR-wide "salami slicing" language.
- Missing/misplaced Limitations section; an incomplete, generic, or misleading Responsible NLP Research Checklist.
- Not following the official ACL-family style template.
- Author-list changes during ARR-to-EMNLP commitment are not permitted; only author-order changes are allowed at that stage.

## Template

`templates/acl-style-files/` — same shared *ACL family package used for ACL, EMNLP, and NAACL, fetched from `github.com/acl-org/acl-style-files` (master branch) on 2026-09-03. See `venues/acl2026.md`'s Template section for the file list; nothing EMNLP-specific here — copy the whole directory when starting a new paper.
