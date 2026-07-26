# Astro-MCP

> A production-grade Model Context Protocol (MCP) server for professional astrology powered by Swiss Ephemeris.

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://python.org)
[![FastMCP](https://img.shields.io/badge/FastMCP-3.x-green.svg)](https://github.com/jlowin/fastmcp)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/YOUR_USERNAME/Astro-MCP/actions/workflows/ci.yml/badge.svg)](../../actions)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-black.svg)](https://docs.astral.sh/ruff/)

Astro-MCP is an open-source, production-ready Model Context Protocol server that exposes professional astrology tools using the Swiss Ephemeris.

Designed for AI assistants, desktop clients, automation platforms, and custom applications, Astro-MCP provides mathematically precise astronomical calculations while remaining modular, extensible, and standards compliant.

---

# Features

- Swiss Ephemeris precision
- FastMCP 3.x server
- Model Context Protocol compliant
- Tropical and Sidereal zodiac support
- Multiple house systems
- Natal chart calculations
- Transit calculations
- Solar returns
- Secondary progressions
- Synastry
- Composite charts
- Aspect calculations
- Planetary positions
- Lunar nodes
- Fixed stars (planned)
- Asteroids (planned)
- Time zone support
- Geocoding
- REST API
- Structured JSON responses
- Docker support
- GitHub Actions CI/CD
- Fully typed Python
- Extensive automated tests

---

# Project Goals

Astro-MCP aims to provide a modern astrology engine that can be integrated into AI systems through the Model Context Protocol.

Goals include:

- Scientific astronomical calculations
- Transparent methodology
- Reproducible chart calculations
- Professional software architecture
- Extensible plugin system
- Open source collaboration

---

# Architecture

```
                +----------------+
                | AI Assistant   |
                +--------+-------+
                         |
                  Model Context Protocol
                         |
                +--------v--------+
                |   Astro-MCP     |
                +--------+--------+
                         |
        +----------------+----------------+
        |                |                |
        v                v                v
  Natal Charts     Transit Engine    REST API
        |                |                |
        +----------------+----------------+
                         |
                Swiss Ephemeris
```

---

# Supported Calculations

## Natal Charts

- Planet positions
- Houses
- Angles
- Aspects
- Elements
- Modalities
- Chart ruler
- Essential dignities

---

## Transits

- Current transits
- Future transits
- Historical transits
- Transit aspects
- Orb filtering

---

## Solar Returns

- Annual return charts
- Return house overlays
- Return aspects

---

## Progressions

- Secondary progressions
- Progressed Moon
- Progressed angles

---

## Synastry

- Cross-chart aspects
- Relationship compatibility
- Composite chart generation

---

# Supported House Systems

- Placidus
- Whole Sign
- Koch
- Equal
- Campanus
- Regiomontanus
- Topocentric
- Porphyry

---

# Zodiac Systems

- Tropical
- Sidereal (Lahiri)
- Sidereal (Fagan-Bradley)
- Sidereal (Krishnamurti)

---

# Installation

## Clone

```bash
git clone https://github.com/YOUR_USERNAME/Astro-MCP.git

cd Astro-MCP
```

---

## Create Environment

```bash
python -m venv .venv

source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

---

## Install

```bash
pip install -e .
```

---

## Development

```bash
pip install -e ".[dev]"
```

---

# Running

## MCP Server

```bash
python -m astro_mcp
```

or

```bash
fastmcp run src/astro_mcp/server.py
```

---

## REST API

```bash
uvicorn astro_mcp.api:app --reload
```

---

# Example Tools

## Natal Chart

```json
{
  "name": "Natal Chart",
  "arguments": {
    "date": "1992-08-13",
    "time": "16:01",
    "latitude": 47.774,
    "longitude": -96.608,
    "timezone": "America/Chicago"
  }
}
```

---

## Transit Report

```json
{
  "name": "Current Transits",
  "arguments": {
    "date": "2026-07-26"
  }
}
```

---

# Project Structure

```
Astro-MCP/

src/
    astro_mcp/
        api.py
        server.py
        config.py
        services/
        tools/
        models/

tests/

docs/

examples/

scripts/

.github/
```

---

# Development

## Formatting

```bash
ruff format .
```

---

## Lint

```bash
ruff check .
```

---

## Type Checking

```bash
mypy src
```

---

## Testing

```bash
pytest
```

---

# Docker

```bash
docker compose up
```

---

# GitHub Actions

Continuous Integration includes:

- Ruff
- MyPy
- Pytest
- Package build
- Wheel validation
- Docker build
- Release artifacts

---

# Roadmap

## Version 0.1

- Natal charts
- Transits
- REST API
- FastMCP

## Version 0.2

- Solar returns
- Progressions
- Synastry

## Version 0.3

- Composite charts
- Asteroids
- Fixed stars

## Version 1.0

- Stable API
- Plugin system
- Documentation complete

---

# Contributing

Contributions are welcome.

Please read:

- CONTRIBUTING.md
- CODE_OF_CONDUCT.md
- SECURITY.md

before submitting pull requests.

---

# License

Released under the MIT License.

See LICENSE for details.

---

# Acknowledgements

- Swiss Ephemeris
- FastMCP
- Model Context Protocol
- Pydantic
- FastAPI
- Uvicorn

---

# Disclaimer

Astro-MCP performs astronomical calculations and exposes astrology-related tooling.

Interpretation of charts is subjective and varies across astrological traditions. This project does not claim scientific validation for astrological interpretations. Users should distinguish between the underlying astronomical calculations and any interpretive layer built on top of them.

---

# Star History

If you find Astro-MCP useful, please consider starring the repository.

⭐ Contributions, bug reports, and feature requests are always welcome.
