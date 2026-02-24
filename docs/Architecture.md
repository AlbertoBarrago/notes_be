# Architecture — albz-notes-be

## Overview

A production-style REST API backend for a notes application.
Built with **FastAPI + SQLAlchemy + MySQL**, containerised with Docker, and structured around a clean layered architecture.

**Core capabilities:**

- JWT authentication + Google OAuth 2.0
- Role-based access control (`ADMIN` / `GUEST`)
- Per-user/IP rate limiting (middleware + DB-backed)
- Audit logging on every write operation
- Email-based password reset via background tasks
- Admin back-office API
- In-memory LRU cache on note queries

---

## Tech Stack

| Layer | Technology |
|---|---|
| Runtime | Python 3.12 |
| Framework | FastAPI 0.115 |
| ORM | SQLAlchemy 2.0 |
| Database | MySQL (`mysql-connector-python`) |
| Migrations | Alembic |
| Auth | PyJWT + bcrypt + passlib |
| Email | fastapi-mail |
| Package manager | uv |
| Container | Docker + docker-compose |

---

## Layered Architecture

```
HTTP Request
     │
     ▼
┌──────────────────────────────────────┐
│  Middleware                          │
│  RateLimitMiddleware · CORSMiddleware│  ← runs before every request
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│  API Endpoints  (app/api/v1/)        │  ← thin handlers, no business logic
│  auth · notes · users · oauth        │
│  backoffice · healthcheck · home     │
└──────────────────┬───────────────────┘
                   │  calls
                   ▼
┌──────────────────────────────────────┐
│  Managers / Repositories             │  ← all business logic lives here
│  NoteManager · UserManager           │
│  LoginManager · PasswordManager      │
│  BackofficeManager · CommonService   │
└──────────────────┬───────────────────┘
                   │  reads/writes via
                   ▼
┌──────────────────────────────────────┐
│  Database Layer  (app/db/)           │
│  SQLAlchemy ORM models               │
│  User · Note · Audit · RateLimit     │
└──────────────────────────────────────┘
```

---

## Directory Layout

```
app/
├── main.py                  # Entry point — wires routers and mounts /static
├── core/
│   ├── setup.py             # App factory: FastAPI instance, CORS, middleware
│   ├── settings.py          # Pydantic settings from .env
│   ├── middleware/
│   │   └── rate_limit.py    # RateLimitMiddleware (DB-backed, per user/IP)
│   └── exceptions/          # Domain error handlers (static raise methods)
│       ├── auth.py          # AuthErrorHandler
│       ├── note.py          # NoteErrorHandler
│       ├── user.py          # UserErrorHandler
│       └── generic.py       # GlobalErrorHandler
├── api/v1/endpoints/        # Route handlers
│   ├── auth.py              # Login, register, token refresh
│   ├── oauth.py             # Google OAuth flow
│   ├── notes.py             # CRUD + search + pagination
│   ├── users.py             # User profile management
│   ├── backoffice.py        # Admin-only endpoints
│   └── healthcheck.py
├── repositories/            # Business logic
│   ├── auth/
│   │   ├── login/           # LoginManager (JWT, credentials)
│   │   ├── oauth/           # Google OAuth manager
│   │   ├── reset/           # PasswordManager (reset flow)
│   │   └── common/
│   │       └── services.py  # CommonService: email, user lookup, audit log
│   ├── note/
│   │   ├── repository.py    # NoteManager (CRUD, search, pagination)
│   │   └── cache/           # CacheRepository (LRU cache wrapper)
│   ├── user/                # UserManager
│   ├── backoffice/          # BackofficeManager
│   ├── audit/               # log_audit_event helper
│   └── logger/              # LoggerService (structured logging)
├── db/
│   ├── mysql.py             # Engine, SessionLocal, get_db(), get_current_user()
│   └── models/
│       ├── user/model.py    # User ORM model
│       ├── notes/model.py   # Note ORM model
│       ├── audit/model.py   # Audit ORM model
│       └── rate_limit/      # RateLimit ORM model
├── schemas/                 # Pydantic request/response models
├── dto/                     # Data Transfer Objects (from_model() → plain dict)
└── email/                   # Email templates + send helpers
```

---

## Data Models

```
users
├── id          UUID (PK)
├── username    string
├── email       string (unique)
├── password    bcrypt hash
├── role        ADMIN | GUEST
└── ──── has many ────► notes, audit

notes
├── id          int (PK, auto)
├── title       string
├── content     text
├── is_public   bool
├── tags        JSON array
├── image_url   string (optional)
├── created_at / updated_at
└── user_id     FK → users.id

audit
├── id          int (PK, auto)
├── action      string   (e.g. "Create Note")
├── description string
├── created_at
└── user_id     FK → users.id

rate_limits
├── id          int (PK, auto)
├── identifier  string   (user ID or IP address)
├── requests    int      (request count in window)
└── window_start datetime
```

---

## Key Design Patterns

### 1. Dependency Injection (FastAPI `Depends`)

`get_db()` provides a scoped SQLAlchemy session; `get_current_user()` decodes the JWT and returns the authenticated `User`. Both are injected via `Depends()` in every protected endpoint — no global state.

```python
@router.get("/notes")
def list_notes(db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    ...
```

### 2. Manager / Dispatcher Pattern

Business logic lives in Manager classes, not in endpoints. Each manager exposes a single dispatcher method that routes to specific operations via a dict of lambdas (or a `match` statement for `LoginManager`). This keeps endpoints thin and logic testable in isolation.

```python
def perform_note_action(action, note=None, note_id=None, current_user=None, **kwargs):
    actions = {
        "add_note":    lambda: self.add_note(note, current_user),
        "update_note": lambda: self.update_note(note_id, note, current_user),
        "delete_note": lambda: self.delete_note(note_id, current_user),
        ...
    }
    return actions[action]()
```

### 3. Centralised Error Handling

`HTTPException` is never raised directly in business logic. Domain-specific handler classes expose static `raise_*` methods that standardise error responses.

```python
# app/core/exceptions/note.py
class NoteErrorHandler:
    @staticmethod
    def raise_note_not_found():
        raise HTTPException(status_code=404, detail="Note not found")
```

### 4. Audit Logging

Every write operation (create, update, delete) calls `CommonService(db).log_action(user_id, action, description)`, which writes to the `audit` table.

### 5. LRU Caching

`CacheRepository` wraps note list queries with `@lru_cache(maxsize=128)`. The cache layer sits inside the repository tier, transparent to endpoints.

> **Scaling note:** LRU is sufficient for a single-instance deployment. If the app is scaled horizontally, each process holds its own isolated cache. The natural upgrade is **Redis** — a shared external cache consistent across all instances.

### 6. DTO Layer

`NoteDTO`, `UserDTO`, etc. expose a `from_model()` class method that converts an ORM object into a plain `dict`, decoupling the API response shape from the ORM model.

### 7. Background Tasks for Email

Password reset and welcome emails are dispatched via FastAPI's `BackgroundTasks`. The HTTP response is returned immediately; email delivery happens asynchronously without blocking.

---

## Authentication Flows

### JWT (standard)

```
POST /api/v1/auth/login
  → LoginManager validates credentials (bcrypt)
  → issues JWT (sub = user UUID, exp = configurable)
  → client sends Bearer token on subsequent requests
  → get_current_user() decodes + looks up User on every request
```

### Google OAuth 2.0

```
GET /api/v1/oauth/login     → redirect to Google consent screen
GET /api/v1/oauth/callback  → exchange code for token, upsert User, issue JWT
```

### Password Reset

```
POST /api/v1/auth/forgot-password
  → generate signed token, send email via BackgroundTasks
POST /api/v1/auth/reset-password?token=...
  → PasswordManager validates token, updates bcrypt hash
```

---

## Request Lifecycle

```
1. Request arrives
2. RateLimitMiddleware checks identifier (user ID or IP) against rate_limits table
   → 429 if limit exceeded, otherwise increments counter and adds X-RateLimit-* headers
3. CORS headers applied
4. Router matches path → endpoint handler called
5. get_db() opens a scoped DB session
6. get_current_user() decodes JWT → User (for protected routes)
7. Endpoint calls Manager.perform_*_action(action, ...)
8. Manager executes business logic, calls CommonService.log_action() on writes
9. DTO converts ORM model → dict
10. Response returned; DB session closed in finally block
```

---

## API Surface

| Domain | Prefix | Auth required |
|---|---|---|
| Auth | `/api/v1/auth` | No (login/register) |
| OAuth | `/api/v1/oauth` | No |
| Users | `/api/v1/users` | Yes |
| Notes | `/api/v1/notes` | Yes |
| BackOffice | `/api/v1/backoffice` | Yes (ADMIN only) |
| Healthcheck | `/healthcheck` | No |

Interactive docs: `http://localhost:8080/docs`

---

## Design Decisions

| Decision | Rationale |
|---|---|
| `uv` over pip/poetry | Faster resolution, lockfile reproducibility, single tool for venv + packages |
| MySQL over PostgreSQL | Project constraint; SQLAlchemy abstracts it so migrations work identically |
| LRU cache in-process | Zero-dependency for single-instance; replace with Redis for horizontal scaling |
| Rate limiting in DB | Keeps the stack simple (no Redis required); trades some performance for simplicity |
| Pydantic v1 shim | Some schemas use `pydantic.v1` for backwards compatibility; new code targets v2 |
| Alembic for migrations | Schema changes are versioned and reproducible; bootstrap SQL also in `sql/` |
