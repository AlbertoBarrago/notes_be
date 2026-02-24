-- =============================================================================
-- reset.sql
-- Wipes all data and reloads the development seed in one shot.
-- Equivalent to running truncate.sql followed by seed.sql.
-- Usage:  mysql -u notez_app -p notez_be < sql/reset.sql
--
-- WARNING: all existing data will be permanently deleted.
-- =============================================================================

USE notez_be;

-- ----- truncate (preserves schema) ------------------------------------------
SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE audit;
TRUNCATE TABLE notes;
TRUNCATE TABLE rate_limits;
TRUNCATE TABLE users;

SET FOREIGN_KEY_CHECKS = 1;

-- ----- seed ------------------------------------------------------------------

-- Credentials:
--   admin@notez.dev  /  admin123
--   alice@notez.dev  /  guest123
--   bob@notez.dev    /  demo456

INSERT INTO users (id, username, email, hashed_password, role, created_at, updated_at) VALUES
(
    'b1c5e78a-91f7-488f-8718-e696c20a600f',
    'admin', 'admin@notez.dev',
    '$2b$12$JKT3GaO0vO2w.vBpRd2YWO5vJZ/cyYgPro97oDkj/WXrxm/amqiMm',
    'ADMIN', '2025-01-10 09:00:00', '2025-01-10 09:00:00'
),
(
    '99fd5bec-23f0-454a-bea4-cb3b192bbb97',
    'alice', 'alice@notez.dev',
    '$2b$12$VFFu5VviIUhMlS6wLzLelekAFbjF2UFZGFiq1zRMktNRLoIg109/W',
    'GUEST', '2025-01-15 10:30:00', '2025-02-01 14:00:00'
),
(
    'e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5',
    'bob', 'bob@notez.dev',
    '$2b$12$iYdRYnVdBrGwV2R28v8pBeIElQa6Au2VyZ7.qImVHu.Qc/ajA6Fs6',
    'GUEST', '2025-02-03 08:15:00', '2025-02-03 08:15:00'
);

INSERT INTO notes (user_id, title, content, is_public, tags, created_at, updated_at) VALUES
('b1c5e78a-91f7-488f-8718-e696c20a600f', 'Welcome to Notez',      'Official welcome note. Explore the public feed to discover what others are writing.', TRUE,  '["announcement","welcome"]',           '2025-01-10 09:05:00', '2025-01-10 09:05:00'),
('b1c5e78a-91f7-488f-8718-e696c20a600f', 'Admin Runbook',          'Internal runbook for administrators. See full version in seed.sql.',                  FALSE, '["admin","ops","internal"]',           '2025-01-11 11:00:00', '2025-02-10 16:30:00'),
('b1c5e78a-91f7-488f-8718-e696c20a600f', 'API Rate Limit Policy',  '1000 req / 60-min window per user. Anonymous traffic tracked by IP. Returns 429.',   TRUE,  '["api","policy"]',                     '2025-01-12 14:00:00', '2025-01-12 14:00:00'),
('99fd5bec-23f0-454a-bea4-cb3b192bbb97', 'My First Note',          'Hello world! Just trying out the app. Looks clean so far.',                           FALSE, '["personal","hello"]',                 '2025-01-15 10:35:00', '2025-01-15 10:35:00'),
('99fd5bec-23f0-454a-bea4-cb3b192bbb97', 'Python Learning Path',   'Tracking my progress: Pydantic v2 ✓ — Async/await next.',                             TRUE,  '["python","learning","programming"]',  '2025-01-20 09:00:00', '2025-02-05 18:00:00'),
('99fd5bec-23f0-454a-bea4-cb3b192bbb97', 'Recipe: Quick Pasta',    '200g spaghetti, garlic, cherry tomatoes, olive oil, basil. Cook al dente, toss.',     TRUE,  '["food","recipe"]',                    '2025-01-22 19:30:00', '2025-01-22 19:30:00'),
('99fd5bec-23f0-454a-bea4-cb3b192bbb97', 'Book List 2025',         'Clean Code, Designing Data-Intensive Applications, The Pragmatic Programmer.',         FALSE, '["books","personal"]',                 '2025-02-01 08:00:00', '2025-02-01 08:00:00'),
('99fd5bec-23f0-454a-bea4-cb3b192bbb97', 'JWT Auth Notes',         'Access tokens: 15 min. Refresh: 1 day. Algorithm: HS256. Dep: get_current_user().',   FALSE, '["dev","auth","jwt"]',                 '2025-02-10 11:00:00', '2025-02-10 11:00:00'),
('e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5', 'Intro to SQL Indexes',   'Speeds SELECT, slows writes. Index WHERE/JOIN/ORDER BY columns. Avoid over-indexing.', TRUE, '["sql","database","learning"]',        '2025-02-03 08:20:00', '2025-02-03 08:20:00'),
('e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5', 'Docker Cheatsheet',      'docker ps / up -d / down / exec -it bash / logs -f / image prune -a',                 TRUE,  '["docker","devops","cheatsheet"]',     '2025-02-05 15:00:00', '2025-02-15 10:00:00'),
('e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5', 'Meeting Notes — Sprint 3','Decisions: tagging, pagination, password reset email. Next sync: Friday 15:00 CET.',  FALSE, '["meeting","work"]',                   '2025-02-12 14:00:00', '2025-02-12 14:00:00'),
('e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5', 'Git Workflow',            'main=prod. Branch: feature/* fix/*. PR → squash merge. Never force-push to main.',    TRUE,  '["git","workflow","dev"]',             '2025-02-14 09:30:00', '2025-02-14 09:30:00'),
('e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5', 'Personal Goals Q1 2025', 'Ship MVP. FastAPI course. Exercise 3x/week. 2 technical books.',                       FALSE, '["personal","goals"]',                 '2025-02-03 08:30:00', '2025-02-03 08:30:00');

INSERT INTO audit (user_id, action, description, timestamp) VALUES
('b1c5e78a-91f7-488f-8718-e696c20a600f', 'Login',       'User logged in successfully',  '2025-01-10 09:00:00'),
('b1c5e78a-91f7-488f-8718-e696c20a600f', 'Create Note', 'User create note successfully','2025-01-10 09:05:00'),
('99fd5bec-23f0-454a-bea4-cb3b192bbb97', 'Login',       'User logged in successfully',  '2025-01-15 10:30:00'),
('99fd5bec-23f0-454a-bea4-cb3b192bbb97', 'Create Note', 'User create note successfully','2025-01-15 10:35:00'),
('99fd5bec-23f0-454a-bea4-cb3b192bbb97', 'Update Note', 'User update note successfully','2025-02-05 18:00:00'),
('e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5', 'Login',       'User logged in successfully',  '2025-02-03 08:15:00'),
('e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5', 'Create Note', 'User create note successfully','2025-02-03 08:20:00'),
('e0ca8acc-cdfd-4a0d-9766-5bf93ab733b5', 'Update Note', 'User update note successfully','2025-02-15 10:00:00');

SELECT 'users' AS tbl, COUNT(*) AS rows FROM users
UNION ALL SELECT 'notes',      COUNT(*) FROM notes
UNION ALL SELECT 'audit',      COUNT(*) FROM audit
UNION ALL SELECT 'rate_limits',COUNT(*) FROM rate_limits;
