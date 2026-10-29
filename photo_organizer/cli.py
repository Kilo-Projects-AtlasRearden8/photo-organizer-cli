"""Command-line interface for the photo organizer.

Local-first: no cloud uploads, no network access. Supports batch mode and a
dry-run option that previews changes without touching the filesystem.
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import List, Optional

from photo_organizer.dedup import find_near_duplicates
from photo_organizer.organizer import organize_photos, RenamePlan


def _collect_files(paths: List[str], recursive: bool) -> List[str]:
    """Collect all photo-like files from *paths*."""
    extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".heic"}
    files: List[str] = []

    for path in paths:
        if os.path.isfile(path):
            files.append(os.path.abspath(path))
        elif os.path.isdir(path):
            if recursive:
                for root, _dirs, filenames in os.walk(path):
                    for name in filenames:
                        if os.path.splitext(name)[1].lower() in extensions:
                            files.append(os.path.abspath(os.path.join(root, name)))
            else:
                for name in os.listdir(path):
                    full = os.path.join(path, name)
                    if os.path.isfile(full) and os.path.splitext(name)[1].lower() in extensions:
                        files.append(os.path.abspath(full))
        else:
            print(f"warning: skipping nonexistent path: {path}", file=sys.stderr)

    # De-duplicate while preserving order.
    seen = set()
    unique: List[str] = []
    for f in files:
        if f not in seen:
            seen.add(f)
            unique.append(f)
    return unique


def _apply_plan(plans: List[RenamePlan], dry_run: bool) -> int:
    """Apply (or preview) a rename plan. Returns the number of changes."""
    changes = 0
    for plan in plans:
        destination = os.path.join(os.path.dirname(plan.source) or ".", plan.destination)
        if os.path.abspath(plan.source) == os.path.abspath(destination):
            continue
        changes += 1
        if dry_run:
            print(f"[dry-run] would rename: {plan.source} -> {destination}")
        else:
            os.rename(plan.source, destination)
            print(f"renamed: {plan.source} -> {destination}")
    return changes


def _report_duplicates(paths: List[str], threshold: float) -> int:
    """Print near-duplicate pairs. Returns the number of pairs found."""
    dupes = find_near_duplicates(paths, threshold=threshold)
    if not dupes:
        print("No near-duplicate filenames detected.")
        return 0
    print(f"Near-duplicate filename pairs (threshold >= {threshold:.2f}):")
    for dup in dupes:
        print(
            f"  {dup.similarity:.2f}  {dup.path_a}  <->  {dup.path_b}"
        )
    return len(dupes)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="photo-organizer",
        description="Organize photos by date and event, detect near-duplicate "
        "filenames, and suggest consistent renames. Local-only.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Files or directories to organize (default: current directory).",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Recursively scan directories for photos.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview renames without modifying any files.",
    )
    parser.add_argument(
        "--duplicates",
        action="store_true",
        help="Detect and report near-duplicate filenames.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.85,
        help="Similarity threshold for near-duplicate detection (0.0-1.0).",
    )
    parser.add_argument(
        "--no-event",
        action="store_true",
        help="Do not include event text in suggested rename targets.",
    )
    parser.add_argument(
        "--date-format",
        default="%Y-%m-%d",
        help="strftime format for the date portion of rename targets.",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    target_paths = args.paths if args.paths else [os.getcwd()]
    files = _collect_files(target_paths, recursive=args.recursive)

    if not files:
        print("No photo files found.")
        return 0

    if args.duplicates:
        _report_duplicates(files, threshold=args.threshold)

    plans = organize_photos(
        files,
        date_format=args.date_format,
        include_event=not args.no_event,
    )

    changes = _apply_plan(plans, dry_run=args.dry_run)

    if args.dry_run:
        print(f"\nDry-run complete: {changes} file(s) would be renamed.")
    else:
        print(f"\nComplete: {changes} file(s) renamed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
