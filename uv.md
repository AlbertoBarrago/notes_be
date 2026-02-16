# UV Guide

Quick reference for using [uv](https://docs.astral.sh/uv/) as Python package manager in this project.

## What is uv?

`uv` is an extremely fast Python package and project manager written in Rust. It replaces `pip`, `pip-tools`, `virtualenv`, and more in a single tool.

## Setup

### Install uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# or with Homebrew
brew install uv
```

### Create a virtual environment

```bash
uv venv --python 3.12 .venv
```

### Install dependencies

```bash
# From requirements.txt
uv pip install -r requirements.txt

# Or a single package
uv pip install fastapi-mail
```

## Running commands

The most important thing: **always use `uv run`** to execute CLI tools. This ensures they use the `.venv` Python and its installed packages, even without activating the venv.

```bash
# Start dev server
uv run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

# Run tests
uv run pytest -p no:warnings test/**/*.py

# Run linter
uv run pylint app/

# Run migrations
uv run alembic upgrade head
uv run alembic revision --autogenerate -m "description"
```

### Why `uv run`?

Without it, your shell uses whatever `uvicorn`/`pytest`/etc. is first in your `$PATH` — often a system-wide install that **does not** see packages in `.venv`. This is exactly what causes errors like:

```
ModuleNotFoundError: No module named 'fastapi_mail'
```

### Alternative: activate the venv

If you prefer, you can activate the venv first and then run commands normally:

```bash
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

But `uv run` is simpler and doesn't require remembering to activate.

## Migrating to pyproject.toml (optional)

`uv` can manage dependencies via `pyproject.toml` instead of `requirements.txt`. This unlocks lockfiles and dependency groups.

```bash
# Initialize a pyproject.toml from existing requirements
uv init
uv add -r requirements.txt
```

This creates a `pyproject.toml` with your deps and a `uv.lock` lockfile. After that:

```bash
# Install all deps from lockfile (fast, reproducible)
uv sync

# Add a new dependency
uv add httpx

# Add a dev-only dependency
uv add --dev pytest

# Remove a dependency
uv remove httpx

# Update all deps
uv lock --upgrade
uv sync
```

## Useful commands

| Command                        | Description                              |
|--------------------------------|------------------------------------------|
| `uv run <cmd>`                 | Run a command using `.venv` Python       |
| `uv pip install <pkg>`         | Install a package into `.venv`           |
| `uv pip install -r req.txt`    | Install from requirements file           |
| `uv pip list`                  | List installed packages                  |
| `uv pip show <pkg>`            | Show package details                     |
| `uv venv --python 3.12 .venv`  | Create a venv with specific Python       |
| `uv sync`                      | Install deps from `pyproject.toml` lock  |
| `uv add <pkg>`                 | Add dependency to `pyproject.toml`       |
| `uv lock`                      | Regenerate the lockfile                  |
| `uv python list`               | List available Python versions           |
| `uv python install 3.12`       | Install a Python version                 |
