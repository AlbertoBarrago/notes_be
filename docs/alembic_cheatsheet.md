# Alembic Cheatsheet

Quick reference for Alembic database migrations in this project.
All commands must be prefixed with `uv run` (or use `make` targets where available).

---

## Setup

```bash
# alembic.ini is already configured — script_location = alembic
# DB URL is read from .env via env.py (not hardcoded in alembic.ini)
uv run alembic --version
```

---

## Daily Commands

### Generate a migration (autogenerate from models)

```bash
uv run alembic revision --autogenerate -m "description of change"
# shortcut via Makefile:
make migration msg="description of change"
```

> Alembic compares ORM models (`app/db/models/`) against the current DB schema and generates the diff.

### Apply all pending migrations

```bash
uv run alembic upgrade head
# shortcut via Makefile:
make migrate
```

### Apply N steps forward

```bash
uv run alembic upgrade +1
uv run alembic upgrade +2
```

### Roll back one migration

```bash
uv run alembic downgrade -1
```

### Roll back to a specific revision

```bash
uv run alembic downgrade <revision_id>
# e.g.
uv run alembic downgrade a296c3965be2
```

### Roll back everything (back to empty schema)

```bash
uv run alembic downgrade base
```

---

## Inspection

### Show current revision applied to DB

```bash
uv run alembic current
```

### Show migration history

```bash
uv run alembic history
uv run alembic history --verbose   # includes docstrings
```

### Show pending migrations (not yet applied)

```bash
uv run alembic history -r current:head
```

### Show heads (latest revision(s))

```bash
uv run alembic heads
```

### Show the SQL that would be run (dry-run)

```bash
uv run alembic upgrade head --sql
uv run alembic downgrade -1 --sql
```

---

## Creating Migrations

### Empty migration (manual)

```bash
uv run alembic revision -m "add index on notes.user_id"
```

### Autogenerate from models

```bash
uv run alembic revision --autogenerate -m "add tags column to notes"
```

> After generating, always **review** the file in `alembic/versions/` before applying. Autogenerate misses some changes (e.g. check constraints, server defaults).

---

## Migration File Anatomy

```python
# alembic/versions/<rev>_<slug>.py

revision = 'abc123'       # this revision's ID
down_revision = 'xyz789'  # parent revision (None if first)
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('notes', sa.Column('summary', sa.String(255), nullable=True))

def downgrade() -> None:
    op.drop_column('notes', 'summary')
```

---

## Common `op` Operations

```python
from alembic import op
import sqlalchemy as sa

# Add a column
op.add_column('table_name', sa.Column('col', sa.String(255), nullable=True))

# Drop a column
op.drop_column('table_name', 'col')

# Rename a column
op.alter_column('table_name', 'old_name', new_column_name='new_name')

# Change column type / nullable
op.alter_column('table_name', 'col',
    existing_type=sa.String(100),
    type_=sa.String(255),
    nullable=False)

# Create a table
op.create_table('new_table',
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('name', sa.String(100), nullable=False),
)

# Drop a table
op.drop_table('new_table')

# Add an index
op.create_index('ix_notes_user_id', 'notes', ['user_id'])

# Drop an index
op.drop_index('ix_notes_user_id', table_name='notes')

# Add a foreign key
op.create_foreign_key('fk_notes_user', 'notes', 'users', ['user_id'], ['id'])

# Execute raw SQL
op.execute("UPDATE notes SET is_public = 0 WHERE is_public IS NULL")
```

---

## Stamping (Mark Without Running)

```bash
# Mark DB as being at head without running migrations
uv run alembic stamp head

# Mark DB at a specific revision
uv run alembic stamp <revision_id>

# Mark DB as having no migrations applied
uv run alembic stamp base
```

> Useful when bootstrapping from `sql/create.sql` — stamp the DB so Alembic knows it's up to date.

---

## Project-Specific Notes

- **`alembic/env.py`** reads `DATABASE_URL` from the app's settings (`.env`) — no hardcoded URL in `alembic.ini`.
- **`alembic/versions/`** contains all migration files. Current initial migration: `a296c3965be2_create_tables_from_models.py`.
- **Bootstrap alternative**: `sql/create.sql` can be used instead of Alembic for a fresh DB — then `alembic stamp head`.
- Autogenerate requires models to be imported in `env.py` via `target_metadata = Base.metadata`.
- MySQL-specific: autogenerate may emit redundant `alter_column` for `VARCHAR` length; review before applying.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `Can't locate revision` | Run `uv run alembic history` to verify the chain |
| `Target database is not up to date` | Apply pending migrations first: `upgrade head` |
| Autogenerate shows no changes | Ensure all models are imported in `env.py` |
| MySQL column charset noise | Review and remove no-op `alter_column` calls before applying |
| `ModuleNotFoundError` | Always prefix with `uv run` — bare `alembic` uses system Python |
