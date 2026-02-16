# TODO

## Environment & Tooling

- [x] **Use `uv run` instead of bare commands** — All CLI tools (`uvicorn`, `pytest`, `alembic`, `pylint`) should be prefixed with `uv run` to ensure they use `.venv` dependencies. Without this, system-installed binaries may be picked up instead, causing missing module errors (e.g. `fastapi_mail`).
- [x] **Migrate from `requirements.txt` to `pyproject.toml`** — `uv` natively supports `pyproject.toml` with `[project.dependencies]`. This enables `uv sync`, lockfiles (`uv.lock`), and dependency groups (dev, test).
- [x] **Update CLAUDE.md and README.md commands** — Replace bare `uvicorn`/`pytest`/`alembic`/`pylint` commands with their `uv run` equivalents.
- [x] **Pin all dependency versions consistently** — Some deps use `==`, others `~=`, others have no constraint. Pick one strategy (recommend `>=X.Y,<X+1` or let `uv lock` handle it).

## Code Quality

- [x] **Add BackOffice API** — `get_users`, `get_notes`, `get_audit` (already noted in README).
- [x] **Add type hints to repository methods** — Improves IDE support and catches bugs early.
- [x] **Add `py.typed` marker** — If you plan to distribute or reuse this package.

## DevOps

- [x] **Update Dockerfile to use `uv`** — If using Docker, install deps with `uv sync` instead of `pip install -r requirements.txt` for faster builds and reproducible lockfiles.
- [x] **Add a `Makefile` or `justfile`** — Wrap common commands (`dev`, `test`, `lint`, `migrate`) so contributors don't need to remember flags.
