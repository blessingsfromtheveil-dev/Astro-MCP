"""
Coordinate utilities for Astro-MCP.

Provides:

- Latitude/longitude validation
- Coordinate normalization
- Decimal Degrees <-> DMS conversion
- Formatting helpers
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fmod


@dataclass(frozen=True)
class Coordinates:
    """
    Geographic coordinates in decimal degrees.
    """

    latitude: float
    longitude: float

    def validate(self) -> None:
        validate_latitude(self.latitude)
        validate_longitude(self.longitude)


def validate_latitude(latitude: float) -> float:
    """
    Validate latitude.

    Valid range:
        -90 <= latitude <= 90
    """
    if not -90.0 <= latitude <= 90.0:
        raise ValueError("Latitude must be between -90 and 90 degrees.")

    return latitude


def validate_longitude(longitude: float) -> float:
    """
    Validate longitude.

    Valid range:
        -180 <= longitude <= 180
    """
    if not -180.0 <= longitude <= 180.0:
        raise ValueError("Longitude must be between -180 and 180 degrees.")

    return longitude


def normalize_longitude(longitude: float) -> float:
    """
    Normalize longitude to [-180, 180).
    """
    longitude = fmod(longitude + 180.0, 360.0)

    if longitude < 0:
        longitude += 360.0

    return longitude - 180.0


def clamp_latitude(latitude: float) -> float:
    """
    Clamp latitude to the legal range.
    """
    return max(-90.0, min(90.0, latitude))


def decimal_to_dms(decimal: float) -> tuple[int, int, float]:
    """
    Convert decimal degrees to DMS.

    Returns:
        (degrees, minutes, seconds)
    """
    sign = -1 if decimal < 0 else 1

    decimal = abs(decimal)

    degrees = int(decimal)
    minutes_float = (decimal - degrees) * 60

    minutes = int(minutes_float)
    seconds = (minutes_float - minutes) * 60

    return (
        degrees * sign,
        minutes,
        seconds,
    )


def dms_to_decimal(
    degrees: int,
    minutes: int,
    seconds: float,
) -> float:
    """
    Convert DMS -> decimal degrees.
    """
    sign = -1 if degrees < 0 else 1

    value = (
        abs(degrees)
        + minutes / 60
        + seconds / 3600
    )

    return sign * value


def format_latitude(latitude: float) -> str:
    """
    Human-readable latitude.
    """
    validate_latitude(latitude)

    direction = "N" if latitude >= 0 else "S"

    deg, minute, second = decimal_to_dms(abs(latitude))

    return f"{deg}°{minute:02d}'{second:05.2f}\" {direction}"


def format_longitude(longitude: float) -> str:
    """
    Human-readable longitude.
    """
    validate_longitude(longitude)

    direction = "E" if longitude >= 0 else "W"

    deg, minute, second = decimal_to_dms(abs(longitude))

    return f"{deg}°{minute:02d}'{second:05.2f}\" {direction}"


def validate_coordinates(
    latitude: float,
    longitude: float,
) -> Coordinates:
    """
    Validate and return immutable Coordinates.
    """
    validate_latitude(latitude)
    validate_longitude(longitude)

    return Coordinates(latitude, longitude)


__all__ = [
    "Coordinates",
    "validate_latitude",
    "validate_longitude",
    "validate_coordinates",
    "normalize_longitude",
    "clamp_latitude",
    "decimal_to_dms",
    "dms_to_decimal",
    "format_latitude",
    "format_longitude",
]
