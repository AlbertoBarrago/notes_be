# albz-notes-be

A production-ready FastAPI backend for a notes application, featuring JWT authentication, Google OAuth, role-based access control, rate limiting, audit logging, and email-based password reset.

> Swagger UI available at `/docs`

---

## Features

| Feature | Details |
|---|---|
| **Authentication** | JWT (access tokens) + Google OAuth 2.0 |
| **Authorization** | Role-based: `ADMIN` and `GUEST` roles |
| **Rate Limiting** | Per-user/IP tracking via middleware, with `X-RateLimit-*` headers |
| **Audit Logging** | Every write operation is recorded with user, action, and timestamp |
| **Password Reset** | Secure email-based flow via FastAPI-Mail + background tasks |
| **BackOffice API** | Admin-only endpoints for managing users, notes, and audit records |
| **Database** | MySQL with SQLAlchemy ORM and Alembic migrations |
| **Caching** | LRU in-memory cache on note queries |

---

## Tech Stack

- **Runtime**: Python 3.12
- **Framework**: FastAPI 0.115
- **Database**: MySQL via `mysql-connector-python`, SQLAlchemy 2.0, Alembic
- **Auth**: PyJWT, bcrypt, passlib
- **Email**: fastapi-mail
- **Package manager**: [uv](https://github.com/astral-sh/uv)

---

## Architecture

The project follows a layered architecture with a clear separation of concerns:

```
HTTP Request
     │
     ▼
┌─────────────────────────────────┐
│   API Endpoints (app/api/)      │  Route handlers — thin, no business logic
│   auth · notes · users · oauth  │
│   backoffice · healthcheck       │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│   Managers / Repositories       │  Business logic, dispatchers, caching
│   (app/repositories/)           │
│   NoteManager · UserManager     │
│   LoginManager · BackofficeManager│
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│   Database Layer (app/db/)      │  SQLAlchemy ORM models, session, JWT decode
│   User · Note · Audit · RateLimit│
└─────────────────────────────────┘
```

### Directory Layout

```
app/
├── api/v1/endpoints/     # Route handlers (auth, notes, users, oauth, backoffice, …)
├── core/
│   ├── setup.py          # FastAPI app factory, CORS, rate-limit middleware
│   └── exceptions/       # Domain error handlers (AuthErrorHandler, NoteErrorHandler, …)
├── db/
│   ├── models/           # ORM models (User, Note, Audit, RateLimit)
│   └── mysql.py          # Engine, SessionLocal, get_db(), get_current_user() deps
├── repositories/
│   ├── auth/             # LoginManager, PasswordManager, CommonService
│   ├── note/             # NoteManager, CacheRepository
│   ├── user/             # UserManager
│   └── backoffice/       # BackofficeManager
├── schemas/              # Pydantic request/response models
├── dto/                  # Data Transfer Objects with from_model() class methods
├── email/                # Email templates and send helpers
└── main.py               # Entry point — calls create_app(), mounts routers
```

### API Routes

| Domain | Prefix |
|---|---|
| Auth | `/api/v1/auth` |
| OAuth | `/api/v1/oauth` |
| Users | `/api/v1/users` |
| Notes | `/api/v1/notes` |
| BackOffice | `/api/v1/backoffice` |
| Healthcheck | `/healthcheck` |
| Home | `/` |

### Key Patterns

- **Dependency injection** — `get_db()` and `get_current_user()` are `Depends()` used across all authenticated endpoints.
- **Manager/dispatcher pattern** — Business logic lives in manager classes. `NoteManager` and `UserManager` use dict-based dispatch; `LoginManager` uses a `match` statement.
- **Error handling** — `HTTPException` is never raised directly. Domain-specific handler classes (`NoteErrorHandler`, `AuthErrorHandler`, etc.) expose static raise methods.
- **Audit logging** — Every write operation calls `CommonService(db).log_action(user_id, action, description)`.
- **Caching** — `CacheRepository` wraps note list queries with `@lru_cache(maxsize=128)`.

---

## Getting Started

### Prerequisites

- Python 3.12+
- MySQL instance
- [`uv`](https://github.com/astral-sh/uv) package manager

### 1. Install dependencies

```bash
uv sync
```

### 2. Configure environment

```bash
cp .env.sample .env
```

Edit `.env` and set the required variables:

| Variable | Description |
|---|---|
| `MYSQL_USER` | Database user |
| `MYSQL_PASSWORD` | Database password |
| `MYSQL_HOST` | Database host |
| `MYSQL_DATABASE` | Database name |
| `SECRET_KEY` | JWT signing secret |

### 3. Run database migrations

```bash
uv run alembic upgrade head
```

Or bootstrap from SQL directly:

```bash
mysql -u root -p < sql/create.sql
```

### 4. Start the development server

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

App: `http://localhost:8080` — Swagger UI: `http://localhost:8080/docs`

---

## Docker

```bash
# Start app + MySQL
docker-compose up -d

# Rebuild after code changes
docker-compose down && docker-compose up --build
```

> Make sure your `.env` file is present before running Docker. If you already have MySQL running locally on port `3306`, update the port mapping in `docker-compose.yml` to avoid conflicts.

---

## Development

### Run tests

```bash
uv run pytest -p no:warnings test/**/*.py
```

Tests use in-memory SQLite and cover ORM models. No external services required.

### Run a single test file

```bash
uv run pytest -p no:warnings test/note.py
```

### Lint

```bash
uv run pylint app/
```

### Alembic migrations

```bash
# Generate a new migration
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head
```

---

## License

MIT
