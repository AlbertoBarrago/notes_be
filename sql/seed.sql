-- =============================================================================
-- seed.sql
-- Populates notez_be with realistic mock data for local development.
-- Run AFTER create.sql (or after truncate.sql for a clean reload).
-- Usage:  mysql -u notez_app -p notez_be < sql/seed.sql
--
-- Credentials for seeded accounts (bcrypt, cost 12):
--   admin@notez.dev   /  admin123
--   alice@notez.dev   /  guest123
--   bob@notez.dev     /  demo456
-- =============================================================================

USE notez_be;

-- =============================================================================
-- USERS
-- =============================================================================
INSERT INTO users (id, username, email, hashed_password, role, created_at, updated_at) VALUES
(
    'b1c5e78a-91f7-488f-8718-e696c20a600f',
    'admin',
    'admin@notez.dev',
    '$2b$12$JKT3GaO0vO2w.vBpRd2YWO5vJZ/cyYgPro97oDkj/WXrxm/amqiMm', -- admin123
    'ADMIN',
    '2025-01-10 09:00:00',
    '2025-01-10 09:00:00'
),
(
    '99fd5bec-23f0-454a-bea4-cb3b192bbb97',
    'alice',
    'alice@notez.dev',
    '$2b$12$VFFu5VviIUhMlS6wLzLelekAFbjF2UFZGFiq1zRMktNRLoIg109/W', -- guest123
    'GUEST',
    '2025-01-15 10:30:00',
    '2025-02-01 14:00:00'
),
(
    'e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5',
    'bob',
    'bob@notez.dev',
    '$2b$12$iYdRYnVdBrGwV2R28v8pBeIElQa6Au2VyZ7.qImVHu.Qc/ajA6Fs6', -- demo456
    'GUEST',
    '2025-02-03 08:15:00',
    '2025-02-03 08:15:00'
);

-- =============================================================================
-- NOTES  (mix of public / private, tagged / untagged, various owners)
-- =============================================================================

-- --- admin's notes -----------------------------------------------------------
INSERT INTO notes (user_id, title, content, is_public, tags, created_at, updated_at) VALUES
(
    'b1c5e78a-91f7-488f-8718-e696c20a600f',
    'Welcome to Notez',
    'This is the official welcome note for all new users. Notez lets you create, organise, and share notes with your team. Explore the public feed to discover what others are writing about.',
    TRUE,
    '["announcement", "welcome"]',
    '2025-01-10 09:05:00',
    '2025-01-10 09:05:00'
),
(
    'b1c5e78a-91f7-488f-8718-e696c20a600f',
    'Admin Runbook',
    'Internal runbook for administrators.\n\n1. Monitor rate_limits table for abuse.\n2. Run `uv run alembic upgrade head` after every deploy.\n3. Rotate SECRET_KEY every 90 days and invalidate all JWTs.\n4. Backups are taken nightly at 02:00 UTC.',
    FALSE,
    '["admin", "ops", "internal"]',
    '2025-01-11 11:00:00',
    '2025-02-10 16:30:00'
),
(
    'b1c5e78a-91f7-488f-8718-e696c20a600f',
    'API Rate Limit Policy',
    'Current limits: 1000 requests per 60-minute window per user. Anonymous requests are tracked by IP. Exceeding the limit returns HTTP 429. Limits can be adjusted via RATE_LIMIT and RATE_LIMIT_WINDOW env vars.',
    TRUE,
    '["api", "policy"]',
    '2025-01-12 14:00:00',
    '2025-01-12 14:00:00'
);

-- --- alice's notes -----------------------------------------------------------
INSERT INTO notes (user_id, title, content, is_public, tags, created_at, updated_at) VALUES
(
    '99fd5bec-23f0-454a-bea4-cb3b192bbb97',
    'My First Note',
    'Hello world! Just trying out the app. Looks clean so far. I can create private notes, tag them, and share selected ones publicly.',
    FALSE,
    '["personal", "hello"]',
    '2025-01-15 10:35:00',
    '2025-01-15 10:35:00'
),
(
    '99fd5bec-23f0-454a-bea4-cb3b192bbb97',
    'Python Learning Path',
    '## Resources I am using\n\n- Official docs: docs.python.org\n- FastAPI tutorial: fastapi.tiangolo.com\n- SQLAlchemy 2.x ORM guide\n\n## Topics covered so far\n\n- [x] Basics & data types\n- [x] Decorators and generators\n- [x] Pydantic v2 models\n- [ ] Async / await patterns\n- [ ] Testing with pytest',
    TRUE,
    '["python", "learning", "programming"]',
    '2025-01-20 09:00:00',
    '2025-02-05 18:00:00'
),
(
    '99fd5bec-23f0-454a-bea4-cb3b192bbb97',
    'Recipe: Quick Pasta',
    'Ingredients (2 servings):\n- 200g spaghetti\n- 2 garlic cloves\n- Cherry tomatoes\n- Olive oil, salt, basil\n\nCook pasta al dente. Sauté garlic in olive oil, add tomatoes, season. Toss with pasta.',
    TRUE,
    '["food", "recipe"]',
    '2025-01-22 19:30:00',
    '2025-01-22 19:30:00'
),
(
    '99fd5bec-23f0-454a-bea4-cb3b192bbb97',
    'Book List 2025',
    'Reading list for this year:\n1. Clean Code — Robert C. Martin\n2. Designing Data-Intensive Applications — Martin Kleppmann\n3. The Pragmatic Programmer — Hunt & Thomas\n4. System Design Interview — Alex Xu',
    FALSE,
    '["books", "personal"]',
    '2025-02-01 08:00:00',
    '2025-02-01 08:00:00'
),
(
    '99fd5bec-23f0-454a-bea4-cb3b192bbb97',
    'JWT Auth Notes',
    'Key points about the JWT implementation in this app:\n- Access tokens expire in TOKEN_EXPIRES_MINUTES (default 15 min)\n- Refresh tokens expire in TOKEN_REFRESH_EXPIRES_MINUTES (default 1440 min = 1 day)\n- Token signing uses HS256 with SECRET_KEY\n- get_current_user() dependency decodes the token on every authenticated request',
    FALSE,
    '["dev", "auth", "jwt"]',
    '2025-02-10 11:00:00',
    '2025-02-10 11:00:00'
);

-- --- bob's notes -------------------------------------------------------------
INSERT INTO notes (user_id, title, content, is_public, tags, created_at, updated_at) VALUES
(
    'e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5',
    'Intro to SQL Indexes',
    'An index speeds up SELECT queries but slows down INSERT/UPDATE/DELETE.\n\nUse indexes on columns frequently used in WHERE, JOIN, or ORDER BY clauses.\n\nAvoid over-indexing: each index takes extra storage and maintenance overhead.',
    TRUE,
    '["sql", "database", "learning"]',
    '2025-02-03 08:20:00',
    '2025-02-03 08:20:00'
),
(
    'e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5',
    'Docker Cheatsheet',
    '```\ndocker ps                    # list running containers\ndocker-compose up -d         # start services in background\ndocker-compose down          # stop and remove containers\ndocker exec -it <id> bash    # open shell in container\ndocker logs -f <id>          # stream logs\ndocker image prune -a        # remove unused images\n```',
    TRUE,
    '["docker", "devops", "cheatsheet"]',
    '2025-02-05 15:00:00',
    '2025-02-15 10:00:00'
),
(
    'e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5',
    'Meeting Notes — Sprint 3 Planning',
    'Attendees: bob, alice, admin\n\nDecisions:\n- Prioritise note tagging feature\n- Add pagination to public feed\n- Fix password reset email template\n\nNext sync: Friday 15:00 CET',
    FALSE,
    '["meeting", "work"]',
    '2025-02-12 14:00:00',
    '2025-02-12 14:00:00'
),
(
    'e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5',
    'Git Workflow',
    'Branch strategy:\n- main: production-ready code\n- feature/<name>: new features\n- fix/<name>: bug fixes\n\nFlow: branch off main → develop → PR → review → squash merge → delete branch.\nNever force-push to main.',
    TRUE,
    '["git", "workflow", "dev"]',
    '2025-02-14 09:30:00',
    '2025-02-14 09:30:00'
),
(
    'e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5',
    'Personal Goals Q1 2025',
    '- Ship the notes app MVP\n- Complete FastAPI course\n- Exercise 3x per week\n- Read 2 technical books',
    FALSE,
    '["personal", "goals"]',
    '2025-02-03 08:30:00',
    '2025-02-03 08:30:00'
);

-- =============================================================================
-- AUDIT  (simulated login / note events for a realistic history)
-- =============================================================================
INSERT INTO audit (user_id, action, description, timestamp) VALUES
('b1c5e78a-91f7-488f-8718-e696c20a600f', 'Login',       'User logged in successfully',            '2025-01-10 09:00:00'),
('b1c5e78a-91f7-488f-8718-e696c20a600f', 'Create Note', 'User create note successfully',           '2025-01-10 09:05:00'),
('b1c5e78a-91f7-488f-8718-e696c20a600f', 'Create Note', 'User create note successfully',           '2025-01-11 11:00:00'),
('b1c5e78a-91f7-488f-8718-e696c20a600f', 'Login',       'User logged in successfully',            '2025-01-12 13:55:00'),
('b1c5e78a-91f7-488f-8718-e696c20a600f', 'Create Note', 'User create note successfully',           '2025-01-12 14:00:00'),
('99fd5bec-23f0-454a-bea4-cb3b192bbb97', 'Login',       'User logged in successfully',            '2025-01-15 10:30:00'),
('99fd5bec-23f0-454a-bea4-cb3b192bbb97', 'Create Note', 'User create note successfully',           '2025-01-15 10:35:00'),
('99fd5bec-23f0-454a-bea4-cb3b192bbb97', 'Login',       'User logged in successfully',            '2025-01-20 08:58:00'),
('99fd5bec-23f0-454a-bea4-cb3b192bbb97', 'Create Note', 'User create note successfully',           '2025-01-20 09:00:00'),
('99fd5bec-23f0-454a-bea4-cb3b192bbb97', 'Create Note', 'User create note successfully',           '2025-01-22 19:30:00'),
('99fd5bec-23f0-454a-bea4-cb3b192bbb97', 'Login',       'User logged in successfully',            '2025-02-01 07:59:00'),
('99fd5bec-23f0-454a-bea4-cb3b192bbb97', 'Create Note', 'User create note successfully',           '2025-02-01 08:00:00'),
('99fd5bec-23f0-454a-bea4-cb3b192bbb97', 'Update Note', 'User update note successfully',           '2025-02-05 18:00:00'),
('99fd5bec-23f0-454a-bea4-cb3b192bbb97', 'Create Note', 'User create note successfully',           '2025-02-10 11:00:00'),
('e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5', 'Login',       'User logged in successfully',            '2025-02-03 08:15:00'),
('e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5', 'Create Note', 'User create note successfully',           '2025-02-03 08:20:00'),
('e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5', 'Create Note', 'User create note successfully',           '2025-02-03 08:30:00'),
('e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5', 'Login',       'User logged in successfully',            '2025-02-05 14:58:00'),
('e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5', 'Create Note', 'User create note successfully',           '2025-02-05 15:00:00'),
('e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5', 'Login',       'User logged in successfully',            '2025-02-12 13:58:00'),
('e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5', 'Create Note', 'User create note successfully',           '2025-02-12 14:00:00'),
('e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5', 'Create Note', 'User create note successfully',           '2025-02-14 09:30:00'),
('e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5', 'Update Note', 'User update note successfully',           '2025-02-15 10:00:00'),
('b1c5e78a-91f7-488f-8718-e696c20a600f', 'Update Note', 'User update note successfully',           '2025-02-10 16:30:00'),
('99fd5bec-23f0-454a-bea4-cb3b192bbb97', 'Get notes',   'User get pagination notes',               '2025-02-20 09:00:00'),
('e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5', 'Get notes',   'User get pagination notes',               '2025-02-20 09:05:00');

-- =============================================================================
-- Quick sanity check
-- =============================================================================
SELECT 'users'       AS tbl, COUNT(*) AS rows FROM users
UNION ALL
SELECT 'notes',               COUNT(*)         FROM notes
UNION ALL
SELECT 'audit',               COUNT(*)         FROM audit
UNION ALL
SELECT 'rate_limits',         COUNT(*)         FROM rate_limits;
