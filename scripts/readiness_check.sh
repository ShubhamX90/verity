#!/usr/bin/env bash
# readiness_check.sh — composite pre-submission readiness check. Tier A,
# entirely read-only: assembles four checks that no single source shipped
# as one tool (packages, citations, lint, structure) plus an anonymization
# scan. See references/pre-submission-checklist.md for what each section
# means and what it deliberately does not check (submission-portal account
# requirements, reciprocal reviewing registration — account/logistics
# matters outside a repo-scoped tool's reach).
#
# Usage: readiness_check.sh <main.tex> [--bib refs.bib] [--page-limit N]
#
# --page-limit has no default — this tool is venue-agnostic, so there is
# no single "the" page limit to assume. Pass the number from the active
# venue profile (see references/venue-profile.md). Without it, the
# Structure check still reports the estimated page count, just without
# comparing it against any limit.
#
# Individual sub-tools (kpsewhich, chktex) degrade gracefully if not
# installed — reported as skipped, not fatal, since the rest of the
# checklist is still useful without them. detex is used for word-count
# estimation if present; a cruder built-in fallback is used if it's not,
# silently, since that check can't meaningfully be "skipped."

set -uo pipefail

FILE=""
BIB=""
PAGE_LIMIT=""
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --bib)
      if [[ $# -lt 2 ]]; then echo "error: --bib requires a value" >&2; exit 2; fi
      BIB="$2"; shift 2 ;;
    --page-limit)
      if [[ $# -lt 2 ]]; then echo "error: --page-limit requires a value" >&2; exit 2; fi
      PAGE_LIMIT="$2"; shift 2 ;;
    --help|-h) grep -E '^# ' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) FILE="$1"; shift ;;
  esac
done

if [[ -z "$FILE" || ! -f "$FILE" ]]; then
  echo "error: main .tex file not found: ${FILE:-<none given>}" >&2
  exit 2
fi

if [[ -n "$PAGE_LIMIT" ]] && ! [[ "$PAGE_LIMIT" =~ ^[0-9]+$ ]]; then
  echo "error: --page-limit must be a positive integer, got: '$PAGE_LIMIT'" >&2
  exit 2
fi

PASS=1
FAIL=0
SKIP=0
declare -a RESULTS

report() {
  # report <status: PASS|FAIL|SKIP> <label> <detail>
  RESULTS+=("$1|$2|$3")
  case "$1" in
    PASS) ;;
    FAIL) FAIL=$((FAIL + 1)) ;;
    SKIP) SKIP=$((SKIP + 1)) ;;
  esac
}

# ---- 1. Packages ---------------------------------------------------------
if command -v kpsewhich &>/dev/null; then
  MISSING_PKGS=()
  DOCCLASS="$(grep -oE '\\documentclass(\[[^]]*\])?\{[^}]+\}' "$FILE" | head -1 | grep -oE '\{[^}]+\}' | tr -d '{}')"
  if [[ -n "$DOCCLASS" ]] && ! kpsewhich "${DOCCLASS}.cls" &>/dev/null; then
    MISSING_PKGS+=("$DOCCLASS (class)")
  fi
  while IFS= read -r pkg; do
    [[ -z "$pkg" ]] && continue
    if ! kpsewhich "${pkg}.sty" &>/dev/null; then
      MISSING_PKGS+=("$pkg")
    fi
  done < <(grep -oE '\\usepackage(\[[^]]*\])?\{[^}]+\}' "$FILE" | grep -oE '\{[^}]+\}' | tr -d '{}' | tr ',' '\n')
  if [[ ${#MISSING_PKGS[@]} -eq 0 ]]; then
    report PASS "Packages" "all resolve via kpsewhich"
  else
    report FAIL "Packages" "missing: ${MISSING_PKGS[*]} — try: tlmgr install <name>"
  fi
else
  report SKIP "Packages" "kpsewhich not on PATH — install a TeX Live distribution to enable this check"
fi

# ---- 2. Citations ---------------------------------------------------------
if [[ -n "$BIB" ]]; then
  if [[ -f "$BIB" && -f "$SCRIPT_DIR/check_citations.py" ]]; then
    CITE_OUT="$(python3 "$SCRIPT_DIR/check_citations.py" --tex "$FILE" --bib "$BIB" 2>&1)"
    CITE_EXIT=$?
    if [[ "$CITE_EXIT" -eq 0 ]]; then
      report PASS "Citations" "no broken/duplicate citations (see full output below for soft notes)"
    else
      report FAIL "Citations" "issues found — see full output below"
    fi
  else
    report SKIP "Citations" "check_citations.py not found or --bib file missing"
  fi
else
  report SKIP "Citations" "no --bib given"
fi

# ---- 3. Lint (chktex) -----------------------------------------------------
if command -v chktex &>/dev/null; then
  LINT_OUT="$(chktex -q -v0 "$FILE" 2>&1)"
  WARN_COUNT="$(echo "$LINT_OUT" | grep -cE '^Warning [0-9]+ in ' || true)"
  ERR_COUNT="$(echo "$LINT_OUT" | grep -cE '^Error [0-9]+ in ' || true)"
  if [[ "$ERR_COUNT" -gt 0 ]]; then
    report FAIL "Lint (chktex)" "$ERR_COUNT error(s), $WARN_COUNT warning(s)"
  elif [[ "$WARN_COUNT" -gt 0 ]]; then
    report PASS "Lint (chktex)" "$WARN_COUNT warning(s), no errors"
  else
    report PASS "Lint (chktex)" "clean"
  fi
else
  report SKIP "Lint (chktex)" "chktex not on PATH"
fi

# ---- 4. Structure ----------------------------------------------------------
if command -v detex &>/dev/null; then
  WORDS="$(detex "$FILE" 2>/dev/null | wc -w | tr -d ' ')"
else
  # Fallback word count: strip comments and common LaTeX commands crudely.
  WORDS="$(grep -v '^\s*%' "$FILE" | sed -E 's/\\[a-zA-Z]+(\[[^]]*\])?(\{[^}]*\})?//g' | wc -w | tr -d ' ')"
fi
EST_PAGES=$(( (WORDS + 249) / 250 ))
N_FIGURES="$(grep -c '\\begin{figure' "$FILE" || true)"
N_TABLES="$(grep -c '\\begin{table' "$FILE" || true)"
N_EQUATIONS="$(grep -cE '\\begin\{(equation|align\*?)\}' "$FILE" || true)"
N_TODO="$(grep -icE 'TODO|FIXME|\bXXX\b' "$FILE" || true)"

STRUCTURE_DETAIL="~${WORDS} words (~${EST_PAGES} est. pages), ${N_FIGURES} figure(s), ${N_TABLES} table(s), ${N_EQUATIONS} equation(s)"
if [[ "$N_TODO" -gt 0 ]]; then
  STRUCTURE_DETAIL="${STRUCTURE_DETAIL}, ${N_TODO} TODO/FIXME marker(s) remaining"
fi
if [[ -z "$PAGE_LIMIT" ]]; then
  report SKIP "Structure" "${STRUCTURE_DETAIL} — no --page-limit given, not compared against any limit (pass the number from the active venue profile to enable this comparison)"
elif [[ "$EST_PAGES" -gt "$PAGE_LIMIT" ]]; then
  report FAIL "Structure" "${STRUCTURE_DETAIL} — estimated page count exceeds the ${PAGE_LIMIT}-page limit (word-count estimate is rough; confirm with an actual compile)"
else
  report PASS "Structure" "$STRUCTURE_DETAIL"
fi

# ---- 5. Anonymization -------------------------------------------------------
ANON_HITS=()
AUTHOR_FIELD="$(grep -oE '\\author\{[^}]*\}' "$FILE" | head -1)"
if [[ -n "$AUTHOR_FIELD" ]] && ! echo "$AUTHOR_FIELD" | grep -qiE 'anonymous|anonymized'; then
  ANON_HITS+=("\\author{} does not say 'anonymous': $AUTHOR_FIELD")
fi
if grep -qiE 'our (previous|prior|earlier) work|we previously (proposed|showed|introduced)' "$FILE"; then
  ANON_HITS+=("first-person self-citation phrasing found — should be third person, e.g. 'Smith et al. showed...'")
fi
NON_ANON_URLS="$(grep -oE 'https?://(github|gitlab)\.com/[^/[:space:]}]+/[^/[:space:]}]+' "$FILE" | grep -viE 'anonymous' || true)"
if [[ -n "$NON_ANON_URLS" ]]; then
  ANON_HITS+=("non-anonymous GitHub/GitLab URL(s) found: $(echo "$NON_ANON_URLS" | tr '\n' ' ')")
fi
if grep -qiE '\\(section\*?\{|subsection\*?\{)(acknowledg[e]?ment)' "$FILE"; then
  ANON_HITS+=("an acknowledgments section is present — should not exist in the submission version")
fi
if [[ ${#ANON_HITS[@]} -eq 0 ]]; then
  report PASS "Anonymization" "no obvious identity leaks found (scanner only — not a guarantee; see pre-submission-checklist.md)"
else
  DETAIL="$(printf '%s; ' "${ANON_HITS[@]}")"
  report FAIL "Anonymization" "${DETAIL%; }"
fi

# ---- Report -----------------------------------------------------------------
echo "== Pre-submission readiness check: $FILE =="
echo ""
printf '%-9s %-20s %s\n' "STATUS" "CHECK" "DETAIL"
for r in "${RESULTS[@]}"; do
  IFS='|' read -r status label detail <<< "$r"
  MARK="?"
  case "$status" in PASS) MARK="✓";; FAIL) MARK="✗";; SKIP) MARK="–";; esac
  printf '%-9s %-20s %s\n' "$MARK $status" "$label" "$detail"
done

if [[ -n "${CITE_OUT:-}" && "$FAIL" -gt 0 ]]; then
  echo ""
  echo "-- citation check detail --"
  echo "$CITE_OUT"
fi

echo ""
echo "$FAIL failure(s), $SKIP check(s) skipped (missing tool or input)."
[[ "$FAIL" -gt 0 ]] && exit 1
exit 0
