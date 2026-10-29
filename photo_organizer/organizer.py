"""Photo organization: propose consistent rename targets by date and event.

Local-only processing. Does not move or rename files itself; it produces a
plan of suggested actions the CLI can apply (or preview in dry-run mode).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Optional

from photo_organizer.parser import parse_date_from_filename, parse_event_from_filename


@dataclass(frozen=True)
class RenamePlan:
    """A single suggested rename for one photo."""

    source: str
    destination: str
    date: Optional[str]  # ISO date string or None
    event: Optional[str]


def _unique_destination(directory: str, destination: str) -> str:
    """Ensure *destination* is unique within *directory* by appending a counter."""
    if not os.path.exists(os.path.join(directory, destination)):
        return destination
    stem, ext = os.path.splitext(destination)
    counter = 1
    while True:
        candidate = f"{stem} ({counter}){ext}"
        if not os.path.exists(os.path.join(directory, candidate)):
            return candidate
        counter += 1


def organize_photos(
    paths: List[str],
    date_format: str = "%Y-%m-%d",
    include_event: bool = True,
) -> List[RenamePlan]:
    """Build a rename plan for *paths*.

    Each destination is constructed as::

        <YYYY-MM-DD> [<event>]<ext>

    when a date and event are found, falling back gracefully when either is
    missing. Files already matching the pattern are left unchanged.
    """
    plans: List[RenamePlan] = []

    for path in paths:
        if not os.path.isfile(path):
            continue

        directory = os.path.dirname(path) or "."
        base = os.path.basename(path)
        _, ext = os.path.splitext(base)

        parsed_date = parse_date_from_filename(base)
        event = parse_event_from_filename(base) if include_event else None

        date_str = parsed_date.isoformat() if parsed_date else None

        parts: List[str] = []
        if date_str:
            parts.append(date_str)
        if event:
            parts.append(event)

        if not parts:
            # Nothing to rename consistently; leave as-is.
            plans.append(RenamePlan(source=path, destination=base, date=date_str, event=event))
            continue

        destination = " ".join(parts) + ext
        destination = _unique_destination(directory, destination)

        plans.append(
            RenamePlan(
                source=path,
                destination=destination,
                date=date_str,
                event=event,
            )
        )

    return plans
