"""Photo organizer package: local-only CLI to organize photos by date and event,
detect near-duplicate filenames, and suggest consistent renames."""

from photo_organizer.parser import parse_date_from_filename, parse_event_from_filename
from photo_organizer.dedup import find_near_duplicates
from photo_organizer.organizer import organize_photos
from photo_organizer.cli import main

__all__ = [
    "parse_date_from_filename",
    "parse_event_from_filename",
    "find_near_duplicates",
    "organize_photos",
    "main",
]

__version__ = "1.0.0"
