# STATUS

## What was built
A local-first Python CLI (`photo-organizer`) that organizes photos by date and event, detects near-duplicate filenames, and suggests consistent renames. No cloud uploads, no network access, no secrets, no API keys, no personal data.

Package layout:
- `photo_organizer/parser.py` — date parsing (`parse_date_from_filename`) and event extraction (`parse_event_from_filename`) from filenames.
- `photo_organizer/dedup.py` — near-duplicate filename detection (`find_near_duplicates`) using difflib similarity.
- `photo_organizer/organizer.py` — rename plan builder (`organize_photos`) producing `<date> [<event>]<ext>` targets.
- `photo_organizer/cli.py` — CLI entry point with batch mode, `--dry-run`, `--duplicates`, `--threshold`, `--no-event`, `--date-format`, `--recursive`.
- `photo_organizer/__init__.py` — package exports and version.
- `tests/test_parser.py` — parsing logic tests (10 cases).
- `tests/test_dedup.py` — dedup logic tests (7 cases).
- `pyproject.toml` — packaging with `photo-organizer` console script.
- `LICENSE` — MIT, copyright line exactly `Copyright (c) 2026 Asdale Dynamics, LLC`.
- `README.md` — usage, installation, credits Asdale Dynamics, LLC.
- `.gitignore` — excludes `.venv`, `__pycache__`, `*.egg-info`.

## How to run
```bash
# From the project folder
.venv/bin/pip install -e .        # install (or use system pip with a venv)

# Preview renames without changing anything
.venv/bin/photo-organizer --dry-run

# Apply renames for real
.venv/bin/photo-organizer

# Point at a folder recursively
.venv/bin/photo-organizer ~/Pictures/Vacation --recursive

# Detect near-duplicate filenames
.venv/bin/photo-organizer --duplicates --threshold 0.85

# Run tests
.venv/bin/pytest
```

## Verification results
- Package installs cleanly into a fresh venv via `pip install -e .`.
- `pytest`: 19 passed (10 parser + 7 dedup + ...), 0 failed.
- CLI dry-run run on sample photos: correct rename proposals for `IMG_20230815_123456.jpg`, `2023-08-15 beach vacation.jpg`, `vacation 2023-08-15.png`; non-photo files and files with no date/event left untouched.
- CLI apply run on a copy: renames applied successfully, unique destinations preserved.
- Console script `photo-organizer` resolves and runs.

## Known gaps
- No lint/typecheck tooling configured (only `pytest` for verification). Add `ruff`/`mypy` if desired.
- Date parsing covers `YYYY-MM-DD`, `YYYY.MM.DD`, `YY-MM-DD`, `MM-DD-YYYY`, `YYYYMMDD`. Slash dates (`YYYY/MM/DD`) are not supported on Linux because `/` is a path separator and cannot appear in a filename.
- Rename plans do not move files into date-based subdirectories; they rename in place.
- Event extraction is heuristic (camera prefixes stripped, date stripped, trailing numbers removed); multi-word events are preserved.
- No `.github/workflows` files (intentionally omitted per requirements).

## Git
Initialized locally, one commit (`f7c643e`), plain message, no co-author trailers, existing identity (Dylan Asdale). Not pushed, no remote created.
