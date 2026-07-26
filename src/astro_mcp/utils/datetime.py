"""
Date and time utilities for Astro-MCP.

Provides:

- Timezone-aware datetime creation
- UTC normalization
- ISO-8601 parsing
- Julian Day conversion
- Julian Day -> datetime conversion
"""

from __future__ import annotations

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import swisseph as swe


def make_datetime(
    year: int,
    month: int,
    day: int,
    hour: int = 0,
    minute: int = 0,
    second: int = 0,
    tz: str = "UTC",
) -> datetime:
    """
    Create a timezone-aware datetime.
    """
    return datetime(
        year,
        month,
        day,
        hour,
        minute,
        second,
        tzinfo=ZoneInfo(tz),
    )


def to_utc(dt: datetime) -> datetime:
    """
    Convert any timezone-aware datetime to UTC.
    """
    if dt.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware.")

    return dt.astimezone(timezone.utc)


def parse_iso(value: str) -> datetime:
    """
    Parse an ISO-8601 timestamp.

    Example:
        2025-03-19T12:33:00-05:00
    """
    dt = datetime.fromisoformat(value)

    if dt.tzinfo is None:
        raise ValueError("ISO datetime must include timezone.")

    return dt


def julian_day(dt: datetime) -> float:
    """
    Convert datetime -> Julian Day (UT).
    """
    utc = to_utc(dt)

    decimal_hours = (
        utc.hour
        + utc.minute / 60
        + utc.second / 3600
        + utc.microsecond / 3_600_000_000
    )

    jd = swe.julday(
        utc.year,
        utc.month,
        utc.day,
        decimal_hours,
    )

    return jd


def datetime_from_jd(jd: float) -> datetime:
    """
    Convert Julian Day -> UTC datetime.
    """
    year, month, day, hour = swe.revjul(jd)

    hours = int(hour)
    minutes = int((hour - hours) * 60)
    seconds = round((((hour - hours) * 60) - minutes) * 60)

    return datetime(
        year,
        month,
        day,
        hours,
        minutes,
        seconds,
        tzinfo=timezone.utc,
    )


def now_utc() -> datetime:
    """
    Current UTC time.
    """
    return datetime.now(timezone.utc)


def utc_iso() -> str:
    """
    Current UTC ISO-8601 string.
    """
    return now_utc().isoformat()


__all__ = [
    "make_datetime",
    "to_utc",
    "parse_iso",
    "julian_day",
    "datetime_from_jd",
    "now_utc",
    "utc_iso",
]
