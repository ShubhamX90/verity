# NeurIPS 2026 requirements

Verified against the live pages on 2026-09-03. Re-verify against these sources directly before relying on anything here for a final submission decision — policy pages can be revised after a CFP goes out, and this cycle's review process was still in progress as of the verification date:
- https://neurips.cc/Conferences/2026/CallForPapers
- https://neurips.cc/Conferences/2026/MainTrackHandbook
- `templates/neurips2026/neurips_2026.tex` (the official style file itself — quoted below where it states policy more precisely than the handbook prose)

This is the Main Track profile. NeurIPS also runs a separate Position Paper track and an Evaluations & Datasets track with their own calls (`CallForPositionPapers` was not fetched; the Position track's LLM policy is explicitly *stricter* than the main track's — it requires papers to be "substantially human-written," per `blog.neurips.cc/2026/06/02/ai-generated-papers-in-the-neurips-2026-position-paper-track/`). If you're writing for a track other than the main track, build a separate profile rather than assuming this one applies.

## Page limits

- **Submission**: main text ≤ 9 pages, including all figures and tables. The style file itself states it most directly: *"Papers may only be up to nine pages long, including figures. Papers that exceed the page limit will not be reviewed (or in any other way considered) for presentation at the conference."*
- References do not count toward the limit. Acknowledgments, the paper checklist, and technical appendices also don't count — the template: *"Additional pages containing acknowledgments, references, checklist, and optional technical appendices do not count as content pages."* Technical appendices have no page limit.
- **Camera-ready**: 10 pages — the Main Track Handbook grants accepted papers one additional content page beyond the 9-page submission limit, with all content (main text, references, appendices, checklist) combined into a single final PDF. Max submission file size is 50MB.

## Anonymization (double-blind)

- Submissions must contain no identifying information that would violate double-blind reviewing. The handbook: *"Papers violating this policy will be desk rejected."*
- Self-citation: cite your own prior work in third person, anonymized — the handbook's own example is *"In the previous work of Smith et al. [1]…"*, not "In our previous work [1]…". For directly concurrent (also-anonymous) work, cite it as *"Anonymous et al. [1] concurrently show…"* and include the anonymized paper as supplementary material if needed.
- Supplementary/code material "should be created by the authors that directly supports the submission content, and, as with the main submission, be anonymized."
- Preprints (e.g. arXiv) posted non-anonymously are permitted — NeurIPS does not require you to avoid posting a preprint — but aggressive advertising of a paper under review may violate the policy; don't publicize the submission as a NeurIPS submission during review.
- During rebuttal, if reviewers ask for code you can send an anonymized link to the AC via an Official Comment, but "make sure all linked files are anonymized."

## AI / LLM use disclosure

Narrower and more targeted than a blanket disclosure requirement — NeurIPS only asks you to document *methodologically significant* agent/LLM use, not general writing assistance:

- **Must be disclosed** (in the experimental setup section or equivalent): use of agents and/or LLMs *"in implementing the method... if it is an important, original, or non-standard component of the approach, e.g. if the paper is about using an LLM as a search heuristic."*
- **Does not need to be documented**: "The use of spell checkers and grammar suggestions, aid for editing purposes, and basic code assistance."
- **Hard rule**: "Agents and LLMs cannot be authors." Authors remain fully responsible for the accuracy of all content, LLM-assisted or not.
- This is a *different, and less prescriptive,* disclosure model than ICLR 2027's explicit required/recommended taxonomy — don't reuse ICLR's disclosure checklist for a NeurIPS paper; the bar here is "did an agent/LLM do something methodologically load-bearing," not "did AI touch any part of the writing process."

## Reviewing — the reciprocal-reviewing mechanism

NeurIPS ties reviewing quality for author-reviewers directly to the visibility of their own paper's reviews, rather than stating a flat "review N papers" quota the way ICLR/ICML do:

- *"Authors who are also reviewers will not see the reviews of their own submission(s) unless they have completed all assigned reviews"* — access is withheld until all assigned reviews are in, up to two days before the rebuttal deadline ends. The same mechanism applies to author-ACs and their own meta-reviews.
- Grossly negligent reviewer-authors risk desk rejection of their own submitted papers as a last-resort sanction at the meta-review stage.
- **Ambiguity flagged**: NeurIPS 2025 ran a "Responsible Reviewing Initiative" under which every submission had to nominate a reciprocal reviewer from among its authors (per `blog.neurips.cc/2025/05/02/responsible-reviewing-initiative-for-neurips-2025/`). The 2026 CallForPapers page still points to the Main Track Handbook for "policies regarding reciprocal reviewing," but the handbook content actually fetched for this profile did not surface an explicit numeric nomination requirement — only the review-withholding and desk-rejection consequences above. Treat "does NeurIPS 2026 require every submission to nominate a specific reviewing author" as **unconfirmed**; check the live Main Track Handbook's reviewing section directly (it may be paginated or gated behind an author-console view not visible to an unauthenticated fetch) before assuming either way.

## Dual submission policy

- *"The reviewing process will treat any other archival submission by an overlapping set of authors as prior work"* — dual submissions to non-archival workshops are explicitly permitted, but submitting the same work to another archival venue while still under review at NeurIPS is explicitly prohibited: *"we explicitly prohibit submitting work to NeurIPS and then later submitting the same work to another archival venue while it is still under review at NeurIPS."*
- Failure to comply "is grounds for desk rejection during any point of the reviewing and program building process."

## Reproducibility / ethics / societal impact — the paper checklist (mandatory)

- A **paper checklist is mandatory** for every submission (`templates/neurips2026/checklist.tex` is the exact form bundled with the template — copy it in when starting a new paper). Its stated purpose: *"to help authors reflect on a wide variety of issues relating to responsible machine learning research, including reproducibility, transparency, research ethics, and societal impact."*
- It covers reproducibility mechanics (code/data availability, hyperparameters, compute resources), ethical practices (human subjects, data privacy, consent, bias), broader societal-impact considerations (safety, security, discrimination, surveillance, deception, environmental cost, human rights), and research-integrity/limitations disclosure.
- Answering "no" to a checklist item is not by itself grounds for rejection — the point is transparency, not a perfect scorecard: *"answering 'no' to some questions is typically not grounds for rejection."*
- The checklist does not count toward the 9-page limit.

## Desk-rejection triggers

- Main text over 9 pages, or violating NeurIPS style (reduced margins, smaller fonts, etc.) — the template itself is the enforcement mechanism (LaTeX won't easily let you cheat it, but manual overrides are explicitly against the rules).
- Author identity revealed anywhere (anonymization breach).
- Dual submission policy violation (see above), at any point during reviewing or program building.
- Author profile "not appropriately updated" — an incomplete/incorrect author record risks desk rejection.
- Grossly negligent reviewing by an author-reviewer, as a last-resort sanction at the meta-review stage.
- LLMs/agents credited as authors.

## Template

`templates/neurips2026/` — fetched directly from `https://media.neurips.cc/Conferences/NeurIPS2026/Formatting_Instructions_For_NeurIPS_2026.zip` on 2026-09-03. Contains `neurips_2026.tex`, `neurips_2026.sty`, and `checklist.tex` (the mandatory reproducibility/ethics checklist form — include it in the submission, it's not just documentation). The handbook is explicit that this is the only accepted format: *"You must format your submission using the LaTeX style file for that year... This is the only template we will accept (note: Microsoft Word template has been discontinued)."* Copy the whole directory when starting a new paper; never edit the `.sty` file directly.
