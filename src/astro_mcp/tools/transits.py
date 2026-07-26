"""
Transit chart MCP tools.

Registers FastMCP tools for calculating planetary transits
using Swiss Ephemeris.
"""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from fastmcp import FastMCP

from astro_mcp.services.swiss import calculate_transits
from astro_mcp.utils.validation import (
    validate_birth_data,
    validate_house_system,
)


def register_transit_tools(mcp: FastMCP) -> None:
    """
    Register transit-related MCP tools.
    """

    @mcp.tool(
        name="current_transits",
        description="Calculate current planetary transits against a natal chart.",
    )
    def current_transits(
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        latitude: float,
        longitude: float,
        timezone: str,
        house_system: str = "W",
        transit_time: str | None = None,
    ) -> dict:
        """
        Calculate planetary transits.

        Args:
            year: Birth year.
            month: Birth month.
            day: Birth day.
            hour: Birth hour.
            minute: Birth minute.
            latitude: Birth latitude.
            longitude: Birth longitude.
            timezone: IANA timezone.
            house_system: Swiss Ephemeris house system.
            transit_time:
                ISO-8601 datetime.
                If omitted, current UTC time is used.

        Returns:
            Dictionary containing transit data.
        """

        validate_birth_data(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            latitude=latitude,
            longitude=longitude,
            timezone=timezone,
        )

        house_system = validate_house_system(house_system)

        if transit_time is None:
            transit_dt = datetime.utcnow()
        else:
            transit_dt = datetime.fromisoformat(transit_time)

            if transit_dt.tzinfo is None:
                transit_dt = transit_dt.replace(
                    tzinfo=ZoneInfo("UTC")
                )

        return calculate_transits(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            latitude=latitude,
            longitude=longitude,
            timezone=timezone,
            house_system=house_system,
            transit_datetime=transit_dt,
        )
