# Changelog

## [1.1.0] - 2026-02-17

### Added
- **BackOffice API** — Admin-only endpoints under `/api/v1/backoffice`:
  - `GET /users` — paginated list of all users
  - `GET /notes` — paginated list of all notes
  - `GET /audit` — paginated list of audit logs
- **`BackofficeManager`** repository with admin role checks and audit logging
- **`AuditDTO`** with `from_model()` and `paginated_response()` for audit log serialization
- **`Makefile`** with targets: `dev`, `test`, `lint`, `migrate`, `migration`, `install`, `docker-up`, `docker-rebuild`
- **`py.typed`** marker (PEP 561) for type checker support
- **Type hints** on all repository manager classes (`NoteManager`, `UserManager`, `LoginManager`, `PasswordManager`)

### Changed
- **Migrated from `requirements.txt` to `pyproject.toml`** — dependencies use `>=X.Y,<X+1` pinning strategy with `uv.lock` for reproducible installs
- **Dockerfile** now uses `uv sync --frozen --no-dev` instead of `pip install -r requirements.txt`
- **CLAUDE.md** and **README.md** updated to use `uv run` prefix for all CLI commands (`uvicorn`, `pytest`, `alembic`, `pylint`)
- README setup simplified from `uv pip install -r requirements.txt` to `uv sync`

### Removed
- `requirements.txt` (replaced by `pyproject.toml`)
