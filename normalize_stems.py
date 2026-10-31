#!/usr/bin/env python3
"""
normalize_stems.py
Normalizes Logic Pro stem filenames and prefixes them with a track number
for use as song tracks in Helix Stadium.

Expected pattern: <Song Title> (<Instrument>)_1.wav
Output pattern:   01_Drums.wav, 02_Bass.wav, etc.

Usage:
    python3 normalize_stems.py <stems_dir>
    python3 normalize_stems.py <stems_dir> --dry-run
    python3 normalize_stems.py <stems_dir> --copy <dest_dir>
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

# ── Adjust track order here ───────────────────────────────────────────────────
TRACK_ORDER = [
    "Drums",
    "Bass",
    "Piano",
    "Guitar",
    "Other",
    "Vocals",
]
# ─────────────────────────────────────────────────────────────────────────────

AUDIO_EXTENSIONS = {".wav", ".aif", ".aiff", ".flac", ".ogg"}


def parse_stem_name(filename: str) -> str | None:
    """
    Extracts the instrument name from a Logic Pro stem filename.
    Expected pattern: <Song Title> (<Instrument>)_1.wav
    Returns the instrument name, or None if the pattern does not match.
    """
    stem = Path(filename).stem  # without extension
    match = re.search(r"\(([^)]+)\)(?:_\d+)?$", stem)
    if match:
        return match.group(1).strip()
    return None


def track_number(instrument: str) -> int | None:
    """Returns the 1-based track number for an instrument name (case-insensitive)."""
    for i, name in enumerate(TRACK_ORDER, start=1):
        if name.lower() == instrument.lower():
            return i
    return None


def build_new_name(instrument: str, number: int, extension: str) -> str:
    # Normalize instrument name to canonical spelling in TRACK_ORDER
    canonical = next(n for n in TRACK_ORDER if n.lower() == instrument.lower())
    return f"{number:02d}_{canonical}{extension}"


def process(source_dir: Path, dest_dir: Path | None, dry_run: bool) -> None:
    files = sorted(
        f for f in source_dir.iterdir()
        if f.is_file() and f.suffix.lower() in AUDIO_EXTENSIONS
    )

    if not files:
        print(f"No audio files found in: {source_dir}")
        sys.exit(1)

    renames: list[tuple[Path, str]] = []
    warnings: list[str] = []

    for f in files:
        instrument = parse_stem_name(f.name)
        if instrument is None:
            warnings.append(f"  ⚠️  Pattern not recognized, skipping: {f.name}")
            continue

        number = track_number(instrument)
        if number is None:
            warnings.append(
                f"  ⚠️  Instrument '{instrument}' not in TRACK_ORDER, skipping: {f.name}"
            )
            continue

        new_name = build_new_name(instrument, number, f.suffix.lower())
        renames.append((f, new_name))

    if warnings:
        print("Warnings:")
        for w in warnings:
            print(w)
        print()

    if not renames:
        print("Nothing to do.")
        return

    action = "Copy" if dest_dir else "Rename"
    print(f"{'[DRY-RUN] ' if dry_run else ''}{action} {len(renames)} file(s):\n")

    target_dir = dest_dir or source_dir

    for src, new_name in sorted(renames, key=lambda x: x[1]):
        dest = target_dir / new_name
        print(f"  {src.name}")
        print(f"    → {new_name}")

        if not dry_run:
            if dest.exists():
                print(f"    ⚠️  Already exists, skipping: {dest}")
                continue
            if dest_dir:
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
            else:
                src.rename(dest)

    if dry_run:
        print("\n(Dry-run: no files modified. Remove --dry-run to apply changes.)")
    else:
        print(f"\n✓ Done. Files are located in: {target_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Normalizes Logic Pro stem filenames for Helix Stadium."
    )
    parser.add_argument("source", type=Path, help="Directory containing exported stems")
    parser.add_argument(
        "--copy", metavar="DEST", type=Path, default=None,
        help="Copy to DEST instead of renaming in place"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview changes without modifying files"
    )
    args = parser.parse_args()

    if not args.source.is_dir():
        print(f"Error: directory not found: {args.source}")
        sys.exit(1)

    process(args.source, args.copy, args.dry_run)


if __name__ == "__main__":
    main()
