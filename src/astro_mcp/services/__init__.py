"""
Astro-MCP service layer.

This package provides integrations with external libraries and services,
including Swiss Ephemeris, geocoding, and astronomical calculations.
"""

from .swiss import (
    SwissEphemeris,
    PlanetPosition,
    swiss,
)

__all__ = [
    "SwissEphemeris",
    "PlanetPosition",
    "swiss",
]
