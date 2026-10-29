"""Date parsing logic for photo filenames.

Local-first, no cloud dependencies. Parses common date patterns found in
photo filenames such as IMG_20230815_123456.jpg, 2023-08-15 vacation.jpg,
vacation 2023-08-15.jpg, DSC_1234.JPG (no date), etc.
"""

from __future__ import annotations

import os
import re
from datetime import date, datetime
from typing import Optional

# Common date patterns:
#   20230815        YYYYMMDD
#   2023-08-15      YYYY-MM-DD
#   2023.08.15      YYYY.MM.DD
#   23-08-15        YY-MM-DD
#   08-15-2023      MM-DD-YYYY
_DATE_PATTERNS = [
    (re.compile(r"(?P<y>\d{4})[-.](?P<m>\d{2})[-.](?P<d>\d{2})"), "y,m,d"),
    (re.compile(r"(?P<y>\d{2})[-.](?P<m>\d{2})[-.](?P<d>\d{2})"), "y,m,d"),
    (re.compile(r"(?P<m>\d{2})[-.](?P<d>\d{2})[-.](?P<y>\d{4})"), "m,d,y"),
    (re.compile(r"(?P<y>\d{4})(?P<m>\d{2})(?P<d>\d{2})"), "y,m,d"),
]


def parse_date_from_filename(filename: str) -> Optional[date]:
    """Return a :class:`datetime.date` parsed from *filename*, or ``None``.

    Only the basename is inspected; directory separators are ignored. The
    first matching date pattern wins. Two-digit years are interpreted
    relative to the current year via :meth:`datetime.strptime` semantics
    (00-69 -> 2000-2069, 70-99 -> 1970-1999).
    """
    if not filename:
        return None

    base = os.path.basename(filename)

    for pattern, order in _DATE_PATTERNS:
        match = pattern.search(base)
        if not match:
            continue
        try:
            y = int(match.group("y"))
            m = int(match.group("m"))
            d = int(match.group("d"))
            # Normalize two-digit years.
            if y < 100:
                y += 2000 if y <= 69 else 1900
            return date(y, m, d)
        except (ValueError, TypeError):
            continue
    return None


def parse_event_from_filename(filename: str) -> Optional[str]:
    """Return a cleaned "event" token extracted from *filename*, or ``None``.

    The event is the human-readable portion of a filename after stripping
    the date pattern, camera prefixes (IMG_, DSC_, etc.), extensions, and
    surrounding punctuation/whitespace. Returns ``None`` when no usable
    event text remains.
    """
    if not filename:
        return None

    base = filename.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]

    # Drop extension.
    name = base.rsplit(".", 1)[0] if "." in base else base

    # Strip known camera/device prefixes.
    name = re.sub(r"^(IMG|DSC|PXL|IMG_|DSC_|PXL_)", "", name, flags=re.IGNORECASE)

    # Strip date patterns so the leftover text is the event.
    for pattern, _order in _DATE_PATTERNS:
        name = pattern.sub(" ", name)
    name = name.replace("_", " ").replace("-", " ")
    name = re.sub(r"\s+", " ", name).strip(" ._-")

    # Remove trailing numeric-only leftovers (e.g. sequence numbers).
    tokens = name.split()
    while tokens and tokens[-1].isdigit():
        tokens.pop()

    event = " ".join(tokens).strip()
    return event or None
