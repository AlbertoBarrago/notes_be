# Project Cheatsheets

Quick reference for daily development tasks on **albz-notes-be**.
All Python commands use `uv run` — never call `uvicorn`, `pytest`, or `alembic` directly.

---

## Table of Contents

- [Dev Server](#dev-server)
- [Testing](#testing)
- [Linting](#linting)
- [Migrations](#migrations)
- [Docker](#docker)
- [Environment](#environment)
- [uv Package Manager](#uv-package-manager)
- [API Quick Reference](#api-quick-reference)
- [Make Targets](#make-targets)

---

## Dev Server

```bash
# Start with hot-reload
uv run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

# Swagger UI
open http://localhost:8080/docs

# Healthcheck
curl http://localhost:8080/healthcheck
```

---

## Testing

```bash
# Run all tests (suppresses warnings)
uv run pytest -p no:warnings test/**/*.py

# Run a single test file
uv run pytest -p no:warnings test/note.py
uv run pytest -p no:warnings test/user.py

# Run with verbose output
uv run pytest -p no:warnings -v test/**/*.py

# Run a specific test by name
uv run pytest -p no:warnings -k "test_create_note" test/**/*.py

# Stop on first failure
uv run pytest -p no:warnings -x test/**/*.py
```

> Tests use in-memory SQLite — no running MySQL or external services required.

---

## Linting

```bash
# Lint the entire app
uv run pylint app/

# Lint a single module
uv run pylint app/repositories/note/repository.py

# Disabled rules (see .pylintrc): R0903, R0911-R0917, R0902, C0103, E1120
```

---

## Migrations

```bash
# Apply all pending migrations
uv run alembic upgrade head

# Generate a new migration from model changes
uv run alembic revision --autogenerate -m "add summary column to notes"

# Show current applied revision
uv run alembic current

# Show migration history
uv run alembic history

# Roll back one step
uv run alembic downgrade -1

# Roll back everything
uv run alembic downgrade base

# Stamp DB without running migrations (after manual bootstrap)
uv run alembic stamp head
```

See `docs/alembic_cheatsheet.md` for the full Alembic reference.

---

## Docker

```bash
# Start app + MySQL in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down

# Rebuild after code/Dockerfile changes
docker-compose down && docker-compose up --build

# Check running containers
docker-compose ps
```

> Requires `.env` to be present. If local MySQL is already on port 3306, update the port mapping in `docker-compose.yml`.

---

## Environment

```bash
# Copy sample env
cp .env.sample .env
```

| Variable | Description | Required |
|---|---|---|
| `MYSQL_USER` | Database user | Yes |
| `MYSQL_PASSWORD` | Database password | Yes |
| `MYSQL_HOST` | Database host | Yes |
| `MYSQL_DATABASE` | Database name | Yes |
| `SECRET_KEY` | JWT signing secret | Yes |
| `GOOGLE_CLIENT_ID` | OAuth client ID | OAuth only |
| `GOOGLE_CLIENT_SECRET` | OAuth client secret | OAuth only |

Connection string format: `mysql+mysqlconnector://user:pass@host/db`

---

## uv Package Manager

```bash
# Install / sync all dependencies from pyproject.toml + uv.lock
uv sync

# Add a new dependency
uv add fastapi

# Add a dev dependency
uv add --dev pytest

# Remove a dependency
uv remove some-package

# Update all packages
uv lock --upgrade

# Run any command in the project venv
uv run <command>

# Show installed packages
uv pip list
```

---

## API Quick Reference

All endpoints are prefixed with `/api/v1/` unless noted.

### Auth

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/auth/register` | Register a new user |
| POST | `/api/v1/auth/login` | Login, get JWT |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| POST | `/api/v1/auth/forgot-password` | Send password reset email |
| POST | `/api/v1/auth/reset-password` | Reset password with token |

### OAuth

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/oauth/login` | Redirect to Google consent |
| GET | `/api/v1/oauth/callback` | OAuth callback, issues JWT |

### Notes

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/notes` | List user's notes (paginated) |
| POST | `/api/v1/notes` | Create a note |
| GET | `/api/v1/notes/{id}` | Get a note |
| PUT | `/api/v1/notes/{id}` | Update a note |
| DELETE | `/api/v1/notes/{id}` | Delete a note |

### Users

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/users/me` | Get current user profile |
| PUT | `/api/v1/users/me` | Update profile |
| DELETE | `/api/v1/users/me` | Delete account |

### BackOffice (ADMIN only)

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/backoffice/users` | List all users |
| GET | `/api/v1/backoffice/audit` | List audit log |
| DELETE | `/api/v1/backoffice/users/{id}` | Delete a user |

### System

| Method | Path | Description |
|---|---|---|
| GET | `/healthcheck` | Health status |
| GET | `/` | Home |
| GET | `/docs` | Swagger UI |

---

## Make Targets

```bash
make dev             # Start dev server
make test            # Run all tests
make lint            # Run pylint
make migrate         # Apply migrations (alembic upgrade head)
make migration msg="description"  # Autogenerate migration
make install         # uv sync
make docker-up       # docker-compose up -d
make docker-rebuild  # docker-compose down && up --build
```

---

## Common Patterns in Code

### Add a new endpoint

1. Add route in `app/api/v1/endpoints/<domain>.py`
2. Call manager via `perform_*_action(action, ...)`
3. Use `Depends(get_db)` and `Depends(get_current_user)` for auth

### Add a new manager action

1. Add method to the manager class in `app/repositories/<domain>/`
2. Register it in the dispatcher dict
3. Call `CommonService(db).log_action(...)` for write operations

### Raise an error

```python
# Never do this:
raise HTTPException(status_code=404, detail="Not found")

# Always do this:
NoteErrorHandler.raise_note_not_found()
AuthErrorHandler.raise_unauthorized()
UserErrorHandler.raise_user_not_found()
GlobalErrorHandler.raise_internal_error()
```

### Add a new Pydantic schema

```python
# app/schemas/<domain>.py
from pydantic import BaseModel

class NoteCreate(BaseModel):
    title: str
    content: str
    is_public: bool = False
    tags: list[str] = []
```
