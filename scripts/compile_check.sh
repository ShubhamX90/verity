#!/usr/bin/env bash
# compile_check.sh — compile a LaTeX document and translate errors to plain
# English. Tier A: it runs the compiler and reports what happened, but it
# never rewrites the .tex file itself — the no-bulk-regex rule applies even
# here. Where the source material this was adapted from (latex-document-
# skill's compile_latex.sh) sed-injected fixes in place (missing float
# placement specifiers, a missing \usepackage{microtype} on overfull-hbox
# warnings), this version instead reports the exact fix and location; the
# assistant applies it via a normal Edit call, one location at a time.
#
# Usage: compile_check.sh <file.tex> [--engine pdflatex|xelatex|lualatex] [--verbose]
#
# Requires a working TeX Live installation (pdflatex/xelatex/lualatex,
# bibtex/biber as needed) on PATH. This script does not install one.

set -uo pipefail

FILE=""
ENGINE=""
VERBOSE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --engine) ENGINE="$2"; shift 2 ;;
    --verbose) VERBOSE=1; shift ;;
    --help|-h) grep -E '^# ' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) FILE="$1"; shift ;;
  esac
done

if [[ -z "$FILE" ]]; then
  echo "error: no .tex file given. Run with --help for usage." >&2
  exit 2
fi
if [[ ! -f "$FILE" ]]; then
  echo "error: file not found: $FILE" >&2
  exit 2
fi

BASENAME="$(basename "${FILE%.tex}")"
DIR="$(dirname "$FILE")"
LOG="$DIR/$BASENAME.log"

detect_engine() {
  local content
  content="$(grep -v '^\s*%' "$FILE" 2>/dev/null || true)"
  if echo "$content" | grep -qE '\\usepackage(\[[^]]*\])?\{(fontspec|xeCJK|polyglossia)\}'; then
    echo "xelatex"
  elif echo "$content" | grep -qE '\\usepackage(\[[^]]*\])?\{(luacode|luatextra)\}|\\directlua'; then
    echo "lualatex"
  else
    echo "pdflatex"
  fi
}

if [[ -z "$ENGINE" ]]; then
  ENGINE="$(detect_engine)"
fi

if ! command -v "$ENGINE" &>/dev/null; then
  echo "error: '$ENGINE' not found on PATH. Install a TeX Live distribution first" \
       "(e.g. 'brew install --cask mactex-no-gui' on macOS, 'apt install texlive-full' on Debian/Ubuntu)." >&2
  exit 3
fi

BIB_TOOL=""
if grep -q '\\bibliography{' "$FILE" 2>/dev/null; then
  BIB_TOOL="bibtex"
elif grep -q '\\addbibresource{' "$FILE" 2>/dev/null; then
  BIB_TOOL="biber"
fi

run_engine() {
  if [[ "$VERBOSE" -eq 1 ]]; then
    (cd "$DIR" && "$ENGINE" -interaction=nonstopmode -halt-on-error "$(basename "$FILE")")
  else
    (cd "$DIR" && "$ENGINE" -interaction=nonstopmode -halt-on-error "$(basename "$FILE")") > /dev/null 2>&1
  fi
}

echo "engine: $ENGINE"
[[ -n "$BIB_TOOL" ]] && echo "bibliography tool: $BIB_TOOL"

PASS=1
echo "-- pass $PASS ($ENGINE) --"
if ! run_engine; then
  echo "pass $PASS failed — first-pass failure is treated as fatal (later passes need a working base)."
fi

if [[ -n "$BIB_TOOL" ]]; then
  echo "-- $BIB_TOOL --"
  if [[ "$BIB_TOOL" == "bibtex" ]]; then
    (cd "$DIR" && bibtex "$BASENAME") || echo "$BIB_TOOL reported issues (see above)"
  else
    (cd "$DIR" && biber "$BASENAME") || echo "$BIB_TOOL reported issues (see above)"
  fi
  PASS=2
  echo "-- pass $PASS ($ENGINE) --"
  run_engine || true
fi

PASS=$((PASS + 1))
echo "-- pass $PASS ($ENGINE, final) --"
run_engine || true

if [[ ! -f "$LOG" ]]; then
  echo "error: no .log file produced — compilation did not run at all" >&2
  exit 1
fi

LOGTEXT="$(cat "$LOG")"

echo ""
echo "== error/warning summary (translated) =="
FOUND_ISSUE=0

if echo "$LOGTEXT" | grep -q "File .*\.sty' not found"; then
  FOUND_ISSUE=1
  echo "$LOGTEXT" | grep -oE "File \`[^']+\.sty' not found" | sort -u | while read -r line; do
    pkg="$(echo "$line" | sed -E "s/File \`([a-zA-Z0-9_-]+)\.sty.*/\1/")"
    echo "  MISSING PACKAGE: $pkg — try: tlmgr install $pkg"
  done
fi

if echo "$LOGTEXT" | grep -q "Missing \$ inserted"; then
  FOUND_ISSUE=1
  echo "  MATH MODE: a math symbol appears outside \$...\$ delimiters somewhere — check the line numbers the log reports above 'Missing \$ inserted'."
fi

if echo "$LOGTEXT" | grep -q "Undefined control sequence"; then
  FOUND_ISSUE=1
  echo "  UNDEFINED COMMAND: check spelling, or whether the defining \\usepackage is missing. Line numbers:"
  grep -n "Undefined control sequence" "$LOG" | sed 's/^/    /'
fi

if echo "$LOGTEXT" | grep -qE "Environment .* undefined"; then
  FOUND_ISSUE=1
  echo "  UNDEFINED ENVIRONMENT: check spelling, or whether the defining \\usepackage is missing."
fi

UNDEF_CITES="$(echo "$LOGTEXT" | grep -oE "Citation \`[^']+' .*undefined" | sed -E "s/Citation \`([^']+)'.*/\1/" | sort -u)"
if [[ -n "$UNDEF_CITES" ]]; then
  FOUND_ISSUE=1
  echo "  UNDEFINED CITATIONS (run check_citations.py for the full picture):"
  echo "$UNDEF_CITES" | sed 's/^/    /'
fi

OVERFULL_COUNT="$(echo "$LOGTEXT" | grep -c "Overfull \\\\hbox" || true)"
if [[ "$OVERFULL_COUNT" -gt 0 ]]; then
  FOUND_ISSUE=1
  echo "  OVERFULL HBOX: $OVERFULL_COUNT warning(s) — if this is new, consider adding \\usepackage{microtype} " \
       "to the preamble (apply via a normal Edit at the specific line after the last \\usepackage, not a script)."
fi

if [[ "$FOUND_ISSUE" -eq 0 ]]; then
  echo "  none found in the log"
fi

echo ""
if grep -q "^Output written on" "$LOG"; then
  PDF="$(grep "^Output written on" "$LOG" | head -1)"
  echo "COMPILED: $PDF"
  exit 0
else
  echo "FAILED — no PDF was produced. See the summary above and the full log at $LOG."
  exit 1
fi
