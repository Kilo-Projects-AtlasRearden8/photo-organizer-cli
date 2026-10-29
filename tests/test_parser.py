"""Tests for photo filename parsing logic."""

import pytest

from photo_organizer.parser import parse_date_from_filename, parse_event_from_filename


class TestParseDate:
    def test_yyyymmdd_compact(self):
        assert parse_date_from_filename("IMG_20230815_123456.jpg") == __import__(
            "datetime", fromlist=["date"]
        ).date(2023, 8, 15)

    def test_yyyy_mm_dd(self):
        assert parse_date_from_filename("2023-08-15 vacation.jpg").isoformat() == "2023-08-15"

    def test_yyyy_mm_dd_dot(self):
        assert parse_date_from_filename("2023.08.15 photo.png") is not None

    def test_yy_mm_dd(self):
        assert parse_date_from_filename("23-08-15 photo.jpg") is not None

    def test_mm_dd_yyyy(self):
        assert parse_date_from_filename("08-15-2023 photo.jpg") is not None

    def test_no_date_returns_none(self):
        assert parse_date_from_filename("DSC_1234.JPG") is None
        assert parse_date_from_filename("photo.jpg") is None
        assert parse_date_from_filename("") is None

    def test_invalid_date_ignored(self):
        # 2023-13-45 is not a real date; should not crash, return None.
        assert parse_date_from_filename("2023-13-45 photo.jpg") is None


class TestParseEvent:
    def test_event_extracted_after_date(self):
        assert parse_event_from_filename("2023-08-15 beach vacation.jpg") == "beach vacation"

    def test_event_extracted_before_date(self):
        assert parse_event_from_filename("beach vacation 2023-08-15.jpg") == "beach vacation"

    def test_camera_prefix_stripped(self):
        assert parse_event_from_filename("IMG_20230815_wedding.jpg") == "wedding"

    def test_no_event_returns_none(self):
        assert parse_event_from_filename("IMG_20230815_123456.jpg") is None
        assert parse_event_from_filename("DSC_1234.JPG") is None
        assert parse_event_from_filename("") is None

    def test_underscores_and_dashes_normalized(self):
        assert parse_event_from_filename("2023-08-15-holiday_party.jpg") == "holiday party"
