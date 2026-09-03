# Figures, tables, diagrams — subfolder mapping

**This mapping is a placeholder.** It was written without access to any specific paper repo and needs to be replaced with the actual subfolder names the first time this skill is pointed at a real one. Don't treat the left column below as fact — it's the generic folder categories described when this skill was scoped, not a verified repo layout.

| Generic category (as described when scoping this skill) | Actual path in the real repo | Mechanism | Tier |
|---|---|---|---|
| images / diagrams / charts / illustrations | *(fill in)* | `scripts/figure_check.py` | A (checking existing figures) |
| results / output files | *(fill in)* | source of truth for `scripts/traceability_check.py` and `scripts/reproducibility_audit.py` | A |
| tables / spreadsheets | *(fill in)* | `scripts/table_from_data.py` | A for format conversion of already-verified numbers; **B** if choosing *which* results to present |
| dataset & code | *(fill in)* | `scripts/reproducibility_audit.py` | A |

## Figures

`scripts/figure_check.py` is a **checker**, not a generator, for v1 — it validates files already in the figures folder against these hard rules (from `agent-research-skills`, confirmed sound in the Phase 1 audit):
- DPI ≥ 300, or vector format (PDF/EPS/SVG).
- Colorblind-safe palette — no red/green-only distinctions (roughly 8% of men have red-green color-vision deficiency).
- All text in the figure ≥ 8pt at print size.
- No in-plot title — the LaTeX caption serves that function.

Checking is Tier A. **Generating a new figure is a bigger lift** (the source material's approach is a 3-phase pipeline: query expansion → code-gen with an execution-retry loop → a VLM visual-refinement loop) — not built in this v1 pass. If you want figure generation (not just checking) added, that's a follow-up, not something silently included here. Regardless of whether generation is automated later, **what a figure shows is a content decision (Tier B)** — a newly generated figure needs your review before it goes into the paper, the same as any other new claim.

## Tables

`scripts/table_from_data.py` converts JSON/CSV results into booktabs-formatted LaTeX (bold-best-value, `$\pm$` for standard deviations, `table*` for wide two-column tables). Per the Phase 1 audit, the source script's `--significance` flag was dead code (parsed, never implemented) — dropped in this port rather than silently shipped as a no-op. If you want significance-star annotations, that's new work, not a restored feature.

Numbers going into a table must come from the `results/` (or equivalent) folder — never typed from memory or from a number mentioned earlier in conversation. This is the same discipline `traceability_check.py` enforces for numbers in prose; tables aren't exempt from it.

**If the paper uses `tabularray`/`longtblr` instead of plain `tabular`/`booktabs`** (added per an independent audit finding — this was flagged as worth keeping in Phase 1 and had been dropped): `longtblr`'s style keys are processed **sequentially**, so ordering matters — `hlines`/`vlines` (blanket line weights) must come *before* `hline{1,Z}`/`vline{1,Z}` (outer-border overrides), or the override gets silently clobbered by the blanket setting that follows it:
```latex
\begin{longtblr}[caption={...}, label={tab:xxx}]{
  colspec={...},
  hlines={0.25pt},         % must precede hline{1,Z} below
  vlines={0.25pt},         % must precede vline{1,Z} below
  hline{1,Z}={1.5pt},      % overrides outer borders
  vline{1,Z}={1.5pt},      % overrides outer borders
}
```
Converting an existing `longtable` to `longtblr`: `C{w}/L{w}/R{w}` → `Q[wd=w,c]`/`Q[wd=w,l]`/`Q[wd=w,r]`; `\caption{...\label{tab:x}}\\` → `[caption={...}, label={tab:x}]`; drop `\hline`/`\endfirsthead`/`\endhead`/`\endfoot`/`\endlastfoot`/`\continued` entirely (handled automatically by `longtblr`).

## Diagrams

Not built for v1 — `latex-document-skill`'s Mermaid/Graphviz/PlantUML wrapper scripts were identified as available source material but weren't prioritized for this build. If the paper's diagrams (as opposed to data figures) folder turns out to be load-bearing, port `mermaid_to_image.sh`/`graphviz_to_pdf.sh`/`plantuml_to_pdf.sh` following the same fix-before-port discipline as everything else.

## Backward traceability — the `\hypertarget`/`\hyperlink` convention

This is the tagging convention `scripts/traceability_check.py` verifies — documented here because, per an independent audit finding, it wasn't documented anywhere before, which meant the checker could report "CLEAN" on a paper where nobody had ever actually tagged a number. Read this before relying on that script's output.

**The convention:** every number in the paper that comes from a results file or code output gets wrapped where it's *produced* (in the code/log/results artifact) as:
```latex
\hypertarget{R1a}{91.3}
```
and referenced where it's *used* in the paper's prose as:
```latex
Our method achieves \hyperlink{R1a}{91.3}\% accuracy.
```
`R1a` is an arbitrary label you choose — the convention is just that the same label appears once as a `\hypertarget` (the source of truth) and at least once as a `\hyperlink` (a use of that number in the paper). With `hyperref` loaded, this makes the compiled PDF itself clickable — a reader (or a co-author, or you six months later) can click any number and jump to where it came from.

**Adopting it takes one deliberate step**, not automatic tagging: as you write a results section, wrap each number pulled from `results/` (or whatever the real repo's equivalent folder is called — see the placeholder table above) in a `\hypertarget`, and reference it via `\hyperlink` in the prose. `traceability_check.py --tex <files>` then verifies every `\hyperlink` resolves to a `\hypertarget`, every `\hypertarget` is actually used, and (with `--code-output <log>`) that the tagged value matches what the code/results artifact actually says.

**What "CLEAN" from that script means and doesn't mean:** if you haven't adopted this convention at all, the script will report `0 hypertarget(s), 0 hyperlink(s)` and then `CLEAN` — because there's nothing inconsistent about zero of anything. That is not the same claim as "every number in this paper traces to an artifact." Before trusting a `CLEAN` result as meaning what Non-negotiable rule #5 in `SKILL.md` wants it to mean, check the target/link counts aren't both zero — a real, tagged paper should show a nonzero count in both. (The script's own output states these counts up front for exactly this reason — read them, not just the final `CLEAN`/failure-count line.)

## Reproducibility

See `reproducibility.md` — reads from the dataset/code folder(s), whatever they turn out to be called.

---

**Action item for whoever runs the Phase 4 dry run or the first real-repo session**: replace the "*(fill in)*" column above with actual paths, and delete this note once it's done.
