"""
Natal chart MCP tools.
"""

from __future__ import annotations

from fastmcp import FastMCP

from astro_mcp.services.swiss import calculate_natal_chart
from astro_mcp.utils.validation import (
    validate_birth_data,
    validate_house_system,
)


def register_natal_tools(mcp: FastMCP) -> None:
    """
    Register natal chart tools.
    """

    @mcp.tool(
        name="natal_chart",
        description="Calculate a complete natal chart using Swiss Ephemeris.",
    )
    def natal_chart(
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        latitude: float,
        longitude: float,
        timezone: str,
        house_system: str = "W",
    ) -> dict:
        """
        Calculate a natal chart.

        Args:
            year: Birth year
            month: Birth month
            day: Birth day
            hour: Local birth hour (24-hour)
            minute: Local birth minute
            latitude: Decimal latitude
            longitude: Decimal longitude
            timezone: IANA timezone
            house_system: Swiss Ephemeris house system

        Returns:
            Natal chart dictionary.
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

        return calculate_natal_chart(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            latitude=latitude,
            longitude=longitude,
            timezone=timezone,
            house_system=house_system,
        )
