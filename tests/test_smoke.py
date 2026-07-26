"""
Basic smoke tests for Astro-MCP.

Run with:

    pytest -v

These tests intentionally avoid making astronomical assertions.
They simply verify that the package imports correctly and the
core runtime dependencies are installed.
"""

import importlib

import swisseph


def test_package_import():
    """astro_mcp package imports successfully."""
    module = importlib.import_module("astro_mcp")
    assert module is not None


def test_server_import():
    """Server module imports successfully."""
    module = importlib.import_module("astro_mcp.server")
    assert module is not None


def test_fastmcp_available():
    """FastMCP is installed."""
    fastmcp = importlib.import_module("fastmcp")
    assert fastmcp.__version__


def test_swisseph_available():
    """Swiss Ephemeris is installed."""
    assert swisseph.version


def test_tools_import():
    """Tool modules import."""
    importlib.import_module("astro_mcp.tools.natal")
    importlib.import_module("astro_mcp.tools.transits")


def test_services_import():
    """Service modules import."""
    importlib.import_module("astro_mcp.services.swiss")
