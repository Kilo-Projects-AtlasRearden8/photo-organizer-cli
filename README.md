# Photo Organizer CLI

A local-first Python CLI to organize photos by date and event, detect
near-duplicate filenames, and suggest consistent renames. No cloud uploads,
no network access, no secrets. Everything runs on your machine.

Built by **Asdale Dynamics, LLC** — beginner-friendly AI education, books,
and practical tools. Plain English, step by step, never condescending.

## Features

- **Organize by date and event** — parses dates from filenames
  (`2023-08-15`, `20230815`, `08-15-2023`, etc.) and suggests consistent
  rename targets like `2023-08-15 beach vacation.jpg`.
- **Detect near-duplicate filenames** — flags files with highly similar
  names (e.g. `vacation_2023.jpg` vs `vacation_2024.jpg`) so you can review
  and rename them.
- **Batch mode** — point it at files or directories; it processes them all.
- **Dry-run option** (`--dry-run`) — preview every rename before anything
  changes on disk.
- **Zero dependencies** — pure Python standard library only.
- **Local-first** — your photos never leave your computer.

## Installation

```bash
git clone <this-repo>
cd photo-organizer-cli
pip install -e .
```

Or run directly without installing:

```bash
python -m photo_organizer.cli <paths...>
```

## Usage

Organize photos in the current directory (dry-run first):

```bash
photo-organizer --dry-run
```

Apply the renames for real:

```bash
photo-organizer
```

Organize a specific folder recursively:

```bash
photo-organizer ~/Pictures/Vacation --recursive
```

Detect near-duplicate filenames:

```bash
photo-organizer --duplicates --threshold 0.85
```

Skip event text in rename targets (dates only):

```bash
photo-organizer --no-event
```

## Example

Given `IMG_20230815_123456.jpg`, the tool suggests:

```
2023-08-15.jpg
```

Given `2023-08-15 beach vacation.jpg`, it keeps the event:

```
2023-08-15 beach vacation.jpg
```

## Testing

```bash
pip install pytest
pytest
```

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See [LICENSE](LICENSE).

## About Asdale Dynamics, LLC

Asdale Dynamics, LLC (Indiana, formed October 2026) is founded by Dylan
Asdale, a registered nurse turned AI author. Through his book *The Massive
AI Manual* and hub site dylanasdale.github.io, he explains AI "like a friend
would": plain English, step by step, never condescending. The LLC publishes
beginner-friendly AI education, books and guides, and practical local-first
tools like this one.
