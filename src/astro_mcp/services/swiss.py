"""
Swiss Ephemeris service layer.

Provides a thin wrapper around pyswisseph so the rest of the
application never directly calls the library.

Author: Astro-MCP
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import swisseph as swe

from astro_mcp.coordinates import Coordinates

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
    "Mean Node": swe.MEAN_NODE,
    "True Node": swe.TRUE_NODE,
}

FLAGS = (
    swe.FLG_SWIEPH
    | swe.FLG_SPEED
)


# -----------------------------------------------------------------------------
# Data Models
# -----------------------------------------------------------------------------

@dataclass(slots=True)
class PlanetPosition:
    name: str
    longitude: float
    latitude: float
    distance: float
    longitude_speed: float
    latitude_speed: float
    distance_speed: float


@dataclass(slots=True)
class HouseSystem:
    cusps: List[float]
    ascendant: float
    midheaven: float
    armc: float
    vertex: float


# -----------------------------------------------------------------------------
# Service
# -----------------------------------------------------------------------------

class SwissEphemerisService:
    """
    High-level interface around Swiss Ephemeris.
    """

    def __init__(self, ephemeris_path: str | None = None):

        if ephemeris_path:
            swe.set_ephe_path(ephemeris_path)
            return

        local = Path.cwd() / "ephe"

        if local.exists():
            swe.set_ephe_path(str(local))

    # -------------------------------------------------------------------------

    @staticmethod
    def julian_day(dt: datetime) -> float:
        """
        Convert timezone-aware datetime to Julian Day.
        """

        if dt.tzinfo is None:
            raise ValueError("datetime must be timezone-aware")

        utc = dt.astimezone(timezone.utc)

        return swe.julday(
            utc.year,
            utc.month,
            utc.day,
            utc.hour
            + utc.minute / 60
            + utc.second / 3600
            + utc.microsecond / 3_600_000_000,
        )

    # -------------------------------------------------------------------------

    def planet(self, jd: float, planet: str) -> PlanetPosition:

        body = PLANETS[planet]

        values, _ = swe.calc_ut(jd, body, FLAGS)

        return PlanetPosition(
            name=planet,
            longitude=values[0],
            latitude=values[1],
            distance=values[2],
            longitude_speed=values[3],
            latitude_speed=values[4],
            distance_speed=values[5],
        )

    # -------------------------------------------------------------------------

    def planets(self, jd: float) -> Dict[str, PlanetPosition]:

        return {
            name: self.planet(jd, name)
            for name in PLANETS
        }

    # -------------------------------------------------------------------------

    def houses(
        self,
        jd: float,
        coords: Coordinates,
        system: str = "W",
    ) -> HouseSystem:
        """
        Calculate house cusps.

        W = Whole Sign
        P = Placidus
        K = Koch
        R = Regiomontanus
        C = Campanus
        O = Porphyry
        X = Axial
        """

        cusps, angles = swe.houses_ex(
            jd,
            coords.latitude,
            coords.longitude,
            bytes(system, "ascii"),
        )

        return HouseSystem(
            cusps=list(cusps),
            ascendant=angles[0],
            midheaven=angles[1],
            armc=angles[2],
            vertex=angles[3],
        )

    # -------------------------------------------------------------------------

    @staticmethod
    def sidereal_time(jd: float) -> float:
        return swe.sidtime(jd)

    # -------------------------------------------------------------------------

    def natal_chart(
        self,
        dt: datetime,
        coords: Coordinates,
        house_system: str = "W",
    ) -> dict:

        jd = self.julian_day(dt)

        planets = self.planets(jd)

        houses = self.houses(
            jd,
            coords,
            house_system,
        )

        return {
            "julian_day": jd,
            "planets": planets,
            "houses": houses,
        }

    # -------------------------------------------------------------------------

    def transits(
        self,
        natal_dt: datetime,
        transit_dt: datetime,
        coords: Coordinates,
    ) -> dict:

        natal = self.natal_chart(
            natal_dt,
            coords,
        )

        transit = self.natal_chart(
            transit_dt,
            coords,
        )

        results = {}

        for name in PLANETS:

            natal_lon = natal["planets"][name].longitude
            transit_lon = transit["planets"][name].longitude

            diff = (transit_lon - natal_lon) % 360

            results[name] = {
                "natal": natal_lon,
                "transit": transit_lon,
                "difference": diff,
            }

        return {
            "natal": natal,
            "transits": transit,
            "differences": results,
        }


# -----------------------------------------------------------------------------
# Singleton
# -----------------------------------------------------------------------------

service = SwissEphemerisService()
