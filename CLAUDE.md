# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python project for testing streaming functionality with the Anthropic Development Kit (ADK). The project currently contains a minimal setup with:

- Python virtual environment in `.venv/`
- Standard Python project structure
- MCP (Model Context Protocol) configuration with GitHub server access

## Development Environment

### Virtual Environment
The project uses a Python virtual environment located in `.venv/`. Activate it with:
```bash
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

### Dependencies
Currently no specific dependencies are defined. If dependencies are added later, they would typically be managed through:
- `requirements.txt` for pip
- `pyproject.toml` for modern Python packaging
- `Pipfile` for pipenv

## Common Commands

Since this is a minimal Python project, standard Python development commands would apply:

- Install dependencies: `pip install -r requirements.txt` (when requirements.txt exists)
- Run Python scripts: `python <script_name>.py`
- Run tests: `python -m pytest` (when tests are added)

## MCP Configuration

The project includes MCP (Model Context Protocol) configuration in `.mcp.json` with access to:
- **GitHub MCP Server**: Provides GitHub API functionality including repository management, issues, pull requests, and user information access.

## Architecture

This is currently a minimal project structure suitable for Python development and testing of ADK streaming functionality.