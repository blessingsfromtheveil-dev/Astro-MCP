from fastmcp import FastMCP

mcp = FastMCP(
    name="Astro-MCP",
    version="0.1.0",
)

from astro_mcp.tools.natal import register_natal_tools
from astro_mcp.tools.transits import register_transit_tools

register_natal_tools(mcp)
register_transit_tools(mcp)
