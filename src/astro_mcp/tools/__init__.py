"""
Astro-MCP tool package.

Exports all public MCP tools.
"""

from .natal import register_natal_tools
from .transits import register_transit_tools

__all__ = [
    "register_natal_tools",
    "register_transit_tools",
]
