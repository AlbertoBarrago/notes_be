# Contributing to albz-notes-be

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) — package manager (`pip install uv`)
- MySQL 8+ (or Docker — see below)
- A `.env` file copied from `.env.sample`

## Local setup

```bash
git clone <repo-url>
cd albz_notes_be

uv sync --extra dev        # install all dependencies including dev tools

cp .env.sample .env        # fill in your local DB credentials

# Option A — bare MySQL
mysql -u root -p < sql/create.sql
mysql -u root -p < sql/create_user.sql
mysql -u notez_app -p notez_be < sql/seed.sql

# Option B — Docker (app on :8080, MySQL handled automatically)
docker-compose up -d

uv run alembic upgrade head  # run migrations
uv run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

Swagger UI: http://localhost:8080/docs

## Running tests

```bash
# Endpoint integration tests (SQLite in-memory, no MySQL needed)
uv run pytest -p no:warnings test/endpoints/

# ORM model tests
uv run pytest -p no:warnings test/note.py test/auth.py test/audit.py
```

## Linting

```bash
uv run pylint app/           # must score 10.00/10 before opening a PR
```

## Branch strategy

| Branch | Purpose |
|--------|---------|
| `main` | Production-ready code — never commit directly |
| `feature/<name>` | New features |
| `fix/<name>` | Bug fixes |
| `chore/<name>` | Tooling, deps, config |

## Commit messages

Follow the `<type>: <short description>` convention:

```
feat: add public note search endpoint
fix: await missing on refresh-token handler
chore: migrate settings to pydantic-settings
docs: update CONTRIBUTORS.md
```

## Pull request checklist

- [ ] `uv run pylint app/` scores **10.00/10**
- [ ] `uv run pytest -p no:warnings test/endpoints/` all pass
- [ ] Version bumped in `pyproject.toml` **and** `app/core/setup.py` (releases only)
- [ ] New migration created if models changed (`uv run alembic revision --autogenerate -m "description"`)
- [ ] `sql/seed.sql` and `sql/reset.sql` updated if schema changed

## Releasing a new version

1. **Bump the version** in two places:
   ```bash
   # pyproject.toml  → version = "x.y.z"
   # app/core/setup.py → version="x.y.z"
   ```
2. **Commit**:
   ```bash
   git add pyproject.toml app/core/setup.py
   git commit -m "chore: bump version to x.y.z"
   ```
3. **Tag**:
   ```bash
   git tag -a vx.y.z -m "Release x.y.z"
   git push origin main --tags
   ```
