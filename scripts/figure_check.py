#!/usr/bin/env python3
"""figure_check.py — check figure files already on disk against general
publication-quality hard rules (venue-agnostic — DPI/vector-format and
colorblind-safety norms apply the same way regardless of which conference
is active). Read-only, Tier A. A checker, not a generator: this script
does not create or edit any figure — see references/figures-tables-
diagrams.md for why figure generation itself wasn't built for v1.

Checks:
  - Raster images: DPI >= 300 (or the file is vector format, which is
    exempt from a DPI check entirely).
  - Vector formats (PDF/EPS/SVG) are always accepted on the resolution
    check — there's no meaningful "DPI" for a vector graphic.
  - File format is one of the common publication-safe types.

What this script does NOT check (needs a human or a rendering step, not
static file inspection): colorblind-safe palette, in-figure text size at
print scale, absence of an in-plot title. Those are listed in references/
figures-tables-diagrams.md as hard rules to apply when generating or
reviewing a figure — they're not mechanically checkable from the file
alone without decoding pixel data or parsing the source plotting code,
so this script reports them as reminders rather than pretending to
verify them.

Usage: figure_check.py <file_or_dir> [<file_or_dir> ...] [--min-dpi 300]
"""
from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path

VECTOR_EXTS = {".pdf", ".eps", ".svg"}
RASTER_EXTS = {".png", ".jpg", ".jpeg", ".tiff", ".tif"}
UNSAFE_EXTS = {".gif", ".bmp", ".webp"}


def png_dpi(path: Path) -> tuple[float | None, float | None]:
    """Return (dpi_x, dpi_y) from a PNG's pHYs chunk, or (None, None) if absent."""
    try:
        data = path.read_bytes()
    except OSError:
        return None, None
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None, None
    pos = 8
    while pos + 8 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        chunk_type = data[pos + 4:pos + 8]
        if chunk_type == b"pHYs" and pos + 8 + 9 <= len(data):
            chunk = data[pos + 8:pos + 8 + 9]
            ppu_x, ppu_y, unit = struct.unpack(">IIB", chunk)
            if unit == 1:  # meters
                # Round to the nearest integer DPI: pixels-per-meter is an
                # integer, so converting back to DPI (x2.54cm/in / 100)
                # loses sub-DPI precision (e.g. an exact 300 DPI image
                # round-trips to 299.9994) — round rather than truncate,
                # or a boundary-exact image false-fails the >= check.
                return round(ppu_x * 0.0254), round(ppu_y * 0.0254)
            return None, None  # unit 0 = unspecified aspect ratio only, no real DPI
        if chunk_type == b"IEND":
            break
        pos += 8 + length + 4  # length + type + data + CRC
    return None, None


def jpeg_dpi(path: Path) -> tuple[float | None, float | None]:
    """Return (dpi_x, dpi_y) from a JPEG's JFIF APP0 segment, or (None, None)."""
    try:
        data = path.read_bytes()
    except OSError:
        return None, None
    if data[:2] != b"\xff\xd8":
        return None, None
    pos = 2
    while pos + 4 <= len(data):
        if data[pos] != 0xFF:
            break
        marker = data[pos + 1]
        if marker in (0xD8, 0xD9):
            pos += 2
            continue
        seg_len = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        if marker == 0xE0 and data[pos + 4:pos + 9] == b"JFIF\x00":
            seg = data[pos + 4:pos + 4 + seg_len - 2]
            if len(seg) >= 12:
                units = seg[7]
                dpi_x, dpi_y = struct.unpack(">HH", seg[8:12])
                if units == 1:  # dots per inch
                    return float(dpi_x), float(dpi_y)
                if units == 2:  # dots per cm
                    return dpi_x * 2.54, dpi_y * 2.54
            return None, None
        pos += 2 + seg_len
    return None, None


def check_one(path: Path, min_dpi: int) -> list[str]:
    issues: list[str] = []
    ext = path.suffix.lower()

    if ext in UNSAFE_EXTS:
        issues.append(f"{path}: '{ext}' is not a recommended publication format (prefer PDF/PNG/SVG)")
        return issues

    if ext in VECTOR_EXTS:
        return issues  # vector formats pass the resolution check by definition

    if ext in RASTER_EXTS:
        # Check the file actually looks like the format its extension
        # claims before trying to read DPI from it — otherwise "not really
        # an image" and "real image, just missing DPI metadata" produce
        # the identical, and for the former case actively misleading,
        # "re-export with an explicit DPI setting" message.
        try:
            head = path.read_bytes()[:8]
        except OSError as e:
            issues.append(f"{path}: could not read file ({e})")
            return issues

        if ext == ".png" and head[:8] != b"\x89PNG\r\n\x1a\n":
            issues.append(f"{path}: has a .png extension but the file doesn't start with a PNG "
                           f"signature — this isn't a valid PNG file, not just missing DPI metadata")
            return issues
        if ext in (".jpg", ".jpeg") and head[:2] != b"\xff\xd8":
            issues.append(f"{path}: has a {ext} extension but the file doesn't start with a JPEG "
                           f"signature — this isn't a valid JPEG file, not just missing DPI metadata")
            return issues

        dpi_x = dpi_y = None
        if ext == ".png":
            dpi_x, dpi_y = png_dpi(path)
        elif ext in (".jpg", ".jpeg"):
            dpi_x, dpi_y = jpeg_dpi(path)

        if dpi_x is None:
            issues.append(
                f"{path}: valid {ext} file, but could not read a DPI value from it (no pHYs/JFIF "
                f"density chunk) — cannot confirm it meets the >= {min_dpi} DPI rule. Re-export "
                f"with an explicit DPI setting (e.g. matplotlib's savefig(..., dpi={min_dpi}))."
            )
        elif min(dpi_x, dpi_y) < min_dpi:
            issues.append(f"{path}: {min(dpi_x, dpi_y):.0f} DPI, below the {min_dpi} DPI minimum — "
                           f"prefer a vector format (PDF/EPS/SVG) or re-export at higher resolution")
        return issues

    issues.append(f"{path}: unrecognized image extension '{ext}' — not checked")
    return issues


def collect_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    exts = VECTOR_EXTS | RASTER_EXTS | UNSAFE_EXTS
    for p in paths:
        path = Path(p)
        if path.is_dir():
            files += sorted(f for f in path.rglob("*") if f.is_file() and f.suffix.lower() in exts)
        elif path.is_file():
            files.append(path)
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", help="figure file(s) or a directory to scan recursively")
    ap.add_argument("--min-dpi", type=int, default=300)
    args = ap.parse_args()

    files = collect_files(args.paths)
    if not files:
        print("error: no image files found in the given path(s)", file=sys.stderr)
        return 2

    all_issues: list[str] = []
    for f in files:
        all_issues += check_one(f, args.min_dpi)

    print(f"checked {len(files)} figure file(s)")
    if all_issues:
        print(f"\n== {len(all_issues)} issue(s) ==")
        for i in all_issues:
            print(f"  - {i}")
    else:
        print("no DPI/format issues found")

    print(
        "\nReminder — not mechanically checkable from the file alone, verify by eye or when "
        "generating: colorblind-safe palette (no red/green-only distinctions), all text >= 8pt "
        "at print size, no in-plot title (caption should carry it)."
    )
    return 1 if all_issues else 0


if __name__ == "__main__":
    sys.exit(main())
