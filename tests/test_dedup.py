"""Tests for near-duplicate detection."""

import pytest

from photo_organizer.dedup import find_near_duplicates, NearDuplicate


def test_exact_same_stem_flagged():
    paths = ["a/IMG_001.jpg", "b/IMG_001.png"]
    dupes = find_near_duplicates(paths, threshold=0.85)
    assert len(dupes) == 1
    assert dupes[0].similarity == 1.0


def test_similar_stems_flagged():
    paths = ["a/vacation_2023.jpg", "a/vacation_2024.jpg"]
    dupes = find_near_duplicates(paths, threshold=0.85)
    assert len(dupes) == 1


def test_different_stems_not_flagged():
    paths = ["a/beach.jpg", "b/mountain.png"]
    assert find_near_duplicates(paths, threshold=0.85) == []


def test_threshold_rejects_low_similarity():
    paths = ["a/vacation_2023.jpg", "a/vacation_2024.jpg"]
    dupes = find_near_duplicates(paths, threshold=0.99)
    assert dupes == []


def test_invalid_threshold_raises():
    with pytest.raises(ValueError):
        find_near_duplicates(["a.jpg", "b.jpg"], threshold=1.5)
    with pytest.raises(ValueError):
        find_near_duplicates(["a.jpg", "b.jpg"], threshold=-0.1)


def test_empty_input_returns_empty():
    assert find_near_duplicates([]) == []


def test_return_type():
    paths = ["a/IMG_001.jpg", "b/IMG_001.png"]
    dupes = find_near_duplicates(paths)
    assert isinstance(dupes[0], NearDuplicate)
