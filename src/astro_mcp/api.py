"""
Optional HTTP API.
"""

from fastapi import FastAPI

app = FastAPI(
    title="Astro MCP",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "Astro MCP",
    }
