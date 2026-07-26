"""
Validation utilities for Astro-MCP.
"""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from astro_mcp.utils.coordinates import (
    validate_latitude,
    validate_longitude,
)


def validate_date(
    year: int,
    month: int,
    day: int,
) -> None:
    """
    Validate a calendar date.
    """
    datetime(year, month, day)


def validate_time(
    hour: int,
    minute: int,
    second: int = 0,
) -> None:
    """
    Validate a time.
    """
    if not 0 <= hour <= 23:
        raise ValueError("Hour must be between 0 and 23.")

    if not 0 <= minute <= 59:
        raise ValueError("Minute must be between 0 and 59.")

    if not 0 <= second <= 59:
        raise ValueError("Second must be between 0 and 59.")


def validate_timezone(tz: str) -> str:
    """
    Validate an IANA timezone.

    Example:
        America/Chicago
        UTC
        Europe/London
    """
    try:
        ZoneInfo(tz)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"Unknown timezone: {tz}") from exc

    return tz


def validate_birth_data(
    *,
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    latitude: float,
    longitude: float,
    timezone: str,
) -> None:
    """
    Validate a complete birth record.
    """
    validate_date(year, month, day)
    validate_time(hour, minute)

    validate_latitude(latitude)
    validate_longitude(longitude)

    validate_timezone(timezone)


def validate_house_system(system: str) -> str:
    """
    Validate a Swiss Ephemeris house system.
    """
    allowed = {
        "P",  # Placidus
        "K",  # Koch
        "O",  # Porphyry
        "R",  # Regiomontanus
        "C",  # Campanus
        "A",  # Equal
        "E",  # Equal (variant)
        "B",  # Alcabitius
        "T",  # Topocentric
        "W",  # Whole Sign
        "X",  # Meridian
        "M",  # Morinus
        "H",  # Horizontal
        "V",  # Vehlow
    }

    system = system.upper()

    if system not in allowed:
        raise ValueError(
            f"Unsupported house system '{system}'."
        )

    return system


def validate_zodiac(zodiac: str) -> str:
    """
    Validate zodiac type.
    """
    zodiac = zodiac.lower()

    allowed = {
        "tropical",
        "sidereal",
    }

    if zodiac not in allowed:
        raise ValueError(
            "Zodiac must be 'tropical' or 'sidereal'."
        )

    return zodiac


def validate_ayanamsa(name: str) -> str:
    """
    Validate sidereal ayanamsa.
    """
    allowed = {
        "lahiri",
        "fagan",
        "krishnamurti",
        "raman",
        "true_citra",
    }

    value = name.lower()

    if value not in allowed:
        raise ValueError(
            f"Unsupported ayanamsa '{name}'."
        )

    return value


def validate_planet_name(name: str) -> str:
    """
    Validate a supported planet/body name.
    """
    allowed = {
        "sun",
        "moon",
        "mercury",
        "venus",
        "mars",
        "jupiter",
        "saturn",
        "uranus",
        "neptune",
        "pluto",
        "mean_node",
        "true_node",
        "chiron",
    }

    value = name.lower()

    if value not in allowed:
        raise ValueError(
            f"Unsupported celestial body '{name}'."
        )

    return value


__all__ = [
    "validate_date",
    "validate_time",
    "validate_timezone",
    "validate_birth_data",
    "validate_house_system",
    "validate_zodiac",
    "validate_ayanamsa",
    "validate_planet_name",
  ]
