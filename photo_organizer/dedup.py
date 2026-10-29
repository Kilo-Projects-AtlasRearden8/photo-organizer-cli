"""Near-duplicate filename detection.

Local-only, dependency-free duplicate detection using difflib sequence
matching on filename stems. Files whose stems are similar above a threshold
are reported as near-duplicates so a user can review and rename them.
"""

from __future__ import annotations

import difflib
import os
from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class NearDuplicate:
    """A pair of near-duplicate files with a similarity score."""

    path_a: str
    path_b: str
    similarity: float  # 0.0 .. 1.0


def _stem(path: str) -> str:
    """Return the filename without extension, lowercased for comparison."""
    base = os.path.basename(path)
    stem, _ = os.path.splitext(base)
    return stem.lower()


def find_near_duplicates(
    paths: List[str], threshold: float = 0.85
) -> List[NearDuplicate]:
    """Return pairs of *paths* whose filename stems are near-duplicates.

    Parameters
    ----------
    paths:
        List of file paths to compare.
    threshold:
        Minimum similarity ratio (0.0 to 1.0) to flag a pair.

    Returns
    -------
    list of NearDuplicate
        Each unordered pair appears once, sorted by descending similarity.
    """
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold must be between 0.0 and 1.0")

    stems = [(p, _stem(p)) for p in paths]
    duplicates: List[NearDuplicate] = []

    for i in range(len(stems)):
        for j in range(i + 1, len(stems)):
            path_a, stem_a = stems[i]
            path_b, stem_b = stems[j]
            if not stem_a or not stem_b:
                continue
            ratio = difflib.SequenceMatcher(None, stem_a, stem_b).ratio()
            if ratio >= threshold:
                duplicates.append(
                    NearDuplicate(path_a=path_a, path_b=path_b, similarity=ratio)
                )

    duplicates.sort(key=lambda nd: nd.similarity, reverse=True)
    return duplicates
