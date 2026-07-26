# ============================================================================
# Astro-MCP Makefile
# ============================================================================

.DEFAULT_GOAL := help

PYTHON := python
PIP := pip
UVICORN := uvicorn
PYTEST := pytest
RUFF := ruff
MYPY := mypy
BUILD := python -m build
DOCKER := docker
COMPOSE := docker compose

PACKAGE := astro_mcp

# -----------------------------------------------------------------------------
# Help
# -----------------------------------------------------------------------------

.PHONY: help

help:
	@echo ""
	@echo "Astro-MCP Development Commands"
	@echo ""
	@echo "Environment"
	@echo "  make install          Install package"
	@echo "  make dev              Install development dependencies"
	@echo "  make clean            Remove build artifacts"
	@echo ""
	@echo "Quality"
	@echo "  make format           Format code"
	@echo "  make lint             Run Ruff"
	@echo "  make typecheck        Run MyPy"
	@echo "  make test             Run Pytest"
	@echo "  make coverage         Run tests with coverage"
	@echo ""
	@echo "Build"
	@echo "  make build            Build wheel and source distribution"
	@echo "  make publish-test     Upload to TestPyPI"
	@echo "  make publish          Upload to PyPI"
	@echo ""
	@echo "Run"
	@echo "  make api              Start REST API"
	@echo "  make server           Start MCP server"
	@echo "  make devserver        Start API with auto reload"
	@echo ""
	@echo "Docker"
	@echo "  make docker-build"
	@echo "  make docker-up"
	@echo "  make docker-down"
	@echo "  make docker-logs"
	@echo ""

# -----------------------------------------------------------------------------
# Installation
# -----------------------------------------------------------------------------

.PHONY: install

install:
	$(PIP) install -e .

.PHONY: dev

dev:
	$(PIP) install -e ".[dev,docs]"

# -----------------------------------------------------------------------------
# Formatting
# -----------------------------------------------------------------------------

.PHONY: format

format:
	$(RUFF) format src tests

.PHONY: lint

lint:
	$(RUFF) check src tests

.PHONY: lint-fix

lint-fix:
	$(RUFF) check --fix src tests

# -----------------------------------------------------------------------------
# Static Analysis
# -----------------------------------------------------------------------------

.PHONY: typecheck

typecheck:
	$(MYPY) src

# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------

.PHONY: test

test:
	$(PYTEST)

.PHONY: coverage

coverage:
	$(PYTEST) --cov=$(PACKAGE) --cov-report=term-missing

# -----------------------------------------------------------------------------
# Build
# -----------------------------------------------------------------------------

.PHONY: build

build:
	$(BUILD)

# -----------------------------------------------------------------------------
# Publish
# -----------------------------------------------------------------------------

.PHONY: publish-test

publish-test:
	twine upload --repository testpypi dist/*

.PHONY: publish

publish:
	twine upload dist/*

# -----------------------------------------------------------------------------
# Run
# -----------------------------------------------------------------------------

.PHONY: api

api:
	$(UVICORN) astro_mcp.api:app --host 0.0.0.0 --port 8000

.PHONY: devserver

devserver:
	$(UVICORN) astro_mcp.api:app --reload --host 0.0.0.0 --port 8000

.PHONY: server

server:
	$(PYTHON) -m astro_mcp

# -----------------------------------------------------------------------------
# Docker
# -----------------------------------------------------------------------------

.PHONY: docker-build

docker-build:
	$(COMPOSE) build

.PHONY: docker-up

docker-up:
	$(COMPOSE) up -d

.PHONY: docker-down

docker-down:
	$(COMPOSE) down

.PHONY: docker-restart

docker-restart:
	$(COMPOSE) restart

.PHONY: docker-logs

docker-logs:
	$(COMPOSE) logs -f

# -----------------------------------------------------------------------------
# Cleanup
# -----------------------------------------------------------------------------

.PHONY: clean

clean:
	rm -rf build
	rm -rf dist
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# -----------------------------------------------------------------------------
# Complete CI Validation
# -----------------------------------------------------------------------------

.PHONY: check

check: format lint typecheck test build

# -----------------------------------------------------------------------------
# Release
# -----------------------------------------------------------------------------

.PHONY: release

release: clean check build

# -----------------------------------------------------------------------------
# Git Helpers
# -----------------------------------------------------------------------------

.PHONY: status

status:
	git status

.PHONY: branches

branches:
	git branch

.PHONY: tags

tags:
	git tag

.PHONY: version

version:
	@$(PYTHON) -c "import astro_mcp; print(astro_mcp.__version__)"

# -----------------------------------------------------------------------------
# Ephemeris
# -----------------------------------------------------------------------------

.PHONY: ephemeris

ephemeris:
	mkdir -p ephemeris

# -----------------------------------------------------------------------------
# Documentation
# -----------------------------------------------------------------------------

.PHONY: docs

docs:
	mkdocs serve

.PHONY: docs-build

docs-build:
	mkdocs build

# -----------------------------------------------------------------------------
# Everything
# -----------------------------------------------------------------------------

.PHONY: all

all: clean format lint typecheck test build
