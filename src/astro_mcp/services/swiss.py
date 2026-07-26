"""
Swiss Ephemeris service.

Provides a thin abstraction over pyswisseph for the Astro MCP server.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

import swisseph as swe

DEFAULT_FLAGS = (
    swe.FLG_SWIEPH
    | swe.FLG_SPEED
    | swe.FLG_TOPOCTR
)

PLANETS = {
    "sun": swe.SUN,
    "moon": swe.MOON,
    "mercury": swe.MERCURY,
    "venus": swe.VENUS,
    "mars": swe.MARS,
    "jupiter": swe.JUPITER,
    "saturn": swe.SATURN,
    "uranus": swe.URANUS,
    "neptune": swe.NEPTUNE,
    "pluto": swe.PLUTO,
    "mean_node": swe.MEAN_NODE,
    "true_node": swe.TRUE_NODE,
}


@dataclass(slots=True)
class PlanetPosition:
    name: str
    longitude: float
    latitude: float
    distance: float
    speed_longitude: float
    speed_latitude: float
    speed_distance: float


class SwissEphemeris:

    def __init__(self, ephemeris_path: str | None = None):

        if ephemeris_path:
            path = Path(ephemeris_path).expanduser()
            path.mkdir(parents=True, exist_ok=True)
            swe.set_ephe_path(str(path))

    @staticmethod
    def julian_day(moment: datetime) -> float:

        if moment.tzinfo is None:
            moment = moment.replace(tzinfo=timezone.utc)

        utc = moment.astimezone(timezone.utc)

        hour = (
            utc.hour
            + utc.minute / 60
            + utc.second / 3600
            + utc.microsecond / 3_600_000_000
        )

        return swe.julday(
            utc.year,
            utc.month,
            utc.day,
            hour,
            swe.GREG_CAL,
        )

    @staticmethod
    def set_location(
        latitude: float,
        longitude: float,
        altitude: float = 0.0,
    ) -> None:
        swe.set_topo(longitude, latitude, altitude)

    def planet(
        self,
        jd: float,
        planet: str,
    ) -> PlanetPosition:

        pid = PLANETS[planet.lower()]

        values, _ = swe.calc_ut(
            jd,
            pid,
            DEFAULT_FLAGS,
        )

        return PlanetPosition(
            name=planet,
            longitude=values[0],
            latitude=values[1],
            distance=values[2],
            speed_longitude=values[3],
            speed_latitude=values[4],
            speed_distance=values[5],
        )

    def planets(self, jd: float) -> Dict[str, PlanetPosition]:

        return {
            name: self.planet(jd, name)
            for name in PLANETS
        }

    @staticmethod
    def houses(
        jd: float,
        latitude: float,
        longitude: float,
        system: str = "W",
    ):

        cusps, ascmc = swe.houses_ex(
            jd,
            latitude,
            longitude,
            system.encode(),
        )

        return {
            "cusps": list(cusps),
            "ascendant": ascmc[0],
            "mc": ascmc[1],
            "armc": ascmc[2],
            "vertex": ascmc[3],
            "equatorial_ascendant": ascmc[4],
        }

    @staticmethod
    def ayanamsa(jd: float) -> float:
        return swe.get_ayanamsa_ut(jd)

    @staticmethod
    def sidereal_mode(mode=swe.SIDM_LAHIRI):

        swe.set_sid_mode(mode)

    @staticmethod
    def house_position(
        longitude: float,
        cusps,
    ) -> int:

        for i in range(12):
            start = cusps[i]
            end = cusps[(i + 1) % 12]

            if end < start:
                end += 360

            value = longitude

            if value < start:
                value += 360

            if start <= value < end:
                return i + 1

        return 12

    def natal_chart(
        self,
        dt: datetime,
        latitude: float,
        longitude: float,
        altitude: float = 0.0,
        house_system: str = "W",
    ):

        self.set_location(latitude, longitude, altitude)

        jd = self.julian_day(dt)

        planets = self.planets(jd)

        houses = self.houses(
            jd,
            latitude,
            longitude,
            house_system,
        )

        result = {}

        for name, body in planets.items():
            result[name] = {
                "longitude": body.longitude,
                "latitude": body.latitude,
                "distance": body.distance,
                "speed": body.speed_longitude,
                "house": self.house_position(
                    body.longitude,
                    houses["cusps"],
                ),
            }

        return {
            "julian_day": jd,
            "houses": houses,
            "planets": result,
        }

    def transit_chart(
        self,
        dt: datetime,
        latitude: float,
        longitude: float,
        altitude: float = 0.0,
    ):

        self.set_location(
            latitude,
            longitude,
            altitude,
        )

        jd = self.julian_day(dt)

        return {
            "julian_day": jd,
            "planets": {
                name: vars(position)
                for name, position in self.planets(jd).items()
            },
        }


swiss = SwissEphemeris()
